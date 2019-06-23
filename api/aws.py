from flask import current_app
import boto3
import os


def get_aws_cli():
    access_key = current_app.config['S3_KEY']
    secret_key = current_app.config['S3_SECRET']
    s3 = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      )
    return s3


def get_aws_resource():
    access_key = current_app.config['S3_KEY']
    secret_key = current_app.config['S3_SECRET']
    s3 = boto3.resource('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      )
    return s3


def get_aws_bucketurl():
    aws_host = current_app.config['AWS_HOST']
    bucket = current_app.config['S3_BUCKET']
    return os.path.join(aws_host, bucket)


def upload_fileobj_to_s3(fileobj, savepath):
    bucket = current_app.config['S3_BUCKET']
    file_url = '{0}/{1}'.format(current_app.config['S3_URL'], savepath)

    s3 = get_aws_cli()
    err = None
    try:
        s3.upload_fileobj(fileobj, bucket, savepath, ExtraArgs={"ACL": "public-read"})
        return file_url, err
    except Exception as e:
        err = e
        return file_url, err

def upload_file_to_s3(filepath, savepath):
    bucket = current_app.config['S3_BUCKET']
    file_url = '{0}/{1}'.format(current_app.config['S3_URL'], savepath)

    s3 = get_aws_cli()
    err = None
    try:
        s3.upload_file(filepath, bucket, savepath, ExtraArgs={"ACL": "public-read"})
        return file_url, err
    except Exception as e:
        err = e
        return file_url, err
