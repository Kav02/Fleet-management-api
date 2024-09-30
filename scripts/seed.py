'''CLI script to upload data to the database.'''
import os
import sys
import getpass
import argparse
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


# Retrieve the command line arguments
def parse_args():
    '''Parse command line arguments.'''
    parser = argparse.ArgumentParser(description='Upload data to database.')
    parser.add_argument('path_to_files', type=str, help='Path to the files to upload')
    parser.add_argument('--type', type=str, choices=['taxis', 'trajectories'], required=True, help='Type of data: taxis or trajectories')
    parser.add_argument('--dbname', type=str, required=True, help='Database name')
    parser.add_argument('--host', type=str, required=True, help='Database host')
    parser.add_argument('--username', type=str, required=True, help='Database username')
    args = parser.parse_args()

    return args

# Request the password from the user
def get_password():
    '''Request the password from the user.'''
    password = getpass.getpass(prompt="Enter your password: ")
    return password


# Connect to database
def connect_db(username, host, dbname, password):
    '''Connect to the database.'''
    try:
        url_string = f"postgresql://{username}:{password}@{host}/{dbname}"
        engine = create_engine(url_string)
        conn = engine.connect()
        return conn
    except OperationalError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

# Process data and insert into the database
def insert_taxis_into_database(conn, file_path, type_of_files):
    '''Process data and insert into the database.'''
    chunk_size = 1000
    total_rows = 0
    i = 0
    columns = ['id', 'plate']
    try:
        for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, header=None, names=columns)):
            print ("Path del archivo a insertar : ", file_path)
            i += 1
            columns = ['id', 'plate']
            constraint_name = 'id'
            chunk['id'] = pd.to_numeric(chunk['id'], errors='coerce') #coerce converts non-numeric values to NaN.
            #sa.text() to create a SQL query with the ON CONFLICT clause.
            #:id and :plate are placeholders for the values to be inserted into the table.
            insert_statement = sa.text(f"""
                INSERT INTO {type_of_files} ({', '.join(columns)}) VALUES (:id, :plate) ON CONFLICT ({constraint_name}) DO UPDATE SET {columns[0]} = EXCLUDED.{columns[0]}
                """)
            # Insert data into the database
            #execute() SQLAlchemy insert the data as a list of dictionaries.
            #orient='records' to convert the DataFrame into a list of dictionaries.
            rows_inserted = conn.execute(insert_statement, chunk.to_dict(orient='records')).rowcount
            total_rows += rows_inserted
            print(f"Chunk {chunk_index + 1}: Inserted {rows_inserted} rows into '{type_of_files}' table. Total: {total_rows} rows.")
            #conn.commit() to confirm the transaction and save the changes to the database.
            conn.commit()
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def insert_trajectories_into_database(conn, file_path, type_of_files):
    '''Process data and insert into the database.'''
    chunk_size = 1000
    total_rows = 0
    i = 0
    columns = ['taxi_id', 'date', 'latitude', 'longitude']
    try:
        for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, header=None, names=columns)):
            print ("Path del archivo a insertar : ", file_path)
            i += 1
            columns = ['taxi_id', 'date', 'latitude', 'longitude']
            constraint_name = None
            # Convert columns to the correct data types.
            chunk['taxi_id'] = pd.to_numeric(chunk['taxi_id'], errors='coerce')
            chunk['date'] = pd.to_datetime(chunk['date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
            chunk['latitude'] = pd.to_numeric(chunk['latitude'], errors='coerce')
            chunk['longitude'] = pd.to_numeric(chunk['longitude'], errors='coerce')
            insert_statement = sa.text(f"""
                INSERT INTO {type_of_files} ({', '.join(columns)}) VALUES (:taxi_id, :date, :latitude, :longitude);
                    """)

            rows_inserted = conn.execute(insert_statement, chunk.to_dict(orient='records')).rowcount
            total_rows += rows_inserted
            print(f"Chunk {chunk_index + 1}: Inserted {rows_inserted} rows into '{type_of_files}' table. Total: {total_rows} rows.")
            conn.commit()
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def iterate_files_and_insert_data(path_to_files, type_of_files,files,conn):
    '''Iterate files and insert data into the database.'''
    for file_name in files:
        file_path = os.path.join(path_to_files, file_name)
        print("Path del archivo a iterar: ", file_path)
        if type_of_files == 'taxis':
            insert_taxis_into_database(conn, file_path, type_of_files)
        else:
            insert_trajectories_into_database(conn, file_path, type_of_files)


def main():
    '''Main function.'''
    args = parse_args()
    path_to_files = args.path_to_files
    type_of_files = args.type
    dbname = args.dbname
    host = args.host
    username = args.username
    password= get_password()
    files = os.listdir(path_to_files)
    conn = connect_db(username, host, dbname, password)
    print("Archivos: ", files)
    iterate_files_and_insert_data(path_to_files, type_of_files,files, conn)





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
