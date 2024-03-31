import boto3
import json

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    
    try:
        # Extract the Rekognition job ID from the event
        rekognition_job_id = event['rekognitionJobId']

        # Fetch the analysis results
        response = rekognition.get_label_detection(JobId=rekognition_job_id)
        
        # Check the job status and proceed accordingly
        if response['JobStatus'] == 'SUCCEEDED':
            # Process and return the labels detected in the video
            # This example simplifies the response to include relevant details
            labels = response.get('Labels', [])
            return {
                'statusCode': 200,
                'body': json.dumps({'Labels': labels, 'JobStatus': response['JobStatus']}, default=str)
            }
        else:
            # Handle other job statuses as needed
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Rekognition job did not succeed', 'JobStatus': response['JobStatus']})
            }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': "Missing 'rekognitionJobId' in the input."})
        }
    except Exception as e:
        # Generic error handling
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }