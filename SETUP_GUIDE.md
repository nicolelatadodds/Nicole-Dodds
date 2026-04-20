# Setup Guide: Smartsheet → Excel → SharePoint Sync

This guide walks you through everything from installing Python to running the sync
for the first time. Take it one section at a time.

---

## What This Does

Every 5 minutes, this script will:
1. Read your Smartsheet project plan (task names, start dates, end dates)
2. Build an Excel file with a bullet list of all timing steps and a highlighted Final End Date
3. Upload that Excel file to a folder on your SharePoint or OneDrive automatically

---

## PART 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.12.x"** button
3. Run the installer
   - **Important:** On the first screen, check the box that says **"Add Python to PATH"**
   - Then click **"Install Now"**
4. When it finishes, click **Close**

**Verify it worked:**
- Press `Windows key + R`, type `cmd`, press Enter
- In the black window, type: `python --version`
- You should see something like `Python 3.12.3`
- If you get an error, restart your computer and try again

---

## PART 2 — Download the Project Files

You have two options:

### Option A — Download as ZIP (easiest)
1. Go to the GitHub repository in your browser
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Unzip the folder somewhere easy to find, like `C:\Users\YourName\Documents\smartsheet-sync`

### Option B — Use Git
If you have Git installed:
```
git clone <repository-url>
cd Nicole-Dodds
git checkout claude/smartsheet-excel-sync-G2aS7
```

---

## PART 3 — Open a Terminal in the Project Folder

1. Open **File Explorer** and navigate to the project folder
2. Click in the address bar at the top (where the folder path is shown)
3. Type `cmd` and press **Enter**
4. A black Command Prompt window opens, already inside your project folder

You can confirm you're in the right place — type `dir` and press Enter.
You should see files like `main.py`, `requirements.txt`, etc.

---

## PART 4 — Set Up a Virtual Environment

A virtual environment keeps this project's dependencies separate from everything else on your computer.

Type each of these commands one at a time, pressing Enter after each:

```
python -m venv venv
```
```
venv\Scripts\activate
```

After the second command, you'll see `(venv)` appear at the start of the line.
That means it worked. **Always activate the venv before running the script.**

---

## PART 5 — Install Dependencies

With the venv active, run:

```
pip install -r requirements.txt
```

This downloads and installs all the libraries the script needs.
It will take a minute or two. Wait until you see the command prompt return.

---

## PART 6 — Get Your Smartsheet API Token

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture** in the top-right corner
3. Click **"Personal Settings"**
4. In the left menu, click **"API Access"**
5. Click **"Generate new access token"**
6. Give it a name like `excel-sync`
7. Copy the token — it looks like a long string of random characters
8. **Save it somewhere safe** — you won't be able to see it again

**Get your Sheet ID:**
1. Open the Smartsheet you want to sync
2. Look at the URL in your browser — it will look like:
   `https://app.smartsheet.com/sheets/1234567890123456`
3. The number at the end (`1234567890123456`) is your Sheet ID — copy it

---

## PART 7 — Set Up Microsoft Azure (for SharePoint Upload)

This is the most involved part. You need to register an "app" in Azure so the
script has permission to upload files to your SharePoint/OneDrive.

> **Note:** You need to be an admin on your Microsoft 365 account,
> or ask your IT admin to do steps 7.1–7.5 for you.

### 7.1 — Register an App
1. Go to **https://portal.azure.com** and sign in with your Microsoft work account
2. In the search bar at the top, type **"App registrations"** and click it
3. Click **"+ New registration"**
4. Fill in:
   - **Name:** `smartsheet-excel-sync` (or anything you like)
   - **Supported account types:** Select **"Accounts in this organizational directory only"**
   - Leave **Redirect URI** blank
5. Click **"Register"**

### 7.2 — Copy Your IDs
On the app overview page you'll see:
- **Application (client) ID** — copy this, you'll need it
- **Directory (tenant) ID** — copy this too

### 7.3 — Create a Client Secret
1. In the left menu, click **"Certificates & secrets"**
2. Click **"+ New client secret"**
3. Give it a description like `sync-secret`
4. Set expiry to **24 months**
5. Click **"Add"**
6. **Copy the "Value" immediately** — it disappears after you navigate away

### 7.4 — Add API Permissions
1. In the left menu, click **"API permissions"**
2. Click **"+ Add a permission"**
3. Click **"Microsoft Graph"**
4. Click **"Application permissions"** (not Delegated)
5. In the search box, type `Files.ReadWrite`
6. Check **"Files.ReadWrite.All"**
7. Click **"Add permissions"**
8. Click the **"Grant admin consent for [your org]"** button
9. Click **"Yes"** to confirm

### 7.5 — Find Your Drive ID
Your Drive ID tells the script exactly which OneDrive/SharePoint library to upload to.

1. Go to **https://developer.microsoft.com/en-us/graph/graph-explorer**
2. Sign in with your Microsoft account
3. In the query box, replace the URL with:
   ```
   https://graph.microsoft.com/v1.0/me/drives
   ```
4. Click **"Run query"**
5. In the response, find `"id"` — copy that value (it looks like `b!abc123...`)

> **For a SharePoint document library instead of personal OneDrive:**
> First run: `https://graph.microsoft.com/v1.0/sites?search=YOUR-SITE-NAME`
> Then run: `https://graph.microsoft.com/v1.0/sites/{site-id}/drives`
> Copy the `"id"` of the drive you want.

---

## PART 8 — Create Your `.env` File

The `.env` file stores all your secret credentials. The script reads from it automatically.

