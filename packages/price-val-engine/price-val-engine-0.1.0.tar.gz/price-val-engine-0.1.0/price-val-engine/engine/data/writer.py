import csv
from io import StringIO
from engine.conf import settings
import boto3


class BaseWriter(object):
    
    def write(self):
        raise NotImplemented("")


class CSVWriter(BaseWriter):
    
    def __init__(self, file_path, *args, **kwargs) -> None:
        self.file_path = file_path
        self.__args = args
        self.__kwrgs = kwargs
    
    def get_fs(self):
        return open(self.file_path, 'w')
    
    def write(self, items, headers):
        buffer = self.get_fs()
        writer = csv.DictWriter(buffer, fieldnames=headers, *self.__args, **self.__kwrgs)
        writer.writeheader()
        writer.writerows(items)
        buffer.close()
                    
    
class S3CSVWriter(CSVWriter):
    
    def __init__(self, AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, bucket_name, file_key, *args, **kwargs) -> None:
        super().__init__(file_path=file_key, *args, **kwargs)
        
        self.BUCKET = bucket_name
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_KEY = AWS_SECRET_KEY
        self.client = boto3.client('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_KEY)
        
    def get_fs(self):
        self.buffer = StringIO()
        return self.buffer
        #file_object = self.client.get_object(Bucket=self.BUCKET, key=self.file_path)
        #return StringIO(file_object['Body'].read().decode('utf-8'))
    
    def save(self):
        self.buffer.seek(0)
        self.client.put_object(Bucket=self.BUCKET, key=self.file_path, Body=self.buffer.getvalue())
    
    
    def write(self, items):
        super().write(items)
        self.save()
        
    
    
    
    