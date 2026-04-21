# Complete Guide: Sync Multiple Smartsheets to Excel Using Power Automate
## Scalable Version — Add New Sheets by Editing a Table, Not the Flow

---

## What You're Building

A flow that runs every 5 minutes and:
1. Reads a config table to find all your Smartsheets
2. Clears the old Excel data
3. Loops through every sheet automatically and writes bullets + a Final End Date

**To add a new Smartsheet later:** just add one row to a table. No flow editing needed.

---

## What Your Excel File Will Look Like

```
=== Project Alpha ===
• Kickoff — 1 Apr 2026 to 5 Apr 2026
• Design Phase — 6 Apr 2026 to 20 Apr 2026

=== Project Beta ===
• Discovery — 1 May 2026 to 7 May 2026
• Development — 8 May 2026 to 30 May 2026

FINAL END DATE: 30 May 2026
```

---

## Before You Begin

1. Go to **https://flow.microsoft.com** and sign in
2. Click **⚙️ gear icon** → **"View my licenses"**
3. You need **Power Automate Premium** or **Microsoft 365 Business Premium**
4. If you don't see that, look for a **"Start trial"** button — it gives you 90 days free

---

## STEP 1 — Note Your Smartsheet Column Positions

Because Power Automate's "Get a sheet" action returns columns by position number
(not by name), you need to know what order your columns appear in Smartsheet.

Columns are counted starting from **0** (not 1):

| Smartsheet column | Position number |
|---|---|
| 1st column (leftmost) | 0 |
| 2nd column | 1 |
| 3rd column | 2 |
| 4th column | 3 |

Open one of your Smartsheets and write down the positions for:

```
Task Name column is position: ______
Start Date column is position: ______
End Date column is position: ______
```

**Example for a typical project plan:**
```
Task Name  = position 0
Start Date = position 1
End Date   = position 2
```

> If all your sheets share the same column layout, you only need to do this once.

---

## STEP 2 — Get Your Smartsheet API Token

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture** (top-right) → **"Personal Settings"**
3. Click **"API Access"** in the left sidebar
4. Click **"Generate new access token"**
5. Name it `power-automate` → click **OK**
6. **Copy the token immediately** — paste it into Notepad or Notes. You cannot see it again.

---

## STEP 3 — Collect All Your Sheet IDs

For every Smartsheet you want to include:
1. Open the sheet in your browser
2. Copy the number from the URL:
   `https://app.smartsheet.com/sheets/`**`1234567890123456`**

Write them down with names:
```
Project Alpha  →  1111111111111111
Project Beta   →  2222222222222222
Project Gamma  →  3333333333333333
```

---

## STEP 4 — Create the Excel File on SharePoint or OneDrive

Your Excel file needs **two tabs** (sheets):
- **Sheet Config** — where you list your Smartsheets (the "control panel")
- **Client Status** — where the synced output appears

### 4.1 — Create the file

1. Go to your SharePoint or OneDrive in your browser
2. Navigate to where you want the file to live
3. Click **"+ New"** → **"Excel workbook"**
4. Click the filename at the top and rename it: `Client-Status`
5. Press **Enter**

### 4.2 — Set up the "Sheet Config" tab

This is where you list every Smartsheet you want to pull from.
To add a new sheet later, you just add a row here.

1. At the bottom, the tab currently says **"Sheet1"** — double-click it
2. Rename it: `Sheet Config`
3. Press **Enter**

**Add column headers:**
- Click cell **A1** → type: `SheetName`
- Press **Tab** → in **B1** type: `SheetID`
- Press **Enter**

**Add a placeholder row:**
- Click **A2** → type: `placeholder`
- Click **B2** → type: `0`

**Convert to a Table:**
1. Click cell **A1**
2. Click **Insert** tab → **Table**
3. Confirm range is `$A$1:$B$2`, **"My table has headers"** is ticked → click **OK**
4. Click the **Table Design** tab → rename from `Table1` to: `SheetConfig` → press **Enter**

**Delete the placeholder row:**
Right-click row 2 (the "placeholder" row) → **Delete** → **Table Rows**

