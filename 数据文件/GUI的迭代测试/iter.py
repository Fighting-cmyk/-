import pandas as pd
import numpy as np
class a:
    
    def select(self):
        for brand in ['联想', '惠普','戴尔', 'Apple', '华为', '都可']:
            self.brand=brand
            for inter in ['4G','8G','16G','都可']:
                self.inter_storage=inter
                for solid in ['128G', '256G', '512G', '1T', '都可']:
                    self.solid_storage=solid
                    for touch in [0,1,2]:
                        self.touch=touch
                        for processor in ['R5','R7','i5','i7','都可']:
                            self.processor=processor
                            for send in [0,1,2]:
                                self.send=send
                                for used in [0,1,2]:
                                    self.used=used
                                    for price in [2500,4500,6500,8500,1,0]:
                                        self.price=price
                                        self.match={self.brand:'Brands',self.inter_storage:'Internal Storage',self.send:'Shop Type',self.used:'used',self.processor:'Processor',self.solid_storage:'Solid State Storage',self.touch:'Touch control'}
                                        df = pd.read_csv('summary2.0.csv', encoding="utf_8_sig")
                                        result_init=df
                                        result=df
                                        if self.price == 8500:
                                            result = result[(result['Price'] <= 8500) & (result['Price'] > 6500)]
                                        elif self.price == 1:
                                            result = result[(result['Price'] > 8500)]
                                        elif self.price==0:
                                            result = result
                                        else:
                                            result = result[(result['Price'] <= self.price) & (result['Price'] > self.price-2000)]
                                        result_price=result
                                        result_pre=result
                                        for index,i in enumerate([self.used,self.brand, self.processor, self.inter_storage, self.solid_storage,self.touch,self.send]):
                                            if i!='都可' and i!='都不要' and i!=2:
                                                result = result[result[self.match[i]] == i]
                                            if i == '都不要':
                                                result = result[(result['Brands'] != '联想') & (result['Brands'] != '惠普') & (result['Brands'] != '戴尔') & (result['Brands'] != 'Apple') & (result['Brands'] != '华为')]
                                            if result.empty == True:
                                                if result_pre.shape[0]==1:
                                                    result=result_pre      #从满足的品牌中找到最合适的，基本满足配置
                                                    break
                                                else:
                                                    result=result_pre    
                                                    continue
                                            else:
                                                result_pre=result
                                        if result[result['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False).empty==False:
                                            result=result[result['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False)
                                        if result_price[result_price['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False).empty==False:
                                            result_price=result_price[result_price['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False)
                                        x = pd.concat(result, result_configuration)
                                        x1 = pd.concat(x1, result_price)
                                        with open("l.txt", 'a', encoding='utf_8_sig') as f:
                                            f.write(x1)
x=a()
x.select()