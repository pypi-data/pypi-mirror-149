import os
import uuid
import boto3
import psycopg2

from typing import Any, Dict, List, Tuple


class SimpleStorageService:
    """
    Util class for AWS S3 file and folder management

    Attributes:
        session (boto3.Session): session to connect to aws
        bucket (str): range name of files and folder
        resource (Any): instance connected to aws to reference aws s3
    """
    def __init__(self) -> None:
        self._session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self._bucket = os.getenv("BUCKET")
        self._resource = self._session.resource('s3')

    def push(self, object:Any, path:str, hash:bool=False, extension:str=None) -> str:
        """        
        Method to publish files to storage
        
        Parameters:
            object (Any): file content to be published
            path (str): remote path of the file to be published
            hash (bool | None): defines whether the new file will have a dynamic name
            extension (str | None): defines whether the new file will have a fixed extension

        Returns:
            str: returns the remote path of the published file
        """
        if hash:
            path += f'/{uuid.uuid4()}.{extension}'
        self._resource.Object(self._bucket, path).put(Body=object)
        return path

    def get_bytes(self, path:str) -> Any:
        """        
        Method to get a byte string from a file
        
        Parameters:
            path (str): remote path of the file to be published

        Returns:
            any: return the bytes of the file
        """
        bucket = self._resource.Bucket(self._bucket)
        return bucket.Object(path).get().get('Body').read()

class PostgresRelationalDatabaseService:
    """
    Useful class to manage the specific relational database service for postgres

    Attributes:
        connection (Any): database connection
    """
    def __init__(self) -> None:
        self._connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )

    def _convert_columns_to_tuple(self, columns:Any) -> Tuple[str, Tuple[Any]]:
        if type(columns) == dict:
            keys = list(columns.keys())
            typed_key = ['%s' for _ in range(len(keys))]
            return ', '.join(keys), list(columns.values()), ', '.join(typed_key)
        else:
            return ', '.join(columns), None, ', '.join(['%s' for _ in range(len(columns))])

    def create(self, table_name:str, return_column:str='id', **columns:Dict) -> int:
        """        
        Function to create record in a table in database
        
        Parameters:
            table_name (str): table name to insert
            return_column (str | None): column name to return after inserted
            columns (**kwards): name of columns to be inserted
            
        Returns:
            int: returns the id of the current run
        """
        keys, values, typed_key = self._convert_columns_to_tuple(columns)
        return_value = None

        with self._connection.cursor() as cursor:
            cursor.execute(
                query=f'INSERT INTO {table_name} ({keys}) VALUES ({typed_key}) RETURNING {return_column};',
                vars=values
            )
            return_value = cursor.fetchone()[0]
            self._connection.commit()
        
        return return_value

    def create_many(self, table_name:str, column_name:List[str], values:List[Tuple]) -> None:
        """        
        Function to create multiple records in a table in the database
        
        Parameters:
            table_name (str): table name to insert
            column_name (List[str]): columns to be inserted
            values (List[Tuple]): list of values for columns, each row must be a tuple following the special column order
        """
        keys, _, typed_key = self._convert_columns_to_tuple(column_name)
        with self._connection.cursor() as cursor:
            cursor.execute(
                query=f'INSERT INTO {table_name} ({keys}) VALUES ({typed_key});', 
                vars=values
            )
            self._connection.commit()
