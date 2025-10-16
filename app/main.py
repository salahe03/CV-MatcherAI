"""
FastAPI application for CV-to-Job matching
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import traceback

from app.extract import extract_text
from app.preprocess import preprocess_for_embedding
from app.model import calculate_match_score
from app.skills import match_skills


# Create FastAPI app
app = FastAPI(
    title="CV-to-Job Matcher API",
    description="Match candidate CVs to job descriptions with ML-powered scoring",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "CV-to-Job Matcher API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "match": "/match (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/match")
async def match_cv_to_job(
    cv_file: Optional[UploadFile] = File(None),
    cv_text: Optional[str] = Form(None),
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None)
):
    """
    Match a CV to a job description and return match score, matched skills, and missing skills.
    
    Args:
        cv_file: CV as PDF or text file (optional if cv_text provided)
        cv_text: CV as plain text string (optional if cv_file provided)
        jd_file: Job description as file (optional if jd_text provided)
        jd_text: Job description as plain text (optional if jd_file provided)
        
    Returns:
        JSON with match_score, matched_skills, and missing_skills
    """
    try:
        # Extract CV text
        if cv_file:
            cv_content = await cv_file.read()
            is_pdf = bool(cv_file.filename and cv_file.filename.lower().endswith('.pdf'))
            cv_raw_text = extract_text(cv_content, is_pdf=is_pdf)
        elif cv_text:
            cv_raw_text = extract_text(cv_text, is_pdf=False)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either cv_file or cv_text must be provided"
            )
        
        # Extract job description text
        if jd_file:
            jd_content = await jd_file.read()
            is_pdf = bool(jd_file.filename and jd_file.filename.lower().endswith('.pdf'))
            jd_raw_text = extract_text(jd_content, is_pdf=is_pdf)
        elif jd_text:
            jd_raw_text = extract_text(jd_text, is_pdf=False)
        else:
            raise HTTPException(
                status_code=400,
                detail="Either jd_file or jd_text must be provided"
            )
        
        # Preprocess texts for embedding
        cv_processed = preprocess_for_embedding(cv_raw_text)
        jd_processed = preprocess_for_embedding(jd_raw_text)
        
        # Calculate overall match score using embeddings
        match_score = calculate_match_score(cv_processed, jd_processed)
        
        # Extract and match skills
        matched_skills, missing_skills = match_skills(cv_raw_text, jd_raw_text)
        
        # Prepare response
        response = {
            "match_score": round(match_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }
        
        return JSONResponse(content=response, status_code=200)
    
    except HTTPException:
        raise
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/skills")
async def list_skills():
    """
    List all skills in the database.
    
    Returns:
        JSON with list of all available skills
    """
    from app.skills import get_all_skills
    return {
        "total_skills": len(get_all_skills()),
        "skills": get_all_skills()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
