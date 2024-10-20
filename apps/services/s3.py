import boto3
import base64

# AWS credentials and region
AWS_ACCESS_KEY = 'AKIASLX7KR5YGDXPCJWV'
AWS_SECRET_KEY = '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'
AWS_REGION = 'ap-south-1'

# Configuring AWS credentials and region
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def file_upload_via_base64(file_path, base64string):
    # Decoding base64 string and uploading to S3 bucket
    # buf = base64.b64decode(base64string.split('base64_data b')[1])
    print()
    data = {
        'Bucket':'telegramchatproject',
        'Key': file_path,
        'Body': base64string,
        'ACL': 'public-read',
        'ContentEncoding': 'base64',
        'ContentType': 'image/jpeg'
    }
    try:
        s3.put_object(**data)
        print("Successfully uploaded data to telegramchatproject/" + file_path)
        return True
    except Exception as e:
        print(e)
        return False

def delete_key(file_path):
    # Deleting a specific object from S3 bucket
    try:
        s3.delete_object(Bucket='telegramchatproject', Key=file_path)
        return True
    except Exception as e:
        print(e)
        return False

def file_upload_via_multipart(file_path, content, content_type):
    # Uploading content using multipart to S3 bucket
    data = {
        'Key': file_path,
        'Body': content,
        'ACL': 'public-read',
        'ContentType': content_type
    }
    try:
        response = s3.put_object(**data)
        return response
    except Exception as e:
        print(e)
        return None

def delete_folder(file_path):
    # Deleting a folder and its content from S3 bucket
    try:
        response = s3.list_objects_v2(Bucket='telegramchatproject', Prefix=file_path)
        if 'Contents' in response:
            delete_objects = [{'Key': obj['Key']} for obj in response['Contents']]
            s3.delete_objects(Bucket='telegramchatproject', Delete={'Objects': delete_objects})
            if response['IsTruncated']:
                delete_folder(file_path)
        return True
    except Exception as e:
        print(e)
        return False

# Exporting functions
__all__ = [
    'file_upload_via_base64',
    'delete_key',
    'file_upload_via_multipart',
    'delete_folder'
]