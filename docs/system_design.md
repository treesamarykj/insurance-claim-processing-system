# Health Insurance Claim Processing System

## Overview
This platform processes health insurance claims submitted through multiple channels including scanned documents (PDF) and structured data formats (CSV/JSON).

The system extracts claim data, validates eligibility, performs similarity analysis, and applies fraud detection before storing the results for tracking and auditing.

## Architecture

Frontend
- React dashboard

Backend
- FastAPI services

Processing
- AWS Step Functions
- AWS Lambda

Storage
- Amazon S3 (claim documents & batch files)

Database
- PostgreSQL (claims & batch metadata)

## S3 Storage Structure

claim-processing-bucket
│
├── offline_claims/
│     ├── claim_1001.pdf
│     └── claim_1002.pdf
│
├── online_claims/
│     ├── claim_2001.pdf
│
└── extracted_claims/
      ├── claim_1001.json
      └── claim_1002.json

## High Level Architecture

User
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
S3 (Claim Documents)
   ↓
Step Functions
   ↓
Lambda Processing Services
   ↓
PostgreSQL Database
   ↓
Dashboard APIs

## Claim Intake Channels

The platform supports two claim submission methods.

### Online Claims

Users submit claim details through the web interface.

Flow:

User fills claim form  
      ↓  
API receives request  
      ↓  
Claim record stored in PostgreSQL  
      ↓  
Claim PDF generated and stored in S3  
      ↓  
Processing pipeline triggered

### Offline Claims

Users upload scanned claim documents (PDF).

Flow:

User uploads claim PDF  
      ↓  
File stored in Amazon S3  
      ↓  
Document extraction service extracts structured data  
      ↓  
Claim processing pipeline triggered

## Core Workflow

1. User uploads claim batch
2. Batch stored in S3
3. Step Function triggers processing
4. Lambda services perform checks:
   - Similarity check
   - Historical claim validation
   - Eligibility verification
   - Fraud detection
5. Results stored in PostgreSQL
6. Dashboard shows processing results

## Environments

- dev
- test
- prod
- prod_hotfix

## Batch Input Formats

Supported formats:
- CSV
- JSON

## Core Tables

claims  
claim_batches  
processing_logs

## Event Driven Processing Flow

1. Batch file uploaded through API
2. File stored in Amazon S3
3. S3 event triggers processing workflow
4. AWS Step Functions orchestrate claim processing
5. Each claim passes through multiple Lambda stages:

   - Similarity Check Service
   - Historical Claim Check Service
   - Eligibility Service
   - Benefit Calculation Service
   - Fraud Detection Service

6. Processed claim results stored in PostgreSQL
7. Dashboard retrieves claim status via API

## Processing Pipeline

Upload Batch
      ↓
Store in S3
      ↓
Extract Claim Records
      ↓
Parallel Claim Processing
      ↓
Eligibility + Fraud Checks
      ↓
Store Results in Database
      ↓
Dashboard View

## Service Architecture

The platform consists of multiple services responsible for different stages of claim processing.

### Claim Intake Service
Responsible for:
- Accepting batch uploads (CSV/JSON)
- Storing files in S3
- Creating batch metadata

### Claim Parsing Service
Responsible for:
- Parsing CSV/JSON batch files
- Creating individual claim records

### Claim Processing Service
Responsible for:
- Running validation checks
- Triggering eligibility checks

### Eligibility Service
Responsible for:
- Checking policy eligibility
- Verifying coverage limits

### Fraud Detection Service
Responsible for:
- Detecting duplicate claims
- Similarity analysis
- Risk scoring

### Claim Result Service
Responsible for:
- Updating claim status
- Persisting results in PostgreSQL
- Serving claim results to the dashboard

## Database Architecture

The platform uses PostgreSQL as the primary database.

### claim_batches
Stores batch metadata.

Fields:
- batch_id
- file_name
- total_records
- status
- created_at

### claims
Stores individual claim records.

Fields:
- claim_id
- batch_id
- member_id
- hospital_name
- diagnosis_code
- procedure_code
- claim_amount
- fraud_score
- eligibility_status
- claim_status
- created_at

