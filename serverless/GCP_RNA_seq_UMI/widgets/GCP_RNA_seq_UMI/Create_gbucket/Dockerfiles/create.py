#!/usr/local/bin/python3
import argparse,sys
import random
from google.cloud import storage

def main():
	
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", action='store',dest="bucket_name",default="gcp-test-bucket-".format(random.randint(1,100000)),
                    help="bucket_name, bucket to store project")
    parser.add_argument("-c",action='store',dest="credentials_file",default="/data/credentials.json",
                    help="credentials_file, file with google cloud credentials")    
    args=parser.parse_args()
    credentials_file=args.credentials_file
    bucket_name=args.bucket_name
    storage_client =storage.Client.from_service_account_json(credentials_file)
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        if bucket.name == bucket_name:
            print("bucket name already exists")
            return 0
    bucket=storage_client.create_bucket(bucket_name)
    print("bucket {} created".format(bucket.name))
if __name__ == "__main__":
    main()
