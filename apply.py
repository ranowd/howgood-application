"""Submit a signed job application to the HowGood apply API."""

import hashlib
import hmac
import json
import os

import requests
from dotenv import load_dotenv

REQUIRED_FIELDS = {
    "name": "NAME",
    "email": "EMAIL",
    "resume": "RESUME",
    "location": "LOCATION",
    "linkedin": "LINKEDIN",
    "codeLink": "CODE_LINK",
}
OPTIONAL_TEXT_FIELDS = {
    "repos": "REPOS",
    "notes": "NOTES",
}
OPTIONAL_INT_FIELDS = {
    "yearsPython": "YEARS_PYTHON",
    "yearsDjango": "YEARS_DJANGO",
}


def build_payload() -> dict:
    """Build the request payload from environment variables."""
    payload = {}

    for field, var in REQUIRED_FIELDS.items():
        payload[field] = os.environ[var]

    for field, var in OPTIONAL_TEXT_FIELDS.items():
        value = os.environ.get(var)
        if value:
            payload[field] = value

    for field, var in OPTIONAL_INT_FIELDS.items():
        value = os.environ.get(var)
        if value:
            payload[field] = int(value)

    return payload


def sign(body: bytes, secret: str) -> str:
    """Return the hex-encoded HMAC-SHA256 of the raw request body."""
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def main() -> None:
    load_dotenv()
    body = json.dumps(build_payload()).encode()
    response = requests.post(
        os.environ["API_URL"],
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-HMAC-Signature": sign(body, os.environ["HMAC_SECRET"]),
        },
        timeout=10,
    )
    print(response.status_code, response.text)
    response.raise_for_status()


if __name__ == "__main__":
    main()
