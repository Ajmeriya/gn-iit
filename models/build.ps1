# Build script for Windows PowerShell
# Run this before deploying or for local testing

Write-Host "🔨 Building AI Model Service..." -ForegroundColor Cyan

# Install Python dependencies
Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

# Download spaCy model for JD analyzer
Write-Host "`n📥 Downloading spaCy English model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to download spaCy model!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Build complete!" -ForegroundColor Green

