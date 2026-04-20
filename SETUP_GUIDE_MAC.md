# Setup Guide for Mac: Smartsheet → Excel → SharePoint Sync

This guide walks you through everything from scratch — no prior experience needed.
Work through each part in order.

---

## What This Does

Every 5 minutes, this script will:
1. Read your Smartsheet project plan (task names, start dates, end dates)
2. Build an Excel file with a bullet list of all timing steps and a highlighted Final End Date
3. Upload that Excel file automatically to a folder on your SharePoint or OneDrive

---

## PART 1 — Install Python

Your Mac may already have Python, but it's usually an old version. Install the current one:

1. Go to **https://www.python.org/downloads/mac-osx/**
2. Under "Stable Releases", click the link for the newest version
   (e.g. **"Python 3.12.x - macOS 64-bit universal2 installer"**)
3. Open the downloaded `.pkg` file
4. Click through the installer: Continue → Continue → Agree → Install
5. Enter your Mac password if prompted
6. When it finishes, click **Close**

**Verify it worked:**
1. Press **Command (⌘) + Space** to open Spotlight
2. Type `Terminal` and press **Enter** — a white or black window opens
3. Type the following and press Enter:
   ```
   python3 --version
   ```
4. You should see something like `Python 3.12.3`
5. If you get an error, restart your Mac and try again

> **Keep Terminal open** — you'll use it throughout this guide.

---

## PART 2 — Download the Project Files

### Option A — Download as ZIP (easiest, no Git needed)
1. Go to the GitHub repository in your browser
2. Make sure you are on the branch `claude/smartsheet-excel-sync-G2aS7`
   (use the branch dropdown near the top-left of the page — it may say "main")
3. Click the green **"Code"** button
4. Click **"Download ZIP"**
5. Open your **Downloads** folder and double-click the ZIP to unzip it
6. Move the unzipped folder somewhere permanent, like your **Documents** folder
   - Rename the folder to something simple, e.g. `smartsheet-sync`
   - Full path would be something like: `/Users/nicole/Documents/smartsheet-sync`

### Option B — Use Git (if you have it installed)
In Terminal:
```
cd ~/Documents
git clone <repository-url>
cd Nicole-Dodds
git checkout claude/smartsheet-excel-sync-G2aS7
```

---

## PART 3 — Open Terminal Inside the Project Folder

1. Open **Finder** and navigate to your project folder (e.g. `smartsheet-sync` in Documents)
2. Right-click (or two-finger click) on the folder
3. Click **"New Terminal at Folder"**
   - If you don't see this option: go to **System Settings → Privacy & Security → Full Disk Access**, or enable it via **Finder → Services menu**
   - Alternatively: open Terminal, type `cd ` (with a space), then drag and drop the folder into the Terminal window, then press Enter

4. Confirm you're in the right place by typing:
   ```
   ls
   ```
   You should see files like `main.py`, `requirements.txt`, `config.py`, etc.

---

## PART 4 — Set Up a Virtual Environment

A virtual environment is a self-contained box for this project's libraries.
It keeps things tidy and avoids conflicts with other software on your Mac.

