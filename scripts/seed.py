'''CLI script to upload data to the database.'''
import os
import sys
import pdb
import getpass
import argparse
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, text
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

# 3. Process data and insert into the database
def insert_data_into_database(conn, file_path, type_of_files):
    '''Process data and insert into the database.'''

    chunk_size = 1000
    total_rows = 0
    i = 0
    if type_of_files == 'taxis':
        columns = ['id', 'plate']
    elif type_of_files == 'trajectories':
        columns = ['taxi_id', 'date', 'latitude', 'longitude']
    try:
        for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, header=None, names=columns)):
            print ("Path del archivo a insertar : ", file_path)
            i += 1
            if type_of_files == 'taxis':
                columns = ['id', 'plate']
                constraint_name = 'id'
                chunk['id'] = pd.to_numeric(chunk['id'], errors='coerce')
                #sa.text() para crear una consulta SQL con la cláusula ON CONFLICT.
                #:id y :plate son marcadores de posición para los valores que se insertarán en la tabla.
                insert_statement = sa.text(f"""
                    INSERT INTO {type_of_files} ({', '.join(columns)}) VALUES (:id, :plate) ON CONFLICT ({constraint_name}) DO UPDATE SET {columns[0]} = EXCLUDED.{columns[0]}
                    """)

            elif type_of_files == 'trajectories':
                columns = ['taxi_id', 'date', 'latitude', 'longitude']
                constraint_name = None
                # Convertir las columnas a los tipos de datos correctos.
                chunk['taxi_id'] = pd.to_numeric(chunk['taxi_id'], errors='coerce')
                chunk['date'] = pd.to_datetime(chunk['date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
                chunk['latitude'] = pd.to_numeric(chunk['latitude'], errors='coerce')
                chunk['longitude'] = pd.to_numeric(chunk['longitude'], errors='coerce')
                insert_statement = sa.text(f"""
                    INSERT INTO {type_of_files} ({', '.join(columns)}) VALUES (:taxi_id, :date, :latitude, :longitude);
                     """)
            # Insertar los datos en la base de datos.
            #execute() de SQLAlchemy insertar los datos como una lista de diccionarios.
            #orient='records' para convertir el DataFrame en una lista de diccionarios.
            rows_inserted = conn.execute(insert_statement, chunk.to_dict(orient='records')).rowcount
            total_rows += rows_inserted
            print(f"Chunk {chunk_index + 1}: Inserted {rows_inserted} rows into '{type_of_files}' table. Total: {total_rows} rows.")
            #conn.commit() para confirmar la transacción y guardar los cambios en la base de datos.
            conn.commit()
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

def iterate_files_and_insert_data(path_to_files, type_of_files,files,conn):
    '''Iterate files and insert data into the database.'''
    for file_name in files:
        file_path = os.path.join(path_to_files, file_name)
        print("Path del archivo a iterar: ", file_path)
        insert_data_into_database(conn, file_path, type_of_files)


def main():
    args = parse_args()
    path_to_files = args.path_to_files
    type_of_files = args.type
    dbname = args.dbname
    host = args.host
    username = args.username
    files = os.listdir(path_to_files)
    conn = connect_db(username, host, dbname)
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
