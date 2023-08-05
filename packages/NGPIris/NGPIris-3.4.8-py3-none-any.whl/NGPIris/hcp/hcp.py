#!/usr/bin/env python
"""
Module for simple interfacing with the HCP cloud storage.
"""
import os
import re
import sys
import time
import boto3
import urllib3
import botocore
import threading

from functools import wraps
from botocore.utils import fix_s3_host
from botocore.client import Config
from boto3.s3.transfer import TransferConfig

from NGPIris.preproc import preproc
from NGPIris.hcp.helpers import calculate_etag
from NGPIris.hcp.errors import (UnattachedBucketError, LocalFileExistsError,
                                UnknownSourceTypeError, MismatchChecksumError,
                                ReadLargeFileError, ConnectionError)
from NGPIris.hcp.config import get_config
from NGPIris import log


config = get_config()


class ProgressPercentage(object):
    """Progressbar for both upload and download of files."""
    def __init__(self, source):
        self._source = source

        if isinstance(self._source, str):  # Local file
            self._size = os.path.getsize(self._source)
        elif hasattr(self._source, 'size'):  # Object summary
            self._size = self._source.size
        elif hasattr(self._source, 'content_length'):  # Object
            self._size = self._source.content_length
        else:
            raise UnknownSourceTypeError(f'Unknown source format {source}')

        self._seen_so_far = 0
        self._lock = threading.Lock()

        self._previous_time = time.time()
        self._previous_bytesize = self._seen_so_far
        self._interval = 0.1
        self._speed = 0
        self._creation_time = time.time()

    def _calculate_speed(self):
        curr_time = time.time()
        if curr_time - self._interval > self._previous_time:
            speed = (self._seen_so_far - self._previous_bytesize) / (curr_time - self._previous_time)
            self._speed = round(speed / (1024 ** 2), 2)
            self._previous_time = curr_time
            self._previous_bytesize = self._seen_so_far

        return self._speed

    def _trim_text(self, text):
        """Trim text to fit current terminal size."""
        if not os.isatty(0):
            return ''

        terminal_width = 80
        if sys.platform != "win32":
            terminal_width = os.get_terminal_size()[0]

        if len(text) > terminal_width:
            diff = len(text) - terminal_width
            text = text[:len(text)-diff-3] + '...'

        return text

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            speed = self._calculate_speed()
            percentage = (self._seen_so_far / self._size) * 100
            text = "\r%s  %s / %s  %s  (%.2f%%)" % (self._source,
                                                    self._seen_so_far,
                                                    self._size,
                                                    f'{speed}MB/s',
                                                    percentage)
            text = self._trim_text(text)
            print(f'{text}', end='')
            sys.stdout.flush()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        print('')
        avg_transfer_speed = self._size/(self._previous_time - self._creation_time)
        avg_transfer_speed_mb = avg_transfer_speed / 1_000_000
        rounded_speed = round(avg_transfer_speed_mb, 2)
        print(f'Average transfer speed {rounded_speed} MB/s')


def bucketcheck(fn):
    """Checks to see that bucket is attached before executing."""
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        if hasattr(self, 'bucket'):
            return fn(self, *args, **kwargs)
        else:
            raise UnattachedBucketError('Attempted work on unattached bucket. Aborting...')

    return wrapped


class HCPManager:
    def __init__(self, endpoint="", aws_access_key_id="", aws_secret_access_key="", \
                 bucket=None, credentials_path="", debug=False):
        self.bucketname = bucket
        self.bucket = None
        
        if credentials_path != "":
            [ep, aid, key] = preproc.read_credentials(credentials_path)
            self.set_credentials(ep, aid, key)  
        else:
            self.set_credentials(endpoint, aws_access_key_id, aws_secret_access_key)

        # Very verbose. Use with care.
        if debug:
            boto3.set_stream_logger(name='botocore')

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warnings about missing SLL certificate.

        session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

        s3_config = Config(s3={'addressing_style': 'path',
                               'payload_signing_enabled': True},
                           signature_version='s3v4')

        self.s3 = session.resource('s3',
                                   endpoint_url=self.endpoint,
                                   verify=False,  # Checks for SLL certificate. Disables because of already "secure" solution.
                                   config=s3_config)

        self.transfer_config = TransferConfig(multipart_threshold=config.getint('hcp', 'size_threshold'),
                                              max_concurrency=config.getint('hcp', 'max_concurrency'),
                                              multipart_chunksize=config.getint('hcp', 'chunk_size'))

        self.s3.meta.client.meta.events.unregister('before-sign.s3', fix_s3_host)

        if self.bucketname:
            self.attach_bucket(bucket)

    def list_buckets(self):
        """List all available buckets at endpoint."""
        return [bucket.name for bucket in self.s3.buckets.all()]

    def test_connection(self):
        """Validate the connection works with as little overhead as possible."""
        if self.bucketname is None:
            raise UnattachedBucketError("No bucket assigned for connection test")
        try:
            self.s3.meta.client.head_bucket(Bucket=self.bucketname)
        except Exception:
            raise ConnectionError("Invalid access, credentials or bucket specified.")

    def set_bucket(self, bucket):
        self.bucketname = bucket

    def attach_bucket(self, bucketname):
        """Attempt to attach to the given bucket."""
        if bucketname is None:
            log.error("Attempted to attach bucket. But no bucket named.")
        self.bucket = self.s3.Bucket(bucketname)
        if hasattr(self, 'objects'):
            delattr(self, 'objects')  # Incase of already attached bucket

    def set_credentials(self, endpoint, aws_access_key_id, aws_secret_access_key):
        """Mounts credentials to HCPManager object"""
        self.endpoint = endpoint
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    @bucketcheck
    def get_object(self, key):
        """Return object with exact matching key."""
        obj = self.bucket.Object(key)
        try:
            obj.content_length  # Good enough?
        except botocore.exceptions.ClientError:
            return None
        return obj

    @bucketcheck
    def get_objects(self):
        """Return all objects in bucket."""
        if hasattr(self, 'objects'):
            return self.objects
        else:
            self.objects = list(self.bucket.objects.all())
            return self.objects

    @bucketcheck
    def reload_objects(self):
        """Reload and return all objects in bucket."""
        self.objects = list(self.bucket.objects.all())
        return self.objects

    @bucketcheck
    def search_objects(self, string, mode="all"):
        """Return all objects whose keys contain the given string."""
        if not hasattr(self, 'objects'):
            self.get_objects()

        cstr = re.compile(string)
        if mode == "all":
            return [obj for obj in self.objects if re.search(cstr, obj.key) ]
        elif mode == "file":
            return [obj for obj in self.objects if re.search(cstr, os.path.basename(obj.key))]
        elif mode == "dir":
            return [obj for obj in self.objects if re.search(cstr, obj.key) and obj.key[-1] == "/"]
 

    @bucketcheck
    def upload_file(self, local_path, remote_key, metadata={}, callback=True):
        """Upload local file to remote as key with associated metadata."""
        with ProgressPercentage(local_path) as progress:
            self.bucket.upload_file(local_path,
                                    remote_key,
                                    ExtraArgs={'Metadata': metadata},
                                    Config=self.transfer_config,
                                    Callback=progress if callback else None)

        remote_obj = self.get_object(remote_key)
        calculated_etag = calculate_etag(local_path)

        if calculated_etag != remote_obj.e_tag:
            self.delete_object(remote_obj)
            raise MismatchChecksumError('Local and remote file checksums differ. Removing remote file.')

    @bucketcheck
    def download_file(self, obj, local_path, force=False, callback=True):
        """Download objects file to specified local file."""
        if isinstance(obj, str):
            obj = self.get_object(obj)

        if os.path.exists(local_path):
            if not force:
                raise LocalFileExistsError(f'Local file already exists: {local_path}')

        dirname = os.path.dirname(local_path)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)

        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, os.path.basename(obj.key))

        with ProgressPercentage(obj) as progress:
            self.bucket.download_file(obj.key,
                                      local_path,
                                      Callback=progress if callback else None)

    @bucketcheck
    def delete_object(self, obj):
        """Delete the provided object."""
        self.bucket.delete_objects(Delete={'Objects': [{'Key': obj.key}]})

    @bucketcheck
    def read_object(self, obj):
        """Read the object content. Unwise for large files"""
        if obj.content_length < 100000:  # NOTE Arbitrarily set
            return obj.get()['Body'].read().decode('utf-8')
        else:
            raise ReadLargeFileError(f'Object size too large for reading: {obj.content_length}')
