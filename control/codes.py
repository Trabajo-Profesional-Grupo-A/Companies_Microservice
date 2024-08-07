from fastapi import status

OK = status.HTTP_200_OK
COMPANY_NOT_FOUND = status.HTTP_404_NOT_FOUND
INCORRECT_CREDENTIALS = status.HTTP_401_UNAUTHORIZED
BAD_REQUEST = status.HTTP_400_BAD_REQUEST
INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
CONFLICT = status.HTTP_409_CONFLICT
USER_NOT_FOUND = status.HTTP_404_NOT_FOUND


