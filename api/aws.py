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


def upload_file_to_s3(fileobj=None, filepath=None, filedir=None):
    bucket = current_app.config['S3_BUCKET']
    filename = fileobj.filename
    if filedir:
        savepath = '{0}/{1}'.format(filedir, filename)
    else:
        savepath = filename
    file_url = '{0}/{1}'.format(current_app.config['S3_URL'], savepath)

    s3 = get_aws_cli()
    err = None
    try:
        if fileobj:
            s3.upload_fileobj(fileobj, bucket, savepath, ExtraArgs={"ACL": "public-read"})
            return file_url, err
        elif filepath:
            s3.upload_file(filepath, bucket, savepath, ExtraArgs={"ACL": "public-read"})
            return file_url, err
        else:
            raise Exception

    except Exception as e:
        err = e
        return file_url, err