**Now add your real Smartsheet entries:**
Click in cell **A2** and type your first project name.
Press **Tab** and type its Sheet ID.
Press **Enter** and continue for each sheet:

| SheetName | SheetID |
|---|---|
| Project Alpha | 1111111111111111 |
| Project Beta | 2222222222222222 |
| Project Gamma | 3333333333333333 |

### 4.3 — Add the "Client Status" tab

This is where the output gets written.

1. Click the **+** button at the bottom to add a new tab
2. Double-click the new tab and rename it: `Client Status`

**Add column headers:**
- Click **A1** → type: `Timing Steps`
- Press **Tab** → in **B1** type: `End Date Raw`
- Press **Enter**

**Add a placeholder row:**
- Click **A2** → type: `placeholder`
- Click **B2** → type: `2000-01-01`

**Convert to a Table:**
1. Click **A1** → **Insert** → **Table**
2. Confirm range, tick "My table has headers" → **OK**
3. **Table Design** → rename to: `StatusData` → **Enter**

**Delete the placeholder:**
Right-click row 2 → **Delete** → **Table Rows**

### 4.4 — Save

Press **Ctrl + S** (Windows) or **⌘ + S** (Mac). Close the tab.

---

## STEP 5 — Open Power Automate and Create the Flow

1. Go to **https://flow.microsoft.com**
2. Click **"My flows"** → **"+ New flow"** → **"Scheduled cloud flow"**
3. Fill in:
   - **Flow name:** `Client Status Sync`
   - **Repeat every:** `5` `Minute`
     *(change to `15` if you get a minimum interval error)*
4. Click **"Create"**

---

## STEP 6 — Add a Variable to Track the Final End Date

1. Click **"+ New step"**
2. Search: `Initialize variable` → click it
3. Fill in:
   - **Name:** `FinalEndDate`
   - **Type:** `String`
   - **Value:** `2000-01-01`

---

## STEP 7 — Clear Old Data From the Client Status Tab

### 7.1 — Get the existing rows

1. Click **"+ New step"**
2. Search: `Excel Online Business` → click **"Excel Online (Business)"**
3. Click **"List rows present in a table"**
4. Fill in:
   - **Location:** `SharePoint` or `OneDrive for Business`
   - **Document Library:** your library (usually "Documents")
   - **File:** click the folder icon → navigate to `Client-Status.xlsx`
   - **Table:** `StatusData`
5. Click **"Show advanced options"** → set **Top Count** to `5000`

### 7.2 — Delete each row

1. Click **"+ New step"** → search `Apply to each` → click it
2. Click in the output field → dynamic content panel → under
   **"List rows present in a table"** → click **"value"**
3. Rename this loop: click **"..."** on the loop → **"Rename"** → type `Delete Loop` → Enter

Inside the loop:

4. Click **"Add an action"** → **"Excel Online (Business)"** → **"Delete a row"**
5. Fill in:
   - **Location / Library / File:** same as above
   - **Table:** `StatusData`
   - **Key Column:** `Timing Steps`
   - **Key Value:** click the field → dynamic content →
     under "List rows present in a table" → click **"Timing Steps"**

---

## STEP 8 — Read Your Sheet Config Table

This step fetches the list of all Smartsheets you want to process.

1. Click **"+ New step"** (outside the delete loop)
2. **"Excel Online (Business)"** → **"List rows present in a table"**
3. Fill in:
   - **Location / Library / File:** same Excel file
   - **Table:** `SheetConfig`
4. Click **"Show advanced options"** → set **Top Count** to `500`

---

## STEP 9 — Loop Through Each Sheet in the Config

This is the main loop — it processes every row in your SheetConfig table,
pulling data from each Smartsheet one by one.

1. Click **"+ New step"** → **"Apply to each"**
2. Click in the output field → dynamic content →
   under **"List rows present in a table 2"** *(the SheetConfig one)* → click **"value"**
3. Rename this loop: **"..."** → **"Rename"** → type `Config Loop` → Enter

> **Everything from here until Step 10 goes INSIDE this Config Loop.**

---

### 9.1 — Write the Section Header to Excel

