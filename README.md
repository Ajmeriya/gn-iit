# AI-Powered Job Assessment & Screening Platform

A comprehensive full-stack platform for automated job assessments, candidate screening, and AI-powered resume matching.

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │──────│  Backend    │──────│  Model      │──────│  Database   │
│  (Vercel)   │      │  (Render)   │      │  Service    │      │  (Railway/  │
│             │      │             │      │  (Render)   │      │   Neon/     │
│  React + TS │      │  Spring Boot│      │  Python     │      │   Supabase) │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
```

## 📁 Project Structure

```
AI-Powered-Job-Assessment-Screening-Platform/
├── frontend/          # React + TypeScript frontend
├── backend/           # Spring Boot REST API
├── models/            # Python AI/ML service
│   ├── ai_service.py           # Main Flask API
│   ├── ai_resume_matcher.py    # Resume matching AI
│   ├── assessment_generator.py  # Assessment question generator
│   ├── assessment_scorer.py    # Assessment scoring
│   ├── code_executor.py        # DSA code execution
│   ├── jd_analyzer.py          # Job description analyzer
│   ├── pdf_to_text.py          # PDF resume parser
│   ├── dsa_engine/             # DSA question engine
│   └── tests/                  # Unit tests
├── examples/          # Example usage scripts
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Java** 17+ (for backend)
- **Python** 3.11+ (for model service)
- **PostgreSQL** (or use cloud database)

### Local Development

#### 1. Frontend
```bash
cd frontend
npm install
npm run dev
```

#### 2. Backend
```bash
cd backend
mvn clean install
mvn spring-boot:run
```

#### 3. Model Service
```bash
cd models
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python ai_service.py
```

## 🌐 Deployment

### Model Service (Render)

1. **Repository**: https://github.com/Ajmeriya/gn-iit
2. **Root Directory**: `models`
3. **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. **Start Command**: `bash start.sh`
5. **Environment Variables**:
   - `GEMINI_API_KEY` (required)
   - `GEMINI_API_KEY_2` (optional, for multi-key support)

See `models/DEPLOYMENT.md` for detailed deployment instructions.

### Backend (Render)

- Deploy Spring Boot application
- Set database connection string
- Configure AI service URL: `ai.service.url=https://your-model-service.onrender.com`

### Frontend (Vercel)

- Connect GitHub repository
- Set build command: `npm run build`
- Set output directory: `dist`
- Configure API endpoint

### Database

Choose one:
- **Railway**: PostgreSQL hosting
- **Neon**: Serverless PostgreSQL
- **Supabase**: PostgreSQL with additional features

## 🔑 Environment Variables

### Model Service
- `GEMINI_API_KEY`: Google Gemini API key (required)
- `GEMINI_API_KEY_2`: Secondary API key (optional)
- `PORT`: Service port (auto-set by Render)

### Backend
- `SPRING_DATASOURCE_URL`: Database connection string
- `SPRING_DATASOURCE_USERNAME`: Database username
- `SPRING_DATASOURCE_PASSWORD`: Database password
- `AI_SERVICE_URL`: Model service URL

### Frontend
- `VITE_API_URL`: Backend API URL

## 📚 Features

### For Recruiters
- Create custom assessments (MCQ, SQL, DSA)
- AI-powered resume matching
- Candidate analytics and leaderboard
- Automated shortlisting

### For Candidates
- Apply to job postings
- Take assessments online
- Real-time code execution for DSA
- View results and feedback

## 🛠️ Technology Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: Spring Boot, Java, PostgreSQL
- **AI/ML**: Python, Flask, Sentence-Transformers, Google Gemini API
- **Deployment**: Render, Vercel, Railway/Neon/Supabase

## 📖 Documentation

- **Deployment Guide**: `models/DEPLOYMENT.md`
- **API Documentation**: See backend Swagger UI
- **Architecture**: See `STRUCTURE.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of IIT GN academic/research work.

## 👥 Team

- AI/ML Development
- Backend Development
- Frontend Development

---

**Last Updated**: 2025
**Version**: 1.0.0
