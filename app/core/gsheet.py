from app.core.google_api import gsheets_service


from app.core.settings import config

GSHEETS_ID = config.gsheets_id  # Sheet containing names and email address.
sheet = gsheets_service.spreadsheets()
result = (
    sheet.values()
    # adjust the range to match your sheet
    .get(spreadsheetId=GSHEETS_ID, range="pycontogo2026staff!A2:C200")
    .execute()
)

# print("result", result)

print(len(result.get("values", [])))

values = result.get("values", [])

for row in values:
    attendee_name = row[1]
    attendee_email = row[2]

    print(f"attendee_name: {attendee_name}, attendee_email: {attendee_email}")
