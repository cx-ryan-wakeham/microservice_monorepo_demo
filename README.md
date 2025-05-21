# Microservice Security Demo

This repository contains a collection of intentionally vulnerable microservices designed for security testing and demonstration purposes. Each microservice contains various security vulnerabilities that are commonly found in real-world applications.

## Structure

The microservices are organized into the following groups:

### E-Commerce Services
- `product-catalog`: Product management and inventory service
- `payment-processor`: Payment processing and transaction service
- `user-authentication`: User management and authentication service

### Analytics Services
- `data-collector`: Data collection and aggregation service
- `report-generator`: Report generation and visualization service

### Infrastructure Services
- `service-registry`: Service discovery and registration
- `config-manager`: Configuration management service

## Security Vulnerabilities

Each microservice contains intentional security vulnerabilities for demonstration purposes, including but not limited to:

### Application Vulnerabilities
- SQL Injection
- Cross-Site Scripting (XSS)
- Insecure Deserialization
- Broken Authentication
- Sensitive Data Exposure
- XML External Entities (XXE)
- Broken Access Control
- Security Misconfiguration
- Using Components with Known Vulnerabilities
- Insufficient Logging & Monitoring

### Infrastructure as Code Vulnerabilities
- Public access to resources (S3, RDS, EC2)
- Overly permissive IAM policies and roles
- Hardcoded credentials and secrets
- Missing encryption configurations
- Open security groups and network access
- No VPC or network segmentation
- Disabled security features
- Weak password policies
- Missing authentication controls
- Excessive service permissions

## Security Scanning

This repository includes automated security scanning using Checkmarx One. The scanning is configured to run:

- On every push to the main branch
- On every pull request to the main branch
- Manually via workflow dispatch

Each microservice is scanned independently, with results organized by service in the Checkmarx One dashboard. The scanning configuration can be found in `.github/workflows/checkmarx-scan.yml`.

### Required Secrets

To run the security scans, the following secrets need to be configured in your GitHub repository:

- `REGION`: Your Checkmarx One region
- `TENANT`: Your Checkmarx One tenant name
- `CLIENT_ID`: Your Checkmarx One client ID
- `CLIENT_SECRET`: Your Checkmarx One client secret

## Warning

⚠️ **IMPORTANT**: These services are intentionally vulnerable and should ONLY be used in isolated environments for security testing and educational purposes. DO NOT deploy these services in production or expose them to the internet.
