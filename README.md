# Jenkins AI Failure Explainer 🤖

> Automatically analyzes Jenkins pipeline failures using AI and sends plain-English explanations via email — zero manual steps.

![Live](https://img.shields.io/badge/Live-AWS-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.1-green?style=flat-square)
![Jenkins](https://img.shields.io/badge/Jenkins-2.541-red?style=flat-square)
![Terraform](https://img.shields.io/badge/Terraform-1.14-purple?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-yellow?style=flat-square)

---

## 🚀 Live Demo

| Service | URL |
|---|---|
| Dashboard | http://13.205.117.51 |
| Jenkins | http://13.205.117.51:8080 |
| API Health | http://13.205.117.51:5000/health |

---

## 💡 What It Does

When a Jenkins pipeline fails:

```
Build Fails in Jenkins
        ↓
Webhook triggered automatically
        ↓
Flask fetches the build log
        ↓
Groq AI analyzes the failure
        ↓
Plain-English email sent to your inbox
        ↓
Zero manual steps required
```

---

## 🎯 Key Features

- **Auto-trigger** — Jenkins calls the webhook on every failure automatically
- **AI Analysis** — Groq LLaMA AI explains the cause and fix in plain English
- **Email Alerts** — Get notified instantly with cause, fix and failed step
- **Live Dashboard** — View all pipelines with status badges in one place
- **Secure** — Credentials never stored, `.env` never pushed to GitHub
- **Cloud Deployed** — Fully live on AWS EC2 with Terraform

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python + Flask | Backend API |
| Groq LLaMA AI | Pipeline failure analysis |
| Jenkins | CI/CD pipeline |
| HTML + CSS + JS | Frontend dashboard |
| Nginx | Serve dashboard on port 80 |
| AWS EC2 | Cloud server |
| Terraform | Infrastructure as Code |
| GitHub | Version control |

---

## 📁 Project Structure

```
jenkins-ai-explainer/
├── app.py                  ← Flask backend with all API routes
├── ai_explainer.py         ← Groq AI integration
├── log_collector.py        ← Fetches Jenkins build logs
├── email_sender.py         ← Gmail SMTP email notifications
├── main.py                 ← Run without dashboard (CLI mode)
├── jenkins_dashboard.html  ← Frontend dashboard
├── .env.example            ← Environment variables template
├── .gitignore              ← Excludes secrets from GitHub
├── requirements.txt        ← Python dependencies
├── terraform/
│   ├── main.tf             ← AWS resources (EC2, VPC, SG, EIP)
│   ├── variables.tf        ← Input variables
│   ├── outputs.tf          ← Output values (URLs, IPs)
│   └── userdata.sh         ← EC2 bootstrap script
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- Jenkins (local or AWS)
- Groq API key (free at console.groq.com)
- Gmail App Password
- AWS account (for deployment)
- Terraform (for infrastructure)

### 1. Clone the Repository

```bash
git clone https://github.com/Sidd07-hub/jenkins-ai-explainer.git
cd jenkins-ai-explainer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your real values:

```env
GROQ_API_KEY=your_groq_api_key_here

JENKINS_URL=http://localhost:8080
JENKINS_USER=your_jenkins_username
JENKINS_TOKEN=your_jenkins_api_token

EMAIL_SENDER=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=youremail@gmail.com
```

### 4. Run the Backend

```bash
python app.py
```

### 5. Open the Dashboard

Open `jenkins_dashboard.html` in your browser.

---

## 🔑 How to Get API Keys

### Groq API Key (Free)
1. Go to `console.groq.com`
2. Sign in with Google
3. API Keys → Create API Key
4. Copy and paste in `.env`

### Jenkins API Token
1. Jenkins → Your Name (top right) → Configure
2. API Token → Add New Token
3. Generate → Copy immediately

### Gmail App Password
1. Google Account → Security → 2-Step Verification → ON
2. Search "App Passwords"
3. Select Mail → Generate
4. Copy the 16-character code

---

## 🔄 Auto-Trigger Setup

Add this to your Jenkins job Post-build Actions → Execute shell:

```bash
curl -X POST http://YOUR-IP:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"job":"your-job-name"}'
```

Now every failed build automatically triggers AI analysis and sends an email!

---

## ☁️ AWS Deployment with Terraform

### Prerequisites
- AWS CLI configured (`aws configure`)
- SSH key pair generated (`ssh-keygen -t rsa -b 4096`)
- Terraform installed

### Deploy

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### What Gets Created

| Resource | Purpose |
|---|---|
| VPC | Private network |
| Internet Gateway | Internet access |
| Subnet | Network segment |
| Security Group | Firewall (ports 22, 80, 5000, 8080) |
| EC2 t3.micro | Server (free tier eligible) |
| Elastic IP | Fixed public IP |

### Cost

**$0/month** for 12 months on AWS free tier.

---

## 📡 API Routes

| Method | Route | Description |
|---|---|---|
| POST | `/connect` | Test Jenkins connection |
| POST | `/pipelines` | Fetch all Jenkins jobs |
| POST | `/analyze` | Analyze a failed pipeline |
| POST | `/webhook` | Auto-trigger from Jenkins |
| GET | `/health` | Health check |

---

## 📧 Email Format

```
Subject: Jenkins Build Failed - your-job #42

Jenkins Pipeline Failure Report
================================

JOB NAME: your-job
BUILD NUMBER: #42

CAUSE:
Step 3 failed because npm is not installed on the server.

FIX:
1. Install Node.js and npm on the server
2. Run: sudo apt-get install -y nodejs npm
3. Re-trigger the build

FAILED STEP:
npm install

================================
Auto-generated by Jenkins AI Explainer
```

---

## 🔒 Security

- `.env` file is never committed to GitHub
- Terraform secrets (`terraform.tfvars`) are excluded via `.gitignore`
- Credentials passed only through secure environment variables
- Jenkins credentials used only for the current session in dashboard

---

## 🗺️ Roadmap

- [ ] Add Slack notifications
- [ ] Build history and analytics dashboard
- [ ] Support for GitLab CI and GitHub Actions
- [ ] HTTPS with Let's Encrypt SSL
- [ ] Docker containerization
- [ ] Kubernetes deployment

---

## 🤝 Contributing

Pull requests are welcome! For major changes please open an issue first.

---

## 👨‍💻 Author

**Siddhesh**
- GitHub: [@Sidd07-hub](https://github.com/Sidd07-hub)
- LinkedIn: [www.linkedin.com/in/siddhesh-nikumb-7884392b2]

---

## ⭐ If this project helped you, give it a star!
