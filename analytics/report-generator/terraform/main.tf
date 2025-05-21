terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Insecure: Lambda function with no VPC configuration and excessive permissions
resource "aws_lambda_function" "report_generator" {
  filename         = "report_generator.zip"
  function_name    = "report-generator"
  role            = aws_iam_role.report_generator_role.arn
  handler         = "index.handler"
  runtime         = "nodejs14.x"
  
  # Insecure: No environment encryption
  environment {
    variables = {
      DB_PASSWORD = "supersecret123"
      API_KEY     = "sk_live_51H1t2KZvKYlo2CdO1fF2g3H4j5K6l7M8n9O0p1Q2r3S4t5U6v7W8x9Y0z1"
    }
  }
}

# Insecure: Overly permissive IAM role
resource "aws_iam_role" "report_generator_role" {
  name = "report_generator_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "report_generator_policy" {
  name = "report_generator_policy"
  role = aws_iam_role.report_generator_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*",
          "dynamodb:*",
          "rds:*",
          "ec2:*",
          "iam:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# Insecure: DynamoDB table with no encryption and public access
resource "aws_dynamodb_table" "reports" {
  name           = "reports"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "report_id"
  
  attribute {
    name = "report_id"
    type = "S"
  }

  # Insecure: No encryption at rest
  server_side_encryption {
    enabled = false
  }
}

# Insecure: API Gateway with no authentication
resource "aws_api_gateway_rest_api" "report_api" {
  name = "report-generator-api"
}

resource "aws_api_gateway_resource" "reports" {
  rest_api_id = aws_api_gateway_rest_api.report_api.id
  parent_id   = aws_api_gateway_rest_api.report_api.root_resource_id
  path_part   = "reports"
}

resource "aws_api_gateway_method" "reports" {
  rest_api_id   = aws_api_gateway_rest_api.report_api.id
  resource_id   = aws_api_gateway_resource.reports.id
  http_method   = "ANY"
  authorization = "NONE"
} 