Inside the Config Loop:

1. Click **"Add an action"** → **"Excel Online (Business)"** → **"Add a row into a table"**
2. Fill in Location / Library / File / Table (StatusData) as before
3. Click in the **"Timing Steps"** field → click the **"Expression"** tab → type:

   ```
   concat('=== ', items('Config_Loop')?['SheetName'], ' ===')
   ```

4. Click **"OK"**
5. Click in the **"End Date Raw"** field → type: `2000-01-01`

---

### 9.2 — Get the Current Sheet From Smartsheet

Still inside the Config Loop:

1. Click **"Add an action"**
2. Search: `Smartsheet` → click **"Get a sheet"**
   *(click "Start trial" if prompted)*

**Connect your Smartsheet account (first time only):**
- Click **"Sign in"** → log in → click **"Allow"**

**Configure:**
3. Click in the **"Sheet Id"** field → click the **"Expression"** tab → type:

   ```
   items('Config_Loop')?['SheetID']
   ```

4. Click **"OK"**
5. Rename this action: **"..."** → **"Rename"** → type `Get Current Sheet` → Enter

---

### 9.3 — Loop Through the Rows of the Current Sheet

Still inside the Config Loop (after "Get Current Sheet"):

1. Click **"Add an action"** → search `Apply to each` → click it
2. Click in the output field → click the **"Expression"** tab → type:

   ```
   body('Get_Current_Sheet')?['rows']
   ```

3. Click **"OK"**
4. Rename this loop: **"..."** → **"Rename"** → type `Sheet Rows Loop` → Enter

> You now have a loop inside a loop:
> - Outer loop: Config Loop (one iteration per sheet)
> - Inner loop: Sheet Rows Loop (one iteration per row in that sheet)

---

### 9.4 — ACTION 1: Build the Bullet Text

Inside the **Sheet Rows Loop**:

1. Click **"Add an action"** → search `Compose` → click **"Compose"** (Data Operation)
2. Click in the **Inputs** field → click the **"Expression"** tab
3. Type the expression below, replacing `0`, `1`, `2` with your column positions from Step 1:

   ```
   concat('• ', items('Sheet_Rows_Loop')?['cells']?[0]?['displayValue'], ' — ', items('Sheet_Rows_Loop')?['cells']?[1]?['displayValue'], ' to ', items('Sheet_Rows_Loop')?['cells']?[2]?['displayValue'])
   ```

   **What to change:**
   - `?[0]` → your Task Name position
   - `?[1]` → your Start Date position
   - `?[2]` → your End Date position

4. Click **"OK"**

---

### 9.5 — ACTION 2: Write the Bullet Row to Excel

Still inside the Sheet Rows Loop:

1. Click **"Add an action"** → **"Excel Online (Business)"** → **"Add a row into a table"**
2. Fill in Location / Library / File / Table (StatusData) as before
3. Click in the **"Timing Steps"** field → **Dynamic content** → under **"Compose"** → click **"Outputs"**
4. Click in the **"End Date Raw"** field → **Expression** tab → type:

   ```
   items('Sheet_Rows_Loop')?['cells']?[2]?['displayValue']
   ```

   *(Replace `2` with your End Date column position)*

5. Click **"OK"**

---

### 9.6 — ACTION 3: Track the Latest End Date

Still inside the Sheet Rows Loop:

1. Click **"Add an action"** → search `Condition` → click **"Condition"**
2. Fill in:
   - **Left field** → **Expression** tab → type:
     ```
     items('Sheet_Rows_Loop')?['cells']?[2]?['displayValue']
     ```
   - **Middle dropdown:** change to **"is greater than"**
   - **Right field** → **Dynamic content** → click **"FinalEndDate"**

**In the "If yes" branch only:**

3. Click **"Add an action"** → search `Set variable` → click it
4. Fill in:
   - **Name:** `FinalEndDate`
   - **Value** → **Expression** tab → type:
     ```
     items('Sheet_Rows_Loop')?['cells']?[2]?['displayValue']
     ```

Leave the **"If no"** branch empty.

---

### 9.7 — Add a Spacer Row Between Sheets

