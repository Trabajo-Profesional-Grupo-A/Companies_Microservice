import os
from fastapi import HTTPException, Header
import requests

TIMEOUT = 10
API_USERS_URL = "https://users-microservice-mmuh.onrender.com"
API_COMPANY_URL = "https://companies-microservice.onrender.com"
API_MATCHING_URL = "http://34.133.224.150:8000"

def get_user_from_email(user_email: str):
    """
    This function gets the user from the email.
    """
    params = {"email": user_email}
    url = API_USERS_URL + "/users/user/email"
    response = requests.get(url, params=params, timeout=TIMEOUT)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail={"Unknown error"})

    return response.json()