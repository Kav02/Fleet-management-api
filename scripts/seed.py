import os
import sys
import getpass
import argparse
import pandas as pd
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 1.Retrieve the command line arguments
def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description='Upload data to database.')
    parser.add_argument('path_to_files', type=str, help='Path to the files to upload')
    parser.add_argument('--type', type=str, choices=['taxis', 'trajectories'], required=True, help='Type of data: taxis or trajectories')
    parser.add_argument('--dbname', type=str, required=True, help='Database name')
    parser.add_argument('--host', type=str, required=True, help='Database host')
    #parser.add_argument('--port', type=int, required=True, help='Database port')
    parser.add_argument('--username', type=str, required=True, help='Database username')
    args = parser.parse_args()
    return args

# 2. Connect to database
def connect_db(username, host, dbname):
    '''Connect to the database.'''
    try:
        password = getpass.getpass(prompt="Enter your password: ")
        url_string = f"postgresql://{username}:{password}@{host}/{dbname}"
       #url_string = f"postgresql://{os.getenv('PGSQL_USER')}:{password}@{os.getenv('PGSQL_HOST')}/{os.getenv('PGSQL_DATABASE')}"
        engine = create_engine(url_string)
        conn = engine.connect()
        return conn
    except OperationalError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

# 3.Read the file using Pandas

def process_taxi(file_path):
    try:
        taxi_columns = ['id', 'plate']
        df = pd.read_csv(file_path, chunksize=1000, header=None, names=taxi_columns)
        for chunk in df:
            chunk['id'] = pd.to_numeric(chunk['id'], errors='coerce')
            chunk['plate'] = chunk['plate'].astype(str)

        return df
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def process_trajectories(file_path):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    try:
        trajectory_columns = ['taxi_id', 'date', 'latitude', 'longitude']
        df = pd.read_csv(file_path, chunksize=100, header=None, names=trajectory_columns)
        for chunk in df:
            chunk['taxi_id'] = pd.to_numeric(chunk['taxi_id'], errors='coerce')
            chunk['date'] = pd.to_datetime(chunk['date'], format=datetime_format, errors='coerce')
            chunk['latitude'] = pd.to_numeric(chunk['latitude'], errors='coerce')
            chunk['longitude'] = pd.to_numeric(chunk['longitude'], errors='coerce')

            return df
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

# 4.Use to_sql() from Pandas to insert data into the database
def insert_data_into_database(conn, df, type_of_files):
    # Convert the dataframes to SQL tables
    df_to_sql = df.to_sql(
        name=type_of_files,
        con=conn,
        if_exists='append',
        index=False,
        dtype={'date': DateTime()}  # Convert 'date' to DateTime
    )


def main():
    args = parse_args()
    path_to_files = args.path_to_files
    type_of_files = args.type
    dbname = args.dbname
    host = args.host
    #port = args.port
    username = args.username
    files= os.listdir(path_to_files)
    conn = connect_db(username, host, dbname)
    if conn:
        for file_name in files:
            file_path = os.path.join(path_to_files, file_name)
            if type_of_files == 'taxis':
                df = process_taxi(file_path)
            elif type_of_files == 'trajectories':
                df = process_trajectories(file_path)
            insert_data_into_database(conn, df, type_of_files)

if __name__ == "__main__":
    main()

# 7. Inserción de datos en la base de datos:
    # execute() de SQLAlchemy para ejecutar la consulta SQL generada o insertar los datos como una lista de diccionarios.
    # Especificae la tabla de destino y los datos a insertar.
    # Realizar la inserción por lotes .
# Procesar los datos del DataFrame de Pandas.
# Conectarse a la base de datos.
# Convertir el DataFrame de Pandas en un diccionario
# Inserta los datos procesados en la tabla de la base de datos usando execute() de SQLAlchemy.
# Cierra la conexión a la base de datos.

# Seleccionar las columnas para la inserción en la base de datos.
