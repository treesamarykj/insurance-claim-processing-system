from fastapi import APIRouter
from app.models.claim_model import ClaimRequest
from app.services.claim_service import create_claim_service,insert_query, get_claim_by_id, get_claims_by_member

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "service running..."}

@router.post("/claims")
def create_claim(claim: ClaimRequest):

    create_claim_service(claim)

    return {"message": "Claim created successfully"}

@router.get("/claims")
def fetch_claims():

    claims = insert_query()

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

@router.get("/claims/{claim_id}")
def fetch_claim_by_id(claim_id: int):

    claim = get_claim_by_id(claim_id)

    if not claim:
        return {"message": "Claim not found"}

    return {
        "claim_id": claim[0],
        "batch_id": claim[1],
        "member_id": claim[2],
        "hospital_name": claim[3],
        "diagnosis_code": claim[4],
        "procedure_code": claim[5],
        "claim_amount": claim[6],
        "fraud_score": claim[7],
        "eligibility_status": claim[8],
        "claim_status": claim[9]
    }

@router.get("/claims/member/{member_id}")
def fetch_claim_by_member_id(member_id:str):
    
    claims = get_claims_by_member(member_id)

    if not claims:
        return{"message":"no history"}

    result = []

    for claim in claims:
        result.append({
            "claim_id": claim[0],
            "batch_id": claim[1],
            "member_id": claim[2],
            "hospital_name": claim[3],
            "diagnosis_code": claim[4],
            "procedure_code": claim[5],
            "claim_amount": claim[6],
            "fraud_score": claim[7],
            "eligibility_status": claim[8],
            "claim_status": claim[9]
        })

    return result