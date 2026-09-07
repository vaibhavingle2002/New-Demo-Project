import boto3
import json
import os
from datetime import datetime, timedelta


# ============================================================
# AWS CLIENTS
# ============================================================

ce = boto3.client(
    "ce",
    region_name="us-east-1"
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.environ.get(
        "AWS_REGION",
        "ap-south-1"
    )
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID",
    "us.amazon.nova-lite-v1:0"
)


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print(
        "Starting Bedrock-based FinOps analysis..."
    )


    # ========================================================
    # DATE RANGE
    # ========================================================

    end_date = datetime.utcnow().date()

    start_date = (
        end_date - timedelta(days=7)
    )


    start = start_date.strftime(
        "%Y-%m-%d"
    )

    end = end_date.strftime(
        "%Y-%m-%d"
    )


    # ========================================================
    # COST EXPLORER
    # ========================================================

    response = ce.get_cost_and_usage(

        TimePeriod={
            "Start": start,
            "End": end
        },

        Granularity="DAILY",

        Metrics=[
            "UnblendedCost"
        ],

        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )


    print(
        "AWS cost data collected."
    )


    # ========================================================
    # PREPARE COST DATA
    # ========================================================

    service_costs = {}

    total_cost = 0


    for result in response.get(
        "ResultsByTime",
        []
    ):

        for group in result.get(
            "Groups",
            []
        ):

            service = group[
                "Keys"
            ][0]


            amount = float(
                group[
                    "Metrics"
                ]["UnblendedCost"][
                    "Amount"
                ]
            )


            total_cost += amount


            service_costs[
                service
            ] = service_costs.get(
                service,
                0
            ) + amount


    # ========================================================
    # PREPARE PROMPT
    # ========================================================

    cost_summary = json.dumps(
        service_costs,
        indent=2
    )


    prompt = f"""
You are an AWS FinOps assistant.

Analyze the following AWS cost data.

Total AWS cost for the last 7 days:
${total_cost:.4f}

Service-wise cost:

{cost_summary}

Provide:

1. Highest-cost AWS services
2. Potential cost optimization opportunities
3. Services that should be reviewed
4. General FinOps recommendations

Keep the response concise and practical.
"""


    # ========================================================
    # BEDROCK REQUEST
    # ========================================================

    request_body = {

        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],

        "inferenceConfig": {
            "maxTokens": 500
        }

    }


    print(
        f"Invoking Amazon Bedrock model: "
        f"{MODEL_ID}"
    )


    response = bedrock.invoke_model(

        modelId=MODEL_ID,

        body=json.dumps(
            request_body
        ),

        contentType="application/json",

        accept="application/json"

    )


    # ========================================================
    # RESPONSE
    # ========================================================

    result = json.loads(
        response["body"].read()
    )


    print(
        "Bedrock analysis completed."
    )


    print(
        json.dumps(
            result,
            indent=2
        )
    )


    return {

        "statusCode": 200,

        "body": {

            "message":
                "Bedrock FinOps analysis completed.",

            "total_cost":
                round(
                    total_cost,
                    4
                ),

            "analysis":
                result

        }

    }
