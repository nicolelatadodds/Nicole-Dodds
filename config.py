import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    smartsheet_token: str
    smartsheet_sheet_id: int
    graph_client_id: str
    graph_client_secret: str
    graph_tenant_id: str
    sharepoint_drive_id: str
    sharepoint_file_path: str
    poll_interval_seconds: int
    local_output_path: str


def load_config() -> Config:
    missing = []

    def require(key: str) -> str:
        val = os.getenv(key)
        if not val:
            missing.append(key)
        return val or ""

    sheet_id_str = os.getenv("SMARTSHEET_SHEET_ID", "0")
    try:
        sheet_id = int(sheet_id_str)
    except ValueError:
        sheet_id = 0
        missing.append("SMARTSHEET_SHEET_ID (must be a valid integer)")

    cfg = Config(
        smartsheet_token=require("SMARTSHEET_ACCESS_TOKEN"),
        smartsheet_sheet_id=sheet_id,
        graph_client_id=require("GRAPH_CLIENT_ID"),
        graph_client_secret=require("GRAPH_CLIENT_SECRET"),
        graph_tenant_id=require("GRAPH_TENANT_ID"),
        sharepoint_drive_id=require("SHAREPOINT_DRIVE_ID"),
        sharepoint_file_path=require("SHAREPOINT_FILE_PATH"),
        poll_interval_seconds=int(os.getenv("POLL_INTERVAL_SECONDS", "300")),
        local_output_path=os.getenv("LOCAL_OUTPUT_PATH", "output/client_status.xlsx"),
    )

    if missing:
        raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")
    if cfg.smartsheet_sheet_id == 0:
        raise EnvironmentError("SMARTSHEET_SHEET_ID must be a non-zero integer")

    return cfg
