# Complete Guide: Sync Multiple Smartsheets to Excel Using Power Automate

This is the full guide from start to finish — no other documents needed.
Every click is described. Take it one part at a time.

---

## What You're Building

A flow that runs automatically every 5 minutes and:
1. Clears the old data from your Excel file
2. Pulls rows from each of your Smartsheet project plans
3. Writes them into one Excel file on SharePoint/OneDrive, organized like this:

```
=== Project Alpha ===
• Kickoff Meeting — 1 Apr 2026 to 5 Apr 2026
• Design Phase — 6 Apr 2026 to 20 Apr 2026
• Build Phase — 21 Apr 2026 to 15 May 2026

=== Project Beta ===
• Discovery — 1 May 2026 to 7 May 2026
• Development — 8 May 2026 to 30 May 2026

=== Project Gamma ===
• Planning — 1 Jun 2026 to 14 Jun 2026

FINAL END DATE: 14 Jun 2026
```

---

## Before You Begin — Check Your Power Automate Plan

1. Go to **https://flow.microsoft.com** and sign in with your Microsoft work account
2. Click the **gear icon ⚙️** in the top-right corner → click **"View my licenses"**
3. If you see **Power Automate Premium** or **Microsoft 365 Business Premium** — you're all set
4. If you see a free or basic plan, look for a **"Try premium"** or **"Start trial"** button
   when you first use the Smartsheet connector — Power Automate offers a free 90-day trial

---

## What You'll Need Before Starting

- [ ] A **Microsoft work account** with access to SharePoint or OneDrive
- [ ] Access to **Power Automate** at flow.microsoft.com
- [ ] A **Smartsheet account** with the sheets you want to sync
- [ ] The **Sheet ID** for each Smartsheet (instructions below)
- [ ] About **1 hour** of uninterrupted time

---

## STEP 1 — Collect Your Smartsheet Sheet IDs

You need the ID of every Smartsheet sheet you want to include.

For **each** sheet:
1. Open the sheet in your browser
2. Look at the URL — it looks like:
   `https://app.smartsheet.com/sheets/1234567890123456`
3. Copy the 16-digit number at the end

Write them all down right now, with a label for each:

```
Sheet 1 name: _______________________   ID: ____________________
Sheet 2 name: _______________________   ID: ____________________
Sheet 3 name: _______________________   ID: ____________________
Sheet 4 name: _______________________   ID: ____________________
(add more as needed)
```

---

## STEP 2 — Get Your Smartsheet API Token

You only do this once.

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture** in the top-right corner
3. Click **"Personal Settings"**
4. Click **"API Access"** in the left sidebar
5. Click **"Generate new access token"**
6. Name it `power-automate-sync` → click **OK**
7. **Copy the token right now** — it's a long string of letters and numbers
8. Paste it into a note somewhere safe — you will NOT be able to see it again

---

## STEP 3 — Create the Excel File on SharePoint or OneDrive

Power Automate writes to Excel using a feature called a **Table**.
You need to set up the file and table before building the flow.

### 3.1 — Create the file

1. Go to your **SharePoint** site or **OneDrive** in your browser
2. Navigate to the folder where you want the status file to live
   (create a new folder if needed — e.g. call it "Client Status Reports")
3. Click **"+ New"** → **"Excel workbook"**
4. The file opens in your browser
5. Click the filename at the very top of the page (it says something like "Book") 
   and rename it to: `Client-Status`
6. Press **Enter**

### 3.2 — Rename the sheet tab

1. At the bottom of the Excel file, you'll see a tab called **"Sheet1"**
2. **Double-click** on it
3. Type: `Client Status`
4. Press **Enter**

### 3.3 — Set up the column headers

Click on cell **A1** and type:
```
Timing Steps
```
Press **Tab** to move to cell B1 and type:
```
End Date Raw
```
Press **Enter**

> The "End Date Raw" column stores just the date so the flow can find
> the latest one. You can hide this column later so it doesn't show to clients.

### 3.4 — Add a placeholder row

