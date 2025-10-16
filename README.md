# CV-to-Job Matcher

A machine learning-powered REST API that quantifies the match between candidate resumes and job descriptions. Built with DistilBERT embeddings and FastAPI, this service returns match scores, identified skills, and gaps in candidate qualifications.

## Overview

This application addresses the challenge of efficiently screening candidates by automating the comparison between CVs and job requirements. Using transformer-based natural language processing, it provides objective, quantifiable metrics for candidate-job fit.

## Key Capabilities

- **Semantic Matching**: Leverages DistilBERT embeddings to understand contextual similarity beyond keyword matching
- **Quantified Scoring**: Returns normalized similarity scores (0-1 range) using cosine distance metrics
- **Skills Intelligence**: Automatically identifies 100+ technical skills with precise pattern matching
- **Gap Analysis**: Highlights missing qualifications to support candidate development
- **Format Flexibility**: Handles PDF documents and plain text inputs
- **Production Ready**: Containerized with Docker for consistent deployment across environments


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

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Docker (optional, recommended for production)
- 8GB RAM minimum (12GB recommended for optimal performance)

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/salahe03/CV-MatcherAI.git
cd CV-MatcherAI
```

2. **Create and activate virtual environment**

**Unix/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the development server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Verify installation**
- API Root: http://localhost:8000
- Interactive Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

> **Note**: The first request may take 5-10 seconds as the DistilBERT model downloads (~250MB) and initializes.

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Match Endpoint - Text Input

```bash
curl -X POST "http://localhost:8000/match" \
  -F "cv_text=Senior Software Engineer with 5 years experience in Python, Django, and AWS" \
  -F "jd_text=Seeking Backend Engineer proficient in Python, Django, PostgreSQL, and cloud platforms"
```

### Match Endpoint - File Upload

```bash
curl -X POST "http://localhost:8000/match" \
  -F "cv_file=@path/to/resume.pdf" \
  -F "jd_file=@path/to/job_description.txt"
```

### Python Client Example

```python
import requests

def match_candidate(cv_text: str, job_description: str) -> dict:
    """Match a candidate CV to a job description."""
    response = requests.post(
        "http://localhost:8000/match",
        data={
            "cv_text": cv_text,
            "jd_text": job_description
        }
    )
    response.raise_for_status()
    return response.json()

# Example usage
result = match_candidate(
    cv_text="Machine Learning Engineer with PyTorch and NLP experience...",
    job_description="Looking for ML Engineer with deep learning expertise..."
)

print(f"Match Score: {result['match_score']}")
print(f"Matched Skills: {', '.join(result['matched_skills'])}")
print(f"Missing Skills: {', '.join(result['missing_skills'])}")
```

### Interactive Testing

Access the automatically generated API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test endpoints directly from your browser.

## Docker Deployment

### Building the Container

```bash
docker build -t cv-matcher:latest .
```

Build time: ~20-30 minutes (includes PyTorch and transformer models)  
Image size: ~12.7GB

### Running the Container

**Foreground (with logs):**
```bash
docker run -p 8000:8000 cv-matcher:latest
```

**Background (detached mode):**
```bash
docker run -d -p 8000:8000 --name cv-matcher-app cv-matcher:latest
```

**With automatic restart:**
```bash
docker run -d -p 8000:8000 --restart unless-stopped --name cv-matcher-app cv-matcher:latest
```

### Container Management

```bash
# View logs
docker logs cv-matcher-app

# Stop container
docker stop cv-matcher-app

# Start existing container
docker start cv-matcher-app

# Remove container
docker rm cv-matcher-app

# Remove image (frees ~12.7GB)
docker rmi cv-matcher:latest
```

### Sharing the Image

**Option 1: Docker Hub**
```bash
docker login
docker tag cv-matcher:latest yourusername/cv-matcher:latest
docker push yourusername/cv-matcher:latest
```

**Option 2: GitHub Container Registry**
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker tag cv-matcher:latest ghcr.io/USERNAME/cv-matcher:latest
docker push ghcr.io/USERNAME/cv-matcher:latest
```

**Option 3: Export as file (offline sharing)**
```bash
docker save cv-matcher:latest -o cv-matcher.tar
# Recipients load with: docker load -i cv-matcher.tar
```

## Cloud Deployment

### Google Cloud Run

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/cv-matcher

# Deploy
gcloud run deploy cv-matcher \
  --image gcr.io/YOUR_PROJECT_ID/cv-matcher \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --allow-unauthenticated
```

### AWS ECS / Azure Container Instances

The Docker image is compatible with any container orchestration platform. Ensure minimum 2GB RAM allocation for optimal performance.

## Architecture

### Machine Learning Pipeline

**Model Architecture:**
- **Base Model**: DistilBERT (distilbert-base-uncased)
- **Parameters**: 66M (distilled from BERT-base's 110M)
- **Framework**: PyTorch with Hugging Face Transformers
- **Embedding Dimension**: 768
- **Context Window**: 512 tokens

**Similarity Computation:**
- Mean pooling over token embeddings
- Cosine similarity between CV and JD embeddings
- Score normalization to [0, 1] range
- Formula: `score = (cosine_similarity + 1) / 2`

**Skills Extraction:**
- Database: 100+ technical skills across multiple domains
- Method: Regex-based pattern matching with case-insensitive search
- Categories: Programming languages, frameworks, cloud platforms, databases, DevOps tools

### Processing Pipeline

```
Input (CV + JD)
    ↓
