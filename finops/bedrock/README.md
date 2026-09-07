<div align="center">

# 🤖 AWS Bedrock FinOps Experiment

### 🧠 AI-Powered AWS Cost Analysis & Optimization

<p>
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS-Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS-Cost%20Explorer-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<br>

### 👨‍💻 Experiment Designed & Implemented By

# **Vaibhav Ingle**

### AWS DevOps Engineer | Cloud & DevOps Enthusiast

<br>

<a href="https://github.com/vaibhavingle2002">
<img src="https://img.shields.io/badge/GitHub-vaibhavingle2002-181717?style=for-the-badge&logo=github"/>
</a>

<a href="https://www.linkedin.com/in/vaibhav-ingle-82518a274/">
<img src="https://img.shields.io/badge/LinkedIn-Vaibhav%20Ingle-0A66C2?style=for-the-badge&logo=linkedin"/>
</a>

<a href="mailto:devopsguyvaibhav888@gmail.com">
<img src="https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

</div>

---

# 📌 Table of Contents

- [About the Experiment](#-about-the-experiment)
- [Objective](#-objective)
- [Why Amazon Bedrock](#-why-amazon-bedrock)
- [Architecture](#-architecture)
- [Detailed Architecture Flow](#-detailed-architecture-flow)
- [AWS Services Used](#-aws-services-used)
- [Prerequisites](#-prerequisites)
- [Step 1 - Verify AWS Region](#1--verify-aws-region)
- [Step 2 - Enable Cost Explorer](#2--enable-cost-explorer)
- [Step 3 - Create Lambda Function](#3--create-lambda-function)
- [Step 4 - Create IAM Role](#4--create-iam-role)
- [Step 5 - Configure Cost Explorer Permissions](#5--configure-cost-explorer-permissions)
- [Step 6 - Configure Bedrock Permissions](#6--configure-bedrock-permissions)
- [Step 7 - Configure Lambda Environment Variables](#7--configure-lambda-environment-variables)
- [Step 8 - Create the Lambda Function](#8--create-the-lambda-function)
- [Step 9 - Deploy the Python Code](#9--deploy-the-python-code)
- [Step 10 - Test Cost Explorer](#10--test-cost-explorer)
- [Step 11 - Test Amazon Bedrock](#11--test-amazon-bedrock)
- [Step 12 - Bedrock Model Testing](#12--bedrock-model-testing)
- [Step 13 - Error Encountered](#13--error-encountered)
- [Step 14 - Troubleshooting](#14--troubleshooting)
- [Step 15 - Final Result](#15--final-result)
- [Production FinOps Solution](#-production-finops-solution)
- [Project Structure](#-project-structure)
- [Code](#-code)
- [Security](#-security)
- [Learning Outcomes](#-learning-outcomes)
- [Future Enhancements](#-future-enhancements)
- [Project Status](#-project-status)
- [Author](#-author)

---

# 🤖 About the Experiment

This folder contains an **experimental Amazon Bedrock integration for AWS FinOps**.

The objective was to explore whether Generative AI could analyze AWS Cost Explorer data and generate intelligent recommendations for cloud cost optimization.

The experiment was implemented independently from the main RAG application.

The intended workflow was:

```text
AWS Cost Explorer
        │
        ▼
AWS Lambda
        │
        ▼
Python Cost Processing
        │
        ▼
FinOps Prompt
        │
        ▼
Amazon Bedrock
        │
        ▼
AI Cost Analysis
        │
        ▼
Optimization Recommendations