Click on cell **A2** and type: `placeholder`
Click on cell **B2** and type: `2000-01-01`

### 3.5 — Convert to a Table

1. Click back on cell **A1**
2. Click the **"Insert"** tab in the ribbon at the top
3. Click **"Table"**
4. A small dialog box appears showing `=$A$1:$B$2`
5. Make sure **"My table has headers"** is ticked/checked
6. Click **"OK"**

The cells should now have a blue striped style — that means it's a Table.

### 3.6 — Name the Table

1. Click anywhere inside the table
2. Click the **"Table Design"** tab that appears in the top ribbon
   (you may need to scroll right to find it, or it may appear automatically)
3. On the far left, find the box that says **"Table1"**
4. Click it, delete "Table1", and type: `StatusData`
5. Press **Enter**

### 3.7 — Delete the placeholder row

1. Click on cell **A2** (the row with "placeholder")
2. Right-click → **"Delete"** → **"Table Rows"**

### 3.8 — Save the file

Press **Ctrl + S** (Windows) or **⌘ + S** (Mac).
You can now close this browser tab — Power Automate will write to the file automatically.

---

## STEP 4 — Open Power Automate and Start a New Flow

1. Go to **https://flow.microsoft.com**
2. Sign in with your Microsoft work account
3. In the left menu, click **"My flows"**
4. Click **"+ New flow"** near the top of the page
5. Click **"Scheduled cloud flow"**

A dialog box appears:

- **Flow name:** Type `Client Status Sync`
- **Starting:** Leave as today
- **Repeat every:** Type `5` and choose `Minute` from the dropdown
  > If you get an error about interval limits, change to `15` minutes
- Click **"Create"**

You're now inside the flow editor. You'll see one box at the top labelled **"Recurrence"**.

---

## STEP 5 — Add a Variable to Track the Final End Date

This creates a "container" that stores the latest end date as the flow processes each sheet.

1. Click **"+ New step"** below the Recurrence box
2. In the search bar, type: `Initialize variable`
3. Click **"Initialize variable"** (listed under the Variables connector)
4. Fill in:
   - **Name:** `FinalEndDate`
   - **Type:** `String`
   - **Value:** `2000-01-01`
     > This starting value is intentionally old so any real date will be larger

---

## STEP 6 — Clear Old Data From Excel

Every time the flow runs, it needs to wipe the old rows before writing fresh ones.
This takes two steps: first get the old rows, then delete them one by one.

### 6.1 — Get the existing rows

1. Click **"+ New step"**
2. Search for: `Excel Online Business`
3. Click **"Excel Online (Business)"**
4. Click **"List rows present in a table"**
5. Fill in:
   - **Location:** Choose `SharePoint` or `OneDrive for Business`
     (whichever is where your Excel file lives)
   - **Document Library:** Select your library (usually "Documents")
   - **File:** Click the folder icon and navigate to your `Client-Status.xlsx` file
   - **Table:** Select `StatusData`
6. Click **"Show advanced options"** at the bottom of this step
7. Find **"Filter Query"** — leave it blank
8. Find **"Top Count"** — type `5000`
   > This makes sure it fetches all rows, not just the default limit

### 6.2 — Delete each row

1. Click **"+ New step"**
2. Search for: `Apply to each`
3. Click **"Apply to each"** (listed under Control)
4. Click inside the **"Select an output from previous steps"** field
5. The dynamic content panel opens on the right side
6. Under **"List rows present in a table"**, click **"value"**

You're now inside the loop. Add a delete action:

7. Inside the loop box, click **"Add an action"**
8. Search for: `Excel Online Business`
9. Click **"Excel Online (Business)"** → **"Delete a row"**
10. Fill in:
    - **Location:** Same as before
    - **Document Library:** Same as before
    - **File:** Same file
    - **Table:** `StatusData`
    - **Key Column:** `Timing Steps`
    - **Key Value:** Click in the field → in the dynamic content panel,
      look under **"List rows present in a table"** → click **"Timing Steps"**

> This loops through every row in the Excel table and deletes it,
> leaving a clean empty table ready for fresh data.

---

## STEP 7 — Add Your First Smartsheet (Sheet 1)

This is the main pattern. You'll repeat it for every sheet you have.

### 7.1 — Write the section header to Excel

1. Click **"+ New step"** (outside and below the delete loop)
2. Search for: `Excel Online Business`
3. Click **"Excel Online (Business)"** → **"Add a row into a table"**
4. Fill in:
   - **Location, Document Library, File, Table:** same as before
   - **Timing Steps field:** Type the name of your first project, like:
     ```
     === Project Alpha ===
     ```
   - **End Date Raw field:** Type:
     ```
     2000-01-01
     ```
     > Header rows get a dummy date so they don't affect the Final End Date calculation

### 7.2 — Get the rows from your first Smartsheet

1. Click **"+ New step"**
2. Search for: `Smartsheet`
3. Click the **Smartsheet** connector
   > If a prompt appears about a premium trial, click **"Start trial"** to continue
4. Click **"List rows in a sheet"**

**Connect your Smartsheet account:**
A sign-in panel appears:
- Click **"Sign in"**
- Enter your Smartsheet email and password
- Click **"Allow"** to grant access
- You're returned to the flow

**Configure the action:**
- **Sheet:** Click the dropdown and select your first sheet by name
  > If it doesn't appear, click **"Enter custom value"** and paste your Sheet 1 ID
- Leave all other settings as default

### 7.3 — Loop through Sheet 1's rows

1. Click **"+ New step"**
2. Search for: `Apply to each`
3. Click **"Apply to each"**
4. Click in the **"Select an output from previous steps"** field
5. In the dynamic content panel, look under **"List rows in a sheet"** (your Sheet 1 action)
   and click **"rows"**

You're now inside the loop. Add three actions inside it:

---

**ACTION 1 — Write the bullet row to Excel**

6. Inside the loop, click **"Add an action"**
7. Search for: `Excel Online Business`
8. Click **"Excel Online (Business)"** → **"Add a row into a table"**
9. Fill in Location, Library, File, Table as before
10. Click in the **"Timing Steps"** field
11. Type: `• ` (bullet point, then a space)
12. Click the **"Add dynamic content"** link that appears below the field
13. In the panel, look under your Sheet 1 **"List rows in a sheet"** section
    and click **"Task Name"**
    > You'll now see `• ` followed by a blue token for Task Name
14. Click back in the field after the Task Name token and type: ` — `
15. Click **"Add dynamic content"** again → click **"Start Date"**
16. Type: ` to `
17. Click **"Add dynamic content"** again → click **"End Date"**

The field should now look like:
```
• [Task Name] — [Start Date] to [End Date]
```
(where the square bracket items are blue tokens)

18. Click in the **"End Date Raw"** field
19. Click **"Add dynamic content"** → click **"End Date"**
    > This stores the raw date so we can find the overall maximum later

---

**ACTION 2 — Check if this row's end date is the latest so far**

20. Inside the loop, click **"Add an action"**
21. Search for: `Condition`
22. Click **"Condition"** (listed under Control)

Fill in the condition:
- **First field (left):** Click it → dynamic content → click **"End Date"**
  (from your Sheet 1 Smartsheet action)
- **Middle dropdown:** Change to **"is greater than"**
- **Third field (right):** Click it → dynamic content → click **"FinalEndDate"**
  (the variable you created in Step 5)

**In the "If yes" branch:**
23. Click **"Add an action"**
24. Search for: `Set variable`
25. Click **"Set variable"**
26. Fill in:
    - **Name:** `FinalEndDate`
    - **Value:** Click in the field → dynamic content → click **"End Date"**
      (from your Sheet 1 Smartsheet action)

**Leave the "If no" branch empty.**

---

That's the complete block for Sheet 1.
Your flow now looks like this:

