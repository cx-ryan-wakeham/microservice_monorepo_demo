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

# Insecure: ECS cluster with no encryption and public access
resource "aws_ecs_cluster" "payment_processor" {
  name = "payment-processor-cluster"
  
  # Insecure: No encryption configuration
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

# Insecure: ECS task definition with sensitive environment variables
resource "aws_ecs_task_definition" "payment_processor" {
  family                   = "payment-processor"
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = 256
  memory                  = 512

  # Insecure: Hardcoded sensitive credentials
  container_definitions = jsonencode([
    {
      name  = "payment-processor"
      image = "payment-processor:latest"
      environment = [
        {
          name  = "STRIPE_SECRET_KEY"
          value = "sk_live_51H1t2KZvKYlo2CdO1fF2g3H4j5K6l7M8n9O0p1Q2r3S4t5U6v7W8x9Y0z1"
        },
        {
          name  = "DB_PASSWORD"
          value = "PaymentDB123!"
        },
        {
          name  = "API_SECRET"
          value = "super_secret_key_123"
        }
      ]
    }
  ])
}

# Insecure: Security group with overly permissive rules
resource "aws_security_group" "payment_processor" {
  name        = "payment-processor-sg"
  description = "Security group for payment processor"
  vpc_id      = aws_vpc.payment_processor.id

  # Insecure: Allow all inbound traffic
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Insecure: Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Insecure: VPC with public subnets and no NACLs
resource "aws_vpc" "payment_processor" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "payment-processor-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.payment_processor.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "payment-processor-public"
  }
}

# Insecure: KMS key with no rotation and public access
resource "aws_kms_key" "payment_processor" {
  description             = "Payment processor encryption key"
  deletion_window_in_days = 7
  enable_key_rotation     = false
  
  # Insecure: No key policy restrictions
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "*"
        }
        Action = [
          "kms:*"
        ]
        Resource = "*"
      }
    ]
  })
} 