import numpy as np
import psycopg2
import pandas as pd
from psycopg2 import extras

# Datos de conexión
host = '34.71.211.75'
database = 'lokl'
user = 'postgres'
password = 'LOKL2025**'
port = '5432'

def SaveHotels(hotels_df):
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
            'hotel_reviews', 'hotel_puntuation', 'staff', 'installations_services', 
            'cleaning', 'confort', 'value_for_money', 'location', 'wifi'
        ]
        
        for col in columnas_a_float:
            hotels_df[col] = hotels_df[col].astype('str')  # Convertir a string para usar .str.replace()
            hotels_df[col] = hotels_df[col].str.replace(',', '.') 
            hotels_df[col] = hotels_df[col].replace({'': np.nan, 'None': np.nan, 'none': np.nan})
            hotels_df[col] = hotels_df[col].replace('', np.nan)  # Reemplazar cadenas vacías por NaN
            hotels_df[col] = hotels_df[col].astype(float) 

        # Asegurar que todas las demás columnas que son 'object' o 'text' estén como strings
        columnas_a_string = [
            'date', 'future_date', 'hotel_title', 'hotel_coordinates', 'hotel_address', 
            'neighborhood', 'codigo_postal', 'services', 'features'
        ]
        hotels_df[columnas_a_string] = hotels_df[columnas_a_string].astype(str)

        # Mapeo de nombres de columnas del DataFrame a las columnas de la base de datos
        column_mapping = {
            'date': 'date',
            'future_date': 'futuredate',
            'hotel_title': 'hoteltitle',
            'hotel_coordinates': 'hotelcoordinates',
            'hotel_address': 'hoteladdress',
            'neighborhood': 'neighborhood',
            'codigo_postal': 'postalcode',
            'hotel_puntuation': 'hotelpuntuation',
            'hotel_reviews': 'hotelreviews',
            'services': 'services',
            'staff': 'staff',
            'installations_services': 'installationsservices',
            'cleaning': 'cleaning',
            'confort': 'confort',
            'value_for_money': 'valueformoney',
            'location': 'location',
            'wifi': 'wifi',
            'features': 'features'
        }

        # Renombrar las columnas del DataFrame según el mapeo
        hotels_df = hotels_df.rename(columns=column_mapping)

        # Convertir DataFrame en una lista de tuplas
        values = [tuple(x) for x in hotels_df.to_numpy()]

        # Definir los nombres de las columnas en la tabla
        columnas = ', '.join(column_mapping.values())

        # Crear una consulta SQL para insertar los datos
        insert_query = f"""
        INSERT INTO hotels ({columnas})
        VALUES %s
        """

        # Usar psycopg2's `execute_values` para insertar eficientemente muchos registros
        extras.execute_values(cursor, insert_query, values)
        
        # Confirmar los cambios
        connection.commit()
        print("Datos insertados exitosamente en la tabla 'hotels'.")

    except Exception as error:
        print(f"Error al insertar datos en la base de datos, tabla 'hotels': {error}")
    finally:
        # Cerrar conexión
        if connection:
            cursor.close()
            connection.close()