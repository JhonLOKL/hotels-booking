import gspread
from oauth2client.service_account import ServiceAccountCredentials
from decouple import config
from src.utils.credentials import credentials

def SaveBedrooms(bedrooms_df):
    try:
        json_credenciales = credentials()
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credenciales = ServiceAccountCredentials.from_json_keyfile_dict(json_credenciales, scope)
        gc = gspread.authorize(credenciales)
        
        spreadsheet = gc.open_by_url(config('HOTELS_URL'))
        sheet_title = 'bedrooms_df'
        worksheet = spreadsheet.worksheet(sheet_title)
        
        all_values = worksheet.get_all_values()
        empty_rows = [i + 2 for i, row in enumerate(all_values[1:]) if not any(row)]
        
        if len(empty_rows) < len(bedrooms_df):
            extra_rows_needed = len(bedrooms_df) - len(empty_rows)
            empty_rows.extend([len(all_values) + i + 1 for i in range(extra_rows_needed)])

        columnas_df = bedrooms_df.columns.tolist()
        columnas_hoja = worksheet.row_values(1)
        values = bedrooms_df[columnas_df].astype(str).values.tolist()

        for row in values:
            while len(row) < len(columnas_hoja):
                row.append('')
        
        cell_range = f'A{empty_rows[0]}:{chr(64+len(columnas_hoja))}{empty_rows[-1]}'
        worksheet.update(cell_range, values)
        
        print("Bedrooms successfully saved")

    except gspread.exceptions.APIError as api_error:
        print(f"API error: {api_error}")
    except gspread.exceptions.GSpreadException as gs_error:
        print(f"gspread error: {gs_error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

def SaveBedroomsPrices(bedroomsPrices_df):
    try:
        json_credenciales = credentials()
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credenciales = ServiceAccountCredentials.from_json_keyfile_dict(json_credenciales, scope)
        gc = gspread.authorize(credenciales)
        
        spreadsheet = gc.open_by_url(config('HOTELS_URL'))
        sheet_title = 'prices_df'
        worksheet = spreadsheet.worksheet(sheet_title)
        
        all_values = worksheet.get_all_values()
        empty_rows = [i + 2 for i, row in enumerate(all_values[1:]) if not any(row)]
        
        if len(empty_rows) < len(bedroomsPrices_df):
            extra_rows_needed = len(bedroomsPrices_df) - len(empty_rows)
            empty_rows.extend([len(all_values) + i + 1 for i in range(extra_rows_needed)])

        columnas_df = bedroomsPrices_df.columns.tolist()
        columnas_hoja = worksheet.row_values(1)
        values = bedroomsPrices_df[columnas_df].astype(str).values.tolist()

        for row in values:
            while len(row) < len(columnas_hoja):
                row.append('')
        
        cell_range = f'A{empty_rows[0]}:{chr(64+len(columnas_hoja))}{empty_rows[-1]}'
        worksheet.update(cell_range, values)
        
        print("Bedrooms prices successfully saved")

    except gspread.exceptions.APIError as api_error:
        print(f"API error: {api_error}")
    except gspread.exceptions.GSpreadException as gs_error:
        print(f"gspread error: {gs_error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
