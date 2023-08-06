from engine.data import reader, writer
from engine.exceptions import ImproperlyConfigured
from engine.conf.settings import VALIDATION_PIPELINES
from engine.validations.base_rules import *

__all__ = [
    "Engine"
 ]


class BaseValidationEngine(object):
    validation_rules = VALIDATION_PIPELINES
    data_reader = None
    data_writer = None
    
    def __init__(self, 
        input_file_path, 
        output_file_path,
        S3_config=None
        ) -> None:
        
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.S3_config = S3_config or {}
        
        self.items = []

    def all(self):
        if self.data_reader is None:
            raise ImproperlyConfigured(
                "Invalid Data Reader class !"
            )
        rows = []
        
        for row in self.data_reader(
                    file_path=self.input_file_path,
                    **self.S3_config
                ).read():
            rows.append(row)
        return rows
    
    def __import_model(self, name:str):
        components = name.split('.')
        module = __import__(components[0])
        for comp in components[1:]:
            module = getattr(module, comp)        
        return module
        
    
    def validate(self, row):
        for validation_cls in self.validation_rules:
            klass = self.__import_model(validation_cls)
            validation = klass()
            if not validation.is_valid(row):
                return False, validation.errors
        return True, {"category": "success", "sevearity": "",  "reason": "success"}
    
    def validate_all(self):
        for item in self.all():
            is_valid, response = self.validate(item)
            print(response)
            self.items.append({**item, 'is_valid': is_valid, **response})
        return self.items
    
    def save(self):
        if self.data_writer is None:
            raise ImproperlyConfigured(
                "Invalid Data Writer class"
            )  
        if len(self.items):
            fieldnames = list(self.items[0].keys())
            print(fieldnames)
            self.data_writer(
                file_path=self.output_file_path,
                **self.S3_config
            ).write(self.items, headers=fieldnames)
        
    
class ValidationEngine(BaseValidationEngine):
    data_reader = reader.CSVReader
    data_writer = writer.CSVWriter
    

Engine = ValidationEngine