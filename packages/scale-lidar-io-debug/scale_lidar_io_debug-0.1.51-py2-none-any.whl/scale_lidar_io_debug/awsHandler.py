import boto3
import base64
import math
from botocore.exceptions import ClientError
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from pymongo import MongoClient
from urllib.parse import urlparse
import json
import os


_AWS_SESSION = None

def get_aws_session():
    global _AWS_SESSION
    if _AWS_SESSION is None:
        _AWS_SESSION = boto3.Session(profile_name='production-developer') # UPDATE: 02-19-2021, change to use prod-dev ased on last change in okta scripts. aws session (session is stored in  ~/.aws/credentials)
    return _AWS_SESSION

def rsa_signer(message):
    if (os.environ.get('CLOUDFRONT') and os.environ.get('CLOUDFRONT_KEY')):
        CLOUDFRONT = json.loads(get_secret(os.environ.get('CLOUDFRONT')))

        private_key = serialization.load_pem_private_key(base64.b64decode(CLOUDFRONT[os.environ.get('CLOUDFRONT_KEY')]), password=None, backend=default_backend())
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
    else:
        pass

'''
    Attachments can be stored on different s3 buckets, we need to map them to the different cloudfront urls.
'''
def get_cloudfront_url(url):
    if (os.environ.get('CLOUDFRONT_URLS')):
        URLS = os.environ.get('CLOUDFRONT_URLS')
        urls = dict([ (u.split(':')[0], u.split(':')[1]) for u in URLS.split(',') ])
        url_data = urlparse(url)
        if urls[url_data.netloc.split('.')[0]]:
            cd_url = f"https://{urls[url_data.netloc.split('.')[0]]}{url_data.path}"
        else:
            cd_url = f"https://{url_data.netloc}{url_data.path}"

        return cd_url
    else:
        pass

'''
    Get public url

    Since we can not acces to s3 attachments url directly, we need to use the CloudFront alternative + sign those url to be able to access them
'''
def get_signed_url(url):
    if (os.environ.get('CLOUDFRONT') and os.environ.get('CLOUDFRONT_KEY')):
        CLOUDFRONT = json.loads(get_secret(os.environ.get('CLOUDFRONT')))
        key_id = CLOUDFRONT[os.environ.get('CLOUDFRONT_ID')]
        expires = datetime.datetime.today() + datetime.timedelta(hours=10)

        cloudfront_signer = CloudFrontSigner(key_id, rsa_signer) # create CloudFront signer using the secrets

        cd_url = get_cloudfront_url(url)
        signed_url = cloudfront_signer.generate_presigned_url( cd_url, date_less_than=expires)
        return signed_url
    else:
        pass


def get_db_connection():
    if (os.environ.get('MONGODB_URI') and os.environ.get('MONGODB_DB') and os.environ.get('MONGODB_CONNECTION')):
        MONGODB_URI = get_secret(os.environ.get('MONGODB_URI'))
        MONGODB_DB = os.environ.get('MONGODB_DB')
        uri = f"{json.loads(MONGODB_URI)['MONGODB_URI_READ_ONLY']}"
        client = MongoClient(uri)
        db = getattr(client, MONGODB_DB)
        return db
    else:
        pass

def get_db_3d_connection():
    if (os.environ.get('MONGODB_URI') and os.environ.get('MONGODB_DB') and os.environ.get('MONGODB_CONNECTION')):
        MONGODB_URI = get_secret(os.environ.get('MONGODB_URI'))
        MONGODB_DB = os.environ.get('MONGODB_DB')
        uri = f"{json.loads(MONGODB_URI)['MONGODB_URI_3D_READ_ONLY']}"
        client = MongoClient(uri)
        db = getattr(client, MONGODB_DB)
        return db
    else:
        pass

'''
    Get AWS data using AWS secret
'''
def get_secret(secret_name):
    region_name = "us-west-2"
    # Create a Secrets Manager client
    session = get_aws_session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return secret
