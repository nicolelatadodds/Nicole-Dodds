import logging
import logging.handlers
import os
import time

import schedule

from config import load_config
from excel_writer import write_client_status
from sharepoint_uploader import upload_to_sharepoint
from smartsheet_client import fetch_sheet_data

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            "logs/sync.log", maxBytes=5 * 1024 * 1024, backupCount=3
        ),
    ],
)
logger = logging.getLogger(__name__)


def run_sync_cycle(cfg) -> None:
    logger.info("── Sync cycle starting ──")

    try:
        sheet_data = fetch_sheet_data(cfg.smartsheet_token, cfg.smartsheet_sheet_id)
    except Exception as exc:
        logger.error("Smartsheet fetch failed: %s", exc, exc_info=True)
        return

    if not sheet_data.rows:
        logger.warning("Sheet returned 0 rows — skipping write and upload")
        return

    try:
        write_client_status(sheet_data, cfg.local_output_path)
    except Exception as exc:
        logger.error("Excel write failed: %s", exc, exc_info=True)
        return

    try:
        upload_to_sharepoint(
            client_id=cfg.graph_client_id,
            client_secret=cfg.graph_client_secret,
            tenant_id=cfg.graph_tenant_id,
            drive_id=cfg.sharepoint_drive_id,
            file_path_in_drive=cfg.sharepoint_file_path,
            local_file_path=cfg.local_output_path,
        )
    except Exception as exc:
        logger.error("SharePoint upload failed: %s", exc, exc_info=True)

    logger.info("── Sync cycle complete ──")


def main() -> None:
    cfg = load_config()
    logger.info(
        "Starting sync service. Sheet ID=%d, interval=%ds",
        cfg.smartsheet_sheet_id,
        cfg.poll_interval_seconds,
    )

    run_sync_cycle(cfg)
    schedule.every(cfg.poll_interval_seconds).seconds.do(run_sync_cycle, cfg)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
