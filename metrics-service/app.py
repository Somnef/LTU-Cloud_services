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

region = "eu-north-1" 

ec2_client = create_client("ec2", region)
cloudwatch_client = create_client("cloudwatch", region)

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
    app.run(host="0.0.0.0", port=5002)
