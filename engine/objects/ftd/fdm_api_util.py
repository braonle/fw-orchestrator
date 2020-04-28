#!/usr/bin/env python

import requests
from requests import HTTPError
import os

# Disable insecure request warnings
if os.name == 'nt':
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

elif os.name == 'posix':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fdm_login(
    host,
    port,
    username,
    password,
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
    host,
    port,
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


def fdm_create_network(
    access_token,
    host,
    port,
    name: str = "TEST_NETWORK",
    description: str = "Test NW from Python",
    subType: str = "NETWORK",
    value: str = "1.1.1.0/24"
):
    """Create a new network in FDM."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Data for the network object to be created
    network_object = {
        "name": name,
        "description": description,
        "subType": subType,
        "value": value,
        "type": "networkobject"
    }

    response = requests.post(
        f"https://{host}:{port}/api/fdm/latest/object/networks",
        headers=headers,
        json=network_object,
        verify=False,
    )
    # response.raise_for_status()

    return response.json()


def fdm_get_ntp(
    access_token,
    host,
    port,
):
    """Get the list of all NTP objects in FDM."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://{host}:{port}/api/fdm/latest/devicesettings/default/ntp",
        headers=headers,
        verify=False,
    )
    response.raise_for_status()

    return response.json()


def fdm_get_dns_server_groups(
    access_token,
    host,
    port,
):
    """Get the list of all DNS server groups in FDM."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://{host}:{port}/api/fdm/latest/object/dnsservergroups",
        headers=headers,
        verify=False,
    )
    response.raise_for_status()

    return response.json()


def fdm_get_access_policies(
    access_token,
    host,
    port,
):
    """Get the list of all access policies in FDM."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://{host}:{port}/api/fdm/latest/policy/accesspolicies",
        headers=headers,
        verify=False,
    )
    response.raise_for_status()

    return response.json()


def fdm_get_access_rules(
    access_token,
    host,
    port,
    access_policy_id
):
    """Get the list of the access rules of an access policy."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        f"https://{host}:{port}/api/fdm/latest/policy/accesspolicies/{access_policy_id}/accessrules",
        headers=headers,
        verify=False,
    )
    response.raise_for_status()

    return response.json()
