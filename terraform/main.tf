terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ── Key Pair (to SSH into EC2) ─────────────────────────────────────────────
resource "aws_key_pair" "jenkins_key" {
  key_name   = "jenkins-ai-key"
  public_key = file(var.public_key_path)
}

# ── VPC ────────────────────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "jenkins-ai-vpc" }
}

# ── Internet Gateway ───────────────────────────────────────────────────────
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "jenkins-ai-igw" }
}

# ── Subnet ─────────────────────────────────────────────────────────────────
resource "aws_subnet" "main" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
  tags = { Name = "jenkins-ai-subnet" }
}

# ── Route Table ────────────────────────────────────────────────────────────
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = { Name = "jenkins-ai-rt" }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

# ── Security Group ─────────────────────────────────────────────────────────
resource "aws_security_group" "main" {
  name        = "jenkins-ai-sg"
  description = "Allow Jenkins, Flask, and SSH"
  vpc_id      = aws_vpc.main.id

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Jenkins
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask backend
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP for Nginx dashboard
ingress {
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

  # All outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "jenkins-ai-sg" }
}

# ── EC2 Instance ───────────────────────────────────────────────────────────
resource "aws_instance" "jenkins_ai" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]
  key_name               = aws_key_pair.jenkins_key.key_name

  user_data = templatefile("${path.module}/userdata.sh", {
    groq_api_key   = var.groq_api_key
    email_sender   = var.email_sender
    email_password = var.email_password
    email_receiver = var.email_receiver
  })

  tags = { Name = "jenkins-ai-server" }
}

# ── Elastic IP ─────────────────────────────────────────────────────────────
resource "aws_eip" "jenkins_ai" {
  instance = aws_instance.jenkins_ai.id
  domain   = "vpc"
  tags     = { Name = "jenkins-ai-eip" }
}
