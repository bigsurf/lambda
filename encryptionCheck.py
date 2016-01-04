# This is a minimal viable product (MVP) that automates S3 encryption enforcement. The MVP allows customers to detect/mitigate unencrypted S3 object. 
# This Python code is used to create a Lambda function.
# Event source: S3 - ObjectCreatedByPut

import json
import urllib
import boto3

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Print received S3 event that invoked this Lambda function 
    print("Received event: " + json.dumps(event, indent=2))
    
    #Retrieve bucket and key of the object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    try:
        #Retrieve metadata from the object 
        response = s3.head_object(Bucket=bucket, Key=key)
        print (response)
        
        #Determine if the object is encrypted
        if 'ServerSideEncryption' in  response:
            print ('Object is encrypted!!')
        else:
            #If the object is not encrypted, delete the object
            print ('ALERT!!! object not encrypted! Deleting the object!')
            s3.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        raise e
        