1. In your project folder, find the file called `.env.example`
2. Make a **copy** of it and rename the copy to `.env`
   (just `.env` — no `.example` at the end)
3. Open `.env` with Notepad (right-click → Open with → Notepad)
4. Fill in each value using what you collected above:

```
SMARTSHEET_ACCESS_TOKEN=paste-your-smartsheet-token-here
SMARTSHEET_SHEET_ID=paste-your-16-digit-sheet-id-here

GRAPH_CLIENT_ID=paste-your-azure-application-client-id-here
GRAPH_CLIENT_SECRET=paste-your-azure-client-secret-value-here
GRAPH_TENANT_ID=paste-your-azure-directory-tenant-id-here

SHAREPOINT_DRIVE_ID=paste-your-drive-id-here
SHAREPOINT_FILE_PATH=/Client Status/Nicole-Dodds-Status.xlsx

POLL_INTERVAL_SECONDS=300
LOCAL_OUTPUT_PATH=output/client_status.xlsx
```

**Notes:**
- `SHAREPOINT_FILE_PATH` is the folder path and filename inside your OneDrive/SharePoint.
  Change `/Client Status/Nicole-Dodds-Status.xlsx` to whatever folder and filename you want.
  The folder must already exist in your SharePoint/OneDrive.
- `POLL_INTERVAL_SECONDS=300` means every 5 minutes. Change to `60` for every minute, etc.
- Do **not** put quotes around the values
- Do **not** add spaces around the `=` sign

5. Save the file (Ctrl+S), then close Notepad

---

## PART 9 — Check Your Smartsheet Column Names

The script expects these exact column names in your Smartsheet:
- `Task Name`
- `Start Date`
- `End Date`
- `Notes`

**To check:**
1. Open your Smartsheet
2. Look at the column headers at the top of each column
3. If your columns have different names (e.g. "Task" instead of "Task Name"),
   open `smartsheet_client.py` in Notepad, find these lines near the top, and update them:

```python
COL_TASK_NAME  = "Task Name"
COL_START_DATE = "Start Date"
COL_END_DATE   = "End Date"
COL_NOTES      = "Notes"
```

Change the text in quotes to exactly match your column headers (case-sensitive).

---

## PART 10 — Run the Script

1. Go back to your Command Prompt (the one inside the project folder)
2. Make sure you see `(venv)` at the start of the line. If not, run:
   ```
   venv\Scripts\activate
   ```
3. Run the script:
   ```
   python main.py
   ```

You should see output like:
```
2026-04-20 10:00:00  INFO     __main__: Starting sync service. Sheet ID=1234567890, interval=300s
2026-04-20 10:00:01  INFO     smartsheet_client: Fetched 12 task rows from sheet 1234567890
2026-04-20 10:00:02  INFO     excel_writer: Wrote Client Status sheet to output/client_status.xlsx
2026-04-20 10:00:04  INFO     sharepoint_uploader: Uploaded output/client_status.xlsx via simple PUT → /Client Status/Nicole-Dodds-Status.xlsx
2026-04-20 10:00:04  INFO     __main__: ── Sync cycle complete ──
```

4. Check your SharePoint/OneDrive folder — the Excel file should be there!
5. The script will keep running and sync every 5 minutes. Leave the window open.
6. To stop it, press `Ctrl + C`

---

## PART 11 — Keep It Running Automatically (Optional)

If you want the sync to run automatically in the background without keeping a window open:

### Option A — Windows Task Scheduler
1. Press `Windows key`, search for **"Task Scheduler"**, open it
2. Click **"Create Basic Task"** on the right
3. Name it `Smartsheet Excel Sync`
4. Set trigger to **"When the computer starts"**
5. Set action to **"Start a program"**
6. Program/script: browse to `venv\Scripts\python.exe` inside your project folder
7. Add arguments: `main.py`
8. Start in: your full project folder path (e.g. `C:\Users\Nicole\Documents\smartsheet-sync`)
9. Finish. The script will now start automatically when you log in.

---

## Troubleshooting

| Error message | What to do |
|---|---|
| `Missing required env vars` | Open `.env` and make sure all values are filled in with no blank lines |
| `ApiError: 401` from Smartsheet | Your Smartsheet token is wrong or expired — regenerate it in Part 6 |
| `Column 'Task Name' not found` | Your Smartsheet column headers don't match — see Part 9 |
| `MSAL token acquisition failed` | Azure credentials are wrong — double-check client ID, secret, and tenant ID |
| `403 Forbidden` from Graph API | Admin consent wasn't granted — repeat step 7.4 |
| `404 Not Found` from Graph API | The folder in `SHAREPOINT_FILE_PATH` doesn't exist — create it in SharePoint first |
| `python is not recognized` | Python isn't on your PATH — reinstall Python and check "Add to PATH" |
| `(venv)` not showing | Run `venv\Scripts\activate` again before running the script |

---

## What the Excel File Looks Like

When the script runs, your SharePoint Excel file will have a **"Client Status"** tab with:

- A navy blue title header: **"Client Status Report"**
- A timestamp showing when it was last synced
- A bullet list of every task row:
  > • Project Kickoff — 1 Apr 2026 to 15 Apr 2026
  > • Design Phase — 16 Apr 2026 to 30 Apr 2026
  > • Build Phase — 1 May 2026 to 31 May 2026
- A yellow highlighted **FINAL END DATE** showing the latest end date across all rows

The file is fully overwritten each sync cycle, so it always reflects the current state of your Smartsheet.
