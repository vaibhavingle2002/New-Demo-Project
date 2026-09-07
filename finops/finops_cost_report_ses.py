import os
from datetime import datetime, timedelta

import boto3


# ============================================================
# CONFIGURATION
# ============================================================

SENDER_EMAIL = os.environ["SENDER_EMAIL"]

RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

AWS_REGION = os.environ.get(
    "AWS_REGION",
    "ap-south-1"
)


# ============================================================
# AWS CLIENTS
# ============================================================

# Cost Explorer API
# Cost Explorer is accessed through us-east-1 endpoint.

ce = boto3.client(
    "ce",
    region_name="us-east-1"
)


# SES
ses = boto3.client(
    "ses",
    region_name=AWS_REGION
)


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print(
        "Starting AWS FinOps Dashboard..."
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
        "Cost data collected successfully."
    )


    # ========================================================
    # PROCESS COST DATA
    # ========================================================

    daily_costs = {}

    service_costs = {}


    for result in response.get(
        "ResultsByTime",
        []
    ):

        date = result[
            "TimePeriod"
        ]["Start"]


        total_daily_cost = 0


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


            total_daily_cost += amount


            service_costs[
                service
            ] = service_costs.get(
                service,
                0
            ) + amount


        daily_costs[
            date
        ] = total_daily_cost


    # ========================================================
    # TOTAL COST
    # ========================================================

    total_cost = sum(
        daily_costs.values()
    )


    days = len(
        daily_costs
    )


    average_daily_cost = (

        total_cost / days

        if days

        else 0
    )


    # ========================================================
    # HIGHEST COST SERVICE
    # ========================================================

    if service_costs:

        highest_service = max(
            service_costs,
            key=service_costs.get
        )

        highest_service_cost = (
            service_costs[
                highest_service
            ]
        )

    else:

        highest_service = "N/A"

        highest_service_cost = 0


    # ========================================================
    # SORT SERVICES
    # ========================================================

    sorted_services = sorted(

        service_costs.items(),

        key=lambda x: x[1],

        reverse=True
    )


    # ========================================================
    # SERVICE BREAKDOWN HTML
    # ========================================================

    service_rows = ""


    for service, cost in sorted_services[:10]:

        percentage = (

            (cost / total_cost) * 100

            if total_cost

            else 0
        )


        service_rows += f"""
        <tr>
            <td>{service}</td>
            <td>${cost:.4f}</td>
            <td>{percentage:.2f}%</td>
        </tr>
        """


    # ========================================================
    # DAILY COST HTML
    # ========================================================

    daily_rows = ""


    for date, cost in daily_costs.items():

        daily_rows += f"""
        <tr>
            <td>{date}</td>
            <td>${cost:.4f}</td>
        </tr>
        """


    # ========================================================
    # OPTIMIZATION RECOMMENDATIONS
    # ========================================================

    recommendations = []


    if highest_service != "N/A":

        recommendations.append(
            f"Review usage of "
            f"{highest_service}, which is "
            f"the highest-cost service."
        )


    if average_daily_cost > 0:

        recommendations.append(
            "Monitor daily cost trends "
            "and investigate unexpected increases."
        )


    recommendations.append(
        "Review unused resources and "
        "consider appropriate rightsizing."
    )


    recommendation_html = ""


    for recommendation in recommendations:

        recommendation_html += f"""
        <li>{recommendation}</li>
        """


    # ========================================================
    # HTML DASHBOARD
    # ========================================================

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <title>AWS FinOps Dashboard</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                padding: 30px;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
            }}

            h1 {{
                color: #232f3e;
            }}

            .cards {{
                display: flex;
                gap: 20px;
                margin: 20px 0;
            }}

            .card {{
                flex: 1;
                background: #f1f5f9;
                padding: 20px;
                border-radius: 8px;
            }}

            .value {{
                font-size: 25px;
                font-weight: bold;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th,
            td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background: #232f3e;
                color: white;
            }}

            li {{
                margin-bottom: 10px;
            }}

        </style>

    </head>


    <body>

        <div class="container">

            <h1>
                AWS FinOps Dashboard
            </h1>

            <p>
                Cost analysis period:
                {start} to {end}
            </p>


            <div class="cards">

                <div class="card">

                    <div>
                        Total 7-Day Cost
                    </div>

                    <div class="value">
                        ${total_cost:.4f}
                    </div>

                </div>


                <div class="card">

                    <div>
                        Average Daily Cost
                    </div>

                    <div class="value">
                        ${average_daily_cost:.4f}
                    </div>

                </div>


                <div class="card">

                    <div>
                        Highest Cost Service
                    </div>

                    <div class="value">
                        {highest_service}
                    </div>

                </div>

            </div>


            <h2>
                Service-wise Cost
            </h2>


            <table>

                <tr>
                    <th>Service</th>
                    <th>Cost</th>
                    <th>Percentage</th>
                </tr>

                {service_rows}

            </table>


            <h2>
                Daily Cost
            </h2>


            <table>

                <tr>
                    <th>Date</th>
                    <th>Cost</th>
                </tr>

                {daily_rows}

            </table>


            <h2>
                Optimization Recommendations
            </h2>


            <ul>

                {recommendation_html}

            </ul>


            <hr>

            <p>
                Generated automatically by
                AWS Lambda + Cost Explorer.
            </p>

        </div>

    </body>

    </html>
    """


    print(
        "HTML FinOps dashboard generated."
    )


    # ========================================================
    # SEND EMAIL USING SES
    # ========================================================

    ses.send_email(

        Source=SENDER_EMAIL,

        Destination={
            "ToAddresses": [
                RECIPIENT_EMAIL
            ]
        },

        Message={

            "Subject": {
                "Data":
                    "AWS FinOps Daily Cost Dashboard"
            },

            "Body": {

                "Html": {
                    "Data": html
                }

            }

        }

    )


    print(
        "FinOps dashboard email sent successfully."
    )


    return {

        "statusCode": 200,

        "body": {

            "message":
                "FinOps dashboard generated and sent successfully.",

            "total_cost":
                round(total_cost, 4)

        }

    }
