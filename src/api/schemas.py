from pydantic import BaseModel
from typing import Optional, Dict, Any

class ExtractResponse(BaseModel):
    """Response schema for extraction results"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class PatientDetailsResponse(BaseModel):
    """Patient details extracted from document"""
    patient_name: Optional[str] = None
    patient_age: Optional[str] = None
    patient_id: Optional[str] = None
    # Add other fields as needed

class PrescriptionResponse(BaseModel):
    """Prescription details extracted from document"""
    patient_name: Optional[str] = None
    medicines: Optional[list] = None
    dosage: Optional[str] = None
    # Add other fields as needed