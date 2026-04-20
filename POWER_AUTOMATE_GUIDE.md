# Step-by-Step Guide: Smartsheet → Excel Sync Using Power Automate

No coding required. This guide walks through every click.

---

## Before You Start — Check Your Power Automate Plan

The Smartsheet connector in Power Automate is a **"Premium" connector**, which means
you need a plan that includes premium connectors. Here's how to check:

1. Go to **https://flow.microsoft.com** and sign in with your Microsoft work account
2. Click the **gear icon ⚙️** in the top-right corner
3. Click **"View my licenses and add-ons"**
4. If you see **"Power Automate Premium"** or **"Microsoft 365 Business Premium"** — you're good
5. If you only see **"Power Automate Free"** or **"Microsoft 365 Business Basic/Standard"**,
   the Smartsheet connector may not be available to you without upgrading

> **If you don't have premium:** You can still try — Power Automate gives you a
> **90-day free trial of premium** when you first try to use a premium connector.
> Click through any trial prompts and you can use it for free while you get set up.

---

## What You'll Need

- A **Smartsheet account** with the sheet you want to sync
- A **Microsoft 365 account** (work or school) with access to SharePoint or OneDrive
- Access to **Power Automate** at flow.microsoft.com
- About **45 minutes** to complete the setup

---

## PART 1 — Prepare Your Excel File on SharePoint/OneDrive

Power Automate writes to Excel using a feature called a **Table**.
You need to set this up first before building the flow.

### Step 1.1 — Create the Excel file

1. Go to your **SharePoint site** or **OneDrive** in your browser
2. Navigate to the folder where you want the client status file to live
   (create a new folder if needed — e.g. "Client Status")
3. Click **"+ New"** → **"Excel workbook"**
4. A new Excel file opens in the browser — rename it by clicking the filename at the top:
   change it to `Nicole-Dodds-Status`

### Step 1.2 — Rename the first sheet tab

1. At the bottom of the Excel file, you'll see a tab called **"Sheet1"**
2. Double-click it and rename it to: `Client Status`
3. Press **Enter**

### Step 1.3 — Add a header row

Click on cell **A1** and type exactly:
```
Timing Steps
```
Press **Enter**.

