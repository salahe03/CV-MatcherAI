# Quick Start Guide

## 🚀 Getting Started (3 Steps)

### 1. Setup (First Time Only)
```powershell
.\setup.ps1
```

### 2. Run the Server
```powershell
.\run.ps1
```

### 3. Test the API
Open another terminal and run:
```powershell
python test_api.py
```

## 📝 Manual Testing

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Match CV to Job
```powershell
$cv = @"
John Doe - Python Developer
Skills: Python, Django, React, PostgreSQL
Experience: 3 years
"@

$jd = @"
Looking for Python Developer with:
- Python, Django
- React or Vue.js
- SQL databases
- Docker experience
"@

$response = Invoke-RestMethod -Uri "http://localhost:8000/match" -Method Post -Form @{
    cv_text = $cv
    jd_text = $jd
}

$response | ConvertTo-Json
```

### Test with Sample Files
```powershell
$cv = Get-Content "sample_data\example_cv.txt" -Raw
$jd = Get-Content "sample_data\example_jd.txt" -Raw

$response = Invoke-RestMethod -Uri "http://localhost:8000/match" -Method Post -Form @{
    cv_text = $cv
    jd_text = $jd
}

$response | ConvertTo-Json
```

## 🌐 Access Points

- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Skills List**: http://localhost:8000/skills

## 🐳 Docker Commands

### Build
```bash
docker build -t cv-matcher .
```

### Run
```bash
docker run -p 8000:8000 cv-matcher
```

### Test
```bash
docker ps  # Check if container is running
curl http://localhost:8000/health
```

## 📊 Expected Output

```json
{
  "match_score": 0.87,
  "matched_skills": [
    "Python",
    "PyTorch",
    "Docker",
    "Kubernetes",
    "AWS",
    "FastAPI",
    "PostgreSQL"
  ],
  "missing_skills": [
    "TensorFlow",
    "GraphQL",
    "Azure"
  ]
}
```

## 🔧 Troubleshooting

### Port already in use
```powershell
# Find and kill process on port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Module not found errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Model download issues
- Ensure internet connection
- Model (~250MB) downloads on first run
- Takes 5-10 seconds for first request

## 📦 Project Files

```
cv_matcher/
├── app/
│   ├── __init__.py         # Package init
│   ├── main.py             # FastAPI app
│   ├── model.py            # ML model
│   ├── preprocess.py       # Text processing
│   ├── extract.py          # PDF extraction
│   └── skills.py           # Skills matching
├── sample_data/
│   ├── example_cv.txt      # Sample CV
│   └── example_jd.txt      # Sample JD
├── requirements.txt        # Dependencies
├── Dockerfile              # Container config
├── .dockerignore           # Docker ignore
├── .gitignore              # Git ignore
├── setup.ps1               # Setup script
├── run.ps1                 # Run script
├── test_api.py             # Test script
├── QUICKSTART.md           # This file
└── README.md               # Full docs
```

## 🎯 Success Criteria Checklist

- [x] FastAPI runs on port 8000
- [x] `/match` endpoint accepts files and text
- [x] Returns JSON with score, matched, and missing skills
- [x] Docker image builds successfully
- [x] Match score between 0-1
- [x] Skills correctly extracted
- [x] Sample test files included
- [x] Comprehensive documentation

## 💡 Tips

1. **First request is slow**: Model loads on first request (5-10s)
2. **Use /docs**: Interactive Swagger UI for easy testing
3. **Check /skills**: See all 100+ skills in database
4. **PDF support**: Works with both PDF and text files
5. **Flexible input**: Use files OR text, not both required

## 📚 Next Steps

1. Run the setup script
2. Start the server
3. Open http://localhost:8000/docs
4. Try the examples
5. Test with your own CVs and job descriptions!

---

**Need help?** Check README.md for detailed documentation.