In Terminal (make sure you're inside the project folder), run these two commands
**one at a time**, pressing Enter after each:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

After the second command, you'll see `(venv)` appear at the very start of the line, like:
```
(venv) nicole@Macbook smartsheet-sync %
```

That means it worked. **Every time you open a new Terminal window to run this script,
you must run `source venv/bin/activate` first.**

---

## PART 5 — Install Dependencies

With `(venv)` showing in your Terminal, run:

```
pip install -r requirements.txt
```

This downloads and installs all the libraries the script needs.
It will take 1–3 minutes. A lot of text will scroll by — that's normal.
Wait until you see the `(venv)` prompt return at the bottom.

---

## PART 6 — Get Your Smartsheet API Token

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture / avatar** in the top-right corner
3. Click **"Personal Settings"**
4. In the left sidebar, click **"API Access"**
5. Click **"Generate new access token"**
6. Give it a name like `excel-sync` and click **OK**
7. A long string of characters appears — this is your token
8. Click the **copy icon** next to it, or select all the text and copy it
9. **Paste it somewhere safe right now** (e.g. a note in Notes.app) — you cannot see it again

**Get your Sheet ID:**
1. Open the Smartsheet you want to sync in your browser
2. Look at the URL — it will look like:
   `https://app.smartsheet.com/sheets/1234567890123456`
3. The 16-digit number at the end is your Sheet ID — copy it

---

## PART 7 — Set Up Microsoft Azure (for SharePoint/OneDrive Upload)

This is the most involved part. It gives the script permission to upload files
to your SharePoint or OneDrive. You only do this once.

> **Note:** You need to be a Microsoft 365 admin, or ask your IT admin
> to complete steps 7.1–7.4 for you and hand you the three IDs.

### 7.1 — Register an App in Azure

1. Go to **https://portal.azure.com** in your browser
2. Sign in with your **Microsoft work account** (the one connected to your SharePoint)
3. In the search bar at the very top, type **"App registrations"** and click the result
4. Click **"+ New registration"** near the top-left
5. Fill in the form:
   - **Name:** `smartsheet-excel-sync`
   - **Supported account types:** Select **"Accounts in this organizational directory only"**
   - Leave **Redirect URI** completely blank
6. Click **"Register"** at the bottom

### 7.2 — Copy Your Two IDs

After registering, you land on the app's overview page. You'll see two important values:

- **Application (client) ID** — looks like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **Directory (tenant) ID** — also looks like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

Copy both values and save them in your notes.

### 7.3 — Create a Client Secret

1. In the left menu, click **"Certificates & secrets"**
2. Click **"+ New client secret"**
3. In the **Description** box, type `sync-secret`
4. Set **Expires** to **24 months**
5. Click **"Add"**
6. A new row appears in the table — under the **"Value"** column you'll see a long string
7. **Copy it immediately** and save it in your notes — it will be hidden after you leave this page

### 7.4 — Add API Permissions

1. In the left menu, click **"API permissions"**
2. Click **"+ Add a permission"**
3. A panel slides in — click **"Microsoft Graph"**
4. Click **"Application permissions"** (the second option, NOT "Delegated permissions")
5. In the search box, type `Files.ReadWrite`
6. Expand the **Files** section and check **"Files.ReadWrite.All"**
7. Click **"Add permissions"** at the bottom
8. Back on the permissions page, click the button **"Grant admin consent for [your org name]"**
9. Click **"Yes"** in the confirmation box
10. The status column should now show a green checkmark

### 7.5 — Find Your Drive ID

The Drive ID tells the script exactly which OneDrive or SharePoint document library to upload to.

1. Go to **https://developer.microsoft.com/en-us/graph/graph-explorer**
2. Sign in with the same Microsoft work account (click "Sign in to Graph Explorer" on the left)
3. In the query box at the top, you'll see a URL. Replace it with:
   ```
   https://graph.microsoft.com/v1.0/me/drives
   ```
4. Click the blue **"Run query"** button
5. In the response panel below, look for `"id"` — it looks like `b!AbCdEfGh...`
6. Copy that value — this is your **Drive ID**

> **If you want a SharePoint site library instead of personal OneDrive:**
>
> First, run this query (replace `your-site-name` with part of your SharePoint site name):
> ```
> https://graph.microsoft.com/v1.0/sites?search=your-site-name
> ```
> Copy the `"id"` from the result. Then run:
> ```
> https://graph.microsoft.com/v1.0/sites/{paste-site-id-here}/drives
> ```
> Find the drive named "Documents" (or whichever library you want) and copy its `"id"`.

---

## PART 8 — Create Your `.env` File

The `.env` file is where you store all your credentials. The script reads it automatically.

### Step 1 — Make a copy of the example file

In Terminal (inside your project folder with `(venv)` active):
```
cp .env.example .env
```

### Step 2 — Open the `.env` file in TextEdit

1. Open **Finder** and navigate to your project folder
2. Press **Command (⌘) + Shift + .** to show hidden files
   (files starting with `.` are hidden by default on Mac)
3. You should now see a file called `.env`
4. Right-click it → **Open With → TextEdit**

> If TextEdit opens it in rich text mode, go to **Format → Make Plain Text**

### Step 3 — Fill in your values

Replace each placeholder with the real values you collected:

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

**Important rules:**
- No spaces around the `=` sign
- No quotes around any values
- `SHAREPOINT_FILE_PATH` is the path **inside** your OneDrive/SharePoint drive.
  The folder (`Client Status` in this example) must already exist there.
  Change the path and filename to whatever you want.
- `POLL_INTERVAL_SECONDS=300` = every 5 minutes. Use `60` for every minute.

### Step 4 — Save and close

Press **Command (⌘) + S** to save, then close TextEdit.

Press **Command (⌘) + Shift + .** again in Finder to hide hidden files again (optional).

---

## PART 9 — Check Your Smartsheet Column Names

The script looks for these exact column header names in your Smartsheet:
- `Task Name`
- `Start Date`
- `End Date`
- `Notes`

**To check:**
1. Open your Smartsheet in the browser
2. Look at the column headers at the top of each column
3. If your column names are different (e.g. `Task` instead of `Task Name`),
   you need to update the script:

Open Terminal in your project folder and run:
```
open -e smartsheet_client.py
```

This opens the file in TextEdit. Near the top you'll see:
```python
COL_TASK_NAME  = "Task Name"
COL_START_DATE = "Start Date"
COL_END_DATE   = "End Date"
COL_NOTES      = "Notes"
```

Change the text inside the quotes to exactly match your column headers.
Spelling and capitalisation must match exactly.
Save (⌘+S) and close TextEdit.

---

## PART 10 — Run the Script

1. Go back to your Terminal window (the one inside the project folder)
2. Make sure `(venv)` is showing at the start of the line.
   If not, run:
   ```
   source venv/bin/activate
   ```
3. Run the script:
   ```
   python3 main.py
   ```

**What success looks like:**
```
2026-04-20 10:00:00  INFO     __main__: Starting sync service. Sheet ID=1234567890, interval=300s
2026-04-20 10:00:01  INFO     smartsheet_client: Fetched 12 task rows from sheet 1234567890
2026-04-20 10:00:02  INFO     excel_writer: Wrote Client Status sheet to output/client_status.xlsx
2026-04-20 10:00:04  INFO     sharepoint_uploader: Uploaded output/client_status.xlsx → /Client Status/Nicole-Dodds-Status.xlsx
2026-04-20 10:00:04  INFO     __main__: ── Sync cycle complete ──
```

4. Go to your SharePoint or OneDrive and open the `Client Status` folder
   — the Excel file should be there!
5. The script keeps running in the background and syncs every 5 minutes.
   **Leave the Terminal window open** while you want it to keep syncing.
6. To stop it, press **Control + C** in the Terminal window.

---

## PART 11 — Keep It Running Automatically (Optional)

If you want the sync to run every time you log in to your Mac,
without manually opening Terminal:

### Using Login Items (simplest method)

1. First, create a small shell script. In Terminal:
   ```
   nano ~/Documents/smartsheet-sync/run_sync.sh
   ```
2. Type (or paste) the following — replace the path with your actual project folder path:
   ```bash
   #!/bin/bash
   cd /Users/nicole/Documents/smartsheet-sync
   source venv/bin/activate
   python3 main.py >> logs/sync.log 2>&1
   ```
3. Press **Control + O**, then **Enter** to save. Press **Control + X** to exit.
4. Make it executable:
   ```
   chmod +x ~/Documents/smartsheet-sync/run_sync.sh
   ```
5. Go to **System Settings → General → Login Items**
6. Click the **+** button under "Open at Login"
7. Navigate to your project folder and select `run_sync.sh`
8. Click **Add**

The script will now run automatically each time you log in.
You can check `logs/sync.log` in your project folder to see what it's been doing.

---

## Troubleshooting

| Error message | What to do |
|---|---|
| `Missing required env vars` | Open `.env` — make sure every line is filled in and there are no typos |
| `command not found: python3` | Python didn't install correctly — redo Part 1 |
| `No module named 'smartsheet'` | You forgot to activate venv — run `source venv/bin/activate` then `pip install -r requirements.txt` |
| `ApiError: 401` (Smartsheet) | Your Smartsheet token is wrong or expired — regenerate it (Part 6) |
| `Column 'Task Name' not found` | Your column headers don't match — see Part 9 |
| `MSAL token acquisition failed` | Azure credentials are wrong — check client ID, secret, and tenant ID in `.env` |
| `403 Forbidden` (Graph API) | Admin consent wasn't granted for the Azure app — redo step 7.4 |
| `404 Not Found` (Graph API) | The folder in `SHAREPOINT_FILE_PATH` doesn't exist — create the folder in SharePoint/OneDrive first |
| `(venv)` not showing | Run `source venv/bin/activate` before running the script |
| File shows in OneDrive but not SharePoint | Double-check you used the correct Drive ID for the SharePoint library (not your personal OneDrive) |

---

## What the Excel File Looks Like

When the script runs successfully, your SharePoint/OneDrive Excel file will have
a **"Client Status"** tab with:

- A navy blue title bar: **"Client Status Report"**
- A line showing when it was last synced
- A bullet list of every task in your Smartsheet:
  > • Project Kickoff — 1 Apr 2026 to 15 Apr 2026
  > • Design Phase — 16 Apr 2026 to 30 Apr 2026
  > • Build Phase — 1 May 2026 to 31 May 2026
- A yellow-highlighted row at the bottom: **FINAL END DATE — 31 May 2026**

The file is completely rebuilt on every sync cycle, so it always matches
whatever is currently in your Smartsheet.
