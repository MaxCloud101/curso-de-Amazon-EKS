import boto3
from flask import Flask, jsonify

app = Flask(__name__)


def get_eks_clusters():
    eks_client = boto3.client("eks")
    region = eks_client.meta.region_name
    paginator = eks_client.get_paginator("list_clusters")
    clusters = []

    for page in paginator.paginate():
        for cluster_name in page.get("clusters", []):
            clusters.append({
                "name": cluster_name,
                "region": region,
            })

    return clusters

@app.route("/")
def list_eks_clusters():
    return jsonify(get_eks_clusters())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
