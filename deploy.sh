#!/bin/bash

# Set your project ID
PROJECT_ID="finalthesis-465407"
REGION="asia-southeast1"
SERVICE_NAME="ml-model-api"

echo "🚀 Starting deployment to Google Cloud Platform..."
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"

# Enable required APIs
echo "📋 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the container
echo "🔨 Building Docker container..."
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Push to Container Registry
echo "📤 Pushing to Container Registry..."
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10

echo "✅ Deployment completed!"
echo "🌐 Your API is now available at:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

echo ""
echo "📝 To test your API, use:"
echo "curl -X GET \$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')"
echo ""
echo "curl -X POST \$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')/predict \\"
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