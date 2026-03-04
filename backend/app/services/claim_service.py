from app.db.database import get_db_connection

def create_claim_service(claim):

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO claims (
        batch_id,
        member_id,
        hospital_name,
        diagnosis_code,
        procedure_code,
        claim_amount
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (
        claim.batch_id,
        claim.member_id,
        claim.hospital_name,
        claim.diagnosis_code,
        claim.procedure_code,
        claim.claim_amount
    ))

    conn.commit()

    cursor.close()
    conn.close()

def get_all_claims():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM claims")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows