# Pulling From Multiple Smartsheets

This guide shows you how to modify your flow (Power Automate or Make.com)
to pull data from several Smartsheet sheets into one Excel document.

---

## How It Works

The flow runs once, then processes each of your sheets **one after the other**:

1. Clear the old Excel data
2. Write a header line → then all rows from **Sheet 1**
3. Write a header line → then all rows from **Sheet 2**
4. Write a header line → then all rows from **Sheet 3**
5. (repeat for as many sheets as you have)

The Excel file ends up looking like this:

```
=== Project Alpha ===
• Kickoff — 1 Apr 2026 to 15 Apr 2026
• Design Phase — 16 Apr 2026 to 30 Apr 2026

=== Project Beta ===
• Discovery — 1 May 2026 to 10 May 2026
• Build Phase — 11 May 2026 to 31 May 2026

=== Project Gamma ===
• Planning — 1 Jun 2026 to 14 Jun 2026

FINAL END DATE (All Projects): 31 May 2026
```

---

## Before You Start — Gather Your Sheet IDs

You'll need the Sheet ID for each Smartsheet you want to include.

For each sheet:
1. Open the sheet in your browser
2. Copy the number from the URL:
   `https://app.smartsheet.com/sheets/`**`1234567890123456`**
3. Write them down in a list, with a name for each:

```
Sheet 1: Project Alpha  →  ID: 1111111111111111
Sheet 2: Project Beta   →  ID: 2222222222222222
Sheet 3: Project Gamma  →  ID: 3333333333333333
```

---

---

# POWER AUTOMATE — Multi-Sheet Setup

---

## PART 1 — Open and Edit Your Existing Flow

1. Go to **https://flow.microsoft.com**
2. Click **"My flows"** in the left menu
3. Click your flow **"Smartsheet to Excel Sync"**
4. Click **"Edit"** at the top

You'll see the flow you already built. You're going to add a new section for each additional sheet.

---

## PART 2 — Understand the Structure You're Building

Your current flow has this shape:
```
[Recurrence]
    ↓
[Delete old Excel rows]  ← runs once, clears everything
    ↓
[Get Sheet 1 rows]
[Loop → write each row to Excel]
    ↓
[Write Final End Date]
```

You're going to change it to:
```
[Recurrence]
    ↓
[Delete old Excel rows]  ← still runs once
    ↓
[Write "=== Project Alpha ===" header row]
[Get Sheet 1 rows]
[Loop → write each row to Excel]
    ↓
[Write "=== Project Beta ===" header row]
[Get Sheet 2 rows]
[Loop → write each row to Excel]
    ↓
[Write "=== Project Gamma ===" header row]
[Get Sheet 3 rows]
[Loop → write each row to Excel]
    ↓
[Write Overall Final End Date]
```

---

## PART 3 — Add a Section Header Before Your First Sheet's Data

1. In the flow editor, find the step just before your first
   **"List rows in a sheet"** action
2. Click the **"+"** button between the "Delete rows" section and the first Smartsheet step
3. Click **"Add an action"**
4. Search for `Excel Online`
5. Click **"Excel Online (Business)"** → **"Add a row into a table"**
6. Fill in:
   - **Location, Document Library, File, Table:** same as your other Excel steps
   - **Timing Steps field:** type the name of your first project, like:
     ```
     === Project Alpha ===
     ```
7. Click **"OK"**

Now your first sheet's rows will appear right below that header.

---

## PART 4 — Add a Second Sheet (Repeat for Each Additional Sheet)

Do this after the loop that processes your first sheet's rows.

### Step 4.1 — Add a blank spacer row (optional but looks nicer)

1. Click **"+"** after the first sheet's loop
2. Add another **"Excel Online → Add a row into a table"** action
3. In the **Timing Steps** field, type a single space: ` `
   (this creates a visible gap between sections in Excel)

### Step 4.2 — Add the header for the second sheet

1. Click **"+"** after the spacer
2. Add another **"Excel Online → Add a row into a table"** action
3. In the **Timing Steps** field, type:
   ```
   === Project Beta ===
   ```

### Step 4.3 — Get the second sheet's rows from Smartsheet

1. Click **"+"**
2. Search for `Smartsheet` → click **"List rows in a sheet"**
3. In the **Sheet** dropdown, select your second sheet
   (or click **"Enter custom value"** and paste its Sheet ID)

### Step 4.4 — Loop through the second sheet's rows

1. Click **"+"**
2. Search for `Apply to each` → click **"Apply to each"**
3. In the **"Select an output"** field, select **"rows"** from the
   **second** Smartsheet action (not the first one — they'll both appear in the list,
   so check the label carefully)

