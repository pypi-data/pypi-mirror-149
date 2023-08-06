import csv
from io import StringIO
from engine.exceptions import ImproperlyConfigured
from engine.conf import settings
import boto3


class BaseReader(object):
    
    def read(self):
        raise NotImplemented("")


class CSVReader(BaseReader):
    
    def __init__(self, file_path, *args, **kwargs) -> None:
        print(file_path)
        self.file_path = file_path
        self.__args = args
        self.__kwrgs = kwargs
    
    def get_fs(self):
        return open(self.file_path)
            
    def read(self):
        fs = self.get_fs()
        for row in csv.DictReader(fs, *self.__args, **self.__kwrgs):
            yield row
        fs.close()
                    
    
class S3CSVReader(CSVReader):
    
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, bucket_name, file_key, *args, **kwargs) -> None:
        super().__init__(file_path=file_key, *args, **kwargs)
        
        self.BUCKET = bucket_name
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_KEY = AWS_SECRET_KEY
        self.client = boto3.client('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_KEY)
        
    def get_fs(self):
        file_object = self.client.get_object(Bucket=self.BUCKET, key=self.file_path)
        return StringIO(file_object['Body'].read().decode('utf-8'))
    
    
class GCSCSVReader(CSVReader):
    
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, bucket_name, file_key, *args, **kwargs) -> None:
        super().__init__(file_path=file_key, *args, **kwargs)
        
        self.BUCKET = bucket_name
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_KEY = AWS_SECRET_KEY
        self.client = boto3.client('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_KEY)
        
    def get_fs(self):
        file_object = self.client.get_object(Bucket=self.BUCKET, key=self.file_path)
        return StringIO(file_object['Body'].read().decode('utf-8'))
    
    
    