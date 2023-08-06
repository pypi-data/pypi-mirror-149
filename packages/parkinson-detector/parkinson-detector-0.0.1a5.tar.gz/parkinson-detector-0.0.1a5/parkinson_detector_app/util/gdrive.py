import os
import requests


def download_file_from_google_drive(link: str, destination: str):
    """
    This method downloads file from google drive and saves it in the given destination

    Parameters
    ----------
    link:str
        link to the location in google drive

    destination:str
        destination in which the file will be saved

    """
    URL = "https://docs.google.com/uc?export=download"
    id = max(link.split('/'), key=len)
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)


def get_confirm_token(response):
    """
    This method handles the authentication before the google drive

    Parameters
    ----------
    response: requests.models.Response
        response from first request to google drive, case authentication needed it will ask for a token

    Returns
    -------
    value:
        token for dowload case needed, None otherwise

    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    """
    This method saves the response given from google drive (file).

    Parameters
    ----------
    response: requests.models.Response
        response given from the google drive (mostly file)

    destination: str
        destination where the file saved
    """
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
