from fastapi import APIRouter
from app.models.claim_model import ClaimRequest
from app.services.claim_service import create_claim_service,get_all_claims

router = APIRouter()

@router.post("/claims")

def create_claim(claim: ClaimRequest):

    create_claim_service(claim)

    return {"message": "Claim created successfully"}

@router.get("/claims")
def fetch_claims():

    claims = get_all_claims()

    result = []

    for row in claims:
        result.append({
            "claim_id": row[0],
            "batch_id": row[1],
            "member_id": row[2],
            "hospital_name": row[3],
            "diagnosis_code": row[4],
            "procedure_code": row[5],
            "claim_amount": row[6],
            "fraud_score": row[7],
            "eligibility_status": row[8],
            "claim_status": row[9],
            "created_at": str(row[10])
        })

    return result