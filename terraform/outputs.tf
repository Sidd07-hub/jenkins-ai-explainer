output "public_ip" {
  description = "Public IP of the server"
  value       = aws_eip.jenkins_ai.public_ip
}

output "jenkins_url" {
  description = "Jenkins dashboard URL"
  value       = "http://${aws_eip.jenkins_ai.public_ip}:8080"
}

output "flask_url" {
  description = "Flask backend URL"
  value       = "http://${aws_eip.jenkins_ai.public_ip}:5000"
}

output "webhook_url" {
  description = "Webhook URL for Jenkins post-build action"
  value       = "http://${aws_eip.jenkins_ai.public_ip}:5000/webhook"
}

output "ssh_command" {
  description = "Command to SSH into the server"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_eip.jenkins_ai.public_ip}"
}