from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import pandas as pd
from typing import TypeAlias
import logging

logger = logging # use default logger

class GoogleSheet:
    def __init__(self, sheet_obj):
        self.sheet = sheet_obj

    def read(self) -> pd.DataFrame:
        sheet = self.sheet
        data = sheet.get('values', [])

        if not data:
            logger.warn(f"read_google_sheet - No data found in the specified worksheet.")
            print(f"No data found in the specified worksheet.")

            # Return empty DataFrame
            return pd.DataFrame()

        else:
            logger.info(f"read_google_sheet - Read of Google Sheet Successful.")
            print(f"Read of Google Sheet Successful.")

            # Convert to DataFrame
            # First row as headers, rest as data
            headers = data[0]
            rows = data[1:] if len(data) > 1 else []

            # Pad rows with fewer columns with fill_value
            fill_value = None
            max_columns = len(headers)
            padded_rows = [row + [fill_value] * (max_columns - len(row)) for row in rows]

            # Create DataFrame
            df = pd.DataFrame(padded_rows, columns=headers)
        
            return df

    def update(self, df: pd.DataFrame) -> tuple[bool, str]:

        # Convert DataFrame to list of lists (including headers)
        values = [df.columns.tolist()] + df.values.tolist()

        # Prepare the body for the API request
        body = {
            'values': values
        }

        # Update the sheet with DataFrame contents
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        updated_cells = result.get('updatedCells', 0)
        return True, f"Successfully updated {updated_cells} cells"

class GoogleSheetManager:
    def __init__(self):
        self._service = None

    def connect(self, credentials_file):
        """
        Connects to the Google Sheets API using service account credentials.

        Args:
            credentials_file (str): Path to the Google service account credentials file.

        Returns:
            build: The Google Sheets API service object.
        """
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        CONFIG_FILE = credentials_file

        if not os.path.exists(CONFIG_FILE):
            raise Exception(f"Configuration file not found: {CONFIG_FILE}")

        try:
            creds = service_account.Credentials.from_service_account_file(
                CONFIG_FILE,
                scopes=SCOPES
            )

            self._service = build('sheets', 'v4', credentials=creds)
            return self.service

        except Exception as e:
            raise Exception(f"Failed to create Google Sheets service: {str(e)}")
    
    @property
    def service(self):
        if self._service is None:
            raise Exception("Connect not executed")
        return self._service
    
    def sheet(self, spreadsheet_id, sheet_name):
        sheet = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, # spreadsheet id is base64 in edit url
            range=sheet_name
        ).execute()
        return GoogleSheet(sheet)
