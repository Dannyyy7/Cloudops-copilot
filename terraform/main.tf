terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2" # Updated to Sydney region
}

# Dynamically lookup official Ubuntu 22.04 AMI in ap-southeast-2
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

# Security Group: Allow SSH (22), Jenkins (8080), Streamlit (8501)
resource "aws_security_group" "devops_sg" {
  name        = "devops-cloudops-sg"
  description = "Allow inbound web traffic and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance using t3.micro & Java 21 / 2026 Jenkins setup
resource "aws_instance" "devops_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro" # Updated instance type
  security_groups = [aws_security_group.devops_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y

              # Create a 2GB swap file to assist t3.micro RAM during Jenkins & Docker builds
              sudo fallocate -l 2G /swapfile
              sudo chmod 600 /swapfile
              sudo mkswap /swapfile
              sudo swapon /swapfile
              echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

              # Install Docker
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker

              # Install Java 21 & Fontconfig
              sudo apt-get install -y fontconfig openjdk-21-jre

              # Install Jenkins using 2026 key
              sudo mkdir -p /etc/apt/keyrings
              sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key
              echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

              sudo apt-get update -y
              sudo apt-get install -y jenkins

              # Enable & start Jenkins service
              sudo systemctl enable --now jenkins

              # Allow Jenkins user to run Docker without sudo
              sudo usermod -aG docker jenkins
              sudo systemctl restart jenkins
              EOF

  tags = {
    Name = "CloudOps-Copilot-Server"
  }
}

output "server_public_ip" {
  value       = aws_instance.devops_server.public_ip
  description = "Public IP of EC2 Instance"
}
