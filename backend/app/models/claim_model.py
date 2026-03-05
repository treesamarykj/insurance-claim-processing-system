from pydantic import BaseModel
from typing import Optional

class ClaimRequest(BaseModel):
    batch_id: str
    member_id: str
    hospital_name: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: float
    fraud_score: Optional[float] = None
    eligibility_status: Optional[str] = None
    claim_status: Optional[str] = None
    
