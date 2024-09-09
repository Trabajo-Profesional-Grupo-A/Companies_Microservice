"""
This module contains the API endpoints for the companies service.
"""
import requests
import base64
import firebase_admin
from firebase_admin import credentials
import os
import json
from firebase_admin import credentials, auth
from firebase_admin.auth import InvalidIdTokenError

from typing import List

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

from control.models.models import CompanySignUp, CompanySignIn, CompanyResponse, CompanyUpdate
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

def initialize_firebase():
    if not firebase_admin._apps:
        service_account_info = json.loads(base64.b64decode(os.environ.get('FIREBASE_SERVICE_ACCOUNT_KEY')).decode('utf-8'))
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)

initialize_firebase()

router = APIRouter(
    tags=["Companies"],
    prefix="/companies",
)
origins = ["*"]

from repository.company_repository import create_company, get_company, update_company, search_companies_by_name

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
        return CompanyResponse(email=company["email"], name=company["name"], description=company["description"], phone=company["phone"], address=company["address"])

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


@router.get("/search", response_model=List[CompanyResponse])
def search_company(name: str, offset: int = 0, amount: int = 5):
    """
    Search for companies by name.
    """
    try:
        companies = search_companies_by_name(name, offset, amount)
        if not companies:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="No companies found.")
        return [CompanyResponse.parse_obj(user) for user in companies]
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.post("/sign-in-google")
def sign_in_google(token: str):
    """
    Sign in a user with Google.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        email = decoded_token["email"]
        user = get_company(email)
        if not user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        token = generate_token(email)
        return {"message": "User signed in successfully.", "token": token}
    except InvalidIdTokenError:
        raise HTTPException(status_code=INCORRECT_CREDENTIALS, detail="Invalid token.")
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
