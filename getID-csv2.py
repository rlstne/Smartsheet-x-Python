
import smartsheet
import pandas as pd
from datetime import datetime
import time


start_time = datetime.now()
print(start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("")
print('This Scipt Generates Sheet ID from workspace')

print("""
# 1 - Enter site IDs here
# 2 - Enter site IDs here
# 3 - Enter site IDs here
""")

try:
    selection = int(input('Select Workspace to generate sheet ID (1, 2, or 3): '))
    if selection == 1:
        wdid = '#1'
        print("")
        get1 = datetime.now()
        print(get1.strftime("%Y-%m-%d %H:%M:%S"), "Generating Sheets IDs x")
    elif selection == 2:
        wdid = '#1'
        print("")
        get2 = datetime.now()
        print(get2.strftime("%Y-%m-%d %H:%M:%S"), "Generating Sheets IDs x")
    elif selection == 3:
        wdid = '#1'
        print("")
        get3 = datetime.now()
        print(get3.strftime("%Y-%m-%d %H:%M:%S"), "Generating Sheets IDs x")
    else:
        print('Invalid selection.')
        wdid = None
except ValueError:
    print('Please enter a valid number.')
    wdid = None

API_TOKEN = 'insert token' # Replace with your actual token
WORKSPACE_ID = wdid  # Replace with your actual workspace ID

# Initialize Smartsheet client

init = datetime.now()
print(init.strftime("%Y-%m-%d %H:%M:%S"), 'Initializing Smartsheet Client')

smartsheet_client = smartsheet.Smartsheet(API_TOKEN)



# List to store sheet information
sheet_data = []

# Recursive function to traverse folders and subfolders
def traverse_folder(folder_id, folder_path, workspace_name):
    folder_content = smartsheet_client.Folders.get_folder(folder_id)
    
    # Add sheets in the current folder
    for sheet in folder_content.sheets:
        sheet_data.append({
            "Workspace Name": workspace_name,
            "Folder Path": folder_path,
            "Sheet Name": sheet.name,
            "Sheet ID": str(sheet.id)
        })
    
    # Recurse into subfolders
    for subfolder in folder_content.folders:
        traverse_folder(subfolder.id, f"{folder_path}/{subfolder.name}", workspace_name)

wrk = datetime.now()
print(wrk.strftime("%Y-%m-%d %H:%M:%S"), 'Getting Workspace Items')

# Get the workspace
workspace = smartsheet_client.Workspaces.get_workspace(WORKSPACE_ID)
workspace_name = workspace.name

# Sheets directly under the workspace (not in folders)
for sheet in workspace.sheets:
    sheet_data.append({
        "Workspace Name": workspace_name,
        "Folder Path": "Root",
        "Sheet Name": sheet.name,
        "Sheet ID": str(sheet.id)
    })

fldr = datetime.now()
print(fldr.strftime("%Y-%m-%d %H:%M:%S"),'Processing folders')

# Traverse each folder in the workspace
for folder in workspace.folders:
    traverse_folder(folder.id, folder.name, workspace_name)

fin = datetime.now()
print(fin.strftime("%Y-%m-%d %H:%M:%S"),'Exporting to CSV')

# Create a DataFrame and export to CSV
df = pd.DataFrame(sheet_data)
df.to_csv("smartsheet_sheets.csv", index=False)


print("")
print("Sheet data has been exported to smartsheet_sheets.csv")
print("")
end_time = datetime.now()

print("Start Time   :", start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("End Time     :", end_time.strftime("%Y-%m-%d %H:%M:%S"))

elapsed = end_time - start_time

print("Elapsed time :", elapsed)