This goes inside the Config Loop but **outside** the Sheet Rows Loop
(click the **"Add an action"** button at the Config Loop level, not the inner loop level):

1. Click **"Add an action"** (Config Loop level) → **"Excel Online (Business)"** → **"Add a row into a table"**
2. **Timing Steps:** type a single space: ` `
3. **End Date Raw:** `2000-01-01`

---

## STEP 10 — Write the Final End Date

This goes **outside** the Config Loop entirely (at the bottom of the flow):

1. Click **"+ New step"** (at the very bottom)
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. Fill in Location / Library / File / Table (StatusData) as before
4. Click in **"Timing Steps"** → type `FINAL END DATE: ` (with a space after the colon)
5. Click **"Add dynamic content"** → click **"FinalEndDate"**
6. Click in **"End Date Raw"** → **Dynamic content** → click **"FinalEndDate"**

---

## STEP 11 — Save the Flow

Click **"Save"** in the top-right.
Wait for the green **"Your flow was saved"** message.

If you see red error banners, read the message — it will tell you which field needs fixing.

---

## STEP 12 — Test the Flow

1. Click **"Test"** → **"Manually"** → **"Test"** → **"Run flow"** → **"Done"**
2. Watch each step turn green (takes 1–3 minutes)
3. Open `Client-Status.xlsx` on SharePoint → click the **"Client Status"** tab
4. You should see sections for each sheet with bullets and a Final End Date at the bottom

---

## STEP 13 — Turn the Flow On

1. Click the back arrow ← to go back to the flow overview
2. Confirm the toggle says **"On"** (green)
3. If it says Off, click it to turn it on

The flow now runs in Microsoft's cloud — your computer can be off.

---

## STEP 14 — Hide the "End Date Raw" Column (Optional)

1. Open `Client-Status.xlsx`
2. Click the **"B"** column header
3. Right-click → **"Hide"**

---

## How to Add a New Smartsheet Later

1. Open `Client-Status.xlsx`
2. Click the **"Sheet Config"** tab
3. Click the next empty row in the table
4. Type the project name in column A and its Sheet ID in column B
5. Save the file

That's it. The flow will pick it up automatically on the next run.

---

## Flow Structure Summary

```
[Recurrence — every 5 min]
[Initialize variable: FinalEndDate = 2000-01-01]
[List rows: StatusData]           ← get old output rows
[Delete Loop → Delete each row]   ← wipe old output
[List rows: SheetConfig]          ← get list of sheets
[Config Loop]                     ← one pass per sheet
    [Excel: Add header row "=== SheetName ==="]
    [Get Current Sheet]           ← fetch that sheet's data
    [Sheet Rows Loop]             ← one pass per task row
        [Compose: build bullet text]
        [Excel: Add bullet row]
        [Condition: update FinalEndDate if later]
    [Excel: Add spacer row]
[Excel: Add "FINAL END DATE" row]
```

---

## Troubleshooting

| What you see | What to do |
|---|---|
| Premium connector prompt | Click "Start trial" — 90 days free |
| "Invalid expression" error | Check for curly/smart quotes — must use straight single quotes `'` |
| Smartsheet step fails with 401 | Connection expired — click the action, click the connection name, sign in again |
| All cells appear blank in Excel | Column position numbers are wrong — recheck Step 1 and update the `?[0]`, `?[1]`, `?[2]` values |
| "Table not found" error | Check table names are exactly `SheetConfig` and `StatusData` (Table Design tab in Excel) |
| Header rows appear but no bullets | Check `body('Get_Current_Sheet')?['rows']` — the action name must match exactly (spaces become underscores) |
| A sheet's data is missing | Check that the Sheet ID in your SheetConfig table is correct — no spaces, correct digits |
| Final End Date shows `2000-01-01` | Your End Date column is empty in Smartsheet, or the column position number is wrong |
| Flow times out | Increase interval to 15 or 30 minutes |
| "value" appears twice in dynamic content panel | Power Automate lists both Excel steps — pick the one labelled "List rows present in a table 2" (the SheetConfig one) for the Config Loop |