### processing_logs
Tracks claim processing steps.

Fields:
- log_id
- claim_id
- stage
- status
- message
- created_at



## Claim Processing Pipeline

The system processes claims through a multi-stage pipeline orchestrated by AWS Step Functions.

Each claim goes through the following stages:

1. Claim Intake  
   - Batch file uploaded
   - Metadata stored in database

2. Claim Parsing  
   - CSV/JSON parsed
   - Individual claims extracted

3. Similarity Check  
   - Detect duplicate claims
   - Compare against historical claims

4. Historical Claim Validation  
   - Check previous claims for the member
   - Detect repeated treatments

5. Eligibility Verification  
   - Validate insurance policy
   - Verify treatment coverage

6. Benefit Calculation  
   - Determine payable amount
   - Apply policy limits

7. Fraud Detection  
   - Identify abnormal patterns
   - Assign fraud risk score

8. Claim Finalization  
   - Update claim status
   - Store results in database

### Processing Flow

Upload Batch
      ↓
Parse Claims
      ↓
Similarity Check
      ↓
Historical Validation
      ↓
Eligibility Check
      ↓
Benefit Calculation
      ↓
Fraud Detection
      ↓
Store Results

## Scalability and Fault Tolerance

The platform is designed to handle large volumes of insurance claims.

### Horizontal Scaling

The system uses serverless services that automatically scale:

- AWS Lambda scales based on request volume
- Step Functions allow parallel claim processing
- S3 supports unlimited file storage

### Batch Processing

Claims are processed in batches to efficiently handle large datasets.

Example:

Batch Size = 1000 claims

Step Functions can process claims in parallel using Lambda workers.

### Fault Handling

If a claim processing stage fails:

- The error is logged in the processing_logs table
- Step Functions retry the failed step
- Failed claims are marked for manual review

### Retry Strategy

Each Lambda stage can retry failed operations:

- Database connection errors
- Temporary service failures

Retry example:

- Retry count: 3
- Exponential backoff

### Monitoring

System monitoring is implemented using:

- AWS CloudWatch logs
- Processing logs stored in PostgreSQL

## Event Driven Architecture

The system follows an event-driven architecture to decouple services and enable asynchronous claim processing.

### Event Sources

The main event sources include:

- Batch file upload events
- Claim processing events
- Processing completion events

### Event Flow

1. Claim batch uploaded through API
2. File stored in Amazon S3
3. S3 upload event triggers processing workflow
4. AWS Step Functions orchestrate claim processing
5. Each processing stage invokes Lambda functions
6. Processing results stored in PostgreSQL
7. Dashboard APIs retrieve claim status

### Event Pipeline

User Upload
     ↓
API Service
     ↓
Store File in S3
     ↓
S3 Event Trigger
     ↓
Step Functions Workflow
     ↓
Lambda Processing Services
     ↓
PostgreSQL Database
     ↓
Dashboard API

## Security and Compliance

The platform handles sensitive healthcare data and must follow strict security practices.

### Data Protection

Sensitive data such as patient information and claim details are protected using:

- Encryption at rest (S3 and PostgreSQL)
- Encryption in transit using HTTPS

### Access Control

Role-based access control (RBAC) is implemented for different user roles:

- Claim processors
- Administrators
- Auditors

### Secure Storage

Claim documents stored in Amazon S3 use:

- Private buckets
- Access policies
- Versioning for audit purposes

### Audit Logging

All claim processing activities are logged:

- Claim status updates
- Processing stages
- User actions

Logs are stored for auditing and compliance monitoring.

### Secrets Management

Environment credentials such as database passwords and AWS keys are stored securely using environment configuration files.


## Machine Learning Components

Machine learning models are used to enhance claim processing.

### Document Extraction

Scanned claim documents are processed using OCR/ML models to extract structured information such as member ID, diagnosis code, and claim amount.

### Claim Similarity Detection

A similarity model compares new claims with historical claims to detect duplicates or suspicious patterns.

### Fraud Detection

A fraud detection model assigns a fraud probability score based on claim attributes and historical data.