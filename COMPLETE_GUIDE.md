# Complete Guide: Sync Multiple Smartsheets to Excel Using Power Automate

This is the full guide from start to finish — one document, every click described.

---

## What You're Building

A flow that runs automatically every 5 minutes and:
1. Clears the old data from your Excel file
2. Pulls rows from each of your Smartsheet project plans
3. Writes them all into one Excel file on SharePoint/OneDrive, like this:

```
=== Project Alpha ===
• Kickoff Meeting — 1 Apr 2026 to 5 Apr 2026
• Design Phase — 6 Apr 2026 to 20 Apr 2026

=== Project Beta ===
• Discovery — 1 May 2026 to 7 May 2026
• Development — 8 May 2026 to 30 May 2026

FINAL END DATE: 30 May 2026
```

---

## Before You Begin — Check Your Power Automate Plan

1. Go to **https://flow.microsoft.com** and sign in with your Microsoft work account
2. Click the **gear icon ⚙️** in the top-right → click **"View my licenses"**
3. If you see **Power Automate Premium** or **Microsoft 365 Business Premium** — you're good
4. If you're on a basic plan, Power Automate will offer a **free 90-day trial** when you
   first try to use the Smartsheet connector — click through it to continue

---

## What You'll Need Before Starting

- [ ] Microsoft work account with SharePoint or OneDrive access
- [ ] Access to Power Automate at flow.microsoft.com
- [ ] A Smartsheet account
- [ ] The **Sheet ID** for each Smartsheet you want to include (instructions in Step 1)
- [ ] About **1 hour** of uninterrupted time

---

## STEP 1 — Collect Your Smartsheet Sheet IDs

For **each** sheet you want to include:
1. Open the sheet in your browser
2. Look at the URL: `https://app.smartsheet.com/sheets/`**`1234567890123456`**
3. Copy the 16-digit number at the end

Write them all down:
```
Sheet 1 name: _______________________   ID: ____________________
Sheet 2 name: _______________________   ID: ____________________
Sheet 3 name: _______________________   ID: ____________________
(add more as needed)
```

---

## STEP 2 — Note Your Smartsheet Column Order

Because you'll use **"Get a sheet"** (instead of "List rows"), you need to know
what position each column is in. Power Automate counts columns starting from **0**.

1. Open any one of your Smartsheets
2. Look at the columns left to right and write them down:

```
Position 0 (1st column): _______________   ← usually the task/row name
Position 1 (2nd column): _______________
Position 2 (3rd column): _______________
Position 3 (4th column): _______________
```

**Example — a typical project plan:**
```
Position 0: Task Name
Position 1: Start Date
Position 2: End Date
Position 3: Notes
```

You'll need the position numbers for Task Name, Start Date, and End Date.
Keep this list next to you while building the flow.

> If your sheets have the same column layout, this applies to all of them.
> If they differ, note the positions for each sheet separately.

---

## STEP 3 — Get Your Smartsheet API Token

1. Log in to **https://app.smartsheet.com**
2. Click your **profile picture** top-right → **"Personal Settings"**
3. Click **"API Access"** in the left sidebar
4. Click **"Generate new access token"**
5. Name it `power-automate` → click **OK**
6. **Copy the token immediately** and paste it somewhere safe (Notepad, Notes app)
   — you cannot see it again after you leave this page

---

## STEP 4 — Create the Excel File on SharePoint or OneDrive

### 4.1 — Create the file

1. Go to your **SharePoint** site or **OneDrive** in your browser
2. Navigate to the folder where you want the file (create a folder if needed)
3. Click **"+ New"** → **"Excel workbook"**
4. Click the filename at the top and rename it: `Client-Status`
5. Press **Enter**

### 4.2 — Rename the sheet tab

1. At the bottom, double-click the **"Sheet1"** tab
2. Rename it: `Client Status`
3. Press **Enter**

### 4.3 — Set up column headers

- Click cell **A1** and type: `Timing Steps`
- Press **Tab** to go to **B1** and type: `End Date Raw`
- Press **Enter**

### 4.4 — Add a placeholder row (needed to create the table)

- Click **A2** and type: `placeholder`
- Click **B2** and type: `2000-01-01`

### 4.5 — Convert to a Table

1. Click back on cell **A1**
2. Click the **"Insert"** tab in the ribbon
3. Click **"Table"**
4. Confirm the range shows `$A$1:$B$2` and **"My table has headers"** is ticked
5. Click **"OK"**

The cells turn blue/striped — that means it's a Table.

### 4.6 — Name the Table

1. Click anywhere inside the table
2. Click the **"Table Design"** tab in the ribbon
3. On the far left, click the name box (says "Table1")
4. Delete it and type: `StatusData`
5. Press **Enter**

