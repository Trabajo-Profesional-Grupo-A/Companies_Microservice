from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import CompanySignUp, CompanyUpdate
DB_URI = "mongodb+srv://nencinoza:4VxMOntx1i2W8uQm@users.6jjtd5n.mongodb.net/?retryWrites=true&w=majority&appName=users"

client = MongoClient(DB_URI, server_api=ServerApi('1'))

db = client.companies
collection = db.companies
collection.create_index([('email', 1)], unique=True)


def create_company(company: CompanySignUp): 
    """
    Create a new company.
    """
    try:
        company_dict = dict(company)
        company_dict["description"] = ""
        collection.insert_one(company_dict)
    except errors.DuplicateKeyError as e:
        raise ValueError("Company with this email already exists.")


def get_company(email: str):
    """
    Get a company by email.
    """
    try:
        return collection.find_one({"email": email})
    except Exception as e:
        raise ValueError(str(e))

def update_company(email:str, company_update: CompanyUpdate):
    """
    Update a company's description.
    """
    try:
        collection.update_one({"email": email}, {"$set": {"description": company_update.description, "name": company_update.name}})
    except Exception as e:
        raise ValueError(str(e))