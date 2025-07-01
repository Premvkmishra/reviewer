from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import io
from app.services.huggingface import analyze_code

router = APIRouter()

class CodeInput(BaseModel):
    code: str
    language: Optional[str] = None

class AnalysisResponse(BaseModel):
    markdown_feedback: str
    language_detected: Optional[str] = None
    analysis_time: float
    code_length: int

@router.post("/analyze")
async def analyze_endpoint(input: CodeInput):
    if len(input.code) > 50_000:  # Increased limit for file uploads
        raise HTTPException(status_code=400, detail="Code too long (max 50,000 characters)")
    
    if not input.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        import time
        start_time = time.time()
        
        feedback = await analyze_code(input.code, input.language)
        
        analysis_time = time.time() - start_time
        
        return AnalysisResponse(
            markdown_feedback=feedback,
            language_detected=input.language,
            analysis_time=round(analysis_time, 2),
            code_length=len(input.code)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-file")
async def analyze_file_endpoint(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size (max 1MB)
    if file.size and file.size > 1_048_576:
        raise HTTPException(status_code=400, detail="File too large (max 1MB)")
    
    # Check file extension
    allowed_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.html', '.css', '.sql', '.sh', '.txt']
    file_ext = '.' + file.filename.split('.')[-1].lower() if '.' in file.filename else ''
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        content = await file.read()
        code = content.decode('utf-8')
        
        # Auto-detect language if not provided
        if not language:
            language_map = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
                '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust',
                '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala',
                '.html': 'HTML', '.css': 'CSS', '.sql': 'SQL', '.sh': 'Shell'
            }
            language = language_map.get(file_ext, 'Unknown')
        
        return await analyze_endpoint(CodeInput(code=code, language=language))
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be text-based")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@router.get("/supported-languages")
async def get_supported_languages():
    return {
        "languages": [
            {"code": "python", "name": "Python", "extensions": [".py"]},
            {"code": "javascript", "name": "JavaScript", "extensions": [".js"]},
            {"code": "typescript", "name": "TypeScript", "extensions": [".ts"]},
            {"code": "java", "name": "Java", "extensions": [".java"]},
            {"code": "cpp", "name": "C++", "extensions": [".cpp", ".cc", ".cxx"]},
            {"code": "c", "name": "C", "extensions": [".c"]},
            {"code": "csharp", "name": "C#", "extensions": [".cs"]},
            {"code": "php", "name": "PHP", "extensions": [".php"]},
            {"code": "ruby", "name": "Ruby", "extensions": [".rb"]},
            {"code": "go", "name": "Go", "extensions": [".go"]},
            {"code": "rust", "name": "Rust", "extensions": [".rs"]},
            {"code": "swift", "name": "Swift", "extensions": [".swift"]},
            {"code": "kotlin", "name": "Kotlin", "extensions": [".kt"]},
            {"code": "scala", "name": "Scala", "extensions": [".scala"]},
            {"code": "html", "name": "HTML", "extensions": [".html", ".htm"]},
            {"code": "css", "name": "CSS", "extensions": [".css"]},
            {"code": "sql", "name": "SQL", "extensions": [".sql"]},
            {"code": "shell", "name": "Shell", "extensions": [".sh", ".bash"]}
        ]
    } 