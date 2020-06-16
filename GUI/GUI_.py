from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import pandas as pd
import operator
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import win32com.client as win
import webbrowser

class GUI:


    def __init__(self):
        self.brand = '都可'
        self.result = ''
        self.result_price=''
        self.price=0
        self.used = 2
        self.send = 2
        self.processor = '都可'
        self.inter_storage = '都可'
        self.solid_storage = '都可'
        self.touch = 2
        
    def choice(self):
        self.brand = rVar1.get()
        if rVar2.get()==0:
            self.price = 2500
        elif rVar2.get() == 1:
            self.price = 4500
        elif rVar2.get() == 2:
            self.price = 6500
        elif rVar2.get() == 3 or rVar2.get() == 4:
            self.price = 8500
        elif rVar2.get() == 5:
            self.price=0
        self.used = rVar3.get()
        self.send = rVar4.get()
        self.processor = rVar5.get()
        self.inter_storage = rVar6.get()
        self.solid_storage = rVar7.get()
        self.touch = rVar8.get()
        
    def select(self):
        self.match={self.brand:'Brands',self.inter_storage:'Internal Storage',self.send:'Shop Type',self.used:'used',self.processor:'Processor',self.solid_storage:'Solid State Storage',self.touch:'Touch control'}
        df = pd.read_csv('summary2.0.csv', encoding="utf_8_sig")
        result=df
        if self.price == 8500 and rVar2.get() == 3:
            result = result[(result['Price'] <= 8500) & (result['Price'] > 6500)]
        elif self.price == 8500 and rVar2.get() == 4:
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
                    if index==1 and result[result['Brands']=='联想'].empty==False:
                        result=result[result['Brands']=='联想']
                    elif index==2 and result[result['Processor']=='i5'].empty==False:
                        result=result[result['Processor']=='i5']
                    elif index==3 and result[result['Internal Storage']=='8G'].empty==False:
                        result=result[result['Internal Storage']=='8G']
                    elif index==4 and result[result['Solid State Storage']=='512G'].empty==False:
                        result=result[result['Solid State Storage']=='512G'] 
                    elif index==5 and result[result['Touch control']==0].empty==False:
                        result=result[result['Touch control']==0] #从满足的品牌中找到最合适的，基本满足配置
                    continue
            else:
                result_pre=result       
        return (result,result_price)
        
    def set_Radiobutton(self, frame, labelname, tagnames, contain, row):
        Label(frame,text=labelname).grid(row=row,column=0,sticky=W)
        if isinstance(contain,IntVar):
            contain.set(len(tagnames)-1)
            for index,tagname in enumerate(tagnames):
                Radiobutton(frame, text=tagname, variable=contain, value=index, command=self.choice).grid(row=row, column=index + 1, sticky=W)
        else:
            contain.set('都可')
            for index,tagname in enumerate(tagnames):
                Radiobutton(frame, text=tagname, variable=contain, value=tagnames[index], command=self.choice).grid(row=row, column=index + 1, sticky=W)
    
    def check(self):
        result,result_price = self.select()
        if result[result['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False).empty==False:
            result=result[result['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False)
        if result_price[result_price['Favorable rate']>=90].sort_values(by=['Sale', 'Favorable rate'],ascending=False).empty==False:
            result_price = result_price[result_price['Favorable rate'] >= 90].sort_values(by=['Sale', 'Favorable rate'], ascending=False)

        number_result_href = result.iloc[0, -9]
        number_result = re.search(r'[0-9]+', number_result_href).group()
        number_price_href = result_price.iloc[0, -9]
        number_price = re.search(r'[0-9]+', number_price_href).group()
        if os.path.exists(number_result + '.jpg') and os.path.exists(number_price + '.jpg'):
            jpg1 = number_result + '.jpg'
            jpg2 = number_price + '.jpg'
        elif os.path.exists(number_result + '.jpg') == False and os.path.exists(number_price + '.jpg'):
            jpg1 = 'replace.jpg'
            jpg2 = number_price + '.jpg'
        elif os.path.exists(number_result + '.jpg') and os.path.exists(number_price + '.jpg') == False:
            jpg1 = number_price + '.jpg'
            jpg2 = 'replace.jpg'
        else:
            jpg1=jpg2='replace.jpg'
        img3=Image.open(jpg1)
        img3=img3.resize((200, 200), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(img3)
        label1.img = img3
        label1.config(image=img3)
        label1_brand.config(text=result.iloc[0,0] + ' ' + result.iloc[0, 1])
        label1_href.config(text='http:'+result.iloc[0, -9])
        img4=Image.open(jpg2)
        img4=img4.resize((200, 200), Image.ANTIALIAS)
        img4 = ImageTk.PhotoImage(img4)
        label2.img = img4
        label2.config(image=img4)
        label2_brand.config(text=result_price.iloc[0,0] + ' ' + result_price.iloc[0, 1])
        label2_href.config(text='http:'+result_price.iloc[0, -9])
        self.result = result
        self.result_price=result_price
    
    def rada(self):
        if isinstance(self.result,str):
            df = pd.read_csv('summary2.0.csv', encoding="utf_8_sig")
            rad_result = df.iloc[2,:]
            rad_price = df.iloc[45,:]
        else:
            rad_result = self.result.iloc[0,:]
            rad_price = self.result_price.iloc[0,:]
        labels = np.array([u'运存', u'处理器', u'固态存储', u'价格', '好评度']) 
        dataLenth = 5 
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        if not (rad_result['Model']==rad_price['Model'] and rad_result['Price']==rad_price['Price']):
            if pd.isna(rad_result['Internal Storage']):
                rad_result['Internal Storage'] = '8G'
            if pd.isna(rad_result['Processor']):
                rad_result['Processor'] = 'i5'
            if pd.isna(rad_result['Solid State Storage']):
                rad_result['Solid State Storage'] = '512G'
            if pd.isna(rad_result['Solid State Storage'])=='1T':
                rad_result['Solid State Storage'] = '1024G'
            if pd.isna(rad_result['Solid State Storage'])=='2T':
                rad_result['Solid State Storage'] = '2048G'
            if rad_result['Internal Storage'] == '128G+1T' or rad_result['Internal Storage'][:-1] == '128G+2T' or rad_result['Internal Storage'][:-1] == '256G+2T':
                rad_result['Internal Storage'] = '1024G'
            
            if pd.isna(rad_price['Internal Storage']):
                rad_price['Internal Storage'] = '8G'
            if pd.isna(rad_price['Processor']):
                rad_price['Processor'] = 'i5'
            if pd.isna(rad_price['Solid State Storage']):
                rad_price['Solid State Storage'] = '512G'
            if pd.isna(rad_price['Solid State Storage'])=='1T':
                rad_price['Solid State Storage'] = '1024G'
            if pd.isna(rad_price['Solid State Storage'])=='2T':
                rad_price['Solid State Storage'] = '2048G'
            if rad_price['Internal Storage'] == '128G+1T' or rad_price['Internal Storage'][:-1] == '128G+2T' or rad_price['Internal Storage'][:-1] == '256G+2T':
                rad_price['Internal Storage'] = '1024G'
            data_radar1 = np.array([int(rad_result['Internal Storage'][:-1])/16, int(rad_result['Processor'][1:])/5, int(rad_result['Solid State Storage'][:-1])/512, int(rad_result['Price'])/4500, int(rad_result['Favorable rate'])/100])
            data_radar2 = np.array([int(rad_price['Internal Storage'][:-1])/16, int(rad_price['Processor'][1:])/5, int(rad_price['Solid State Storage'][:-1])/512, int(rad_price['Price'])/4500, int(rad_price['Favorable rate'])/100])
            angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False) 
            data_radar1 = np.concatenate((data_radar1, [data_radar1[0]])) 
            data_radar2 = np.concatenate((data_radar2, [data_radar2[0]])) 
            angles = np.concatenate((angles, [angles[0]]))
            plt.polar(angles, data_radar1, 'ro-', linewidth=1)  
            plt.polar(angles, data_radar2, 'bo-', linewidth=1) 
            plt.thetagrids(angles * 180/np.pi, labels)
            plt.fill(angles, data_radar1, facecolor='r', alpha=0.25) 
            plt.fill(angles, data_radar2, facecolor='b', alpha=0.25)
            plt.ylim(0, 2)
            plt.legend([rad_result['Model'],rad_price['Model']],bbox_to_anchor=(-0.4, 0.8), loc="center left")
            plt.title(u'性能')
            plt.show()
        else:
            if pd.isna(rad_result['Internal Storage']):
                rad_result['Internal Storage'] = '8G'
            if pd.isna(rad_result['Processor']):
                rad_result['Processor'] = 'i5'
            if pd.isna(rad_result['Solid State Storage']):
                rad_result['Solid State Storage'] = '512G'
            if pd.isna(rad_result['Solid State Storage'])=='1T':
                rad_result['Solid State Storage'] = '1024G'
            if pd.isna(rad_result['Solid State Storage'])=='2T':
                rad_result['Solid State Storage'] = '2048G'
            if rad_result['Internal Storage'] == '128G+1T' or rad_result['Internal Storage'][:-1] == '128G+2T' or rad_result['Internal Storage'][:-1] == '256G+2T':
                rad_result['Internal Storage'] = '1024G'

            data_radar1 = np.array([int(rad_result['Internal Storage'][:-1])/16, int(rad_result['Processor'][1:])/5, int(rad_result['Solid State Storage'][:-1])/512, int(rad_result['Price'])/4500, int(rad_result['Favorable rate'])/100])
            angles = np.linspace(0, 2*np.pi, dataLenth, endpoint=False) 
            data_radar1 = np.concatenate((data_radar1, [data_radar1[0]])) 
            angles = np.concatenate((angles, [angles[0]]))
            plt.polar(angles, data_radar1, 'ro-', linewidth=1)  
            plt.thetagrids(angles * 180/np.pi, labels)
            plt.fill(angles, data_radar1, facecolor='r', alpha=0.25) 
            plt.ylim(0, 2)
            plt.title(u'性能')
            plt.show()
    
    def intro(self):
        if isinstance(self.result,str):
            df = pd.read_csv('summary2.0.csv', encoding="utf_8_sig")
            self.result = df.iloc[2,:]
            self.result_price = df.iloc[45,:]
        else:
            self.result_price = self.result_price.iloc[0,:]
            self.result=self.result.iloc[0,:]
        if not (self.result['Model']==self.result_price['Model'] and self.result['Price']==self.result_price['Price']):
            if (not pd.isna(self.result['Screen size']) and self.result['Screen size']!=' ') and (self.result['Processor']!=' ' and not pd.isna(self.result['Processor'])):
                msg_left = '在您左手边,' + str(self.result['Brands']) + '的这款电脑' + ',是最大程度上可以满足您所有要求的选择,' + '处理器是' + str(self.result['Processor']) + ',' + '屏幕是' + str(self.result['Screen size']) + '英寸' + ',' + str(self.result['Price']) + '的价格也是很合理了呢。'
            elif (pd.isna(self.result['Screen size']) or self.result['Screen size']==' ') and (self.result['Processor']!=' ' and pd.isna(self.result['Processor'])==False):
                msg_left = '在您左手边,' + self.result['Brands'] + '的这款电脑' + ',是最大程度上可以满足您所有要求的选择,' + '处理器是' + self.result['Processor'] + ',' + str(self.result['Price']) + '的价格也是很合理了呢。'
            elif (pd.isna(self.result['Processor']) or self.result['Processor']==' ') and (self.result['Screen size']!=' ' and pd.isna(self.result['Screen size'])==False):
                msg_left = '在您左手边,' + self.result['Brands'] + '的这款电脑' + ',是最大程度上可以满足您所有要求的选择,' + '屏幕是' + str(self.result['Screen size']) + ',' + str(self.result['Price']) + '的价格也是很合理了呢。'
            else:
                msg_left = '在您左手边,' + self.result['Brands'] + '的这款电脑' + ',是最大程度上可以满足您所有要求的选择,' + ',' + str(self.result['Price']) + '的价格也是很合理了呢。小姜能力有限，如果想了解更多详细信息就点击图片下方的链接吧。'

            
            if (not pd.isna(self.result_price['Processor']) and self.result_price['Processor'] != ' ') and (self.result_price['Screen size'] == ' ' or pd.isna(self.result_price['Screen size'])):
                msg_right='在您右手边,' + self.result_price['Brands'] + '的这款电脑' + ',是根据您的价格需求找到的大众最认可的电脑,可以考虑一下,' + '处理器是' + self.result_price['Processor'] + ',' + '价格当然也会满足您的要求啦,只要'+str(self.result_price['Price'])+',只要'+str(self.result_price['Price'])+',真的不考虑一下吗？'
            elif (not pd.isna(self.result_price['Screen size']) and self.result_price['Screen size']!=' ') and (self.result_price['Processor']!=' ' and pd.isna(self.result_price['Processor'])==False):
                msg_right='在您右手边,' + self.result_price['Brands'] + '的这款电脑' + ',是根据您的价格需求找到的大众最认可的电脑,可以考虑一下,' + '屏幕是' + str(self.result_price['Screen size']) + ',' + '价格当然也会满足您的要求啦,只要'+str(self.result_price['Price'])+',只要'+str(self.result_price['Price'])+',真的不考虑一下吗？'
            elif (pd.isna(self.result_price['Processor']) or self.result_price['Processor']==' ') and (self.result_price['Screen size']==' ' or pd.isna(self.result_price['Screen size'])):
                msg_right = '在您右手边,' + self.result_price['Brands'] + '的这款电脑' + ',是根据您的价格需求找到的大众最认可的电脑,可以考虑一下,' + ',' + '只要' + str(self.result_price['Price']) + ',只要' + str(self.result_price['Price']) + ',小姜能力有限，如果想了解更多内容就请点击图片下方的链接吧。'
            else:
                msg_right='在您右手边,' + self.result_price['Brands'] + '的这款电脑' + ',是根据您的价格需求找到的大众最认可的电脑,可以考虑一下,' + '处理器是' + str(self.result_price['Processor']) + ','+'屏幕是' + str(self.result_price['Screen size']) + ',' + '价格当然也会满足您的要求啦,只要'+str(self.result_price['Price'])+',只要'+str(self.result_price['Price'])+',真的不考虑一下吗？'
            speak = win.Dispatch("SAPI.SpVoice")
            speak.Speak(msg_left)
            speak.Speak(msg_right)
        else:
            if (pd.isna(self.result['Screen size']) or self.result['Screen size']==' ') and (self.result['Processor']!=' ' and pd.isna(self.result['Processor'])==False):
                msg = '接下来为您推荐的这款商品不仅具有超高人气，并且可以尽可能满足您所有要求。' + '他就是' + '价值'+str(self.result['Price'])+ '的这一款' + self.result['Brands'] +'电脑，'+ '处理器是' + self.result['Processor'] + ',不要犹豫啦，快点动手吧，更多详情尽在链接中，点击有惊喜'
            elif (pd.isna(self.result['Processor']) or self.result['Processor']==' ') and (self.result[0,-3]!=' ' and pd.isna(self.result['Screen size'])==False):
                msg = '接下来为您推荐的这款商品不仅具有超高人气，并且可以尽可能满足您所有要求。' + '他就是' + '价值'+str(self.result['Price'])+ '的这一款' + self.result['Brands'] +'电脑，'+ '屏幕尺寸是' + str(self.result['Screen size']) + ',不要犹豫啦，快点动手吧，更多详情尽在链接中，点击有惊喜'
            elif (pd.isna(self.result['Screen size']) or self.result['Screen size']==' ') and (self.result['Processor']==' ' or pd.isna(self.result['Screen size'])):
                msg = '接下来为您推荐的这款商品不仅具有超高人气，并且可以尽可能满足您所有要求。' + '他就是' + '价值'+str(self.result['Price'])+ '的这一款,小姜能力有限，如果想了解更多内容就请点击图片下方的链接吧。'
            else:
                msg = '接下来为您推荐的这款商品不仅具有超高人气，并且可以尽可能满足您所有要求。' + '他就是' +'价值'+str(self.result['Price'])+ '的这一款' + self.result['Brands'] +'电脑，' + '处理器是' + self.result['Processor'] + '屏幕是' + str(self.result['Screen size']) + '英寸' + ',不要犹豫啦，快点动手吧，更多详情尽在链接中，点击有惊喜'
            speak = win.Dispatch("SAPI.SpVoice")
            speak.Speak(msg)
    
    def open_url(self,url):
        webbrowser.open(url)
        
        
GUI=GUI()
window=Tk()
window.title('Recommended laptops')
frame1=Frame(window)
frame1.grid()
Label(frame1,text='又到了要换电脑的日子，你选好了吗？').grid()
frame1=Frame(window)
frame1.grid(row=1)
rVar1 = StringVar()
GUI.set_Radiobutton(frame1, "品牌", ['联想', '惠普','戴尔', 'Apple', '华为',  '都可'], rVar1, 1)
rVar2 = IntVar()
GUI.set_Radiobutton(frame1,"价格",['500-2500','2500-4500','4500-6500','6500-8500','8500以上','都可'],rVar2,2)
rVar3 = IntVar()
GUI.set_Radiobutton(frame1,"二手",['否','是','都可'],rVar3,3)
rVar4 = IntVar()
GUI.set_Radiobutton(frame1,"物流",['非京东','京东','都可'],rVar4,4)

rVar5 = StringVar()
GUI.set_Radiobutton(frame1,"处理器",['R5','R7','i5','i7','都可'],rVar5,5)
rVar6=StringVar()
GUI.set_Radiobutton(frame1,"内存",['4G','8G','16G','都可'],rVar6,6)
rVar7=StringVar()
GUI.set_Radiobutton(frame1, "固态", ['128G', '256G', '512G', '1T', '都可'], rVar7, 7)
rVar8 = IntVar()
GUI.set_Radiobutton(frame1,"触控",['非触控','触控','都可'],rVar8,8)
frame2 = Frame(window)
frame2.grid(row=2)
Button(frame2,text='我选好啦！',command=GUI.check).grid(row=0)
frame3 = Frame(window)
frame3.grid(row=3)
img1=Image.open('100005171461.jpg')
img1=img1.resize((200, 200), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1)
label1 = Label(frame3, image=img1)
label1.img = img1
label1.grid(row=2, column=0)
label1_brand = Label(frame3, text='联想 小新13pro')
label1_brand.grid(row=3,column=0)
label1_href = Label(frame3, text='http://item.jd.com/100005171461.html')
label1_href.grid(row=4,column=0)
label1_href.bind("<Button-1>", lambda event : GUI.open_url(label1_href["text"]))

Button(frame3, text='性能雷达', command=GUI.rada).grid(row=2, column=1)
Button(frame3,text='收听介绍',command=GUI.intro).grid(row=3,column=1)


img2=Image.open('100005603836.jpg')
img2=img2.resize((200, 200), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img2)
label2 = Label(frame3, image=img2)
label2.img = img2
label2.grid(row=2, column=2)
label2_brand = Label(frame3, text='惠普 暗夜精灵5')
label2_brand.grid(row=3,column=2)
label2_href = Label(frame3, text='http://item.jd.com/100005603836.html')
label2_href.grid(row=4,column=2)
label2_href.bind("<Button-1>", lambda event: GUI.open_url(label2_href["text"]))
frame4 = Frame(window)
frame4.grid(row=4)
Label(frame4,text='10195000441 姜琼').grid()
window.mainloop()