```
[Recurrence]
[Initialize variable: FinalEndDate]
[List rows from Excel]
[Apply to each → Delete row]
[Add row: === Project Alpha ===]
[List rows from Smartsheet: Sheet 1]
[Apply to each → Sheet 1 rows]
    [Add row to Excel with bullet text]
    [Condition: if End Date > FinalEndDate]
        [Yes: Set FinalEndDate = End Date]
```

---

## STEP 8 — Add Your Second Smartsheet (Sheet 2)

Repeat this pattern outside and below the Sheet 1 loop.

### 8.1 — Add a blank spacer row

1. Click **"+ New step"** (outside the Sheet 1 loop)
2. Search for: `Excel Online Business`
3. Click **"Excel Online (Business)"** → **"Add a row into a table"**
4. Fill in the same Location/Library/File/Table
5. **Timing Steps field:** press the spacebar once (just a single space)
6. **End Date Raw field:** type `2000-01-01`

### 8.2 — Write the Sheet 2 header

1. Click **"+ New step"**
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. **Timing Steps:** type:
   ```
   === Project Beta ===
   ```
4. **End Date Raw:** `2000-01-01`

### 8.3 — Get Sheet 2's rows from Smartsheet

1. Click **"+ New step"**
2. Search for: `Smartsheet`
3. Click **"List rows in a sheet"**
4. The connection is already set up — just choose your second sheet from the dropdown
   (or paste Sheet 2's ID)

### 8.4 — Loop through Sheet 2's rows

1. Click **"+ New step"** → **"Apply to each"**
2. In the output field, select **"rows"** from your **Sheet 2** Smartsheet action
   > Important: make sure you pick from the Sheet 2 action, not Sheet 1.
   > Both will appear in the list — look at the label carefully.

Inside the loop, repeat the same three actions as Sheet 1:

**ACTION 1 — Write the bullet row:**
- Same as Step 7.3 Action 1
- When adding dynamic content for Task Name, Start Date, End Date:
  make sure you're selecting from the **Sheet 2** "List rows" section in the panel,
  not Sheet 1 — they'll both appear, so check the label

**ACTION 2 — Update the Final End Date variable:**
- Same Condition setup as Step 7.3 Action 2
- Left field: End Date from **Sheet 2**
- Right field: FinalEndDate variable
- If yes: Set FinalEndDate = End Date from **Sheet 2**

---

## STEP 9 — Add More Sheets (Repeat for Sheet 3, 4, 5…)

For every additional sheet, repeat Step 8 exactly:

1. Spacer row (single space, date `2000-01-01`)
2. Header row (`=== Project Name ===`, date `2000-01-01`)
3. Smartsheet "List rows" action (select the next sheet)
4. "Apply to each" loop with:
   - Excel "Add a row" action (bullet text using **this sheet's** dynamic content)
   - Condition (comparing **this sheet's** End Date to FinalEndDate variable)

> Each sheet takes about 5 minutes to add once you've done it once.
> The only thing that changes each time is which sheet you select and
> which dynamic content tokens you pick inside the loop.

---

## STEP 10 — Write the Final End Date

After all your sheet blocks, add the overall final end date row.

1. Click **"+ New step"** (at the very bottom, outside all loops)
2. Click **"Excel Online (Business)"** → **"Add a row into a table"**
3. Fill in Location/Library/File/Table as before
4. Click in the **"Timing Steps"** field and type:
   ```
   FINAL END DATE: 
   ```
   (include the space after the colon)
5. Click **"Add dynamic content"** → click **"FinalEndDate"**
   (the variable — it's listed under the Variables section)
6. **End Date Raw field:** Click it → dynamic content → click **"FinalEndDate"**

---

## STEP 11 — Save the Flow

Click the **"Save"** button in the top-right corner of the screen.
Wait for the confirmation message: **"Your flow was saved"**

If you see any red error banners, read the message — it usually tells you
exactly which field is missing something.

---

## STEP 12 — Test the Flow

1. Click **"Test"** in the top-right corner
2. Select **"Manually"**
3. Click **"Test"**
4. Click **"Run flow"**
5. Click **"Done"**

You'll be taken to a screen showing each step of the flow running in real time.
Each step will show a green tick when it completes, or a red X if it fails.

**The flow will take 1–3 minutes to finish** — it has a lot of steps.
Wait for it to complete before checking Excel.

**If everything is green:**
1. Go to your SharePoint/OneDrive
2. Open `Client-Status.xlsx`
3. Click the **"Client Status"** tab
4. You should see all your sheets' data organized with headers and bullets
5. The last row should say `FINAL END DATE: ` followed by the latest date

**If you see a red X on any step:**
1. Click the red step to expand it
2. Read the error message
3. Check the Troubleshooting section at the bottom of this guide

---

## STEP 13 — Confirm the Flow is Turned On

1. Click the back arrow (←) to return to the flow's main page
2. You should see a green **"On"** badge next to the flow name
3. If it says **"Off"**, click the toggle to turn it on

The flow will now run automatically every 5 minutes (or whatever interval you set).
You don't need to do anything else — it runs in the background even when your
computer is off, because it runs in Microsoft's cloud.

---

## STEP 14 — Hide the "End Date Raw" Column in Excel (Optional)

The "End Date Raw" column is there to help the flow track dates, but you
probably don't want clients to see it.

1. Open your `Client-Status.xlsx` file
2. Click the **"B"** column header to select the whole column
3. Right-click → **"Hide"**

The column is now hidden but still works. The flow will continue writing to it.

---

## How to Add a New Sheet Later

When you start a new project and want to add its Smartsheet to the sync:

1. Get the new Sheet ID from the Smartsheet URL
2. Go to **flow.microsoft.com** → **My flows** → click your flow → click **Edit**
3. Scroll to the bottom of the flow (before the Final End Date step)
4. Add the same pattern as Step 8:
   - Spacer row
   - Header row with the new project name
   - Smartsheet "List rows" action pointing to the new sheet
   - "Apply to each" loop with the Excel write and date condition actions
5. Click **Save**

---

## Troubleshooting

| What you see | What to do |
|---|---|
| Premium connector prompt | Click **"Start trial"** — 90 days free |
| Red X on the Smartsheet step | Your Smartsheet token may have expired — go to the step, click the connection name, sign in again |
| Red X on the Excel step — "Table not found" | Double-check the table is named exactly `StatusData` in your Excel file (Table Design tab) |
| Red X on the Excel step — "File not found" | Click the file field in that step and re-navigate to your file |
| Flow runs but Excel shows nothing | The delete loop ran but the write loops failed — click each red step for details |
| Dynamic content shows Task Name from wrong sheet | Inside the loop, when adding dynamic content, check the section header in the panel to make sure you're picking from the right sheet's action |
| "Apply to each" picks up wrong rows | Each "Apply to each" must have its own output — make sure you selected **"rows"** from the correct Smartsheet step |
| Final End Date shows `2000-01-01` | All your rows have empty End Date fields — fill in end dates in Smartsheet, then re-run |
| Flow times out before finishing | Increase the interval to 15 or 30 minutes, or reduce the number of rows being processed |
| Dates show in wrong format (e.g. US vs UK) | Smartsheet returns dates as `YYYY-MM-DD` — you can leave as-is or reformat in Excel using a custom date format on the column |
| Flow ran but I don't see a new section for one sheet | Check that the "Apply to each" loop for that sheet selected "rows" from the right Smartsheet step |

---

## Quick Reference: The Pattern for Each Sheet

Every sheet follows the same 4-step pattern:

```
① Add row to Excel: "=== Sheet Name ===" (with date 2000-01-01)

② Smartsheet: List rows in a sheet
   → Select this sheet's ID

③ Apply to each: rows (from ② above)
   → Add row to Excel:
        Timing Steps: • [Task Name] — [Start Date] to [End Date]
        End Date Raw: [End Date]
   → Condition: [End Date] is greater than [FinalEndDate variable]
        If Yes: Set variable FinalEndDate = [End Date]

④ (Add spacer row before the next sheet)
```

Print this pattern out and keep it next to you while building the flow.
Each new sheet is just this pattern repeated, pointed at a different sheet.
