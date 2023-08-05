#!/usr/bin/env python

import builtins
import click
import json
import logging
import pathlib
import pdb
import pytest
import re
import mock
import os
import sys
import random
import string

from NGPIris import log, WD
from NGPIris.cli.base import root

from click.testing import CliRunner
from distutils.sysconfig import get_python_lib
from unittest.mock import patch, mock_open

testWD = os.path.join(WD, '..', 'tests')
credentials_path = os.path.join(testWD, '..', 'credentials.json')
f1target =  os.path.join("unittest","test_reads_R1.fastq.gz") 
bucket = "ngs-test"

# Generate a random string to prepend to /tmp files to not clash with existing files
random_string = ''.join(random.choices(string.ascii_letters, k=8))
metadata_name = f'{random_string}_metadata.json'

@pytest.fixture
def runner():
    runnah = CliRunner()
    return runnah

def test_version(runner):
    res = runner.invoke(root, '--version')
    assert res.exit_code == 0

###
### All the below test rely on bucket "ngs-test" existing!
###

def test_base(runner):
    cmd = f"-b {bucket} -c {credentials_path}"
    res = runner.invoke(root, cmd.split())
    #Command should complain about lack of subcommand
    assert res.exit_code == 2

def test_hci_base(runner):
    cmd = f"-b {bucket} -c {credentials_path} hci"
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0

def test_upload(runner):
    source = os.path.join(testWD,"data","test_reads_R1.fastq.gz")

    cmd = f"-b {bucket} -c {credentials_path} upload {source} -o {f1target} -m /tmp/{metadata_name} --silent"
    log.debug(cmd)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0


def test_search(runner):
    cmd = f"-b {bucket} -c {credentials_path} search {f1target}"
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0 

def test_download(runner):
    dest =  os.path.join('tmp','tst.fq')
    cmd = f"-b {bucket} -c {credentials_path} download -f {f1target} -o /{dest} --silent"
    log.debug(cmd)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0

def test_delete(runner):
    cmd1 = f"-b {bucket} -c {credentials_path} delete {f1target} -f"
    res1 = runner.invoke(root, cmd1.split())
    cmd2 = f"-b {bucket} -c {credentials_path} delete {os.path.join('unittest', metadata_name)} -f"
    res2 = runner.invoke(root, cmd2.split())
    assert res1.exit_code == 0
    assert res2.exit_code == 0

def test_upload_no_destination(runner):
    source = os.path.join(testWD,"data","test_reads_R1.fastq.gz")
    code_cnt = 0

    dest = os.path.basename(source)

    cmd = f"-b {bucket} -c {credentials_path} upload {source} -m /tmp/{metadata_name} --silent"
    log.debug(cmd)
    res = runner.invoke(root, cmd.split())
    code_cnt = code_cnt + res.exit_code
    cmd1 = f"-b {bucket} -c {credentials_path} delete {dest} -f"
    res1 = runner.invoke(root, cmd1.split())
    cmd2 = f"-b {bucket} -c {credentials_path} delete {metadata_name} -f"
    res2 = runner.invoke(root, cmd2.split())
    code_cnt = code_cnt + res1.exit_code
    code_cnt = code_cnt + res2.exit_code
    assert code_cnt == 0


