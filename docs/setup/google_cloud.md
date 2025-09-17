# Google Cloud Platform Setup Guide

This guide walks you through setting up Google Cloud Platform (GCP) and Google AI Studio for the Professional Business Card Designer project.

## 📋 Prerequisites

- Google account with access to Google Cloud Platform
- Credit card for billing setup (required for image generation)
- Basic familiarity with command line tools

## 🚀 Step-by-Step Setup

### 1. Google Cloud CLI Installation

#### macOS (using Homebrew)
```bash
# Install Google Cloud CLI
brew install google-cloud-sdk

# Or using the installation script
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Verify installation
gcloud --version
```

#### Linux
```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update && sudo apt-get install google-cloud-cli

# Verify installation
gcloud --version
```

#### Windows
1. Download the [Google Cloud CLI installer](https://cloud.google.com/sdk/docs/install)
2. Run the installer and follow the setup wizard
3. Open a new command prompt and verify: `gcloud --version`

### 2. Google Cloud Project Setup

#### Initialize gcloud
```bash
# Initialize gcloud and authenticate
gcloud init

# Follow the prompts to:
# 1. Login to your Google account
# 2. Select or create a project
# 3. Choose a default compute region
```

#### Create a New Project (Alternative)
```bash
# Create a new project specifically for this application
gcloud projects create business-card-designer-2025 \
    --name="Business Card Designer" \
    --labels=type=ai-project,purpose=business-cards

# Set the project as default
gcloud config set project business-card-designer-2025

# Verify project settings
gcloud config list
```

#### Link Billing Account
```bash
# List available billing accounts
gcloud billing accounts list

# Link billing account to project (replace BILLING_ACCOUNT_ID)
gcloud billing projects link business-card-designer-2025 \
    --billing-account=BILLING_ACCOUNT_ID
```

### 3. Enable Required APIs

```bash
# Enable Google AI Platform API
gcloud services enable aiplatform.googleapis.com

# Enable Generative Language API (for Gemini)
gcloud services enable generativelanguage.googleapis.com

# Enable Cloud Resource Manager API
gcloud services enable cloudresourcemanager.googleapis.com

# Enable Cloud Billing API
gcloud services enable cloudbilling.googleapis.com

# Verify enabled services
gcloud services list --enabled
```

### 4. Authentication Setup

#### Application Default Credentials
```bash
# Set up application default credentials
gcloud auth application-default login

# This creates credentials in:
# ~/.config/gcloud/application_default_credentials.json
```

#### Service Account (Production)
For production deployments, create a service account:

```bash
# Create service account
gcloud iam service-accounts create business-card-designer \
    --display-name="Business Card Designer Service Account" \
    --description="Service account for business card AI generation"

# Grant necessary roles
gcloud projects add-iam-policy-binding business-card-designer-2025 \
    --member="serviceAccount:business-card-designer@business-card-designer-2025.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding business-card-designer-2025 \
    --member="serviceAccount:business-card-designer@business-card-designer-2025.iam.gserviceaccount.com" \
    --role="roles/ml.developer"

# Create and download service account key
gcloud iam service-accounts keys create ~/business-card-designer-key.json \
    --iam-account=business-card-designer@business-card-designer-2025.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=~/business-card-designer-key.json
```

## 🎯 Google AI Studio Setup

### 1. Access Google AI Studio

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Accept the terms of service

### 2. Create API Key

```bash
# Option 1: Through Web Interface
# 1. Click "Get API Key" in Google AI Studio
# 2. Select "Create API key in new project" or use existing project
# 3. Copy the generated API key

# Option 2: Through gcloud (if available)
gcloud alpha services api-keys create \
    --display-name="Business Card Designer API Key" \
    --project=business-card-designer-2025
```

### 3. Configure API Key Restrictions (Recommended)

For security, restrict your API key:

1. Go to [Google Cloud Console > Credentials](https://console.cloud.google.com/apis/credentials)
2. Find your API key and click "Edit"
3. Under "Application restrictions":
   - Choose "HTTP referrers" for web apps
   - Choose "IP addresses" for server apps
4. Under "API restrictions":
   - Select "Restrict key"
   - Choose "Generative Language API"

### 4. Test API Access

```bash
# Test API key (replace YOUR_API_KEY)
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello, world!"}]}]}' \
     -X POST \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

## 💰 Billing and Cost Management

### Understanding Costs

- **Gemini 2.5 Flash Image**: $0.039 per image generation
- **Gemini Pro Text**: $0.00025 per 1K input tokens, $0.0005 per 1K output tokens
- **Storage**: Minimal costs for temporary file storage

### Set Up Budget Alerts

```bash
# Create a budget (replace BILLING_ACCOUNT_ID)
gcloud billing budgets create \
    --billing-account=BILLING_ACCOUNT_ID \
    --display-name="Business Card Designer Budget" \
    --budget-amount=50 \
    --threshold-rule=percent=50 \
    --threshold-rule=percent=75 \
    --threshold-rule=percent=90 \
    --notification-email=your-email@example.com
```

### Cost Control Best Practices

1. **Use Caching**: Enable caching to avoid regenerating identical designs
2. **Batch Processing**: Generate multiple variations in single requests
3. **Set Daily Limits**: Configure `MAX_GENERATIONS_PER_DAY` in your `.env`
4. **Monitor Usage**: Check Cloud Console billing regularly

```python
# Example cost control in your application
from src.utils.cost_tracker import CostTracker

cost_tracker = CostTracker(
    daily_budget=25.00,
    cost_per_generation=0.039,
    alert_threshold=0.80
)

if cost_tracker.can_generate():
    # Proceed with generation
    result = generate_business_card(prompt)
    cost_tracker.record_generation()
else:
    print("Daily budget limit reached. Try again tomorrow.")
```

## 🔧 Configuration Verification

### Environment Variables Check

Create a verification script:

```python
# scripts/verify_setup.py
import os
import google.generativeai as genai
from google.cloud import aiplatform

def verify_setup():
    """Verify all required configurations are working."""
    
    # Check environment variables
    api_key = os.getenv('GOOGLE_API_KEY')
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
        
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT not found in environment")
        return False
    
    # Test Gemini API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('Hello, this is a test.')
        print("✅ Gemini API working correctly")
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False
    
    # Test Google Cloud AI Platform
    try:
        aiplatform.init(project=project_id)
        print("✅ Google Cloud AI Platform initialized")
    except Exception as e:
        print(f"❌ AI Platform error: {e}")
        return False
    
    print("🎉 All configurations verified successfully!")
    return True

if __name__ == "__main__":
    verify_setup()
```

Run the verification:

```bash
cd business-card-designer-2025
python scripts/verify_setup.py
```

## 🚨 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "API not enabled" | Run `gcloud services enable generativelanguage.googleapis.com` |
| "Quota exceeded" | Check quotas in Cloud Console > IAM & Admin > Quotas |
| "Invalid API key" | Verify API key in Google AI Studio |
| "Permission denied" | Check IAM roles for your account/service account |
| "Billing not enabled" | Link billing account to your project |

### Quota Limits

Default quotas for Gemini APIs:
- **Requests per minute**: 60
- **Requests per day**: 1,500
- **Images per day**: 100

To increase quotas:
1. Go to [Cloud Console > Quotas](https://console.cloud.google.com/iam-admin/quotas)
2. Filter by "Generative Language API"
3. Select the quota you want to increase
4. Click "Edit Quotas" and submit a request

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
export DEBUG_MODE=true
export VERBOSE_LOGGING=true
python examples/quick_start.py
```

### Support Resources

- [Google Cloud Support](https://cloud.google.com/support/)
- [Google AI Studio Documentation](https://ai.google.dev/)
- [Gemini API Reference](https://ai.google.dev/api)
- [Cloud Console](https://console.cloud.google.com/)

## 🔐 Security Best Practices

### API Key Security
- Never commit API keys to version control
- Use environment variables or secret management services
- Rotate API keys regularly
- Implement IP restrictions for production

### Access Control
```bash
# Principle of least privilege - only grant necessary roles
gcloud projects add-iam-policy-binding business-card-designer-2025 \
    --member="user:developer@company.com" \
    --role="roles/aiplatform.user"
```

### Monitoring
Set up logging and monitoring:

```bash
# Enable audit logs
gcloud logging sinks create business-card-audit \
    bigquery.googleapis.com/projects/business-card-designer-2025/datasets/audit_logs \
    --log-filter='protoPayload.serviceName="aiplatform.googleapis.com"'
```

---

**Next Steps**: After completing this setup, proceed to [API Configuration Guide](api_configuration.md) for detailed API integration instructions.