Text Extraction (PyPDF2)
    ↓
Preprocessing (cleaning, normalization)
    ↓
┌─────────────────┬─────────────────┐
│   Embedding     │     Skills      │
│   Generation    │   Extraction    │
│   (DistilBERT)  │   (Regex)       │
└────────┬────────┴────────┬────────┘
         ↓                 ↓
    Cosine Similarity   Match/Gap Analysis
         ↓                 ↓
    Match Score      Matched/Missing Skills
         └─────────┬─────────┘
                   ↓
              JSON Response
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI | 0.104+ |
| ASGI Server | Uvicorn | 0.24+ |
| ML Framework | PyTorch | 2.1+ |
| NLP Library | Transformers | 4.35+ |
| PDF Processing | PyPDF2 | 3.0+ |
| Scientific Computing | NumPy, Pandas, Scikit-learn | Latest |

## Testing

### Automated Test Suite

Run the included test script:
```bash
python test_api.py
```

This validates:
- Health endpoint connectivity
- Text-based matching
- File upload functionality
- Skills database retrieval

### Manual Testing with Sample Data

The repository includes example files in `sample_data/`:
- `example_cv.txt` - Sample resume
- `example_jd.txt` - Sample job description

```bash
# Test with provided samples
curl -X POST "http://localhost:8000/match" \
  -F "cv_file=@sample_data/example_cv.txt" \
  -F "jd_file=@sample_data/example_jd.txt"
```

### Expected Response Format

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

**Score Interpretation:**
- `0.9 - 1.0`: Excellent match
- `0.8 - 0.9`: Strong match
- `0.7 - 0.8`: Good match
- `0.6 - 0.7`: Moderate match
- `< 0.6`: Weak match

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

## Performance Characteristics

### Latency
- **Cold Start**: 5-10 seconds (model initialization)
- **Warm Requests**: 200-800ms per comparison
- **Throughput**: ~5-10 requests/second (single instance, CPU)

### Resource Requirements

| Environment | RAM | CPU | Storage |
|-------------|-----|-----|---------|
| Development | 2GB | 2 cores | 2GB |
| Production | 4GB | 4 cores | 5GB |
| Optimal | 8GB+ | 8 cores | 10GB |

### Optimization Notes
- Model loaded once per instance (singleton pattern)
- GPU acceleration automatically detected and utilized
- Embeddings computed in single forward pass
- Consider caching for repeated queries

## Error Handling

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Missing required inputs, invalid file format |
| 500 | Internal Error | Model failure, processing exception |

### Common Issues

**Issue**: Model download fails  
**Solution**: Ensure internet connectivity; model (~250MB) downloads on first request

**Issue**: Out of memory errors  
**Solution**: Increase container memory to minimum 2GB; consider using model quantization

**Issue**: PDF extraction returns empty text  
**Solution**: For scanned PDFs, OCR preprocessing required (tesseract-ocr included in Docker image)

**Issue**: Port 8000 already in use  
**Solution**: Stop conflicting service or use alternative port: `uvicorn app.main:app --port 8080`

## Project Structure

```
cv-matcher/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and endpoints
│   ├── model.py          # DistilBERT embedding model
│   ├── preprocess.py     # Text cleaning and normalization
│   ├── extract.py        # PDF and text extraction
│   └── skills.py         # Skills database and matching logic
├── sample_data/
│   ├── example_cv.txt    # Sample resume for testing
│   └── example_jd.txt    # Sample job description
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── .dockerignore        # Docker build exclusions
├── test_api.py          # Automated test suite
└── README.md            # This file
```

## Roadmap

### Planned Enhancements
- [ ] **Multi-format Support**: DOCX, RTF document parsing
- [ ] **Batch Processing**: Endpoint for multiple CV comparisons
- [ ] **Fine-tuning**: Domain-specific model training on recruitment data
- [ ] **Advanced NER**: Named entity recognition for skill extraction
- [ ] **Caching Layer**: Redis integration for repeated queries
- [ ] **Weighted Scoring**: Configurable skill importance weights
- [ ] **Database Integration**: Result storage and analytics
- [ ] **Authentication**: API key management and rate limiting

### Performance Roadmap
- [ ] Model quantization for reduced memory footprint
- [ ] Inference optimization with ONNX Runtime
- [ ] Horizontal scaling with load balancer support

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this project in your research or application, please cite:

```bibtex
@software{cv_matcher_2025,
  author = {Salahe03},
  title = {CV-to-Job Matcher: ML-Powered Resume Screening API},
  year = {2025},
  url = {https://github.com/salahe03/CV-MatcherAI}
}
```

## Acknowledgments

- DistilBERT model by Hugging Face
- FastAPI framework by Sebastián Ramírez
- PyTorch by Meta AI Research

---

**For issues, questions, or feature requests, please open an issue on GitHub.**