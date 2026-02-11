from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
import os
import pandas as pd
from typing import TypeAlias, Any
import logging

logger = logging # use default logger

class GoogleSheet:
    """
    represents a single spreadsheet (i.e. a single tab in sheets)
    and allows read and update operations
    """
    def __init__(self, sheet_obj: Resource):
        self.sheet = sheet_obj

    def read(self) -> pd.DataFrame:
        """
        read spreadsheet from service resource object into dataframe 
        """
        sheet = self.sheet
        data = sheet.get('values', [])

        if not data:
            logger.warn(f"read_google_sheet - No data found in the specified worksheet.")

            # Return empty DataFrame
            return pd.DataFrame()

        else:
            logger.info(f"read_google_sheet - Read of Google Sheet Successful.")

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
        """
        write contents of df into spreadsheet. Note that this
        overwrites the spreadsheet contents
        """
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
        logger.info(f"Successfully updated {updated_cells} cells")
        return True, f"Successfully updated {updated_cells} cells"

class GoogleSheetManager:
    """
    handles the boilerplate of creating an authenticated 
    service and returning a spreadsheet object. 
    """
    def __init__(self):
        self._service = None

    def connect(self, credentials_file:str) -> Resource:
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
    def service(self) -> Resource:
        """
        getter for service. 
        Using service as property allows instantiation of object and 
        authentication to be separated, while also ensuring that all calls
        to service are authenticated
        """
        if self._service is None:
            raise ValueError("Connect not executed")
        return self._service
    
    def sheet(self, spreadsheet_id:str, sheet_name:str) -> GoogleSheet:
        """ 
        Uses instantiated service to fetch Google Sheet 
        `spreadsheet_id` and fetches the `sheet_name` spreadsheet
        """
        try:
            sheet = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, # spreadsheet id is base64 in edit url
                range=sheet_name
            ).execute()
        except Exception as e:
            print(f"Failed to read {spreadsheet_id}:{sheet_name} due to {e}")
            exit()
        return GoogleSheet(sheet)