### 4.7 — Delete the placeholder row

Right-click the row with "placeholder" → **"Delete"** → **"Table Rows"**

### 4.8 — Save

Press **Ctrl + S** (Windows) or **⌘ + S** (Mac). Close the file tab.

---

## STEP 5 — Open Power Automate and Create the Flow

1. Go to **https://flow.microsoft.com**
2. Sign in with your Microsoft work account
3. Click **"My flows"** in the left menu
4. Click **"+ New flow"** → **"Scheduled cloud flow"**
5. Fill in:
   - **Flow name:** `Client Status Sync`
   - **Repeat every:** `5` `Minute`
     *(use `15` if you get an error about the minimum interval)*
6. Click **"Create"**

You're now in the flow editor, with one box at the top labelled **"Recurrence"**.

---

## STEP 6 — Add a Variable to Track the Final End Date

1. Click **"+ New step"**
2. Search: `Initialize variable` → click it
3. Fill in:
   - **Name:** `FinalEndDate`
   - **Type:** `String`
   - **Value:** `2000-01-01`

---

## STEP 7 — Clear Old Data From Excel

Every time the flow runs, it wipes the old rows before writing fresh ones.

### 7.1 — Get the existing Excel rows

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
2. Click in the output field → in the dynamic content panel,
   under **"List rows present in a table"** → click **"value"**

Inside the loop:

3. Click **"Add an action"** → search `Excel Online Business`
4. Click **"Excel Online (Business)"** → **"Delete a row"**
5. Fill in:
   - **Location / Library / File:** same as before
   - **Table:** `StatusData`
   - **Key Column:** `Timing Steps`
   - **Key Value:** click the field → dynamic content →
     under "List rows present in a table" → click **"Timing Steps"**

---

## STEP 8 — Add Your First Smartsheet

This is the core pattern. You'll repeat it for every sheet.

### 8.1 — Write the section header row to Excel

1. Click **"+ New step"** (outside and below the delete loop)
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. Fill in:
   - **Location / Library / File / Table:** same as before
   - **Timing Steps:** type the first project name, e.g.: `=== Project Alpha ===`
   - **End Date Raw:** `2000-01-01`

### 8.2 — Connect to Smartsheet and get the sheet

1. Click **"+ New step"**
2. Search: `Smartsheet` → click the Smartsheet connector
   *(click "Start trial" if prompted about premium)*
3. Click **"Get a sheet"**

**Sign in to Smartsheet (first time only):**
- Click **"Sign in"** → enter your Smartsheet email and password → click **"Allow"**

