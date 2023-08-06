from engine import utils
from engine.conf import settings
from engine.validations.base_rules import BaseRule


EMPTY_VALUES = settings.EMPTY_VALUES or (None, "", [], (), {})

class NullNegativeZeroValidationRule(BaseRule):
    name = 'null-negative-zero-rule'
    message = "Invalid Value"
    sevearity = 'HIGH'
    
    def is_valid(self, item, target_field="final_liquidation_price"):
        print(item)
        value = item[target_field]
        if value in EMPTY_VALUES:
            self.message = "Null Value"
            return False
        if not utils.is_number(value):
            self.message = "Number value Expected"
            return False
        if float(value) == 0.0:
            self.message = "Zero Value"
            return False
        if float(value) < 0.0:
            self.message = "Negative Value"
            return False
        return True

class OutOfRangeValidationRule(BaseRule):
    name = "out-of-range-rule"
    message = "Out of Range"
    sevearity = 'HIGH'
    
    min_value = settings.GEN_VAL_OUT_OF_RANGE_VALUE.get('min_value') or  100000.0
    max_value = settings.GEN_VAL_OUT_OF_RANGE_VALUE.get('max_value') or 10000000.0
    
    def cal_min_value(self):
        return 100
    
    
    
    def is_valid(self, item, target_field="final_liquidation_price"):
        value = item[target_field]
        min_value =  self.cal_min_value()
        if self.min_value <= float(value) > self.max_value:
            self.message = f"{target_field} {value} out of range. <min{self.min_value}> - <max{self.max_value}>"
            return False
        
        return True

