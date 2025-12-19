from schemas import *
from datetime import date
import uuid

def search_patient(request: PatientSearchRequest) -> Patient:
    return Patient(
        patient_id="PAT-123",
        name=request.name,
        dob=date(1985, 6, 15)
    )

def check_insurance_eligibility(
    request: InsuranceEligibilityRequest
) -> InsuranceEligibilityResponse:
    return InsuranceEligibilityResponse(
        patient_id=request.patient_id,
        eligible=True,
        provider="ABC Health Insurance"
    )

def find_available_slots(
    request: AppointmentSlotRequest
) -> list[AppointmentSlot]:
    return [
        AppointmentSlot(
            slot_id="SLOT-001",
            date=request.date_range_start,
            time="10:00 AM"
        )
    ]

def book_appointment(
    request: BookAppointmentRequest
) -> AppointmentConfirmation:
    return AppointmentConfirmation(
        appointment_id=str(uuid.uuid4()),
        patient_id=request.patient_id,
        specialty=request.specialty,
        date=date.today(),
        time="10:00 AM"
    )