Then click on cell **A2** and type a placeholder line (you'll delete this later):
```
placeholder
```

### Step 1.4 — Convert to a Table

This is important — Power Automate can only read/write Excel data that's inside a Table.

1. Click on cell **A1** (the "Timing Steps" header)
2. Click the **"Insert"** tab in the top ribbon
3. Click **"Table"**
4. A dialog box pops up — it should show `=$A$1:$A$2`
5. Make sure **"My table has headers"** is checked
6. Click **"OK"**

The cell should now have a blue/striped background — that means it's a Table.

### Step 1.5 — Name the Table

1. Click anywhere inside the table
2. Click the **"Table Design"** tab that appears in the top ribbon
3. On the far left, you'll see a box that says **"Table1"** — click it
4. Delete "Table1" and type: `TimingSteps`
5. Press **Enter**

### Step 1.6 — Delete the placeholder row

1. Right-click on the row with "placeholder" in it
2. Click **"Delete"** → **"Table Rows"**

### Step 1.7 — Save and close the file

Press **Ctrl + S** (or **⌘ + S** on Mac) to save.
You can close the Excel tab — Power Automate will write to it automatically.

---

## PART 2 — Find Your Smartsheet Sheet ID

1. Open your Smartsheet in the browser
2. Look at the URL — it looks like:
   `https://app.smartsheet.com/sheets/1234567890123456`
3. Copy the number at the end — this is your **Sheet ID**
4. Save it somewhere (e.g. paste it into a Notes document)

---

## PART 3 — Open Power Automate and Create a New Flow

1. Go to **https://flow.microsoft.com**
2. Sign in with your Microsoft work account if prompted
3. In the left menu, click **"My flows"**
4. Click **"+ New flow"** near the top
5. Click **"Scheduled cloud flow"**

   > A "scheduled cloud flow" runs automatically on a timer — perfect for syncing every few minutes.

---

## PART 4 — Set Up the Schedule

A dialog box appears called **"Build a scheduled cloud flow"**:

1. **Flow name:** Type `Smartsheet to Excel Sync`
2. **Starting:** Leave this as today
3. **Repeat every:** Type `5` and select `Minute` from the dropdown
   > Note: If you're on a free trial, you may be limited to every 15 minutes.
   > Change to `15` and `Minute` if you get an error.
4. Click **"Create"**

You're now inside the flow editor. You'll see one box at the top labelled **"Recurrence"**.

---

## PART 5 — Add the Smartsheet "List Rows" Action

This step fetches all the rows from your Smartsheet.

1. Click the **"+ New step"** button below the Recurrence box
2. In the search bar that appears, type: `Smartsheet`
3. You'll see the Smartsheet connector appear — click it
   > If a prompt appears about a premium connector trial, click **"Start trial"** or **"Continue"**
4. You'll see a list of actions — click **"List rows in a sheet"**

### Connect your Smartsheet account

A sign-in prompt will appear:
1. Click **"Sign in"**
2. A Smartsheet login window opens — sign in with your Smartsheet credentials
3. Click **"Allow"** to give Power Automate access
4. You're returned to the flow editor

### Configure the action

1. Click the **"Sheet Id"** field
2. A dropdown appears showing your Smartsheet sheets — click the one you want to sync
   > If your sheet doesn't appear, click **"Enter custom value"** and paste the Sheet ID you copied in Part 2

Leave everything else as default.

---

## PART 6 — Add a Variable to Build the Final End Date

We need to track the latest end date as we loop through rows.
This step creates a "box" to store it.

1. Click **"+ New step"**
2. Search for `Initialize variable`
3. Click **"Initialize variable"** (the one from the "Variables" connector)
4. Fill in:
   - **Name:** `FinalEndDate`
   - **Type:** `String`
   - **Value:** leave blank

---

## PART 7 — Delete Old Rows From Excel

Before writing new data, you need to clear out the old rows from the Excel table.
This takes a few steps.

### Step 7.1 — Get the existing Excel rows

1. Click **"+ New step"**
2. Search for `Excel Online`
3. Click **"Excel Online (Business)"**
4. Click **"List rows present in a table"**
5. Fill in:
   - **Location:** Select `SharePoint` or `OneDrive for Business` depending on where your file is
   - **Document Library:** Select the library (e.g. "Documents")
   - **File:** Click the folder icon and navigate to your `Nicole-Dodds-Status.xlsx` file
   - **Table:** Select `TimingSteps`

### Step 7.2 — Loop through and delete each row

1. Click **"+ New step"**
2. Search for `Apply to each`
3. Click **"Apply to each"** (from Control)
4. Click in the **"Select an output from previous steps"** field
5. In the dynamic content panel that appears on the right, look under
   **"List rows present in a table"** and click **"value"**

Now you're inside the loop. Add a delete action:

6. Inside the loop box, click **"Add an action"**
7. Search for `Excel Online`
8. Click **"Excel Online (Business)"** → **"Delete a row"**
9. Fill in:
   - **Location:** Same as before (SharePoint or OneDrive)
   - **Document Library:** Same as before
   - **File:** Same Excel file
   - **Table:** `TimingSteps`
   - **Key Column:** `Timing Steps`
   - **Key Value:** Click in the field → in the dynamic content panel, look under
     **"List rows present in a table"** → click **"Timing Steps"**

> This loops through every existing row and deletes it one by one, clearing the slate.

---

## PART 8 — Loop Through Smartsheet Rows and Write to Excel

Now add the main loop that reads each Smartsheet task and writes a bullet line to Excel.

### Step 8.1 — Add a new "Apply to each" loop

1. Click **"+ New step"** (outside the delete loop — make sure you click the one at the bottom, not inside the loop)
2. Search for `Apply to each`
3. Click **"Apply to each"**
4. Click in the **"Select an output from previous steps"** field
5. In the dynamic content panel, look under **"List rows in a sheet"** and click **"rows"**

You're now inside a new loop that goes through each Smartsheet row.

### Step 8.2 — Build the bullet text

Inside the loop:

1. Click **"Add an action"**
2. Search for `Compose`
3. Click **"Compose"** (from the Data Operation connector)
4. In the **Inputs** field, click in the box and then click **"Expression"** tab
   in the dynamic content panel
5. Type this expression exactly:

   ```
   concat('• ', items('Apply_to_each_2')?['Task Name'], ' — ', items('Apply_to_each_2')?['Start Date'], ' to ', items('Apply_to_each_2')?['End Date'])
   ```

   > **Note:** Replace `Task Name`, `Start Date`, and `End Date` with your exact
   > Smartsheet column names if they are different. Capitalisation matters.
   >
   > Also replace `Apply_to_each_2` with whatever Power Automate named your loop
   > (hover over the loop title bar to see its exact name — it may be `Apply_to_each_2`
   > or similar).

6. Click **"OK"**

### Step 8.3 — Add the row to Excel

Still inside the loop:

1. Click **"Add an action"**
2. Search for `Excel Online`
3. Click **"Excel Online (Business)"** → **"Add a row into a table"**
4. Fill in:
   - **Location:** Same SharePoint/OneDrive
   - **Document Library:** Same library
   - **File:** Same Excel file
   - **Table:** `TimingSteps`
5. A field labelled **"Timing Steps"** appears (matching your column header)
6. Click in that field → click the **"Dynamic content"** tab →
   look under **"Compose"** → click **"Outputs"**

### Step 8.4 — Track the Final End Date

Still inside the loop, after the Excel action:

1. Click **"Add an action"**
2. Search for `Condition`
3. Click **"Condition"** (from Control)
4. In the first field, click it → Dynamic content → under your Smartsheet loop → click **"End Date"**
5. Set the middle dropdown to **"is greater than"**
6. In the right field, click → Dynamic content → click **"FinalEndDate"** (the variable you created)

**In the "Yes" branch:**
1. Click **"Add an action"**
2. Search for `Set variable`
3. Click **"Set variable"**
4. **Name:** `FinalEndDate`
5. **Value:** Click → Dynamic content → click **"End Date"** (from your Smartsheet loop)

---

## PART 9 — Write the Final End Date to Excel

After the Smartsheet loop (outside it), add the final end date row.

1. Click **"+ New step"** at the bottom (outside the loop)
2. Click **"Excel Online (Business)"** → **"Add a row into a table"**
3. Fill in the same Location, Library, File, Table as before
4. In the **"Timing Steps"** field, click it → switch to **"Expression"** tab → type:

   ```
   concat('FINAL END DATE: ', variables('FinalEndDate'))
   ```

5. Click **"OK"**

---

## PART 10 — Save and Test the Flow

### Save the flow

Click the **"Save"** button in the top-right corner.
Wait for the green "Your flow was saved" message.

### Test it

1. Click the **"Test"** button in the top-right corner
2. Select **"Manually"**
3. Click **"Test"**
4. Click **"Run flow"**
5. Click **"Done"**

You'll see each step light up green as it runs. This takes about 30–60 seconds.

If anything turns red (fails):
- Click the red step to see the error message
- Common issues are listed in the Troubleshooting section below

### Check your Excel file

1. Go to your SharePoint/OneDrive and open `Nicole-Dodds-Status.xlsx`
2. Click the **"Client Status"** tab
3. You should see a row for each task from your Smartsheet, formatted like:
   ```
   • Project Kickoff — 2026-04-01 to 2026-04-15
   • Design Phase — 2026-04-16 to 2026-04-30
   FINAL END DATE: 2026-05-31
   ```

---

## PART 11 — Turn On the Flow

By default the flow is now active and will run on the schedule you set.
To confirm:

1. Go to **"My flows"** in the left menu
2. Find `Smartsheet to Excel Sync`
3. The toggle next to it should say **"On"**
4. If it says "Off", click it to turn it on

Your sync is now running automatically. Every 5 minutes (or however long you set),
it will clear the Excel table and rewrite it with the latest Smartsheet data.

---

## PART 12 — Optional: Get an Email Alert If the Flow Fails

1. Open your flow and click **"Edit"**
2. Click **"+ New step"** at the very end
3. Search for `Send an email`
4. Click **"Send an email (V2)"** from the Office 365 Outlook connector
5. Fill in:
   - **To:** your email address
   - **Subject:** `Smartsheet sync failed`
   - **Body:** `The sync flow encountered an error. Check Power Automate for details.`
6. Now wrap this in a condition so it only sends on failure:
   - Click the three dots `...` on the email step → **"Configure run after"**
   - Uncheck **"is successful"**
   - Check **"has failed"** and **"has timed out"**
   - Click **"Done"**

---

## Troubleshooting

| What you see | What to do |
|---|---|
| "Premium connector" prompt | Click "Start trial" — you get 90 days free |
| Smartsheet step fails with 401 | Your Smartsheet connection expired — click the step, click the connection, sign in again |
| "Sheet not found" | Make sure you selected the right sheet, or paste the Sheet ID manually |
| Excel step fails: "Table not found" | Check the table is named exactly `TimingSteps` (no spaces) in the Excel file |
| Excel step fails: "File not found" | Re-select the file path — the file may have moved |
| Loop runs but Excel shows no rows | The Smartsheet column names in the expression don't match your actual columns — check spelling and capitalisation |
| Flow runs successfully but Excel is empty | The delete loop may have run but the write loop had an error — check each step individually |
| "Apply_to_each_2" in the expression isn't right | Hover over your Smartsheet loop's title bar — copy the exact name shown and use that in the expression |
| Flow runs every 15 min instead of 5 | Free/standard plans have a 15-minute minimum — either upgrade or accept 15-minute syncs |
| Condition step errors on empty End Date | Some rows may have no end date — add a condition before the date comparison to check if End Date is not empty |

---

## How to Edit the Flow Later

To change the schedule, column names, or any step:

1. Go to **flow.microsoft.com → My flows**
2. Click your flow name
3. Click **"Edit"** in the top bar
4. Make your changes
5. Click **"Save"**

---

## What to Do If You Can't Use the Smartsheet Premium Connector

If the premium trial expires and you can't upgrade, here are free alternatives:

1. **Smartsheet's built-in Excel export** — In Smartsheet, click File → Export → Export to Excel.
   It's manual, but it works.

2. **Smartsheet to Google Sheets sync** — Smartsheet has a free native Google Sheets integration.
   Google Sheets can then be connected to Excel via Power Automate's free Google Sheets connector.
   This is more steps but avoids the premium Smartsheet connector.

3. **The Python script** — The script we already built in this repository does the same thing
   and only needs to be set up once. See `SETUP_GUIDE_MAC.md` for Mac instructions.