**Configure the action:**
- **Sheet Id:** paste your Sheet 1 ID from Step 1
  *(type it directly into the field — there's no dropdown for "Get a sheet")*

### 8.3 — Rename this action for clarity

This makes the expressions easier to write later.

1. Click the **"..."** (three dots) in the top-right corner of the "Get a sheet" action box
2. Click **"Rename"**
3. Type: `Get Sheet1`
4. Press **Enter**

### 8.4 — Loop through the rows

1. Click **"+ New step"** → search `Apply to each` → click it
2. Click in the output field → click the **"Expression"** tab
3. Type exactly: `body('Get_Sheet1')?['rows']`
4. Click **"OK"**

> **Why an expression?** "Get a sheet" returns the rows nested inside the response body.
> The expression `body('Get_Sheet1')?['rows']` tells Power Automate to extract just the rows array.
> The `'Get_Sheet1'` part must match the name you gave the action in step 8.3 — spaces become underscores.

**Rename this loop:**
5. Click **"..."** on the Apply to each box → **"Rename"** → type: `Sheet1 Rows` → Enter

---

Now add **three actions** inside this loop:

---

### 8.5 — ACTION 1: Build the bullet text

1. Inside the loop, click **"Add an action"**
2. Search: `Compose` → click **"Compose"** (Data Operation)
3. Click in the **Inputs** field → click the **"Expression"** tab
4. Type the following expression, replacing the index numbers with your column positions from Step 2:

```
concat('• ', items('Sheet1_Rows')?['cells']?[0]?['displayValue'], ' — ', items('Sheet1_Rows')?['cells']?[1]?['displayValue'], ' to ', items('Sheet1_Rows')?['cells']?[2]?['displayValue'])
```

**Explanation of the numbers:**
- `?[0]` = your Task Name column position
- `?[1]` = your Start Date column position
- `?[2]` = your End Date column position

**Example:** If Task Name is position 0, Start Date is position 1, End Date is position 2,
the expression above is already correct. Just change the numbers if yours are different.

> **Note:** `items('Sheet1_Rows')` must match the loop name you set in 8.4.
> Power Automate converts spaces to underscores, so "Sheet1 Rows" becomes `Sheet1_Rows`.

5. Click **"OK"**

---

### 8.6 — ACTION 2: Write the bullet row to Excel

1. Click **"Add an action"** → **"Excel Online (Business)"** → **"Add a row into a table"**
2. Fill in Location / Library / File / Table as before
3. Click in the **"Timing Steps"** field
4. Click **"Add dynamic content"** → under **"Compose"** → click **"Outputs"**
5. Click in the **"End Date Raw"** field → click **"Expression"** tab → type:

```
items('Sheet1_Rows')?['cells']?[2]?['displayValue']
```

*(Replace `2` with your End Date column position)*

6. Click **"OK"**

---

### 8.7 — ACTION 3: Update the Final End Date if this row's date is later

1. Click **"Add an action"** → search `Condition` → click **"Condition"**
2. Fill in:
   - **Left field:** click → **Expression** tab → type:
     `items('Sheet1_Rows')?['cells']?[2]?['displayValue']`
     *(your End Date column index)*
   - **Middle dropdown:** change to **"is greater than"**
   - **Right field:** click → **Dynamic content** tab → click **"FinalEndDate"**

**In the "If yes" branch only:**

3. Click **"Add an action"** → search `Set variable` → click it
4. Fill in:
   - **Name:** `FinalEndDate`
   - **Value:** click → **Expression** tab → type:
     `items('Sheet1_Rows')?['cells']?[2]?['displayValue']`

**Leave the "If no" branch empty.**

---

That's the complete block for Sheet 1. Here's what your flow looks like now:

```
[Recurrence]
[Initialize variable: FinalEndDate = 2000-01-01]
[List rows from Excel]
[Apply to each → Delete each row]
[Excel: Add row "=== Project Alpha ==="]
[Get Sheet1]
[Sheet1 Rows loop]
    [Compose: build bullet text]
    [Excel: Add row with bullet + end date]
    [Condition: if End Date > FinalEndDate]
        [Yes: Set FinalEndDate = End Date]
```

---

## STEP 9 — Add Your Second Smartsheet

Do this outside and below the Sheet1 Rows loop.

### 9.1 — Spacer row

1. Click **"+ New step"**
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. **Timing Steps:** type a single space: ` `
4. **End Date Raw:** `2000-01-01`

### 9.2 — Section header

1. Click **"+ New step"**
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. **Timing Steps:** `=== Project Beta ===`
4. **End Date Raw:** `2000-01-01`

### 9.3 — Get the second sheet

1. Click **"+ New step"** → search `Smartsheet` → click **"Get a sheet"**
2. **Sheet Id:** paste Sheet 2's ID
3. Rename the action: click **"..."** → **"Rename"** → type `Get Sheet2` → Enter

### 9.4 — Loop through Sheet 2's rows

1. Click **"+ New step"** → **"Apply to each"**
2. Click in the output field → **Expression** tab → type:
   `body('Get_Sheet2')?['rows']`
3. Click **"OK"**
4. Rename this loop: **"..."** → **"Rename"** → `Sheet2 Rows` → Enter

Inside the loop, add the same three actions as Step 8, but use `Sheet2_Rows` in every expression:

**ACTION 1 — Compose:**
```
concat('• ', items('Sheet2_Rows')?['cells']?[0]?['displayValue'], ' — ', items('Sheet2_Rows')?['cells']?[1]?['displayValue'], ' to ', items('Sheet2_Rows')?['cells']?[2]?['displayValue'])
```

**ACTION 2 — Excel Add a row:**
- Timing Steps: Compose Outputs (same as before)
- End Date Raw expression: `items('Sheet2_Rows')?['cells']?[2]?['displayValue']`

**ACTION 3 — Condition:**
- Left: `items('Sheet2_Rows')?['cells']?[2]?['displayValue']`
- Middle: `is greater than`
- Right: `FinalEndDate` variable
- If yes: Set FinalEndDate = `items('Sheet2_Rows')?['cells']?[2]?['displayValue']`

---

## STEP 10 — Add More Sheets (Sheet 3, 4, 5…)

For every additional sheet, repeat Step 9 with the next sheet number.
The only things that change each time:

| What changes | Example for Sheet 3 |
|---|---|
| Section header text | `=== Project Gamma ===` |
| Sheet ID in "Get a sheet" | Sheet 3's ID |
| Action rename | `Get Sheet3` |
| Loop rename | `Sheet3 Rows` |
| Expression loop name | `Sheet3_Rows` |

Everything else (the three loop actions, the Excel settings) stays identical.

---

## STEP 11 — Write the Final End Date Row

After all your sheet loops, at the very bottom of the flow:

1. Click **"+ New step"**
2. **"Excel Online (Business)"** → **"Add a row into a table"**
3. Fill in Location / Library / File / Table as before
4. Click in the **"Timing Steps"** field → type `FINAL END DATE: `
5. Click **"Add dynamic content"** → click **"FinalEndDate"** (the variable)
6. Click in the **"End Date Raw"** field → **"Dynamic content"** → click **"FinalEndDate"**

---

## STEP 12 — Save the Flow

Click **"Save"** in the top-right corner.
Wait for the green **"Your flow was saved"** confirmation.

If you see red error banners, read the message — it usually tells you exactly which
field is missing something.

---

## STEP 13 — Test the Flow

1. Click **"Test"** (top-right) → **"Manually"** → **"Test"** → **"Run flow"** → **"Done"**
2. Watch each step turn green as it completes (takes 1–3 minutes)
3. If any step turns red, click it to read the error message
4. Once everything is green, go to your SharePoint/OneDrive and open `Client-Status.xlsx`
5. Click the **"Client Status"** tab — you should see all your sections and bullets

---

## STEP 14 — Confirm the Flow Is On

1. Click the back arrow ← to return to the flow's overview page
2. Confirm the toggle says **"On"** (green)
3. If it says Off, click it to turn it on

The flow now runs automatically in Microsoft's cloud — your computer can be off.

---

## STEP 15 — Hide the "End Date Raw" Column (Optional)

This column is only used internally by the flow. To hide it from clients:

1. Open `Client-Status.xlsx`
2. Click the **"B"** column header to select the whole column
3. Right-click → **"Hide"**

---

## How to Add a New Sheet Later

1. Go to flow.microsoft.com → My flows → click your flow → Edit
2. Scroll to the bottom (before the Final End Date step)
3. Add: spacer row, header row, "Get a sheet" (rename it), Apply to each (rename it),
   and the three loop actions — same as Step 9
4. Click Save

Takes about 5 minutes once you've done it the first time.

---

## Quick Reference — The Pattern for Each Sheet

```
① Excel: Add a row
     Timing Steps: "=== Project Name ==="
     End Date Raw: 2000-01-01

② Smartsheet: Get a sheet
     Sheet Id: [paste the sheet's ID]
     → Rename action to: Get SheetN

③ Apply to each
     Output: body('Get_SheetN')?['rows']   ← Expression tab
     → Rename loop to: SheetN Rows

     Inside the loop:

     A) Compose
        Expression:
        concat('• ', items('SheetN_Rows')?['cells']?[X]?['displayValue'],
               ' — ', items('SheetN_Rows')?['cells']?[Y]?['displayValue'],
               ' to ', items('SheetN_Rows')?['cells']?[Z]?['displayValue'])
        (X = Task Name position, Y = Start Date position, Z = End Date position)

     B) Excel: Add a row into a table
        Timing Steps: [Compose Outputs]
        End Date Raw: items('SheetN_Rows')?['cells']?[Z]?['displayValue']

     C) Condition
        items('SheetN_Rows')?['cells']?[Z]?['displayValue']
        is greater than [FinalEndDate variable]
        → If yes: Set variable FinalEndDate =
          items('SheetN_Rows')?['cells']?[Z]?['displayValue']

④ Excel: Add a row (spacer — single space, date 2000-01-01)
   (add this before the NEXT sheet's header, skip after the last sheet)
```

Replace **N** with the sheet number (Sheet1, Sheet2, Sheet3…)
Replace **X, Y, Z** with your column position numbers from Step 2

---

## Troubleshooting

| What you see | What to do |
|---|---|
| Premium connector prompt | Click "Start trial" — 90 days free |
| "Get a sheet" fails with 401 | Your Smartsheet connection expired — click the action, click the connection, sign back in |
| "Invalid template" error on expression | Check for straight quotes `'` not curly quotes, and no extra spaces inside the expression |
| `body('Get_Sheet1')` returns empty | Check the Sheet ID is correct and you have access to that sheet in Smartsheet |
| Rows appear but all cells are blank | Your column position numbers are wrong — recount from 0 in Smartsheet and update the expressions |
| "Table not found" on Excel step | Confirm the table is named exactly `StatusData` (Table Design tab in Excel) |
| Loop name error in expression | Check that the name in the expression (e.g. `Sheet1_Rows`) exactly matches what you renamed the loop to, with spaces replaced by underscores |
| Final End Date shows 2000-01-01 | All rows have empty End Date cells in Smartsheet — fill them in and re-run |
| Flow times out | Increase the interval to 15 or 30 minutes |
| Only first sheet's data appears | Check each subsequent "Get a sheet" has the correct Sheet ID and each loop's expression references the right action name |
