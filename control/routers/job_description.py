"""
This module contains the API endpoints for the job description service.
"""
from typing import List
import requests
from fastapi import APIRouter, HTTPException
from control.codes import OK, COMPANY_NOT_FOUND, BAD_REQUEST
from control.models.models import JobDescription, JobDescriptionMatch, JobDescriptionNotify, JobDescriptionRequest
from auth.auth_handler import decode_token
from control.routers.aux import API_MATCHING_URL
from repository.company_repository import (
    get_company,
    get_job_description_to_match_by_id,
    update_job_description,
    get_job_description_by_id,
    get_job_descriptions,
    delete_job_description
)

router = APIRouter(
    tags=["Companies"],
    prefix="/companies",
)
origins = ["*"]

@router.post("/company/job_description")
def upload_job_description(token: str, job_description: JobDescriptionRequest):
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
        url = API_MATCHING_URL + f"/matching/job/{job_id}/"
        response = requests.post(
            url,
            json=job_description.dict()
        )
        
        if response.status_code != OK:
            raise HTTPException(status_code=BAD_REQUEST, detail="Error uploading job description to model.")
        
        return {"message": "Job description uploaded successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))


@router.get("/company/job_description/{job_id}", response_model=JobDescription)
def get_job_description(token: str, job_id: str):
    """
    Get a job description by its ID.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        
        job_description = get_job_description_by_id(job_id)
        job_description["id"] = str(job_description.pop("_id"))
        return JobDescription(**job_description)
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    
@router.get("/company/job_description_to_match/{job_id}", response_model=JobDescriptionMatch)
def get_job_description_to_match(job_id: str):
    """
    Get a job description by its ID.
    """
    try:
        job_description = get_job_description_to_match_by_id(job_id)
        job_description["id"] = str(job_description.pop("_id"))
        return JobDescriptionMatch(**job_description)
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))    

@router.get("/company/job_descriptions", response_model=List[JobDescription])
def get_my_job_descriptions(token: str, offset: int = 0, amount: int = 10):
    """
    Get the most recent job descriptions of a company with pagination.
    """
    try:
        email = decode_token(token)["email"]
        job_descriptions = get_job_descriptions(email, offset, amount)
        
        job_descriptions = [
            JobDescription(
                id=str(jd["_id"]),
                title=jd["title"],
                description=jd["description"],
                responsabilities=jd["responsabilities"],
                requirements=jd["requirements"],
                work_model=jd["work_model"],
                age_range=jd["age_range"],
                years_of_experience=jd["years_of_experience"]
            )
            for jd in job_descriptions
        ]
        
        return job_descriptions
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))


@router.delete("/company/job_description/{job_id}")
def delete_job_description_api(token: str, job_id: str):
    """
    Delete a job description by its ID.
    """
    try:
        email = decode_token(token)["email"]
        company = get_company(email)
        if not company:
            raise HTTPException(status_code=COMPANY_NOT_FOUND, detail="Company not found.")
        
        delete_job_description(job_id)

        # Borrar la job description del modelo
        url = API_MATCHING_URL + f"/matching/job/{job_id}/"
        response = requests.delete(url)
        
        if response.status_code != OK:
            raise HTTPException(status_code=BAD_REQUEST, detail="Error deleting job description from model.")
        
        return {"message": "Job description deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))

@router.get("/company/job_description_to_notify/{job_id}", response_model=JobDescriptionNotify)
def get_job_description_to_notify(job_id: str):
    """
    Get a job description by its ID.
    """
    try:
        job_description = get_job_description_to_match_by_id(job_id)


        return JobDescriptionNotify(title=job_description["title"], email=job_description["email"])
    except ValueError as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))    

