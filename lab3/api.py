from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Create EC2 and CloudWatch Clients
def create_client(service, region_name):
    return boto3.client(service, region_name=region_name)

region = "eu-north-1"  # Update your region
# key_pair = "lab3-key"
# security_group = "sg-07fc8258ee8b3f718"
# instance_type = "t3.micro"
# ami_id = "ami-01c5beab73c20ddeb"

ec2_client = create_client("ec2", region)
cloudwatch_client = create_client("cloudwatch", region)

# Flask Endpoints
@app.route("/instances", methods=["GET"])
def list_instances():
    # get all instances in all regions
    response = ec2_client.describe_instances()
    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "Name": next(
                    (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                    "No Name"
                ),
                "InstanceType": instance["InstanceType"],
                "AvailabilityZone": instance["Placement"]["AvailabilityZone"],
            })

    # sort instances by name then by state then by instance id
    instances.sort(key=lambda x: (x["Name"], x["State"], x["InstanceId"]))

    return jsonify({"Instances": instances})

@app.route("/create-instance", methods=["POST"])
def create_instance():
    data = request.json
    instance_name = data["Name"]
    instance_type = data["InstanceType"]
    # ami_id = data["AmiId"]
    # key_pair = data["KeyPair"]
    # security_group = data["SecurityGroup"]
    ami_id = "ami-01c5beab73c20ddeb"
    key_pair = "lab3-key"
    security_group = "sg-07fc8258ee8b3f718"

    # check instance type
    if instance_type not in ["t3.micro"]:
        instance_type = "t3.micro"

    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_pair,
            SecurityGroupIds=[security_group],
            MinCount=1,
            MaxCount=1,
        )
    except Exception as e:
        return jsonify({"Error": str(e)})

    instance_id = response["Instances"][0]["InstanceId"]
    ec2_client.create_tags(Resources=[instance_id], Tags=[{"Key": "Name", "Value": instance_name}])

    return jsonify({"InstanceId": instance_id, "Action": "creating"})

@app.route("/instance-status/<instance_id>", methods=["GET"])
def get_instance_status(instance_id):
    response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
    status = response["InstanceStatuses"][0]["InstanceState"]["Name"] if response["InstanceStatuses"] else "No status available."
    return jsonify({"InstanceId": instance_id, "Status": status})

@app.route("/start-instance/<instance_id>", methods=["POST"])
def start_instance(instance_id):
    ec2_client.start_instances(InstanceIds=[instance_id])
    return jsonify({"InstanceId": instance_id, "Action": "starting"})

@app.route("/stop-instance/<instance_id>", methods=["POST"])
def stop_instance(instance_id):
    ec2_client.stop_instances(InstanceIds=[instance_id])
    return jsonify({"InstanceId": instance_id, "Action": "stopping"})

@app.route("/instance-metrics/<instance_id>", methods=["GET"])
def get_instance_metrics(instance_id):
    metrics = [
        {"Name": "CPUUtilization", "Namespace": "AWS/EC2", "Unit": "Percent"},
        {"Name": "DiskReadBytes", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "DiskWriteBytes", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "NetworkIn", "Namespace": "AWS/EC2", "Unit": "Bytes"},
        {"Name": "NetworkOut", "Namespace": "AWS/EC2", "Unit": "Bytes"},
    ]

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=60)

    metrics_data = []
    for metric in metrics:
        response = cloudwatch_client.get_metric_statistics(
            Namespace=metric["Namespace"],
            MetricName=metric["Name"],
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average", "Maximum"],
            Unit=metric["Unit"],
        )

        metrics_data.append({
            "name": metric["Name"],
            "data": {
                "labels": [datapoint["Timestamp"].isoformat() for datapoint in response["Datapoints"]],
                "datasets": [{
                    "label": metric["Name"],
                    "data": [datapoint["Average"] for datapoint in response["Datapoints"]],
                }],
            },
        })

    return jsonify({"InstanceId": instance_id, "Metrics": metrics_data})

if __name__ == "__main__":
    app.run(debug=True)
