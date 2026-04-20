# Free Options: Smartsheet → Excel Sync (No Premium Connector Needed)

Since Power Automate's Smartsheet connector requires a premium license,
here are your real free alternatives — honest pros and cons included.

---

## Overview of Options

| Option | Automated? | Coding? | Cost | Best for |
|---|---|---|---|---|
| **A — Make.com** | Yes (every 15 min) | None | Free tier available | Best free automated option |
| **B — Smartsheet Publish** | Sort of | None | Free | Sharing a live view, not pushing to SharePoint |
| **C — Manual Export** | No | None | Free | Occasional updates only |
| **D — Python Script** | Yes (every 5 min) | Setup only | Free | Most reliable, already built |

---

## OPTION A — Make.com (Recommended Free Automated Option)

Make.com (formerly Integromat) is a tool very similar to Power Automate,
but its Smartsheet connector is **completely free** — no premium needed.

### What the free tier gives you
- Runs every **15 minutes** minimum
- **1,000 operations per month** (roughly 2–3 syncs per hour if your sheet has ~10 rows)
- If you need more, the paid plan is $9/month for 10,000 operations and 1-minute intervals

---

### PART A1 — Create a Make.com Account

1. Go to **https://www.make.com**
2. Click **"Get started free"**
3. Sign up with your email address (or sign in with Google)
4. Verify your email if prompted
5. You'll land on the Make.com dashboard

---

### PART A2 — Prepare Your Excel File on SharePoint/OneDrive

Same as before — Make.com writes to Excel using a Table.
If you already did this step from the Power Automate guide, skip ahead to A3.

1. Go to your **SharePoint** or **OneDrive** in your browser
2. Go to the folder where you want the file
3. Click **"+ New"** → **"Excel workbook"**
4. Rename the file to `Nicole-Dodds-Status`
5. At the bottom, double-click the **"Sheet1"** tab and rename it `Client Status`
6. Click on cell **A1** and type: `Timing Steps`
7. Click on cell **A2** and type: `placeholder`
8. Click on **A1** again → click **"Insert"** tab → click **"Table"**
9. Make sure **"My table has headers"** is checked → click **"OK"**
10. Click anywhere in the table → click **"Table Design"** tab →
    rename `Table1` to `TimingSteps` → press Enter
11. Right-click the "placeholder" row → **Delete → Table Rows**
12. Save the file (Ctrl/⌘ + S)

---

### PART A3 — Get Your Smartsheet API Token

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture** (top-right)
3. Click **"Personal Settings"**
4. Click **"API Access"** in the left menu
5. Click **"Generate new access token"**
6. Name it `make-sync` → click **OK**
7. **Copy the token immediately** and save it somewhere safe

Also get your **Sheet ID**:
1. Open your Smartsheet in the browser
2. Copy the 16-digit number from the URL:
   `https://app.smartsheet.com/sheets/`**`1234567890123456`**

---

### PART A4 — Create a New Scenario in Make.com

A "Scenario" in Make.com is the same idea as a "Flow" in Power Automate —
it's a set of steps that run automatically.

1. On the Make.com dashboard, click **"Create a new scenario"** (big + button)
2. You'll see a blank canvas with a large circle and a **+** button in the middle
3. Click the **+** button

---

### PART A5 — Set Up the Smartsheet Trigger

1. A panel opens with a search bar — type `Smartsheet`
2. Click the **Smartsheet** icon
3. A list of actions appears — click **"Watch Rows"**
   > "Watch Rows" will check for any new or changed rows on your schedule.
   > This is the trigger that starts your scenario.

4. A connection setup box appears — click **"Add"**
5. In the new window:
   - **Connection name:** type `My Smartsheet`
   - **API Key:** paste your Smartsheet API token from Part A3
