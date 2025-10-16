"""
Skills extraction and matching module
"""

import re
from typing import List, Tuple, Set

# Comprehensive predefined skills list
SKILLS_DATABASE = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "Go", "Rust",
    "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Shell", "Bash",
    
    # Web Technologies
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django",
    "Flask", "FastAPI", "Spring Boot", "ASP.NET", "jQuery", "Bootstrap", "Tailwind",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras", "Scikit-learn",
    "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "NLP", "Computer Vision",
    "Neural Networks", "CNN", "RNN", "LSTM", "Transformer", "BERT", "GPT",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Jenkins", "CI/CD",
    "Terraform", "Ansible", "Git", "GitHub", "GitLab", "CircleCI", "Travis CI",
    
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Oracle",
    "SQL Server", "DynamoDB", "Elasticsearch", "Neo4j", "Firebase",
    
    # Big Data & Analytics
    "Hadoop", "Spark", "Kafka", "Airflow", "ETL", "Data Warehousing", "Tableau",
    "Power BI", "Looker", "Databricks",
    
    # Other Technical Skills
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum", "JIRA", "Testing",
    "Unit Testing", "Integration Testing", "Selenium", "Jest", "pytest",
    "Linux", "Unix", "Windows Server", "Networking", "Security", "OAuth",
    "JWT", "SOLID", "Design Patterns", "OOP", "Functional Programming",
]

# Create case-insensitive pattern for each skill
SKILL_PATTERNS = {
    skill.lower(): re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
    for skill in SKILLS_DATABASE
}


def extract_skills(text: str) -> Set[str]:
    """
    Extract skills from text using regex pattern matching.
    
    Args:
        text: Input text (CV or job description)
        
    Returns:
        Set of matched skills (original case from database)
    """
    found_skills = set()
    
    for skill_lower, pattern in SKILL_PATTERNS.items():
        if pattern.search(text):
            # Find the original case from SKILLS_DATABASE
            original_skill = next(s for s in SKILLS_DATABASE if s.lower() == skill_lower)
            found_skills.add(original_skill)
    
    return found_skills


def match_skills(cv_text: str, jd_text: str) -> Tuple[List[str], List[str]]:
    """
    Match skills between CV and job description.
    
    Args:
        cv_text: Text extracted from CV
        jd_text: Text from job description
        
    Returns:
        Tuple of (matched_skills, missing_skills)
    """
    cv_skills = extract_skills(cv_text)
    jd_skills = extract_skills(jd_text)
    
    matched = cv_skills.intersection(jd_skills)
    missing = jd_skills - cv_skills
    
    return sorted(list(matched)), sorted(list(missing))


def get_all_skills() -> List[str]:
    """Return the complete skills database."""
    return SKILLS_DATABASE.copy()
