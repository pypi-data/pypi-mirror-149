from NGPIris import WD
from NGPIris.hcp import HCPManager
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("bucket",help="Bucket name")
args = parser.parse_args()

#pdb.set_trace()
print(f"Working Directory at {WD}")
hcpm = HCPManager(credentials_path="./credentials.json")
hcpm.set_bucket(args.bucket)
ls = hcpm.list_buckets()
print(f"Buckets: {ls}")
hcpm.test_connection()
print("Connection is working fine!")