Inside this new loop:
4. Click **"Add an action"** → **"Excel Online → Add a row into a table"**
5. Fill in the same Location/Library/File/Table as before
6. In the **Timing Steps** field, click → **Expression** tab → type:
   ```
   concat('• ', items('Apply_to_each_3')?['Task Name'], ' — ', items('Apply_to_each_3')?['Start Date'], ' to ', items('Apply_to_each_3')?['End Date'])
   ```
   > **Important:** The loop name `Apply_to_each_3` will be different for your second loop.
   > Hover over the loop's title bar to see its exact name, then use that in the expression.
   > Each new loop gets a new name (Apply_to_each_2, Apply_to_each_3, etc.)

7. Click **"OK"**

---

## PART 5 — Repeat for Each Additional Sheet

For every extra sheet, repeat Part 4:
- Spacer row
- Header row (`=== Sheet Name ===`)
- Smartsheet "List rows" action (pointing to the new sheet)
- "Apply to each" loop with the Excel "Add a row" action inside

The naming of each loop changes each time, but the process is identical.

---

## PART 6 — Update the Final End Date to Cover All Sheets

Your existing Final End Date variable only tracked one sheet.
To track the maximum date across ALL sheets, you need to update the
variable inside every loop, not just the first one.

In the loop for each sheet, add a **Condition** step (same as before):
- If `End Date` from this row is greater than `FinalEndDate` variable
- Then set `FinalEndDate` = this row's End Date

Do this inside every sheet's loop. The variable keeps updating as
each sheet is processed, so by the end it holds the latest date across all sheets.

The **"Write Final End Date"** step at the very bottom of your flow stays as-is —
it just writes whatever the variable contains after all sheets have been processed.

---

## PART 7 — Save and Test

1. Click **"Save"** in the top-right
2. Click **"Test"** → **"Manually"** → **"Run flow"**
3. Watch each step complete (green = good, red = error)
4. Open your Excel file on SharePoint and check that all sections appear

---

---

# MAKE.COM — Multi-Sheet Setup

---

## PART 1 — Open Your Existing Scenario

1. Go to **https://www.make.com**
2. Click **"Scenarios"** in the left menu
3. Click your scenario to open it
4. Click **"Edit"** (pencil icon)

---

## PART 2 — Add Modules for Each Additional Sheet

In Make.com, you add a new **Smartsheet → Watch Rows** module for each sheet,
chained after the previous one.

### For each additional sheet:

1. Click the **"+"** after your last Excel write action
2. Search for `Smartsheet` → click **"Watch Rows"**
3. Use your existing Smartsheet connection (select it from the dropdown)
4. Select the new sheet in the **Sheet** field
5. Click **"OK"**

Then add:
6. Click **"+"** → **"Flow Control"** → **"Iterator"**
   - **Array:** select **"Rows"** from this new Smartsheet module

7. Click **"+"** → **"Microsoft 365 Excel"** → **"Add a Row"**
   - Same workbook, worksheet, table as before
   - **Timing Steps:** `• {{cells.Task Name}} — {{cells.Start Date}} to {{cells.End Date}}`
   - Make sure the variables are coming from **this** sheet's iterator, not the first one

Repeat for each additional sheet.

---

## PART 3 — Add Section Headers in Make.com

To add the `=== Project Name ===` header rows in Make.com:

1. Click **"+"** before each sheet's Iterator module
2. Search for `Microsoft 365 Excel` → **"Add a Row"**
3. In the **Timing Steps** field, type the header text directly:
   ```
   === Project Alpha ===
   ```

This adds a header row to Excel before that sheet's data.

---

## PART 4 — Test

1. Click **"Run once"** at the bottom of the screen
2. Check each bubble — green = success
3. Open your Excel file and verify all sections appear

---

---

# Tips for Managing Many Sheets

### Keep a master list
Maintain a simple note (or even a cell in the Excel file itself) with each
sheet name and its ID. When you add a new project, add it to the list
and add a new block to your flow.

### Ordering
The sheets appear in Excel in the order you added them to the flow.
To change the order, you need to reorder the blocks in the flow editor.
In Power Automate, you can drag steps up and down.

### A sheet that's empty or not started yet
If a Smartsheet has no rows, the loop simply runs zero times —
no rows are written to Excel for that sheet. The header row still appears.
This is fine and won't cause an error.

### Adding a new sheet later
- In Power Automate: click Edit on your flow → add a new section at the end → Save
- In Make.com: click Edit on your scenario → add new modules → Save
- It takes about 5 minutes per new sheet once you've done it the first time

### Maximum number of sheets
There's no hard limit. In practice, flows with 10–15 sheets run fine.
Above that, the flow may start taking longer than 5 minutes to run,
which could cause it to time out. If that happens, increase the interval
to every 15 or 30 minutes.
