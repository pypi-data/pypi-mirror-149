from engine.validations.base_rules import BaseRule


class DeltaPercentageFromLastDayRule(BaseRule):
    name = "last-price-revision-delta-percentage-rule"
    sevearity = None
    message = "Delta Range greater than +-5% from Last Day. Actual is {1}%"
    
    def is_valid(self, item, target_field="final_liquidation_price"):
        final_lp = float(item['final_liquidation_price'])
        lp = float(item['lp'])
        
        delta = final_lp - lp
        delta_pct = round(100 * delta / lp ,0)
        
        if  -5 <= delta_pct  <= 5:
            return True
        
        elif  -15 <= delta_pct  <= 15:
            self.sevearity = 'LOW'
            self.message= self.message.format("15%", delta_pct) 
            return False
        
        elif  -20 <= delta_pct  <= 20:
            self.sevearity = 'MEDIUM'
            self.message = self.message.format("20%", delta_pct) 
            return False
        
        else:
            self.sevearity = 'HIGH'
            self.message= "Delta is not allowed more than 20%. Actual is {}".format(delta_pct) 
            return False    
    
    
class UnknownRule(BaseRule):
    name = "unknown-rule"
    sevearity = None
    message = "Delta Range greater than +-5% from Last Day. Actual is {1}%"
    
    def is_valid(self, item, target_field="final_liquidation_price"):
        final_lp = float(item['final_liquidation_price'])
        lp = float(item['lp'])
        
        delta = final_lp - lp
        delta_pct = round(100 * delta / lp ,0)
        
        if  -5 <= delta_pct  <= 5:
            return True
        
        elif  -15 <= delta_pct  <= 15:
            self.sevearity = 'LOW'
            self.message= self.message.format("15%", delta_pct) 
            return False
        
        elif  -20 <= delta_pct  <= 20:
            self.sevearity = 'MEDIUM'
            self.message = self.message.format("20%", delta_pct) 
            return False
        
        else:
            self.sevearity = 'HIGH'
            self.message= "Delta is not allowed more than 20%. Actual is {}".format(delta_pct) 
            return False    
    