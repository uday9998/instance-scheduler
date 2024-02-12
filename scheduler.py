import os
import boto3

def get_instance_ids_from_env_var():
    """Retrieves instance IDs from the specified environment variable."""
    raw_instance_id= os.environ['list_of_instances']
    instance_ids = raw_instance_id.split(",")
    return instance_ids

def start_instance(instance_id):
    # Function to start the EC2 instance
    try:
        ec2 = boto3.client('ec2',region_name="af-south-1")
        ec2.start_instances(InstanceIds=[instance_id])
        return True
    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}")
        return False

def stop_instance(instance_id):
    # Function to stop the EC2 instance
    try:
        ec2 = boto3.client('ec2',region_name="af-south-1")
        ec2.stop_instances(InstanceIds=[instance_id])
        return True
    except Exception as e:
        print(f"Error stopping instance {instance_id}: {e}")
        return False

def lambda_handler(event, context):
    instance_ids = get_instance_ids_from_env_var()
    
    for instance_id in instance_ids:
        """Handles a CloudWatch event to start or stop instances."""
        event_name = event['resources'][0].split("/")[-1]

        if 'StartInstances' in event_name:
            success = start_instance(instance_id)
            if success:
                print(f"Successfully started instance {instance_id}")
            else:
                print(f"Failed to start instance {instance_id}")

        elif 'StopInstances' in event_name:
            success = stop_instance(instance_id)
            if success:
                print(f"Successfully stopped instance {instance_id}")
            else:
                print(f"Failed to stop instance {instance_id}")

        else:
            print(f"Ignoring event {event_name} for instance {instance_id}")

    return {
        'statusCode': 200,
        'body': 'Function execution complete.'
    }
