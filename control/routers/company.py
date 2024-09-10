"""
This module contains the API endpoints for the companies service.
"""
import requests
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
from auth.auth_handler import decode_token
from control.models.models import CompanySignUp, CompanySignIn, CompanyResponse, CompanyUpdate, CompanyUpdateDescription, CompanyUpdatePhone, CompanyUpdateAddress
from auth.auth_handler import hash_password, check_password, generate_token, decode_token

router = APIRouter(
    tags=["Companies"],
    prefix="/companies",
)
origins = ["*"]

from repository.company_repository import create_company, get_company, update_company, search_companies_by_name, update_company_description, update_company_phone, update_company_address

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
def api_update_company_description(token: str, company_update: CompanyUpdate):
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


@router.patch("/company/description")
def update_description(token: str, company_update: CompanyUpdateDescription):
    """
    Update a company's description.
    """
    try:
        email = decode_token(token)["email"]
        update_company_description(email, company_update.description)
        return {"message": "Company description updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))


@router.patch("/company/phone")
def update_phone(token: str, company_update: CompanyUpdatePhone):
    """
    Update a company's phone number.
    """
    try:
        email = decode_token(token)["email"]
        update_company_phone(email, company_update.phone)
        return {"message": "Company phone updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))


@router.patch("/company/address")
def update_address(token: str, company_update: CompanyUpdateAddress):
    """
    Update a company's address.
    """
    try:
        email = decode_token(token)["email"]
        update_company_address(email, company_update.address)
        return {"message": "Company address updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
