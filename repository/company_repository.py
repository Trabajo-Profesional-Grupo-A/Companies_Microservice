from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import CompanySignUp, CompanyUpdate, JobDescription
from bson.objectid import ObjectId

DB_URI = "mongodb+srv://nencinoza:4VxMOntx1i2W8uQm@users.6jjtd5n.mongodb.net/?retryWrites=true&w=majority&appName=users"

client = MongoClient(DB_URI, server_api=ServerApi('1'))

db = client.companies
collection = db.companies
collection_jd = db.job_descriptions
collection.create_index([('email', 1)], unique=True)

existing_indexes = collection_jd.index_information()
if 'email_1' in existing_indexes:
    collection_jd.drop_index('email_1')
#collection_jd.create_index([('_id', 1)], unique=True)


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
    
def update_job_description(email:str, job_description: JobDescription):
    """
    Update a company's job description.
    """
    try:
        jd_dict = dict(job_description)
        jd_dict["email"] = email
        result = collection_jd.insert_one(jd_dict)
        return str(result.inserted_id)
    except Exception as e:
        print("falla el insert one")
        raise ValueError(str(e))
    
def modify_job_description(job_id: str, new_data: dict):
    """
    Modify an existing job description.
    """
    try:
        result = collection_jd.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": new_data}
        )
        if result.modified_count > 0:
            return f"Job description with id {job_id} updated successfully."
        else:
            return f"No job description found with id {job_id} or no changes made."
    except Exception as e:
        print("falla el update one")
        raise ValueError(str(e))


def get_job_description_by_id(job_id: str):
    """
    Retrieve a job description by its ID and email.
    """
    try:
        job_description = collection_jd.find_one({"_id": ObjectId(job_id)})
        if not job_description:
            raise ValueError("Job description not found.")
        return job_description
    except Exception as e:
        raise ValueError(str(e))


def get_job_descriptions(email: str, offset: int = 0, amount: int = 10):
    """
    Get the most recent job descriptions of a company with pagination.
    """
    try:
        job_descriptions = list(collection_jd.find({"email": email})
                                .sort("_id", -1)
                                .skip(offset)
                                .limit(amount))
        return job_descriptions
    except Exception as e:
        raise ValueError(str(e))
    
def delete_job_description(job_id: str):
    """
    Delete a job description by its ID.
    """
    try:
        result = collection_jd.delete_one({"_id": ObjectId(job_id)})
        if result.deleted_count > 0:
            return f"Job description with id {job_id} deleted successfully."
        else:
            return f"No job description found with id {job_id}."
    except Exception as e:
        raise ValueError(str(e))