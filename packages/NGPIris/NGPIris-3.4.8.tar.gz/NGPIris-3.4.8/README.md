# NGP Iris 👁
NGP Iris is a light-weight tool for interacting with a [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) backed Hitachi Content Platform. 
NGP Iris is designed with two use cases in mind:
* A simple, clear, real-time interaction with NGPr file management
* Improving process flow for performing off-site data analysis by using automated transfer scripts

## Easy installation

`pip install NGPIris --upgrade` 

## Introduction

NGP Iris provides two  parts. 
A command line interface for intuitive manipulation of single files.
And a python package to import easy to use file manipulation functions

Both of these modes of interaction pipe processes to the HCPManager class. This class is responsible for connecting to the specified endpoints with the provided access keys and manages the upload, download, and querying against the contents of the available buckets.

The connection is made on a higher resource level rather than client level. This will come to change in the future as more advanced features are introduced.


## Usage

### Command Line Interface
Successful installation means the command `iris` is active.
Run it in the terminal, and view the help for each subcommand.

```iris
Usage: iris [OPTIONS] COMMAND [ARGS]...

  NGP intelligence and repository interface software

Options:
  -c, --credentials PATH     File containing ep, id & key  [required]
  -b, --bucket TEXT          Bucket name  [required]
  -ep, --endpoint TEXT       Endpoint URL override
  -id, --access_key_id TEXT  Amazon key identifier override
  -key, --access_key TEXT    Amazon secret access key override
  -l, --logfile PATH         Logs activity to provided file
  --version                  Show the version and exit.
  --help                     Show this message and exit.

Commands:
  delete    Delete a file on the NGPr
  download  Download files using a given query
  hci       HCI dependent commands
  search    List all file hits for a given query
  upload    Upload fastq files / fastq folder structure
```
#### Upload a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE upload FILE2UPLOAD -o /tmp/MYDUMBTESTFILE`

This command will upload your test file, and a meta-data file, to `/tmp/` on the bucket BUCKETNAME. 
 `-m` will specificy where the meta-data file will be stored locally. 
 Without it the meta-data file will appear in your current directory.

#### Download a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE download -f /tmp/MYDUMBTESTFILE -o ./MYDUMBTESTFILE --silent`

This command will download your previously uploaded testfile, and put it in your current directory.
`-f` will overwrite any locally stored file with the same name
`--silent` will remove the download progress bar. Which is sometimes useful when scripting

#### Additional commands
`iris` contains more commands and flags for additional operations. Such as search, deleting, or doing things in a more nuanced way. The help menu packaged with the program is always kept up to date, so refer to that to easily discover more.

### As a package
Listed below are some of the more common use cases.

For more use cases, check out [the CLI file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/cli/functions.py)

For an index of all HCPManager functionality, check out [the HCPManager source file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/hcp/hcp.py)

#### Connect to the HCP
```python
from NGPIris.hcp import HCPManager

endpoint = <>
aws_access_key_id = <>
aws_secret_access_key = <>

hcpm = HCPManager(endpoint, aws_access_key_id, aws_secret_access_key)
```

or more effectively

```python
from NGPIris.hcp import HCPManager

hcpm = HCPManager(credentials_path="./credentials.json",bucket="ngs-test")
hcpm.test_connection()
```

#### Attach a bucket and get all contents
```python
# Attach a bucket
hcpm.attach_bucket(<bucket_name>)

# Attaching to new bucket with already attached bucket
# This flushes the previous buckets object listing
hcpm.set_bucket("bucket_name_1")
hcpm.attach_bucket(bucket_instance_1)

# Grab all object summaries in the attached bucket
objects = hcpm.get_objects()
```
#### Mundane operations
##### Use a search string to find files and download them
```
# Search for objects with keys containing query string and download them
found_objs = hcpm.search_objects(<query_string>)
for obj in found_objs:
    local_file_name = os.path.basename(obj.key)
    hcpm.download_file(obj, <local_file_path>,force=False)
```
##### Perform preliminary checks before uploading a fastq file
```python
from  NGPIris.io  import  io

io.verify_fq_suffix(<local_file_path>)
io.verify_fq_content(<local_file_path>)
io.generate_tagmap(<local_file_path>, "microbial", <output_file_path>) #Generates a json file that describes what pipeline to use on the NGPr
```
##### Uploading a local file
```python

# Upload a file
hcpm.upload_file(<local_file_path>, <remote_key>)

# Upload a file with metadata
# Note that the maximum metadata size is rather small (2KB).

hcpm.upload_file(<local_file_path>, <remote_key>, metadata={'key': value})

```
##### Disable upload/download callback
Upload and download of files per default utilize a progress tracker. This can be disabled by passing `callback=False` to `upload_file()` or `download_file()`.
```python

# Disable progress tracking
hcpm.upload_file(<local_file_path>, <remote_key>, callback=False)
hcpm.download_file(obj, <local_file_path>, callback=False)
```
#### HCI dependant operations (currently defunct)
~~Rather than interfacing directly with the HCI. Files should be searched for using the HCI.~~
~~This requires the use of a password file for connection.~~
~~If `-o` is used a json file with the results is produced, otherwise the result is printed in stdout.~~
##### ~~Search using query (e.g. sample name)~~
```
./hci.py query -i [index_name] -q [query] -p [password_file] -o [output]
```
##### ~~List all queryable indexes and their available fields~~
```
# Lists all indexes and their fields on the HCI
./hci.py index -i all -p [password_file] -o [output]
# Lists specified index and associated fields 
./hci.py index -i [index_name] -p [password_file] -o [output]
```

## Installation 
### Requirements
* [Anaconda](https://www.anaconda.com/products/individual-d) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed
* pip installed
* NGPr credentials 

### Production build
```
pip install NGPIris
```

### Development build
``` 
git clone git@github.com:genomic-medicine-sweden/NGPIris.git
cd NGPIris
bash setup.sh
source activate hcpenv
```
### NGPr Credentials

* Receive your NGPr credentials from your local NGP admin
* Edit NGPIris/credentials.json
```
{
"endpoint" : "https://ACCESSNODESERVERNAME:PORT",
"aws_access_key_id" : "ALONGSTRINGOFCHARSTHATSYMBOLIZEYOURID",
"aws_secret_access_key" : "ANEVENLONGERSTRINGOFCHARSTHATSYMBOLIZEYOURPASSWORD"
}
```
