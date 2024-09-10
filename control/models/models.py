# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from typing import List, Tuple
from pydantic import BaseModel


class CompanySignUp(BaseModel):
    """
    Company sign up model.
    """
    email: str
    password: str
    name: str
    phone: str
    description: str
    address: str

class CompanySignIn(BaseModel):
    """
    Company sign in model.
    """
    email: str
    password: str

class CompanyResponse(BaseModel):
    email: str
    name: str
    description: str
    phone: str
    address: str

class CompanyUpdate(BaseModel):
    """
    Company update model.
    """
    name: str
    description: str
    address: str

class CompanyUpdateDescription(BaseModel):
    """
    Company update description model.
    """
    description: str

class CompanyUpdateAddress(BaseModel):
    """
    Company update address model.
    """
    address: str

class CompanyUpdatePhone(BaseModel):
    """
    Company update phone model.
    """
    phone: str

class JobDescriptionRequest(BaseModel):
    """
    Job description request model.
    """
    title: str
    description: str
    responsabilities: List[str]
    requirements: List[str]
    work_model: str
    age_range: Tuple[int, int]

class JobDescription(BaseModel):
    """
    Job description model.
    """
    id: str
    title: str
    description: str
    responsabilities: List[str]
    requirements: List[str]
    work_model: str
    age_range: Tuple[int, int]

class JobDescriptionMatch(BaseModel):
    """
    Job description match model.
    """
    id: str
    title: str
    description: str
    responsabilities: List[str]
    requirements: List[str]
    work_model: str
    address: str
    age_range: Tuple[int, int]


