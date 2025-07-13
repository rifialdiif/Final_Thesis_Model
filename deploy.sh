#!/bin/bash

# Deployment script for Prediction API to Google Cloud Run
# Run this script in Google Cloud Shell

echo "🚀 Starting deployment of Prediction API to Google Cloud Run..."

# Set project ID
PROJECT_ID="finalthesis-465407"
REGION="asia-southeast1"
SERVICE_NAME="prediction-api"

echo "📋 Setting up project configuration..."
gcloud config set project $PROJECT_ID

echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo "🏗️ Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

echo "✅ Deployment completed!"
echo "🌐 Getting service URL..."

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")

echo "🎉 Your API is now live at: $SERVICE_URL"
echo ""
echo "📝 Test your API:"
echo "Health check: curl $SERVICE_URL/"
echo ""
echo "Prediction test:"
echo "curl -X POST $SERVICE_URL/predict \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"ips_1\": 3.5,"
echo "    \"ips_2\": 3.2,"
echo "    \"ips_3\": 3.8,"
echo "    \"ips_4\": 3.6,"
echo "    \"cuti_1\": \"aktif\","
echo "    \"cuti_2\": \"aktif\","
echo "    \"cuti_3\": \"aktif\","
echo "    \"cuti_4\": \"aktif\","
echo "    \"total_sks_ditempuh\": 120,"
echo "    \"total_sks_tidak_lulus\": 0"
echo "  }'" 