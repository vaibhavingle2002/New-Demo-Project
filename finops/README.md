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

## 🏗️ FinOps Architecture

```text
                    ┌──────────────────────┐
                    │   Amazon EventBridge  │
                    │   Daily Schedule      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     AWS Lambda       │
                    │  FinOps Cost Engine  │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │ AWS Cost Explorer│      │  Python Analysis │
        │  Cost Data       │─────▶│  & Optimization  │
        └──────────────────┘      └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │  HTML Dashboard  │
                                  │ Cost Report      │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │   Amazon SES     │
                                  │   Email Report   │
                                  └──────────────────┘
````

---

## 🔄 How It Works

1. **Amazon EventBridge** triggers the FinOps Lambda function on a daily schedule.
2. **AWS Lambda** starts the automated cost analysis process.
3. Lambda retrieves the latest available AWS cost data from **AWS Cost Explorer**.
4. Cost data is collected with daily granularity and grouped by AWS service.
5. Python processes and aggregates the service-level costs.
6. The system calculates total cost, average daily cost, and highest-cost services.
7. Services are ranked based on their AWS cost contribution.
8. Basic FinOps optimization recommendations are generated based on cost patterns.
9. An **HTML-based FinOps dashboard** is generated automatically.
10. **Amazon SES** sends the dashboard/report through email.

---

## 📧 Email Reporting

The final implementation uses **Amazon SES** for automated email delivery.

The email report includes:

* AWS cost summary
* Total cost for the reporting period
* Average daily cost
* Highest-cost AWS service
* Service-wise cost breakdown
* Cost percentage by service
* Top-cost services
* Basic FinOps optimization recommendations
* HTML visualization of major cost contributors

---

## 🔔 SNS Notification Implementation

An alternative notification implementation was also created using **Amazon SNS**.

The SNS version:

* Retrieves AWS cost data
* Calculates total cost
* Identifies the highest-cost service
* Generates a service-wise cost report
* Publishes the report to an SNS topic
* Can be connected to email or other SNS subscribers

SNS was used as an alternative notification mechanism before the final SES-based email dashboard implementation.

---

## 🤖 Bedrock FinOps Experiment

A separate Bedrock-based FinOps implementation was tested to explore AI-assisted AWS cost analysis.

### Flow

```text
EventBridge
     │
     ▼
Lambda
     │
     ├── AWS Cost Explorer
     │
     ▼
Cost Data
     │
     ▼
Amazon Bedrock
     │
     ▼
