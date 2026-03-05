from app.db.database import get_db_connection


def calculate_fraud_score(claim_amount):

    if claim_amount > 40000:
        return 0.85
    elif claim_amount > 20000:
        return 0.40
    else:
        return 0.10
    
def determine_claim_status(fraud_score):

    if fraud_score > 0.7:
        return "UNDER_REVIEW"
    else:
        return "APPROVED"
    
def create_claim_service(claim):

    fraud_score = calculate_fraud_score(claim.claim_amount)
    claim_status = determine_claim_status(fraud_score)

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO claims (
        batch_id,
        member_id,
        hospital_name,
        diagnosis_code,
        procedure_code,
        claim_amount,
        fraud_score,
        eligibility_status,
        claim_status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(insert_query, (
        claim.batch_id,
        claim.member_id,
        claim.hospital_name,
        claim.diagnosis_code,
        claim.procedure_code,
        claim.claim_amount,
        fraud_score,
        claim.eligibility_status,
        claim_status
    ))

    conn.commit()
    cursor.close()
    conn.close()

def insert_query():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM claims")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_claim_by_id(claim_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM claims WHERE claim_id = %s"

    cursor.execute(query, (claim_id,))
    claim = cursor.fetchone()

    cursor.close()
    conn.close()

    return claim

def update_claim_status(claim_id, claim_status):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE claims
    SET claim_status = %s
    WHERE claim_id = %s
    """

    cursor.execute(query, (claim_status, claim_id))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Claim status updated"}