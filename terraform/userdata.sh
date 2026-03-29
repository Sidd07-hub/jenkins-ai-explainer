#!/bin/bash
set -e

# Update system
apt-get update -y
apt-get upgrade -y

# Install Java (Jenkins needs it)
apt-get install -y openjdk-17-jdk

# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | tee /etc/apt/sources.list.d/jenkins.list > /dev/null
apt-get update -y
apt-get install -y jenkins
systemctl start jenkins
systemctl enable jenkins

# Install Python
apt-get install -y python3 python3-pip python3-venv git curl

# Install Python libraries
pip3 install flask flask-cors groq python-dotenv requests

# Create project directory
mkdir -p /opt/jenkins-ai-explainer
cd /opt/jenkins-ai-explainer

# Clone your GitHub repo
git clone https://github.com/Sidd07-hub/jenkins-ai-explainer.git .

# Create .env file with real values
cat > /opt/jenkins-ai-explainer/.env << EOF
GROQ_API_KEY=${groq_api_key}
JENKINS_URL=http://localhost:8080
JENKINS_USER=admin
JENKINS_TOKEN=will_update_after_setup
EMAIL_SENDER=${email_sender}
EMAIL_PASSWORD=${email_password}
EMAIL_RECEIVER=${email_receiver}
EOF

# Create systemd service so Flask starts automatically
cat > /etc/systemd/system/jenkins-ai.service << EOF
[Unit]
Description=Jenkins AI Explainer Flask Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/jenkins-ai-explainer
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start jenkins-ai
systemctl enable jenkins-ai

# Install Nginx to serve the dashboard
apt-get install -y nginx

# Copy dashboard to Nginx web root
cp /opt/jenkins-ai-explainer/jenkins_dashboard.html /var/www/html/index.html

# Update dashboard to point to AWS Flask URL instead of localhost
sed -i 's|http://localhost:5000|http://13.205.117.51:5000|g' /var/www/html/index.html

# Start Nginx
systemctl start nginx
systemctl enable nginx

echo "Setup complete!"
```

---

## What Changed

Only **2 things** were added at the bottom:
```
Before → echo "Setup complete!"  (that was the last line)

Added:
1. Install Nginx
2. Copy dashboard to /var/www/html/index.html
3. Replace localhost with 13.205.117.51
4. Start Nginx