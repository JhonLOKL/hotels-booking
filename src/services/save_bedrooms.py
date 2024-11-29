import gspread
from oauth2client.service_account import ServiceAccountCredentials
from decouple import config
from src.utils.credentials import credentials
import numpy as np
import psycopg2
import pandas as pd
from psycopg2 import extras

host = '35.226.65.128'
database = 'lokl'
user = 'postgres'
password = 'LOKL2025**'
port = '5432'

def SaveBedrooms(bedrooms_df):
    try:
        # Conexión a la base de datos
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        # Convertir los tipos de datos del DataFrame
        columnas_a_float = [
            'square_meter',
            'total_individual_beds',
            'total_doble_beds',
            'total_bunks',
            'total_sofa_beds',
            'bedrooms',
            'living_rooms',
            'max_capacity_room',
            'price_room',
            'quantity_room'
        ]
        
        for col in columnas_a_float:
            # Asegurar que la columna sea de tipo 'object' antes de aplicar .str
            bedrooms_df[col] = bedrooms_df[col].astype('str')  # Convertir a string para usar .str.replace()
            bedrooms_df[col] = bedrooms_df[col].str.replace(',', '.') 
            bedrooms_df[col] = bedrooms_df[col].replace({'': np.nan, 'None': np.nan, 'none': np.nan})
            bedrooms_df[col] = bedrooms_df[col].astype(float) 

        # Asegurar que todas las demás columnas que son 'object' o 'text' estén como strings
        columnas_a_string = [
            'date',
            'future_date',
            'title_hotel',
            'title_room',
            'breakfast_room',
            'features_room'
        ]
        bedrooms_df[columnas_a_string] = bedrooms_df[columnas_a_string].astype(str)
        # Mapeo de nombres de columnas del DataFrame a las columnas de la base de datos
        column_mapping = {
            'date' : 'date',
            'future_date' : 'futuredate',
            'title_hotel' : 'hoteltitle',
            'title_room' : 'titleroom',
            'square_meter' : 'squaremeter',
            'total_individual_beds' : 'totalindividualbeds',
            'total_doble_beds' : 'totaldoblebeds',
            'total_bunks' : 'totalbunks',
            'total_sofa_beds' : 'totalsofabeds',
            'bedrooms' : 'bedrooms',
            'living_rooms' : 'livingrooms',
            'max_capacity_room' : 'maxcapacityroom',
            'price_room' : 'priceroom',
            'breakfast_room' : 'breakfastroom',
            'features_room' : 'featuresroom',
            'quantity_room' : 'quantityroom',
        }

        # Renombrar las columnas del DataFrame según el mapeo
        bedrooms_df = bedrooms_df.rename(columns=column_mapping)

        # Convertir DataFrame en una lista de tuplas
        values = [tuple(x) for x in bedrooms_df.to_numpy()]

        # Definir los nombres de las columnas en la tabla
        columnas = ', '.join(column_mapping.values())

        # Crear una consulta SQL para insertar los datos
        insert_query = f"""
        INSERT INTO rooms ({columnas})
        VALUES %s
        """

        # Usar psycopg2's `execute_values` para insertar eficientemente muchos registros
        extras.execute_values(cursor, insert_query, values)
        
        # Confirmar los cambios
        connection.commit()
        print("Datos insertados exitosamente en la tabla 'rooms'.")

    except Exception as error:
        print(f"Error al insertar datos en la base de datos, tabla 'rooms': {error}")
    finally:
        # Cerrar conexión
        if connection:
            cursor.close()
            connection.close()
               
def SaveBedroomsPrices(bedroomsPrices_df):
    try:
    # Conexión a la base de datos
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cursor = connection.cursor()

        # Convertir los tipos de datos del DataFrame
        columnas_a_float = [
            'price_room',
            'quantity_room'
        ]
        
        for col in columnas_a_float:
            # Asegurar que la columna sea de tipo 'object' antes de aplicar .str
            bedroomsPrices_df[col] = bedroomsPrices_df[col].astype('str')  # Convertir a string para usar .str.replace()
            bedroomsPrices_df[col] = bedroomsPrices_df[col].str.replace(',', '.') 
            bedroomsPrices_df[col] = bedroomsPrices_df[col].replace({'': np.nan, 'None': np.nan, 'none': np.nan})
            bedroomsPrices_df[col] = bedroomsPrices_df[col].astype(float) 

        # Asegurar que todas las demás columnas que son 'object' o 'text' estén como strings
        columnas_a_string = [
            'date',
            'future_date',
            'title_hotel',
            'title_room'
        ]

        bedroomsPrices_df[columnas_a_string] = bedroomsPrices_df[columnas_a_string].astype(str)
        # Mapeo de nombres de columnas del DataFrame a las columnas de la base de datos
        column_mapping = {
            'date' : 'date',
            'future_date' : 'futuredate',
            'title_hotel' : 'hoteltitle',
            'title_room' : 'roomtitle',
            'price_room' : 'roomprice',
            'quantity_room' : 'roomquantity'
        }

        # Renombrar las columnas del DataFrame según el mapeo
        bedroomsPrices_df = bedroomsPrices_df.rename(columns=column_mapping)

        # Convertir DataFrame en una lista de tuplas
        values = [tuple(x) for x in bedroomsPrices_df.to_numpy()]

        # Definir los nombres de las columnas en la tabla
        columnas = ', '.join(column_mapping.values())

        # Crear una consulta SQL para insertar los datos
        insert_query = f"""
        INSERT INTO prices ({columnas})
        VALUES %s
        """

        # Usar psycopg2's `execute_values` para insertar eficientemente muchos registros
        extras.execute_values(cursor, insert_query, values)
        
        # Confirmar los cambios
        connection.commit()
        print("Datos insertados exitosamente en la tabla 'prices'.")

    except Exception as error:
        print(f"Error al insertar datos en la base de datos, tabla 'prices': {error}")
    finally:
        # Cerrar conexión
        if connection:
            cursor.close()
            connection.close()