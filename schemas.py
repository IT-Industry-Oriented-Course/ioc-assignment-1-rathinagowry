from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PatientSearchRequest(BaseModel):
    name: str

class Patient(BaseModel):
    patient_id: str
    name: str
    dob: date

class InsuranceEligibilityRequest(BaseModel):
    patient_id: str

class InsuranceEligibilityResponse(BaseModel):
    patient_id: str
    eligible: bool
    provider: Optional[str]

class AppointmentSlotRequest(BaseModel):
    specialty: str
    date_range_start: date
    date_range_end: date

class AppointmentSlot(BaseModel):
    slot_id: str
    date: date
    time: str

class BookAppointmentRequest(BaseModel):
    patient_id: str
    slot_id: str
    specialty: str

class AppointmentConfirmation(BaseModel):
    appointment_id: str
    patient_id: str
    specialty: str
    date: date
    time: str
