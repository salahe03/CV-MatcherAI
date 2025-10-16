# CV-to-Job Matcher - End-to-End ML Project

An intelligent FastAPI service that matches candidate CVs to job descriptions using machine learning, returning match scores, matched skills, and missing skills.

## Features

- 🎯 **ML-Powered Matching**: Uses DistilBERT embeddings for semantic similarity
- 📊 **Match Score**: Returns normalized score (0-1) based on cosine similarity
- ✅ **Skills Analysis**: Identifies matched and missing skills automatically
- 📄 **PDF Support**: Extracts text from PDF files or accepts plain text
- 🚀 **FastAPI**: High-performance async API with automatic documentation
- 🐳 **Dockerized**: Fully containerized for easy deployment
- ☁️ **Cloud Ready**: Prepared for deployment on Google Cloud Run or similar platforms

## Project Structure

```
cv_matcher/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app & endpoints
│   ├── model.py         # Embedding generation (DistilBERT)
│   ├── preprocess.py    # Text cleaning & tokenization
│   ├── extract.py       # PDF/text extraction
│   └── skills.py        # Skills matching & extraction
├── sample_data/
│   ├── example_cv.txt   # Sample CV for testing
│   └── example_jd.txt   # Sample job description
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── .dockerignore       # Docker ignore patterns
└── README.md           # This file
```

## API Endpoints

### `POST /match`
Match a CV to a job description.

**Input:**
- `cv_file`: CV as PDF or text file (optional)
- `cv_text`: CV as plain text string (optional)
- `jd_file`: Job description as file (optional)
- `jd_text`: Job description as plain text (optional)

**Output:**
```json
{
  "match_score": 0.87,
  "matched_skills": ["Python", "PyTorch", "Docker"],
  "missing_skills": ["TensorFlow", "Kubernetes"]
}
```

### `GET /health`
Health check endpoint.

**Output:**
```json
{
  "status": "ok"
}
```

### `GET /skills`
List all skills in the database.

## Installation & Setup

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Setup

1. **Clone the repository**
```bash
cd "c:\Users\transfer\Desktop\cv matcher"
```

2. **Create virtual environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Access the API**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Usage Examples

### Using cURL (Plain Text)

```bash
curl -X POST "http://localhost:8000/match" \
  -F "cv_text=I am a Python developer with experience in PyTorch and Docker" \
  -F "jd_text=Looking for a Machine Learning Engineer with Python, TensorFlow, and Kubernetes experience"
```

### Using Python requests

```python
import requests

# With text input
response = requests.post(
    "http://localhost:8000/match",
    data={
        "cv_text": "I am a Python developer with PyTorch and Docker experience",
        "jd_text": "Looking for ML Engineer with Python, TensorFlow, Kubernetes"
    }
)
print(response.json())

# With file input
with open("sample_data/example_cv.txt", "rb") as cv, \
     open("sample_data/example_jd.txt", "rb") as jd:
    response = requests.post(
        "http://localhost:8000/match",
        files={
            "cv_file": cv,
            "jd_file": jd
        }
    )
    print(response.json())
```

### Using PowerShell

```powershell
$cv = Get-Content "sample_data\example_cv.txt" -Raw
$jd = Get-Content "sample_data\example_jd.txt" -Raw

$response = Invoke-RestMethod -Uri "http://localhost:8000/match" -Method Post -Form @{
    cv_text = $cv
    jd_text = $jd
}

$response | ConvertTo-Json
```

## Docker Deployment

### Build the image
```bash
docker build -t cv-matcher:latest .
```

### Run the container
```bash
docker run -p 8000:8000 cv-matcher:latest
```

### Test the containerized API
```bash
curl http://localhost:8000/health
```

## Google Cloud Run Deployment (Optional)

1. **Install Google Cloud SDK**
```bash
gcloud init
```

2. **Build and push to Google Container Registry**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cv-matcher
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy cv-matcher \
  --image gcr.io/YOUR_PROJECT_ID/cv-matcher \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Technical Details

### Machine Learning Model
- **Model**: DistilBERT (distilbert-base-uncased)
- **Framework**: PyTorch + Hugging Face Transformers
- **Similarity**: Cosine similarity on mean-pooled embeddings
- **Score Range**: 0.0 to 1.0 (normalized)

### Skills Database
The system includes 100+ predefined skills across:
- Programming languages (Python, Java, JavaScript, etc.)
- ML/AI frameworks (TensorFlow, PyTorch, Scikit-learn, etc.)
- Cloud platforms (AWS, Azure, GCP)
- DevOps tools (Docker, Kubernetes, Jenkins, etc.)
- Databases (SQL, MongoDB, PostgreSQL, etc.)
- Web technologies (React, Django, FastAPI, etc.)

### Text Processing Pipeline
1. Text extraction (PDF or plain text)
2. Cleaning (lowercase, remove URLs, special chars)
3. Tokenization and normalization
4. Embedding generation using DistilBERT
5. Similarity computation
6. Skills extraction using regex patterns

## Testing

### Test with sample files
```bash
# Using PowerShell
$cv = Get-Content "sample_data\example_cv.txt" -Raw
$jd = Get-Content "sample_data\example_jd.txt" -Raw

Invoke-RestMethod -Uri "http://localhost:8000/match" -Method Post -Form @{
    cv_text = $cv
    jd_text = $jd
}
```

Expected output:
```json
{
  "match_score": 0.85,
  "matched_skills": ["Python", "PyTorch", "Docker", "Kubernetes", "AWS", ...],
  "missing_skills": ["TensorFlow", "GraphQL", ...]
}
```

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **torch**: Deep learning framework
- **transformers**: Hugging Face transformers
- **numpy**: Numerical computing
- **pandas**: Data manipulation
- **scikit-learn**: ML utilities (cosine similarity)
- **PyPDF2**: PDF text extraction
- **opencv-python**: Image processing (for OCR)
- **pytesseract**: OCR engine
- **python-multipart**: File upload support

## Performance Considerations

- **First Request**: May take 5-10 seconds as the model loads
- **Subsequent Requests**: Typically <1 second
- **Memory**: ~500MB RAM for model
- **CPU vs GPU**: Automatically uses GPU if available

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid input)
- `500`: Internal server error

## Troubleshooting

### Model download issues
If the model fails to download, ensure you have internet connectivity. The model (~250MB) is downloaded on first run.

### Memory issues
If running on limited memory, consider using a smaller model or increasing container memory limits.

### PDF extraction issues
For scanned PDFs, ensure tesseract-ocr is installed (included in Docker image).

## Future Enhancements

- [ ] Support for multiple file formats (DOCX, etc.)
- [ ] Fine-tuning on domain-specific data
- [ ] Batch processing endpoint
- [ ] Caching for improved performance
- [ ] Advanced NER for skill extraction
- [ ] Weighted skill matching
- [ ] Database integration for storing results

## License

MIT License

## Contact

For questions or issues, please open an issue on the repository.

---

**Built with ❤️ using FastAPI, PyTorch, and Transformers**