6. Click **"Save"**
7. Now configure the trigger:
   - **Sheet:** Click the dropdown and select your sheet
     (or type your Sheet ID if it doesn't appear)
   - **Maximum number of returned rows:** type `500`
     (or however many rows your sheet might have)
   - **Column names:** leave as default
8. Click **"OK"**

---

### PART A6 — Add a Microsoft OneDrive / Excel Action

Now tell Make.com to write the data to your Excel file.

Because Make.com writes rows one at a time, you'll set up two actions:
one to clear old data, one to add new rows.

#### Step A6a — Clear the old Excel table rows

1. Click the **+** button to the right of your Smartsheet trigger bubble
2. Search for `Excel 365`  
   > Make.com may list this as "Microsoft 365 Excel" or "Excel Online"
3. Click it → click **"Delete a Row"**

4. A connection box appears — click **"Add"**
5. Click **"Sign in with Microsoft"** and sign in with your Microsoft work account
6. Allow the permissions requested
7. Now configure:
   - **Workbook:** Click the folder icon → navigate to your `Nicole-Dodds-Status.xlsx` file
   - **Worksheet:** Select `Client Status`
   - **Table:** Select `TimingSteps`
   - **Row ID:** For now, leave this — we'll come back to it

> **Note:** Clearing all rows before rewriting requires a small workaround.
> See the "Clearing Old Data" tip below.

---

### PART A7 — The Simpler Approach: Overwrite, Don't Delete

Deleting every row then rewriting is complex in Make.com for a beginner.
Here's the simpler approach: **update existing rows in place**.

Instead of Delete + Add, you'll use **"Add a Row"** and set the scenario
to run on a schedule that clears and rewrites only when something changes.

Here's the cleanest beginner-friendly structure:

#### Step 1 — Remove the Delete action (if you added it)
Right-click the Excel bubble → click **"Remove module"**

#### Step 2 — Add an "Iterator" to loop through Smartsheet rows

1. Click the **+** after the Smartsheet trigger
2. Search for `Flow control`
3. Click **"Iterator"**
4. In the **Array** field, click and select **"Rows"** from the Smartsheet data on the right panel
5. Click **"OK"**

The Iterator means Make.com will now process one Smartsheet row at a time.

#### Step 3 — Add the Excel "Add a Row" action

1. Click **+** after the Iterator
2. Search for `Microsoft 365 Excel`
3. Click **"Add a Row"**
4. Configure:
   - **Workbook:** navigate to your `Nicole-Dodds-Status.xlsx`
   - **Worksheet:** `Client Status`
   - **Table:** `TimingSteps`
5. In the **"Timing Steps"** field that appears, click it and type:

   ```
   • {{cells.Task Name}} — {{cells.Start Date}} to {{cells.End Date}}
   ```

   > Replace `Task Name`, `Start Date`, `End Date` with your exact Smartsheet column names.
   > The `{{` and `}}` are Make.com's way of inserting live data.
   > Click the variable picker on the right to find your column names if unsure.

6. Click **"OK"**

---

### PART A8 — Set the Schedule

1. At the top-left of the scenario canvas, find the clock icon that says **"Scheduling"**
2. Click it
3. Set:
   - **Run scenario:** Every
   - **15 minutes** (minimum on free plan; use `1 hour` to save operations)
4. Click **"OK"**

---

### PART A9 — Test the Scenario

1. Click the **"Run once"** button at the bottom of the screen
2. Watch the bubbles light up — green means success, red means error
3. Click any bubble to see exactly what data passed through it
4. Go to your Excel file on SharePoint/OneDrive and check if rows appeared

---

### PART A10 — Turn On the Scenario

1. At the bottom-left of the screen, there's an **ON/OFF toggle**
2. Click it to turn it **ON** (it turns blue)
3. Make.com will now run your scenario automatically on the schedule you set

---

## OPTION B — Smartsheet's Built-In Publish Feature

This is the **simplest option** — no account setup, no flow building.
The tradeoff: it doesn't push a file to SharePoint. Instead, it creates a
**live link** that always downloads the latest version of your sheet as Excel.

### What it does
Anyone who clicks the link gets the current sheet as a downloaded `.xlsx` file.
You (or your clients) would open this link whenever they want the latest version.
It won't automatically appear in SharePoint, but it could replace the need for that.

### How to set it up

1. Open your Smartsheet in the browser
2. Click **File** in the top menu
3. Click **"Publish..."**
4. A dialog box opens — find the section **"Excel Format"** (or "Export as Excel")
5. Toggle it **On**
6. Copy the link that appears
7. Share that link with anyone who needs it

> Clicking the link always downloads the current version of the sheet as Excel.
> No login required for the recipient (if you choose "Anyone with the link").

### Limitation
This doesn't format the data as a "Client Status" document with bullets.
It's the raw Smartsheet data in Excel format.

---

## OPTION C — Manual Export From Smartsheet

The simplest possible option. No setup. Just do it whenever you need to update.

### How to export

1. Open your Smartsheet
2. Click **File** in the top menu
3. Click **"Export"**
4. Click **"Export to Excel"**
5. A `.xlsx` file downloads to your computer
6. Open it, copy the relevant rows, paste them into your client status document
7. Upload the updated file to SharePoint manually

### When this makes sense
If you only update the client status document once a week or less,
manual export may be faster than setting up any automation.

---

## OPTION D — The Python Script (Already Built)

The Python script in this repository does everything automatically —
reads Smartsheet, builds the formatted bullet list, uploads to SharePoint —
with no ongoing subscription cost. You set it up once and it runs forever.

### The only requirement
You need a computer (Mac or PC) that is turned on and connected to the internet
while you want it to sync. If the computer sleeps or shuts down, syncing pauses
until you run the script again.

### To use it
Follow the step-by-step instructions in:
- **`SETUP_GUIDE_MAC.md`** — if you're on a Mac
- **`SETUP_GUIDE.md`** — if you're on a PC

The Azure setup in those guides (Part 7) is the hardest part.
If you can't get Azure permissions, the script can still run and
write the Excel file locally — you'd just copy it to SharePoint manually,
or ask IT to set up the Azure app for you.

---

## Which Option Should You Choose?

```
Do you want syncing to happen automatically (no clicking)?
│
├── YES
│   ├── Are you comfortable running a script once on your Mac?
│   │   ├── YES → Use Option D (Python script) — most reliable, already built
│   │   └── NO  → Use Option A (Make.com) — visual, no coding, free tier
│   │
│   └── How often does your Smartsheet actually change?
│       ├── Rarely (weekly) → Option C (manual export) is honestly fine
│       └── Often (daily)   → Option A or D
│
└── NO — I just need people to see the latest data
    └── Use Option B (Smartsheet Publish link) — zero setup
```

---

## Recommendation

For most people in your situation, the best path is:

1. **Try Option A (Make.com) first** — it's free, visual, and no coding.
   If Make.com's free tier runs out of operations, upgrade to $9/month or switch to the Python script.

2. **Fall back to Option D (Python script)** if Make.com feels too complex —
   the hardest part (the Azure setup) can be skipped if you ask your IT admin
   to just create the Azure app and hand you the three IDs.

3. **Use Option B or C** if this doesn't need to be fully automated —
   many people find that a quick manual export once or twice a week is faster
   than troubleshooting automation.
