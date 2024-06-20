"""
This module contains the API endpoints for the companies service.
"""

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
import firebase_admin
import os

from control.models.models import CompanySignUp, CompanySignIn, CompanyResponse
from auth.auth_handler import hash_password, check_password, generate_token, decode_token
from control.routers.aux import get_user_from_email

router = APIRouter(
    tags=["companies"],
    prefix="/companies",
)
origins = ["*"]

from repository.company_repository import create_company, get_company

from firebase_admin import credentials, storage

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "tpp-grupoa.appspot.com"})

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

@router.get("/get-company", response_model=CompanyResponse)
def get_company_by_token(token: str):
    """
    Get a company by token.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        return CompanySignUp.parse_obj(company)

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    
@router.post("/upload-image")
def upload_image():
    """
    Upload an image.
    """
    try:
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "../../image.png")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No such file or directory: '{image_path}'")
        
        bucket = storage.bucket() 
        blob = bucket.blob("image.png")
        blob.upload_from_filename(image_path)
        return {"message": "Image uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.get("/prueba/conexion")    
def api_prueba_conexion(email: str):
    """
    Get a user by email.
    """
    try:
        user = get_user_from_email(email)
        if not user:
            raise HTTPException(status_code=USER_NOT_FOUND, detail="User not found.")
        return {"message": "User found successfully.", "user": user}

    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))