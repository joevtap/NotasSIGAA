from oauth2client.service_account import ServiceAccountCredentials
import gspread
from dotenv import load_dotenv
import os

load_dotenv()

g_credentials = os.getenv('G_CREDENTIALS')
g_sheet = os.getenv('G_SHEET')
csv_output = os.getenv('CSV_OUTPUT')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(g_credentials, scope)
client = gspread.authorize(credentials)

spreadsheet = client.open(g_sheet)


def upload_csv():
    with open(csv_output, 'r') as file:
        content = file.read()
        client.import_csv(spreadsheet.id, data=content)


if __name__ == '__main__':
    upload_csv()


