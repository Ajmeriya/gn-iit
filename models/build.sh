#!/bin/bash
# Build script for Render deployment

set -e

echo "🔨 Building AI Model Service..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model for JD analyzer
echo "📥 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo "✅ Build complete!"

