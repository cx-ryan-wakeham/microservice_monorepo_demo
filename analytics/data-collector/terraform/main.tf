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

# Insecure: Public S3 bucket with no encryption
resource "aws_s3_bucket" "data_collector_bucket" {
  bucket = "data-collector-bucket-${random_string.suffix.result}"
}

resource "aws_s3_bucket_public_access_block" "data_collector_bucket" {
  bucket = aws_s3_bucket.data_collector_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Insecure: Overly permissive IAM policy
resource "aws_iam_policy" "data_collector_policy" {
  name = "data-collector-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "*"
        Resource = "*"
      }
    ]
  })
}

# Insecure: Public EC2 instance with no security group restrictions
resource "aws_instance" "data_collector" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  # Insecure: Hardcoded credentials
  user_data = <<-EOF
              #!/bin/bash
              export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
              export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
              EOF

  tags = {
    Name = "data-collector"
  }
}

# Insecure: Public RDS instance with no encryption
resource "aws_db_instance" "data_collector_db" {
  identifier           = "data-collector-db"
  engine              = "mysql"
  engine_version      = "5.7"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_type        = "standard"
  publicly_accessible = true
  skip_final_snapshot = true
  
  # Insecure: Weak password
  password = "password123"
  username = "admin"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
} 