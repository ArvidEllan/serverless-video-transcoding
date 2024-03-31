import boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    
    # Extract the Rekognition job ID from the event
    rekognition_job_id = event['rekognitionJobId']
    
    # Check the status of the Rekognition job
    response = rekognition.get_label_detection(JobId=rekognition_job_id)
    
    # Extract the job status
    job_status = response['JobStatus']
    
    # Return the job status along with the rekognitionJobId
    return {
        'rekognitionJobId': rekognition_job_id, 
        'statusCode': 200,
        'status': job_status  
    }