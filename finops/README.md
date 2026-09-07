# 💰 AWS FinOps Automation

<p align="center">

<img src="https://img.shields.io/badge/AWS-FinOps-orange?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/Lambda-Serverless-FF9900?style=for-the-badge&logo=awslambda&logoColor=white"/>
<img src="https://img.shields.io/badge/Cost%20Explorer-AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/SNS-Notifications-EA4335?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/SES-Email%20Reports-527FFF?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/EventBridge-Automation-8C4FFF?style=for-the-badge&logo=amazonaws&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-Boto3-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/CloudWatch-Monitoring-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>

</p>

# 📌 Project Overview

This project implements an automated **AWS FinOps monitoring and reporting system** using AWS Cost Explorer, Lambda, EventBridge, SNS, SES and CloudWatch.

The system collects the latest available AWS cost data, analyzes service-wise spending, identifies high-cost services, generates basic optimization recommendations, and sends automated reports through email.

---

# 🏗️ Architecture

## 📢 SNS Flow

```text
EventBridge
     ↓
AWS Lambda
     ↓
AWS Cost Explorer
     ↓
Python / Boto3
     ↓
Cost Analysis
     ↓
Amazon SNS
     ↓
Email
📧 SES Flow
EventBridge
     ↓
AWS Lambda
     ↓
AWS Cost Explorer
     ↓
Python / Boto3
     ↓
Cost Analysis
     ↓
HTML Dashboard
     ↓
Amazon SES
     ↓
Email
🔄 How It Works
EventBridge triggers the FinOps Lambda function on a scheduled basis.
Lambda calls AWS Cost Explorer using Python and Boto3.
Cost Explorer provides daily AWS cost data grouped by service.
Python processes and aggregates the cost information.
The system calculates total cost, daily cost, average cost and service-wise cost.
The highest-cost AWS services are identified.
Basic FinOps optimization recommendations are generated.
The report is delivered using SNS or SES.
The SES implementation generates a professional HTML cost dashboard.
CloudWatch stores Lambda execution logs for monitoring and troubleshooting.
📢 SNS Implementation

SNS was implemented as the initial notification approach.

Workflow
Cost Explorer → Lambda → Python Analysis → SNS → Email
What it Provides
Total AWS cost
Service-wise cost
Highest-cost service
Simple cost report
Email notification

File:

finops_cost_report_sns.py
📧 SES Implementation

SES is the final reporting implementation.

Workflow
Cost Explorer → Lambda → Python Analysis → HTML Dashboard → SES → Email
What it Provides
Total cost
Average daily cost
Daily cost information
Service-wise cost
Cost percentages
Highest-cost services
Optimization recommendations
HTML-based email dashboard

File:

finops_cost_report_ses.py
⏰ Automated Scheduling

Amazon EventBridge is used to automatically execute the Lambda function.

Example schedule:

cron(0 3 * * ? *)

This executes the FinOps report daily at 03:00 UTC / 08:30 IST.

📊 Cost Analysis

The application analyzes the latest available AWS cost data using:

Metric       → UnblendedCost
Granularity  → Daily
Grouping     → AWS Service
Period       → Last 7 Days

Example analysis:

EC2      → Cost
ECS      → Cost
RDS      → Cost
S3       → Cost
Lambda   → Cost
💡 FinOps Recommendations

The system provides basic recommendations such as:

EC2  → Review instance utilization and sizing
ECS  → Review task CPU and memory configuration
RDS  → Review database sizing
EBS  → Check unused volumes
S3   → Review storage lifecycle policies
📊 Monitoring

AWS CloudWatch is used to monitor Lambda executions and troubleshoot failures.

Lambda
   ↓
CloudWatch Logs
   ↓
Execution Logs / Errors
🔐 Security
Lambda uses an IAM execution role.
AWS credentials are not hard-coded.
SES/SNS configuration is provided through environment variables.
IAM permissions are kept as minimal as practical.
Sensitive information is excluded from GitHub.
🤖 Bedrock Experiment

A separate Amazon Bedrock-based FinOps experiment was also tested.

It is kept separate from the final implementation:

bedrock/
└── finops_bedrock.py

The final FinOps reporting system does not depend on Bedrock.

📁 Project Structure
finops/
│
├── finops_cost_report_sns.py
├── finops_cost_report_ses.py
└── README.md

bedrock/
└── finops_bedrock.py
🧰 AWS Services Used
AWS Service	Purpose
AWS Cost Explorer	Cost data collection
AWS Lambda	FinOps processing
Amazon EventBridge	Scheduled automation
Amazon SNS	Cost notifications
Amazon SES	HTML email reporting
Amazon CloudWatch	Monitoring and logs
AWS IAM	Access control
🎯 Project Outcome

This project demonstrates practical implementation of:

☁️ AWS Cloud
💰 FinOps
🐍 Python / Boto3
⚡ Serverless Automation
📊 Cost Analysis
📧 Email Reporting
⏰ Event-Driven Automation
🔐 IAM Security
📈 CloudWatch Monitoring

The final architecture provides an automated way to monitor AWS spending, analyze cloud costs and deliver actionable FinOps reports without manually checking the AWS Billing dashboard every day.

🚀 Future Enhancements
AWS Budgets integration
Cost Anomaly Detection
Cost forecasting
Multi-account FinOps
Cost allocation tags
Slack / Teams notifications
Grafana dashboard
AI-powered cost analysis
Automated resource rightsizing
Terraform-based deployment
👨‍💻 Author
Vaibhav Ingle

AWS DevOps Engineer | Cloud & DevOps Enthusiast

🔗 Connect With Me

GitHub:
https://github.com/vaibhavingle2002

LinkedIn:
https://www.linkedin.com/in/vaibhav-ingle-82518a274/

Email:
devopsguyvaibhav888@gmail.com

<div align="center">
💰 Monitor • Analyze • Optimize • Automate

AWS FinOps Automation — Built by Vaibhav Ingle 🚀

</div> ```
