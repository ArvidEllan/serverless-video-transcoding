import os
import boto3
from botocore.exceptions import ClientError

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        output_bucket = event['outputBucket']
        transcoded_video_key = event['transcodedVideoKey']

        response = rekognition.start_label_detection(
            Video={
                'S3Object': {
                    'Bucket': output_bucket,
                    'Name': transcoded_video_key
                }
            },
            MinConfidence=50,
            NotificationChannel={
                'SNSTopicArn': os.environ['SNS_TOPIC'],
                'RoleArn': os.environ['REKOGNITION_NOTIFICATION_ROLE_ARN']
            }
        )

        return {
            'rekognitionJobId': response['JobId']
        }

    except ClientError as e:
        print(f'Error: {e}')
        raise e