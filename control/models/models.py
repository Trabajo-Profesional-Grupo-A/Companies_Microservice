# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from typing import List
from pydantic import BaseModel


class CompanySignUp(BaseModel):
    """
    Company sign up model.
    """
    email: str
    password: str
    name: str

class CompanySignIn(BaseModel):
    """
    Company sign in model.
    """
    email: str
    password: str

class CompanyResponse(BaseModel):
    """
    Company response model.
    """
    email: str
    name: str
    description: str

class CompanyUpdate(BaseModel):
    """
    Company update model.
    """
    name: str
    description: str

class JobDescription(BaseModel):
    """
    Job description model.
    """
    title: str
    description: str
    responsabilities: List[str]
    requirements: List[str]