AI-Based FinOps Recommendations
```

The Bedrock Lambda was designed to send AWS cost information to an Amazon Bedrock model and generate recommendations such as:

* Highest-cost services
* Potential optimization opportunities
* Services requiring review
* General FinOps recommendations

The implementation was kept separately under the `bedrock/` directory because the Bedrock model invocation was not available in the AWS account during testing.

---

## 💰 FinOps Analysis

The system analyzes:

* Total AWS cost
* Daily AWS cost
* Service-wise AWS cost
* Highest-cost services
* Cost contribution percentage
* Average daily spending
* Potential optimization areas

The project focuses on **cost visibility, cost analysis, and basic automated governance** rather than real-time billing telemetry.

---

## 📈 Cost Optimization Recommendations

The Lambda function provides basic rule-based FinOps recommendations based on the collected cost information.

Examples include:

* Review high-cost AWS services
* Check unused resources
* Review ECS/Fargate resource allocation
* Review EC2 instance sizing
* Monitor storage and networking costs
* Investigate unexpected service-level cost increases
* Consider scheduling or scaling non-production workloads

---

## ☁️ AWS Services Used

| AWS Service               | Purpose                                |
| ------------------------- | -------------------------------------- |
| Amazon ECS Fargate        | Runs the containerized RAG application |
| Amazon ECR                | Stores Docker images                   |
| Application Load Balancer | Provides application access            |
| AWS Lambda                | Executes FinOps automation             |
| Amazon EventBridge        | Schedules automated reports            |
| AWS Cost Explorer         | Provides AWS cost data                 |
| Amazon SES                | Sends automated email reports          |
| Amazon SNS                | Alternative notification mechanism     |
| Amazon CloudWatch         | Lambda logs and monitoring             |
| AWS IAM                   | Access control and permissions         |
| AWS Secrets Manager       | Secure application secrets             |
| Amazon Bedrock            | Experimental AI-based FinOps analysis  |

---

## 🔐 Security

The project follows AWS security best practices by using:

* IAM roles instead of hardcoded AWS credentials
* AWS Secrets Manager for application secrets
* Environment variables for configuration
* IAM least-privilege permissions where applicable
* CloudWatch for Lambda execution logs
* Private ECR repository for container images

Sensitive API keys and credentials are not stored in the GitHub repository.

---

## 📁 FinOps Project Structure

```text
RAG-Application-AWS-ECS-Fargate-FinOps/
│
├── app.py
├── loader.py
├── Splitters.py
├── model.py
├── Vectors.py
├── Dockerfile
├── requirements.txt
├── .gitignore
│
├── finops/
│   ├── finops_cost_report_ses.py
│   ├── finops_cost_report_sns.py
│   └── README.md
│
├── bedrock/
│   ├── finops_bedrock.py
│   └── README.md
│
├── docs/
│   └── architecture.png
│
└── README.md
```

---

## 🐍 FinOps Python Components

### `finops_cost_report_ses.py`

Main production FinOps Lambda implementation.

Responsibilities:

* Retrieve AWS cost data
* Analyze service-level costs
* Calculate cost metrics
* Generate HTML dashboard
* Generate optimization recommendations
* Send the report through Amazon SES

### `finops_cost_report_sns.py`

Alternative SNS-based FinOps notification implementation.

Responsibilities:

* Retrieve AWS cost data
* Calculate total and service-level costs
* Identify the highest-cost service
* Generate a text-based report
* Publish the report to Amazon SNS

### `bedrock/finops_bedrock.py`

Experimental AI-assisted FinOps implementation.

Responsibilities:

* Retrieve AWS cost data
* Prepare cost summary
* Send cost information to Amazon Bedrock
* Request AI-generated FinOps recommendations

This implementation is retained as an **experimental component** and was not used in the final production workflow.

---

## 📊 Monitoring

AWS CloudWatch is used to monitor the FinOps Lambda execution.

Important logs include:

* FinOps process started
* Cost data collected
* Dashboard generated
* Email successfully sent
* Lambda execution errors

This provides visibility into the automated reporting pipeline.

---

## ⏰ Automation

The FinOps report is scheduled using Amazon EventBridge.

Example schedule:

```text
cron(0 3 * * ? *)
```

This runs the Lambda every day at **03:00 UTC / 08:30 IST**.

---

## 🎯 Project Outcome

This project demonstrates how AWS cloud infrastructure can be combined with **FinOps automation** to continuously monitor cloud spending and provide actionable cost visibility.

The final workflow provides:

```text
AWS Cost Data
      ↓
Cost Analysis
      ↓
FinOps Metrics
      ↓
Optimization Recommendations
      ↓
HTML Dashboard
      ↓
Automated Email
```

---

## 🚀 Future Enhancements

* AWS Cost Anomaly Detection integration
* AWS Budgets integration
* Cost threshold alerts
* ECS Fargate cost optimization
* Automated resource rightsizing
* Savings Plans / Reserved Instances analysis
* Multi-account FinOps reporting
* Historical cost dashboards
* Amazon QuickSight visualization
* AI-powered cost recommendations using Amazon Bedrock when account access is available

---

## 🏆 Key DevOps & Cloud Concepts Demonstrated

* AWS ECS Fargate
* Docker containerization
* Amazon ECR
* Application Load Balancer
* AWS Lambda
* Amazon EventBridge
* AWS Cost Explorer
* Amazon SES
* Amazon SNS
* AWS IAM
* AWS Secrets Manager
* Amazon CloudWatch
* Serverless automation
* Cloud cost monitoring
* FinOps
* Cost optimization
* Automated reporting
* Infrastructure monitoring

---

## 📌 Project Classification

**DevOps / Cloud:** ✅
**FinOps:** ✅
**RAG:** ✅
**Serverless Automation:** ✅
**AI-assisted FinOps:** Experimental
**MLOps:** ❌
**AIOps:** ❌

The project combines a **containerized RAG application on ECS Fargate** with an independent **AWS FinOps automation pipeline** for cloud cost monitoring and reporting.

---

## 👨‍💻 Author

**Vaibhav Sudhakar Ingle**

AWS DevOps Engineer | Cloud & DevOps Enthusiast

Skills demonstrated through this project:

`AWS` `Docker` `ECS` `Fargate` `ECR` `Lambda` `EventBridge` `Cost Explorer` `SES` `SNS` `CloudWatch` `IAM` `Secrets Manager` `FinOps` `Python` `RAG`

```
```
