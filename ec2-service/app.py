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

ec2_client = create_client("ec2", region)

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


@app.route("/start-instance/<instance_id>", methods=["POST"])
def start_instance(instance_id):
    ec2_client.start_instances(InstanceIds=[instance_id])
    return jsonify({"InstanceId": instance_id, "Action": "starting"})


@app.route("/stop-instance/<instance_id>", methods=["POST"])
def stop_instance(instance_id):
    ec2_client.stop_instances(InstanceIds=[instance_id])
    return jsonify({"InstanceId": instance_id, "Action": "stopping"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
