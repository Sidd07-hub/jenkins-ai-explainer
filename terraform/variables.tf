variable "aws_region" {
  description = "AWS region"
  default     = "ap-south-1"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI for ap-south-1"
  default     = "ami-0f58b397bc5c1f2e8"
}

variable "public_key_path" {
  description = "Path to your SSH public key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "groq_api_key" {
  description = "Groq API key"
  sensitive   = true
}

variable "email_sender" {
  description = "Gmail address to send alerts from"
  sensitive   = true
}

variable "email_password" {
  description = "Gmail App Password"
  sensitive   = true
}

variable "email_receiver" {
  description = "Email address to receive alerts"
  sensitive   = true
}
