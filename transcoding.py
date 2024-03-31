import os
import boto3
from botocore.exceptions import ClientError

mediaconvert = boto3.client('mediaconvert')

def lambda_handler(event, context):
    try:
        # Get the input video file details from the event
        input_video = event['inputVideo']
        input_bucket = input_video['bucket']
        input_key = input_video['key']

        # Set up the MediaConvert job settings
        job_settings = {
            'Role': os.environ['MEDIA_CONVERT_ROLE_ARN'],
            'Settings': {
                'Inputs': [
                    {
                        'AudioSelectors': {
                            'Audio Selector 1': {
                                'Offset': 0,
                                'DefaultSelection': 'NOT_DEFAULT',
                                'ProgramSelection': 1
                            }
                        },
                        'VideoSelector': {},
                        'TimecodeSource': 'EMBEDDED',
                        'FileInput': f's3://{input_bucket}/{input_key}'
                    }
                ],
                'OutputGroups': [
                    {
                        'Name': 'File Group',
                        'OutputGroupSettings': {
                            'Type': 'FILE_GROUP_SETTINGS',
                            'FileGroupSettings': {
                                'Destination': f's3://{os.environ["OUTPUT_BUCKET"]}/'
                            }
                        },
                        'Outputs': [
                            {
                                'VideoDescription': {
                                    'ScalingBehavior': 'DEFAULT',
                                    'TimecodeInsertion': 'DISABLED',
                                    'AntiAlias': 'ENABLED',
                                    'Sharpness': 50,
                                    "CodecSettings": {
                                        "Codec": "H_264",
                                        "H264Settings": {
                                            "InterlaceMode": "PROGRESSIVE",
                                            "NumberReferenceFrames": 3,
                                            "Syntax": "DEFAULT",
                                            "Softness": 0,
                                            "GopClosedCadence": 1,
                                            "GopSize": 90,
                                            "Slices": 1,
                                            "GopBReference": "DISABLED",
                                            "SlowPal": "DISABLED",
                                            "SpatialAdaptiveQuantization": "ENABLED",
                                            "TemporalAdaptiveQuantization": "ENABLED",
                                            "FlickerAdaptiveQuantization": "DISABLED",
                                            "EntropyEncoding": "CABAC",
                                            "Bitrate": 5000000,
                                            "FramerateControl": "SPECIFIED",
                                            "RateControlMode": "CBR",
                                            "CodecProfile": "MAIN",
                                            "Telecine": "NONE",
                                            "MinIInterval": 0,
                                            "AdaptiveQuantization": "HIGH",
                                            "CodecLevel": "AUTO",
                                            "FieldEncoding": "PAFF",
                                            "SceneChangeDetect": "ENABLED",
                                            "QualityTuningLevel": "SINGLE_PASS",
                                            "FramerateConversionAlgorithm": "DUPLICATE_DROP",
                                            "UnregisteredSeiTimecode": "DISABLED",
                                            "GopSizeUnits": "FRAMES",
                                            "ParControl": "SPECIFIED",
                                            "NumberBFramesBetweenReferenceFrames": 2,
                                            "RepeatPps": "DISABLED",
                                            "DynamicSubGop": "STATIC",
                                            "ParDenominator": 1,
                                            "FramerateNumerator": 30,
                                            "FramerateDenominator": 1
                                        }
                                    },
                                    'AfdSignaling': 'NONE',
                                    'DropFrameTimecode': 'ENABLED',
                                    'RespondToAfd': 'NONE',
                                    'ColorMetadata': 'INSERT'
                                },
                                'AudioDescriptions': [
                                    {
                                        'AudioTypeControl': 'FOLLOW_INPUT',
                                        'CodecSettings': {
                                            'Codec': 'AAC',
                                            'AacSettings': {
                                                'AudioDescriptionBroadcasterMix': 'NORMAL',
                                                'RateControlMode': 'CBR',
                                                'CodecProfile': 'LC',
                                                'CodingMode': 'CODING_MODE_2_0',
                                                'RawFormat': 'NONE',
                                                'SampleRate': 48000,
                                                'Specification': 'MPEG4',
                                                'Bitrate': 64000
                                            }
                                        },
                                        'LanguageCodeControl': 'FOLLOW_INPUT',
                                        'AudioSourceName': 'Audio Selector 1'
                                    }
                                ],
                                'ContainerSettings': {
                                    'Container': 'MP4',
                                    'Mp4Settings': {
                                        'CslgAtom': 'INCLUDE',
                                        'FreeSpaceBox': 'EXCLUDE',
                                        'MoovPlacement': 'PROGRESSIVE_DOWNLOAD'
                                    }
                                }
                            }
                        ]
                    }
                ],
                'TimecodeConfig': {
                    'Source': 'EMBEDDED'
                }
            }
        }

        # Create the MediaConvert job
        mediaconvert_result = mediaconvert.create_job(**job_settings)
        print(f'MediaConvert job created: {mediaconvert_result["Job"]["Id"]}')

        return {
            'jobId': mediaconvert_result['Job']['Id'],
            'outputBucket': os.environ['OUTPUT_BUCKET'],
            'transcodedVideoKey': f"{input_key}" 
        }


    except ClientError as e:
        print(f'Error: {e}')
        raise e