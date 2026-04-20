import logging
import os

import msal
import requests

logger = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/.default"]
EXCEL_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
SIMPLE_UPLOAD_LIMIT = 4 * 1024 * 1024  # 4 MB


def _get_access_token(client_id: str, client_secret: str, tenant_id: str) -> str:
    """
    Acquires a Graph API token via client credentials flow (no user login).
    The Azure AD app must have Files.ReadWrite.All application permission,
    admin-consented.
    """
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority,
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    if "access_token" not in result:
        raise RuntimeError(
            f"MSAL token acquisition failed: {result.get('error_description', result)}"
        )
    return result["access_token"]


def _upload_simple(
    token: str, drive_id: str, file_path_in_drive: str, local_path: str
) -> None:
    """PUT upload for files under 4 MB."""
    url = f"{GRAPH_BASE}/drives/{drive_id}/root:{file_path_in_drive}:/content"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": EXCEL_CONTENT_TYPE,
    }
    with open(local_path, "rb") as f:
        data = f.read()
    response = requests.put(url, headers=headers, data=data, timeout=30)
    response.raise_for_status()
    logger.info("Uploaded %s via simple PUT → %s", local_path, file_path_in_drive)


def _upload_large(
    token: str, drive_id: str, file_path_in_drive: str, local_path: str
) -> None:
    """
    Chunked upload session for files >= 4 MB.
    The uploadUrl returned by createUploadSession already embeds auth —
    do NOT add an Authorization header to the chunk PUT requests.
    """
    session_url = (
        f"{GRAPH_BASE}/drives/{drive_id}/root:{file_path_in_drive}:/createUploadSession"
    )
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"item": {"@microsoft.graph.conflictBehavior": "replace"}}
    resp = requests.post(session_url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    upload_url = resp.json()["uploadUrl"]

    chunk_size = 5 * 1024 * 1024  # 5 MB (multiple of 320 KB)
    file_size = os.path.getsize(local_path)

    with open(local_path, "rb") as f:
        offset = 0
        while offset < file_size:
            chunk = f.read(chunk_size)
            chunk_len = len(chunk)
            chunk_headers = {
                "Content-Length": str(chunk_len),
                "Content-Range": f"bytes {offset}-{offset + chunk_len - 1}/{file_size}",
            }
            chunk_resp = requests.put(
                upload_url, headers=chunk_headers, data=chunk, timeout=60
            )
            chunk_resp.raise_for_status()
            offset += chunk_len

    logger.info("Uploaded %s via chunked session → %s", local_path, file_path_in_drive)


def upload_to_sharepoint(
    client_id: str,
    client_secret: str,
    tenant_id: str,
    drive_id: str,
    file_path_in_drive: str,
    local_file_path: str,
) -> None:
    """
    Uploads a local .xlsx file to OneDrive/SharePoint via Microsoft Graph API.
    Selects simple PUT for files < 4 MB, chunked session for larger files.
    """
    token = _get_access_token(client_id, client_secret, tenant_id)
    file_size = os.path.getsize(local_file_path)

    if file_size < SIMPLE_UPLOAD_LIMIT:
        _upload_simple(token, drive_id, file_path_in_drive, local_file_path)
    else:
        _upload_large(token, drive_id, file_path_in_drive, local_file_path)
