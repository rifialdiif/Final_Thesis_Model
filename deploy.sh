#!/bin/bash

# Script untuk deploy ke Google Cloud Run
# Pastikan sudah login ke gcloud: gcloud auth login

echo "🚀 Starting deployment to Google Cloud Run..."

# Set project ID
PROJECT_ID="finalthesis-465407"
REGION="asia-southeast1"
SERVICE_NAME="prediksi-kelulusan-api"

echo "📋 Project ID: $PROJECT_ID"
echo "🌍 Region: $REGION"
echo "🔧 Service Name: $SERVICE_NAME"

# Build and push the container
echo "🔨 Building and pushing container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10

echo "✅ Deployment completed!"
echo "🌐 Your API URL will be shown above"
echo "📝 To test the API, use the URL + /predict endpoint" 