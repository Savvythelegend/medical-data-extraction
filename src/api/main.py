from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
from src.ocr.extractor import extract
from src.api.schemas import ExtractResponse
import uuid
import os
import logging
from pathlib import Path

# Setup logging to see extraction results
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/extractor", response_model=ExtractResponse)
def extractor(
        file_format: str = Form(...),
        file: UploadFile = File(...),
):
    contents = file.file.read() 
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}.pdf" # Save uploaded file temporarily

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"Extracting from file: {file_path}, format: {file_format}")
        data = extract(file_path=str(file_path), file_format=file_format)
        
        logger.info(f"Extraction successful: {data}")
        return ExtractResponse(success=True, data=data)
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return ExtractResponse(success=False, error=str(e))
    finally:
        if file_path.exists():
            file_path.unlink() # Remove the temporary file
            logger.info(f"Cleaned up temp file: {file_path}")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)