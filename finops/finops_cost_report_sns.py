import boto3
import os
from datetime import datetime, timedelta


sns = boto3.client("sns")

ce = boto3.client(
    "ce",
    region_name="us-east-1"
)


SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):

    print("Starting AWS FinOps Cost Analysis...")


    end_date = datetime.utcnow().date()

    start_date = (
        end_date - timedelta(days=7)
    )


    response = ce.get_cost_and_usage(

        TimePeriod={
            "Start": start_date.strftime("%Y-%m-%d"),
            "End": end_date.strftime("%Y-%m-%d")
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


    total_cost = 0

    service_costs = {}


    for result in response["ResultsByTime"]:

        for group in result.get("Groups", []):

            service = group["Keys"][0]

            amount = float(
                group["Metrics"]
                ["UnblendedCost"]
                ["Amount"]
            )

            total_cost += amount

            service_costs[service] = (
                service_costs.get(service, 0)
                + amount
            )


    highest_service = (
        max(
            service_costs,
            key=service_costs.get
        )
        if service_costs
        else "N/A"
    )


    message = f"""
AWS FINOPS COST REPORT

Period:
{start_date} to {end_date}

Total AWS Cost:
${total_cost:.4f}

Highest Cost Service:
{highest_service}

Service-wise Cost:
"""


    for service, cost in sorted(
        service_costs.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        message += (
            f"\n{service}: ${cost:.4f}"
        )


    sns.publish(

        TopicArn=SNS_TOPIC_ARN,

        Subject="AWS FinOps Cost Report",

        Message=message
    )


    print(
        "FinOps report sent successfully through SNS."
    )


    return {

        "statusCode": 200,

        "body":
            "FinOps SNS report sent successfully."

    }
