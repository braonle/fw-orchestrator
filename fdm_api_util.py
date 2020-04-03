#!/usr/bin/env python

import requests
from requests import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pformat

from hosts import FDM


# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fdm_login(
    host=FDM.get("host"),
    port=FDM.get("port"),
    username=FDM.get("username"),
    password=FDM.get("password"),
):
    """Login to FDM and return an access token that may be used for API calls.
    
    This login will give you an access token that is valid for ~30 minutes
    with no refresh. Using this token should be fine for short running scripts.
    """

    url = f"https://{host}:{port}/api/fdm/latest/fdm/token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        verify=False,
    )

    try:
        response.raise_for_status()
        access_token = response.json()["access_token"]

    except HTTPError:
        if response.status_code == 400:
            raise HTTPError(f"Error logging in to FDM: {response.text}")
        else:
            raise

    except ValueError:
        raise ValueError("Error parsing the response from FDM")

    return access_token


def fdm_get_networks(
    access_token,
    host=FDM.get("host"),
    port=FDM.get("port")
):
    """Get the list of all Networks in FDM."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://{host}:{port}/api/fdm/latest/object/networks",
        headers=headers,
        verify=False,
    )
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    token = fdm_login()
    if token:
        print("Login was successful!")
        print(f"Access Token: {token}\n")

    networks = fdm_get_networks(token)

    print(
        'Network(s):',
        pformat(networks),
        sep="\n",
    )
