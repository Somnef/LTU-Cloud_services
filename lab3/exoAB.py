import boto3
from datetime import datetime, timedelta
import json


# Create EC2 and CloudWatch Clients
def create_ec2_client(region_name):
    return boto3.client("ec2", region_name=region_name)


def create_cloudwatch_client(region_name):
    return boto3.client("cloudwatch", region_name=region_name)


# List All EC2 Instances
def list_instances(ec2_client):
    response = ec2_client.describe_instances()
    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_data = {
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "Name": next(
                    (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                    "No Name"
                )
            }
            instances.append(instance_data)

    return json.dumps({"Instances": instances}, indent=2)


# Run an EC2 Instance
def run_instance(ec2_client, key_pair, security_group, instance_type, ami_id, instance_count):
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_pair,
        SecurityGroupIds=[security_group],
        MinCount=1,
        MaxCount=1,
    )
    instance_id = response["Instances"][0]["InstanceId"]

    # Assign an incremental name using instance count
    instance_name = f"Instance-{instance_count}"
    ec2_client.create_tags(
        Resources=[instance_id],
        Tags=[{"Key": "Name", "Value": instance_name}],
    )

    return json.dumps({
        "InstanceId": instance_id,
        "Name": instance_name,
        "State": "pending"
    }, indent=2)


# Retrieve Instance Status
def get_instance_status(ec2_client, instance_id):
    response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
    if len(response["InstanceStatuses"]) > 0:
        status = response["InstanceStatuses"][0]["InstanceState"]["Name"]
    else:
        status = "No status available (likely stopped)."

    return json.dumps({
        "InstanceId": instance_id,
        "Status": status
    }, indent=2)


# Stop an EC2 Instance
def stop_instance(ec2_client, instance_id):
    ec2_client.stop_instances(InstanceIds=[instance_id])
    return json.dumps({
        "InstanceId": instance_id,
        "Action": "stopping"
    }, indent=2)


# Monitor EC2 Instance Metrics
def get_instance_metrics(cloudwatch_client, instance_id):
    # Define metrics to monitor
    metrics = [
        {"Name": "CPUUtilization", "Namespace": "AWS/EC2", "Unit": "Percent"},
        {"Name": "DiskReadBytes", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "DiskWriteBytes", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "NetworkIn", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "NetworkOut", "Namespace": "AWS/EC2", "Unit": "Bytes"},
    ]

    # Time range for metric data
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=60)  # Last 60 minutes

    metrics_data = []

    for metric in metrics:
        response = cloudwatch_client.get_metric_statistics(
            Namespace=metric["Namespace"],
            MetricName=metric["Name"],
            Dimensions=[
                {"Name": "InstanceId", "Value": instance_id},
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # Data aggregated every 5 minutes
            Statistics=["Average", "Maximum"],
            Unit=metric["Unit"],
        )

        metric_data = {
            "Metric": metric["Name"],
            "Datapoints": [
                {
                    "Timestamp": datapoint["Timestamp"].isoformat(),
                    "Average": datapoint.get("Average", "N/A"),
                    "Maximum": datapoint.get("Maximum", "N/A"),
                }
                for datapoint in response["Datapoints"]
            ]
        }
        metrics_data.append(metric_data)

    return json.dumps({
        "InstanceId": instance_id,
        "Metrics": metrics_data
    }, indent=2)


# Main Program
if __name__ == "__main__":
    # Define parameters
    region = "eu-north-1"  # Example region
    key_pair = "lab3-key"  # Replace with your key pair
    security_group = "sg-07fc8258ee8b3f718"  # Replace with your security group ID
    instance_type = "t3.micro"
    ami_id = "ami-01c5beab73c20ddeb"  # Replace with your AMI ID

    # Create EC2 and CloudWatch Clients
    ec2_client = create_ec2_client(region)
    cloudwatch_client = create_cloudwatch_client(region)

    # List all instances
    print(list_instances(ec2_client))

    # Keep track of instance count for naming
    instance_count = 1

    # Run an EC2 Instance with Incremental Name
    instance_data = run_instance(
        ec2_client,
        key_pair,
        security_group,
        instance_type,
        ami_id,
        instance_count,
    )
    print(instance_data)

    # Retrieve Instance Status
    instance_id = json.loads(instance_data)["InstanceId"]
    print(get_instance_status(ec2_client, instance_id))

    # Monitor the Instance
    print(get_instance_metrics(cloudwatch_client, instance_id))

    # Stop the EC2 Instance
    print(stop_instance(ec2_client, instance_id))

    # Increment instance count for the next instance
    instance_count += 1
