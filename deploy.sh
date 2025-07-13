#!/bin/bash

# RF_Lupa-Wak! API Deployment Script
# This script automates the deployment process to Google Cloud Platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=""
REGION="asia-southeast1"
SERVICE_NAME="rf-lupa-wak-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/rf-lupa-wak-api"

echo -e "${GREEN}🚀 RF_Lupa-Wak! API Deployment Script${NC}"
echo "=========================================="

# Check if PROJECT_ID is set
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Error: PROJECT_ID is not set${NC}"
    echo "Please set your GCP Project ID in the script or export it:"
    echo "export PROJECT_ID=your-project-id"
    exit 1
fi

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Error: Google Cloud SDK is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker is not installed${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${YELLOW}🔐 Authenticating with Google Cloud...${NC}"
gcloud auth login --quiet

echo -e "${YELLOW}⚙️  Setting project...${NC}"
gcloud config set project $PROJECT_ID

echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo -e "${YELLOW}🐳 Building Docker image...${NC}"
docker build -t $IMAGE_NAME .

echo -e "${YELLOW}📤 Pushing image to Container Registry...${NC}"
docker push $IMAGE_NAME

echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "PYTHONUNBUFFERED=1"

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo -e "${YELLOW}🌐 Your API is now available at:${NC}"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

echo ""
echo -e "${YELLOW}📝 Test your API:${NC}"
echo "Health check:"
echo "curl $(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')"

echo ""
echo "Prediction:"
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
echo "    \"total_sks_tidak_lulus\": 6"
echo "  }'" 