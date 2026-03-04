from pydantic import BaseModel

class ClaimRequest(BaseModel):
    batch_id: str
    member_id: str
    hospital_name: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: float
    
