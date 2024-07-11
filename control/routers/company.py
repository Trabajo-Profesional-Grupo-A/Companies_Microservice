"""
This module contains the API endpoints for the companies service.
"""
import requests

from fastapi import (
    APIRouter,
    HTTPException,
)

from control.codes import (
    COMPANY_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    USER_NOT_FOUND,
    BAD_REQUEST,
    CONFLICT,
)

from control.models.models import CompanySignUp, CompanySignIn, CompanyResponse, CompanyUpdate, JobDescription
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

router = APIRouter(
    tags=["companies"],
    prefix="/companies",
)
origins = ["*"]

from repository.company_repository import create_company, get_company, update_company, update_job_description

@router.post("/sign-up")
def sign_up(company: CompanySignUp):
    """
    Sign up a new company.
    """
    try: 
        company.password = hash_password(company.password)
        create_company(company)
        token = generate_token(company.email)
        return {"message": "Company created successfully.", "token": token}
    except ValueError as e:
        raise HTTPException(status_code=CONFLICT, detail=str(e))

@router.post("/sign-in")
def sign_in(company: CompanySignIn):
    """
    Sign in a company.
    """
    try:
        stored_company = get_company(company.email)
        if not stored_company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="company not found.")
        if check_password(company.password, stored_company["password"]):
            token = generate_token(company.email)
            return {"message": "Company signed in successfully.", "token": token}
        else: 
            raise HTTPException(status_code=INCORRECT_CREDENTIALS, detail="Incorrect email or password.")
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.get("/company", response_model=CompanyResponse)
def get_company_by_token(token: str):
    """
    Get a company by token.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        return CompanyResponse(email=company["email"], name=company["name"], description=company["description"])

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    
@router.put("/company")
def update_company_description(token: str, company_update: CompanyUpdate):
    """
    Update a company's description.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        update_company(email, company_update)
        return {"message": "Company description updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.post("/company/job_description")
def upload_job_description(token: str, job_description: JobDescription):
    """
    Upload a job description.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        
        job_id = update_job_description(email, job_description)

        # Enviar la job description al modelo
        response = requests.post(
            f"http://34.42.161.58:8000/matching/job/{job_id}/",
            json=job_description.dict()
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=BAD_REQUEST, detail="Error uploading job description to model.")
        
        return {"message": "Job description uploaded successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))



    
