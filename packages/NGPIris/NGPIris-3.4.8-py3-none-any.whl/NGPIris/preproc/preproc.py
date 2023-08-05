#!/usr/bin/env python

"""
Module for file validation and generation
"""

import csv
import gzip
import json
import os
import re

from NGPIris import log, WD, TIMESTAMP

from NGPIris.hcp.errors import (UnattachedBucketError, LocalFileExistsError,
                                     UnknownSourceTypeError, MismatchChecksumError,
                                     ConnectionError, MissingCredentialsError)


def verify_fq_suffix(fn):
    """Makes sure the provided file looks like a fastq"""

    #Check suffix
    if not fn.endswith(("fastq.gz","fq.gz","fastq","fq")):
        raise Exception(f"File {fn} is not a fastq")
    log.debug(f'Verified that {fn} is a zipped fastq')
    #Check for unresolved symlink
    if os.path.islink(fn):
        if not os.path.exists(os.readlink(fn)):
            raise Exception(f"File {fn} is an unresolved symlink")


def verify_fq_content(fn):
    """Makes sure fastq file contains fastq data"""
    nuc = set("ATCGN\n")
    lineno = 0
    f1 = gzip.open(fn, "r")
    for line in f1:
        line = line.decode('UTF-8')
        lineno = lineno + 1 
        if lineno == 1:
            corr = re.match("^@",line)
        elif lineno == 2:
            corr = set(line) <= nuc
        elif lineno == 3:
            corr = re.match("^\+",line)
        elif lineno == 4:
            lineno = 0

        if not corr:
            raise Exception(f"File{fn} does not look like a fastq at line {lineno}: {line}")
    f1.close()
    
    if lineno % 4 != 0:
        raise Exception(f"File {fn} is missing data")
    log.debug(f'Verified that {fn} resembles a fastq')


def generate_tagmap(fn, tag, output_path="{}/meta-{}.json".format(os.getcwd(), TIMESTAMP)):
    """Creates a json file with filenames and tags"""
    # Check if meta exists, else make it
    if not os.path.exists(output_path):
        data = {fn: {'tag': tag}}
        with open(output_path, 'w') as out:
            json.dump(data, out, indent=4)
    else:
        # Read the current meta
        with open(output_path, 'r') as inp:
            current_data = json.load(inp)

        # New data
        new_data = {fn: {'tag': tag}}
        updated_data = {**current_data, **new_data}

        # Write updated
        with open(output_path, 'w') as out:
            json.dump(updated_data, out, indent=4)

    log.debug(f'Generated metadata file {output_path}')


def read_credentials(credentials_path):
    """Set endpoint, aws id and aws key using a json-file"""
    with open(credentials_path, 'r') as inp:
        c = json.load(inp)

    ep = c['endpoint']
    aid = c['aws_access_key_id']
    key = c['aws_secret_access_key']
    log.debug("Credentials file successfully utilized")
    if not (isinstance(ep,str) and isinstance(aid,str) and isinstance(key,str)):
        raise MissingCredentialsError('One or more values missing from provided json.')

    return [ep,aid,key]

