# 著作者：叶凯文
# Author: YE KAIWEN
# 版权归著作者叶凯文所有
# Copyright (c) 2022 YE KAIWEN. All Rights Reserved.

import pandas as pd

class NormalTrade:
    def __init__(self,buyfee,sellfee,stopprofit=None,stoploss=None):
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.extralogics=[]
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high'])}
                    revcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.buyfee,sellfee=self.sellfee)
                    revenue=revcalc.calculation(refer=row['refer'])
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold==False:
                        status = 'selling'
                        orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                revenue = revcalc.calculation(refer=row['refer'])
                hold = row['holdlogic']
                for logic in self.extralogics:
                    hold = hold & logic.calc(revenue)
                if hold == False:
                    status = 'selling'
                    orderday = 0
            elif status=='selling':
                orderday+=1
                if row['ordersell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['ordersell'],row['low'])
                    orderinfo['revenue']=revcalc.calculation(refer=orderinfo['sellbid'])
                    orderinfo['cost'] =revcalc.cost(sellbid=orderinfo['sellbid'])
                    orderinfo['revmax'],orderinfo['revmin']=NormalMaxMin(data=data.loc[orderinfo['buyinx']:orderinfo['sellinx'],['high','low','ordersell']],revcalc=revcalc)
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    revenue=revcalc.calculation(refer=row['refer'])
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold:
                        status = 'open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high'])}
                if status=='open':
                    revcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.buyfee,sellfee=self.sellfee)
                    revenue=revcalc.calculation(refer=row['refer'])
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold==False:
                        status = 'selling'
                        orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                revenue = revcalc.calculation(refer=row['refer'])
                hold = row['holdlogic']
                for logic in self.extralogics:
                    hold = hold & logic.calc(revenue)
                if hold == False:
                    status = 'selling'
                    orderday = 0
            elif status=='selling':
                orderday+=1
                if row['callsell']<=row['open']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=row['open']
                    status='close'
                elif row['consell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['consell'],row['low'])
                    status='close'
                if status=='close':
                    orderinfo['revenue'] = revcalc.calculation(refer=orderinfo['sellbid'])
                    orderinfo['cost'] = revcalc.cost(sellbid=orderinfo['sellbid'])
                    ansdata=data[['high','low']][orderinfo['buyinx']:orderinfo['sellinx']]
                    ansdata['ordersell']=data['refer'].shift()[orderinfo['buyinx']:orderinfo['sellinx']]
                    orderinfo['revmax'],orderinfo['revmin']=NormalMaxMin(ansdata,revcalc=revcalc)
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    revenue = revcalc.calculation(refer=row['refer'])
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold:
                        status = 'open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

class MarginTrade:
    def __init__(self,buyfee,sellfee,interest,margin,guarantee,stopprofit=None,stoploss=None):
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.interest=interest/360
        self.margin=margin
        self.guarantee=guarantee
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','closeout','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','closeout','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    holdday=0
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high'])}
                    revcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.buyfee,sellfee=self.sellfee,margin=self.margin,interest=self.interest)
                    revenue, guarantee=revcalc.calculation(refer=row['refer'],holdday=holdday)
                    if guarantee<self.guarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                if guarantee < self.guarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                if row['closeout']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['closeout'],row['low'])
                    orderinfo['revenue'],orderinfo['guarantee']=revcalc.calculation(refer=orderinfo['sellbid'],holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    orderinfo['closetype']='margin-closeout'
                    orderinfo['revmax'],orderinfo['revmin']=MarginMaxMin(data=data.loc[orderinfo['buyinx']:orderinfo['sellinx'],['high','low','ordersell']],revcalc=revcalc)
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
            elif status=='selling':
                holdday += 1
                orderday+=1
                if row['ordersell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['ordersell'],row['low'])
                    orderinfo['revenue'], orderinfo['guarantee'] = revcalc.calculation(refer=orderinfo['sellbid'], holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    orderinfo['closetype']='sell-close'
                    orderinfo['revmax'], orderinfo['revmin'] = MarginMaxMin(data=data.loc[orderinfo['buyinx']:orderinfo['sellinx'], ['high', 'low', 'ordersell']], revcalc=revcalc)
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                    if guarantee < self.guarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','closeout','callbuy','callsell','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','closeout','callbuy','callsell','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    holdday=0
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    holdday=0
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high'])}
                if status=='open':
                    revcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.buyfee,sellfee=self.sellfee,margin=self.margin,interest=self.interest)
                    revenue, guarantee=revcalc.calculation(refer=row['refer'],holdday=holdday)
                    if guarantee<self.guarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                if guarantee < self.guarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                if row['closeout']<=row['open']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = row['open']
                    status = 'close'
                elif row['closeout']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['closeout'],row['low'])
                    status='close'
                if status=='close':
                    orderinfo['revenue'], orderinfo['guarantee'] = revcalc.calculation(refer=orderinfo['sellbid'], holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    orderinfo['closetype']='margin-closeout'
                    ansdata=data[['high','low']][orderinfo['buyinx']:orderinfo['sellinx']]
                    ansdata['ordersell']=data['refer'].shift()[orderinfo['buyinx']:orderinfo['sellinx']]
                    orderinfo['revmax'], orderinfo['revmin'] = MarginMaxMin(data=ansdata, revcalc=revcalc)
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
            elif status=='selling':
                holdday += 1
                orderday+=1
                if row['callsell']<=row['open']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=row['open']
                    status='close'
                elif row['consell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['consell'],row['low'])
                    status='close'
                if status=='close':
                    orderinfo['revenue'], orderinfo['guarantee'] = revcalc.calculation(refer=orderinfo['sellbid'], holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    orderinfo['closetype']='margin-closeout'
                    ansdata=data[['high','low']][orderinfo['buyinx']:orderinfo['sellinx']]
                    ansdata['ordersell']=data['refer'].shift()[orderinfo['buyinx']:orderinfo['sellinx']]
                    orderinfo['revmax'], orderinfo['revmin'] = MarginMaxMin(data=ansdata, revcalc=revcalc)
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                    if guarantee < self.guarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

class ShortSell:
    def __init__(self,buyfee,sellfee,interest,margin,guarantee,stopprofit=None,stoploss=None):
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.interest=interest/360
        self.margin=margin
        self.guarantee=guarantee
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','closeout','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','closeout','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['ordersell']<=row['high']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['ordersell'],row['low'])}
                    revcalc=ShortRevenue(sellbid=orderinfo['sellbid'],sellfee=self.sellfee,buyfee=self.buyfee,margin=self.margin,interest=self.interest)
                    revenue,guarantee=revcalc.calculation(refer=row['refer'],holdday=holdday)
                    if guarantee<self.guarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                if guarantee < self.guarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday+=1
                if row['closeout']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['closeout'],row['high'])
                    orderinfo['revenue'],orderinfo['guarantee']=revcalc.calculation(refer=orderinfo['buybid'],holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    orderinfo['closetype']='margin-closeout'
                    orderinfo['revmax'],orderinfo['revmin']=ShortMaxMin(data.loc[orderinfo['sellinx']:orderinfo['buyinx'],['high','low','orderbuy']],revcalc=revcalc)
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
            elif status=='buying':
                holdday += 1
                orderday+=1
                if row['orderbuy']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['orderbuy'],row['high'])
                    orderinfo['revenue'], orderinfo['guarantee'] = revcalc.calculation(refer=orderinfo['buybid'], holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    orderinfo['closetype'] = 'buy-close'
                    orderinfo['revmax'], orderinfo['revmin'] = ShortMaxMin(data.loc[orderinfo['sellinx']:orderinfo['buyinx'], ['high', 'low', 'orderbuy']], revcalc=revcalc)
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                    if guarantee < self.guarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status='open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','closeout','callbuy','callsell','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','closeout','callbuy','callsell','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['callsell']<=row['open']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':row['open']}
                elif (row['consell']<=row['high']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['consell'],row['low'])}
                if status=='open':
                    revcalc=ShortRevenue(sellbid=orderinfo['sellbid'],sellfee=self.sellfee,buyfee=self.buyfee,margin=self.margin,interest=self.interest)
                    revenue,guarantee=revcalc.calculation(refer=row['refer'],holdday=holdday)
                    if guarantee<self.guarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                if guarantee < self.guarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday+=1
                if row['closeout']>=row['open']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=row['open']
                    status='close'
                elif row['closeout']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['closeout'],row['high'])
                    status='close'
                if status=='close':
                    orderinfo['revenue'],orderinfo['guarantee']=revcalc.calculation(refer=orderinfo['buybid'],holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    orderinfo['closetype']='margin-closeout'
                    ansdata=data[['high','low']][orderinfo['sellinx']:orderinfo['buyinx']]
                    ansdata['orderbuy']=data['refer'].shift()[orderinfo['sellinx']:orderinfo['buyinx']]
                    orderinfo['revmax'],orderinfo['revmin']=ShortMaxMin(data=ansdata,revcalc=revcalc)
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
            elif status=='buying':
                holdday += 1
                orderday+=1
                if row['callbuy']>=row['open']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=row['open']
                    status='close'
                elif row['conbuy']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['conbuy'],row['high'])
                    status='close'
                if status=='close':
                    orderinfo['revenue'],orderinfo['guarantee']=revcalc.calculation(refer=orderinfo['buybid'],holdday=holdday)
                    orderinfo['cost'] = revcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    orderinfo['closetype']='buy-close'
                    ansdata=data[['high','low']][orderinfo['sellinx']:orderinfo['buyinx']]
                    ansdata['orderbuy']=data['refer'].shift()[orderinfo['sellinx']:orderinfo['buyinx']]
                    orderinfo['revmax'],orderinfo['revmin']=ShortMaxMin(data=ansdata,revcalc=revcalc)
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    revenue, guarantee = revcalc.calculation(refer=row['refer'], holdday=holdday)
                    if guarantee < self.guarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status='open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

class NormalTradeHedge:
    def __init__(self,nbuyfee,nsellfee,sbuyfee,ssellfee,sinterest,smargin,sguarantee,stopprofit=None,stoploss=None):
        self.nbuyfee=nbuyfee
        self.nsellfee=nsellfee
        self.sbuyfee=sbuyfee
        self.ssellfee=ssellfee
        self.sinterest=sinterest
        self.smargin=smargin
        self.sguarantee=sguarantee
        self.extralogics = []
        self.buyquota=(1+nbuyfee)/((1+nbuyfee)+smargin)
        self.hedgequota=1-self.buyquota
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer']).difference(set(data.columns)))
            return None
        status = 'close'
        trades = []
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    holdday = 0
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'hedgesell':row['hedgerefer']}
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    srevcalc=ShortRevenue(sellbid=orderinfo['hedgesell'],sellfee=self.ssellfee,buyfee=self.sbuyfee,margin=self.smargin,interest=self.sinterest)
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    srevenue,sguarantee=srevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=nrevenue*self.buyquota+srevenue*self.hedgequota
                    if sguarantee<self.sguarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue=nrevenue*self.buyquota+srevenue*self.hedgequota
                if sguarantee < self.sguarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['hedgebuy']=row['hedgerefer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                orderinfo['revenue'] = nrevenue*self.buyquota+srevenue*self.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                orderinfo['cost']=ncost*self.buyquota+scost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status=='selling':
                holdday += 1
                orderday+=1
                if row['ordersell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['ordersell'],row['low'])
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                    orderinfo['revenue'] = nrevenue*self.buyquota+srevenue*self.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                    orderinfo['cost']=ncost*self.buyquota+scost*self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status='close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = nrevenue*self.buyquota+srevenue*self.hedgequota
                    if sguarantee < self.sguarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status!='close':
            orderinfo['status']=status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','hedgerefer'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','hedgerefer']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'hedgesell':row['hedgerefer']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'hedgesell':row['hedgerefer']}
                if status=='open':
                    holdday = 0
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    srevcalc=ShortRevenue(sellbid=orderinfo['hedgesell'],sellfee=self.ssellfee,buyfee=self.sbuyfee,margin=self.smargin,interest=self.sinterest)
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    srevenue,sguarantee=srevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=nrevenue*self.buyquota+srevenue*self.hedgequota
                    if sguarantee<self.sguarantee:
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue = nrevenue*self.buyquota+srevenue*self.hedgequota
                if sguarantee < self.sguarantee:
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['hedgebuy']=row['hedgerefer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                orderinfo['revenue'] = nrevenue*self.buyquota+srevenue*self.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                orderinfo['cost']=ncost*self.buyquota+scost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status=='selling':
                holdday += 1
                orderday+=1
                if row['callsell']<=row['open']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=row['open']
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    status='close'
                elif row['consell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['consell'],row['low'])
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    status='close'
                if status=='close':
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                    orderinfo['revenue'] = nrevenue*self.buyquota+srevenue*self.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                    orderinfo['cost'] = ncost*self.buyquota+scost*self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = nrevenue*self.buyquota+srevenue*self.hedgequota
                    if sguarantee < self.sguarantee:
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class MarginTradeHedge:
    def __init__(self,mbuyfee,msellfee,minterest,mmargin,mguarantee,sbuyfee,ssellfee,sinterest,smargin,sguarantee,stopprofit=None,stoploss=None):
        self.mbuyfee=mbuyfee
        self.msellfee=msellfee
        self.minterest=minterest
        self.mmargin=mmargin
        self.mguarantee=mguarantee
        self.sbuyfee=sbuyfee
        self.ssellfee=ssellfee
        self.sinterest=sinterest
        self.smargin=smargin
        self.sguarantee=sguarantee
        self.buyquota=(mmargin+mbuyfee)/((mmargin+mbuyfee)+smargin)
        self.hedgequota=1-self.buyquota
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    holdday = 0
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'hedgesell':row['hedgerefer']}
                    mrevcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    srevcalc=ShortRevenue(sellbid=orderinfo['hedgesell'],sellfee=self.ssellfee,buyfee=self.sbuyfee,margin=self.smargin,interest=self.sinterest)
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['refer'],holdday=holdday)
                    srevenue,sguarantee=srevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=mrevenue*self.buyquota+srevenue*self.hedgequota
                    if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=holdday)
                srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue = mrevenue*self.buyquota+srevenue*self.hedgequota
                if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['hedgebuy']=row['hedgerefer']
                mrevenue, orderinfo['guarantee']=mrevcalc.calculation(refer=orderinfo['sellbid'],holdday=holdday)
                srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                orderinfo['revenue'] = mrevenue*self.buyquota+srevenue*self.hedgequota
                mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                orderinfo['cost']=mcost*self.buyquota+scost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                holdday += 1
                orderday += 1
                if row['ordersell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['ordersell'], row['low'])
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=holdday)
                    srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                    orderinfo['revenue'] = mrevenue*self.buyquota+srevenue*self.hedgequota
                    mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                    orderinfo['cost'] = mcost*self.buyquota+scost*self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=holdday)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = mrevenue*self.buyquota+srevenue*self.hedgequota
                    if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','hedgerefer'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','hedgerefer']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'hedgesell':row['hedgerefer']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'hedgesell':row['hedgerefer']}
                if status=='open':
                    holdday = 0
                    mrevcalc = MarginRevenue(buybid=orderinfo['buybid'], buyfee=self.mbuyfee, sellfee=self.msellfee, margin=self.mmargin, interest=self.minterest)
                    srevcalc=ShortRevenue(sellbid=orderinfo['hedgesell'],sellfee=self.ssellfee,buyfee=self.sbuyfee,margin=self.smargin,interest=self.sinterest)
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['refer'],holdday=holdday)
                    srevenue,sguarantee=srevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=mrevenue*self.buyquota+srevenue*self.hedgequota
                    if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                        status='mco'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=holdday)
                srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue = mrevenue*self.buyquota+srevenue*self.hedgequota
                if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['hedgebuy']=row['hedgerefer']
                mrevenue, orderinfo['guarantee']=mrevcalc.calculation(refer=orderinfo['sellbid'],holdday=holdday)
                srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                orderinfo['revenue'] = mrevenue*self.buyquota+srevenue*self.hedgequota
                mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                orderinfo['cost']=mcost*self.buyquota+scost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                holdday += 1
                orderday += 1
                if row['callsell'] <= row['open']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = row['open']
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    status = 'close'
                elif row['consell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['consell'], row['low'])
                    orderinfo['hedgebuy'] = row['hedgerefer']
                    status = 'close'
                if status == 'close':
                    mrevenue, orderinfo['guarantee']=mrevcalc.calculation(refer=orderinfo['sellbid'],holdday=holdday)
                    srevenue, orderinfo['hedgeguarantee'] = srevcalc.calculation(refer=orderinfo['hedgebuy'], holdday=holdday)
                    orderinfo['revenue'] = mrevenue*self.buyquota+srevenue*self.hedgequota
                    mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=holdday)
                    scost = srevcalc.cost(buybid=orderinfo['hedgebuy'],holdday=holdday)
                    orderinfo['cost'] = mcost*self.buyquota+scost*self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=holdday)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = mrevenue*self.buyquota+srevenue*self.hedgequota
                    if (mguarantee < self.mguarantee) | (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class ShortTradeHedge:
    def __init__(self,sbuyfee,ssellfee,sinterest,smargin,sguarantee,mbuyfee,msellfee,minterest,mmargin,mguarantee,stopprofit=None,stoploss=None):
        self.mbuyfee=mbuyfee
        self.msellfee=msellfee
        self.minterest=minterest
        self.mmargin=mmargin
        self.mguarantee=mguarantee
        self.sbuyfee=sbuyfee
        self.ssellfee=ssellfee
        self.sinterest=sinterest
        self.smargin=smargin
        self.sguarantee=sguarantee
        self.extralogics = []
        self.sellquota=smargin/((mmargin+mbuyfee)+smargin)
        self.hedgequota=1-self.sellquota
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','hedgerefer']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['ordersell']<=row['high']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['ordersell'],row['low']),'hedgebuy':row['hedgerefer']}
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    mrevcalc=MarginRevenue(buybid=orderinfo['hedgebuy'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=srevenue*self.sellquota+mrevenue*self.hedgequota
                    if (mguarantee < self.mguarantee) | (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue = srevenue*self.sellquota+mrevenue*self.hedgequota
                if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['hedgesell']=row['hedgerefer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=holdday)
                mrevenue, orderinfo['hedgeguarantee']=mrevcalc.calculation(refer=orderinfo['hedgesell'],holdday=holdday)
                orderinfo['revenue'] = srevenue*self.sellquota+mrevenue*self.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                mcost = mrevcalc.cost(sellbid=orderinfo['hedgesell'], holdday=holdday)
                orderinfo['cost']=scost*self.sellquota+mcost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                holdday += 1
                orderday += 1
                if row['orderbuy'] >= row['low']:
                    orderinfo['buyinx'] = inx
                    orderinfo['buyday'] = orderday
                    orderinfo['buybid'] = min(row['orderbuy'], row['high'])
                    orderinfo['hedgesell'] = row['hedgerefer']
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=holdday)
                    mrevenue, orderinfo['hedgeguarantee'] = mrevcalc.calculation(refer=orderinfo['hedgesell'], holdday=holdday)
                    orderinfo['revenue'] = srevenue*self.sellquota+mrevenue*self.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    mcost = mrevcalc.cost(sellbid=orderinfo['hedgesell'], holdday=holdday)
                    orderinfo['cost'] = scost*self.sellquota+mcost*self.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = srevenue*self.sellquota+mrevenue*self.hedgequota
                    if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic']).difference(set(data.columns)))
            return None
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['callsell']<=row['open']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':row['open'],'hedgebuy':row['hedgerefer']}
                elif (row['consell']<=row['high']):
                    status='open'
                    holdday=0
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['consell'],row['low']),'hedgebuy':row['hedgerefer']}
                if status=='open':
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    mrevcalc=MarginRevenue(buybid=orderinfo['hedgebuy'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['hedgerefer'],holdday=holdday)
                    revenue=srevenue*self.sellquota+mrevenue*self.hedgequota
                    if (mguarantee < self.mguarantee) | (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                holdday+=1
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                revenue = srevenue*self.sellquota+mrevenue*self.hedgequota
                if (mguarantee<self.mguarantee)|(sguarantee<self.sguarantee):
                    status = 'mco'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif status=='mco':
                holdday += 1
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['hedgesell']=row['hedgerefer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=holdday)
                mrevenue, orderinfo['hedgeguarantee']=mrevcalc.calculation(refer=orderinfo['hedgesell'],holdday=holdday)
                orderinfo['revenue'] = srevenue*self.sellquota+mrevenue*self.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                mcost = mrevcalc.cost(sellbid=orderinfo['hedgesell'], holdday=holdday)
                orderinfo['cost']=scost*self.sellquota+mcost*self.hedgequota
                orderinfo['closetype']='margin-closeout'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                holdday += 1
                orderday += 1
                if row['callbuy']>=row['open']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=row['open']
                    orderinfo['hedgesell'] = row['hedgerefer']
                    status='close'
                elif row['conbuy']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['conbuy'],row['high'])
                    orderinfo['hedgesell'] = row['hedgerefer']
                    status='close'
                if status=='close':
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=holdday)
                    mrevenue, orderinfo['hedgeguarantee'] = mrevcalc.calculation(refer=orderinfo['hedgesell'], holdday=holdday)
                    orderinfo['revenue'] = srevenue*self.sellquota+mrevenue*self.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=holdday)
                    mcost = mrevcalc.cost(sellbid=orderinfo['hedgesell'], holdday=holdday)
                    orderinfo['cost'] = scost*self.sellquota+mcost*self.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=holdday)
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['hedgerefer'], holdday=holdday)
                    revenue = srevenue*self.sellquota+mrevenue*self.hedgequota
                    if (mguarantee < self.mguarantee) | (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class NormalIndexFutureHedge:
    def __init__(self,nbuyfee,nsellfee,ibuyfee,isellfee,iavailable,imargin,fkpath,ftfolder,stopprofit=None,stoploss=None):
        self.nbuyfee=nbuyfee
        self.nsellfee=nsellfee
        self.ibuyfee=ibuyfee
        self.isellfee=isellfee
        self.iavailable=iavailable
        self.imargin=imargin
        self.kquery=FutureIndexContractQuery(fkpath=fkpath,ftfolder=ftfolder)
        self.extralogics = []
        self.buyquota=(1+nbuyfee)/((1+nbuyfee)+(iavailable+imargin+isellfee))
        self.hedgequota=1-self.buyquota
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate']=pd.to_datetime(data['tradedate'])
        data=data.set_index('tradedate',drop=True)
        data=data.sort_index(ascending=True)
        status = 'close'
        trades = []
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    frevcalc=FutureIndexShortRevenue(kprice=orderinfo['kprice'],buyfee=self.ibuyfee,sellfee=self.isellfee,available=self.iavailable,margin=self.imargin)
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    frevenue,faccount=frevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=nrevenue*self.buyquota+frevenue*self.hedgequota
                    if faccount<0:
                        status='mco'
                        orderday=0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = nrevenue * self.buyquota + frevenue * self.hedgequota
                if faccount < 0:
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status=='mco')|(status=='maturity'):
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx,'refer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue']=nrevenue*self.buyquota+frevenue*self.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost'] = ncost * self.buyquota + fcost * self.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['ordersell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['ordersell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = nrevenue * self.buyquota + frevenue * self.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = ncost * self.buyquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = nrevenue * self.buyquota + frevenue * self.hedgequota
                    if faccount < 0:
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status = 'close'
        trades = []
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status = 'open'
                    hedgek = self.kquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    hedgek = self.kquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    frevcalc=FutureIndexShortRevenue(kprice=orderinfo['kprice'],buyfee=self.ibuyfee,sellfee=self.isellfee,available=self.iavailable,margin=self.imargin)
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    frevenue,faccount=frevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=nrevenue*self.buyquota+frevenue*self.hedgequota
                    if faccount<0:
                        status='mco'
                        orderday=0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = nrevenue * self.buyquota + frevenue * self.hedgequota
                if faccount < 0:
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status=='mco')|(status=='maturity'):
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx,'refer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue']=nrevenue*self.buyquota+frevenue*self.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost'] = ncost * self.buyquota + fcost * self.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status=='selling':
                orderday+=1
                if row['callsell']<=row['open']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                elif row['consell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['consell'],row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                if status=='close':
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = nrevenue * self.buyquota + frevenue * self.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = ncost * self.buyquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = nrevenue * self.buyquota + frevenue * self.hedgequota
                    if faccount < 0:
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class MarginIndexFutureHedge:
    def __init__(self,mbuyfee,msellfee,minterest,mmargin,mguarantee,ibuyfee,isellfee,iavailable,imargin,fkpath,ftfolder,stopprofit=None,stoploss=None):
        self.mbuyfee=mbuyfee
        self.msellfee=msellfee
        self.minterest=minterest
        self.mmargin=mmargin
        self.mguarantee=mguarantee
        self.ibuyfee=ibuyfee
        self.isellfee=isellfee
        self.iavailable=iavailable
        self.imargin=imargin
        self.kquery=FutureIndexContractQuery(fkpath=fkpath,ftfolder=ftfolder)
        self.extralogics = []
        self.buyquota=(self.mmargin + self.mbuyfee)/((self.mmargin + self.mbuyfee)+(iavailable+imargin+isellfee))
        self.hedgequota=1-self.buyquota
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                    mrevcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    frevcalc = FutureIndexShortRevenue(kprice=orderinfo['kprice'], buyfee=self.ibuyfee, sellfee=self.isellfee, available=self.iavailable, margin=self.imargin)
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['refer'],holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue=mrevenue*self.buyquota+frevenue*self.hedgequota
                    if (mguarantee<self.mguarantee)|(faccount<0):
                        status='mco'
                        orderday=0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = mrevenue * self.buyquota + frevenue * self.hedgequota
                if (mguarantee < self.mguarantee) | (faccount < 0):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                mrevenue, orderinfo['guarantee']=mrevcalc.calculation(refer=orderinfo['sellbid'],holdday=(inx - orderinfo['buyinx']).days)
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = mrevenue*self.buyquota+frevenue*self.hedgequota
                mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=(inx - orderinfo['buyinx']).days)
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost']=mcost*self.buyquota+fcost*self.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['ordersell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['ordersell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = mrevenue * self.buyquota + frevenue * self.hedgequota
                    mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = mcost * self.buyquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = mrevenue * self.buyquota + frevenue * self.hedgequota
                    if (mguarantee < self.mguarantee) | (faccount < 0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    mrevcalc = MarginRevenue(buybid=orderinfo['buybid'], buyfee=self.mbuyfee, sellfee=self.msellfee, margin=self.mmargin, interest=self.minterest)
                    frevcalc = FutureIndexShortRevenue(kprice=orderinfo['kprice'], buyfee=self.ibuyfee, sellfee=self.isellfee, available=self.iavailable, margin=self.imargin)
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue=mrevenue*self.buyquota+frevenue*self.hedgequota
                    if (mguarantee < self.mguarantee) | (faccount < 0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold == False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = mrevenue * self.buyquota + frevenue * self.hedgequota
                if (mguarantee < self.mguarantee) | (faccount < 0):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = mrevenue * self.buyquota + frevenue * self.hedgequota
                mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost'] = mcost * self.buyquota + fcost * self.hedgequota
                if status == 'mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['callsell'] <= row['open']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status = 'close'
                elif row['consell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['consell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status = 'close'
                if status == 'close':
                    mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = mrevenue * self.buyquota + frevenue * self.hedgequota
                    mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = mcost * self.buyquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = mrevenue * self.buyquota + frevenue * self.hedgequota
                    if (mguarantee < self.mguarantee) | (faccount < 0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class ShortIndexFutureHedge:
    def __init__(self,sbuyfee,ssellfee,sinterest,smargin,sguarantee,ibuyfee,isellfee,iavailable,imargin,fkpath,ftfolder,stopprofit=None,stoploss=None):
        self.sbuyfee=sbuyfee
        self.ssellfee=ssellfee
        self.sinterest=sinterest
        self.smargin=smargin
        self.sguarantee=sguarantee
        self.ibuyfee=ibuyfee
        self.isellfee=isellfee
        self.iavailable=iavailable
        self.imargin=imargin
        self.kquery=FutureIndexContractQuery(fkpath=fkpath,ftfolder=ftfolder)
        self.extralogics = []
        self.sellquota = smargin / (smargin + (iavailable+imargin+isellfee))
        self.hedgequota = 1 - self.sellquota
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['ordersell']<=row['high']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['ordersell'],row['low']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    frevcalc = FutureIndexLongRevenue(kprice=orderinfo['kprice'],buyfee=self.ibuyfee,sellfee=self.isellfee,available=self.iavailable,margin=self.imargin)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue*self.sellquota+frevenue*self.hedgequota
                    if (sguarantee < self.sguarantee)|(faccount<0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = srevenue * self.sellquota + frevenue * self.hedgequota
                if (sguarantee < self.sguarantee) | (faccount < 0):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = srevenue*self.sellquota+frevenue*self.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=(inx - orderinfo['sellinx']).days)
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost']=scost*self.sellquota+fcost*self.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                orderday += 1
                if row['orderbuy'] >= row['low']:
                    orderinfo['buyinx'] = inx
                    orderinfo['buyday'] = orderday
                    orderinfo['buybid'] = min(row['orderbuy'], row['high'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = srevenue * self.sellquota + frevenue * self.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = scost * self.sellquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue * self.sellquota + frevenue * self.hedgequota
                    if (sguarantee < self.sguarantee) | (faccount < 0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['callsell']<=row['open']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':row['open'],'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['consell']<=row['high']):
                    status='open'
                    hedgek=self.kquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['consell'],row['low']),'kprice':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    frevcalc = FutureIndexLongRevenue(kprice=orderinfo['kprice'],buyfee=self.ibuyfee,sellfee=self.isellfee,available=self.iavailable,margin=self.imargin)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue*self.sellquota+frevenue*self.hedgequota
                    if (sguarantee < self.sguarantee)|(faccount<0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = srevenue * self.sellquota + frevenue * self.hedgequota
                if (sguarantee < self.sguarantee) | (faccount < 0):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = srevenue*self.sellquota+frevenue*self.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=(inx - orderinfo['sellinx']).days)
                fcost = frevcalc.cost(refer=orderinfo['settle'])
                orderinfo['cost']=scost*self.sellquota+fcost*self.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                orderday += 1
                if row['callbuy']>=row['open']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                elif row['conbuy']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['conbuy'],row['high'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                if status=='close':
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, orderinfo['faccount'] = frevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = srevenue * self.sellquota + frevenue * self.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    fcost = frevcalc.cost(refer=orderinfo['settle'])
                    orderinfo['cost'] = scost * self.sellquota + fcost * self.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    frevenue, faccount = frevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue * self.sellquota + frevenue * self.hedgequota
                    if (sguarantee < self.sguarantee) | (faccount < 0):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class NormalOptionHedge:
    def __init__(self,nbuyfee,nsellfee,obuyfee,osellfee,omultiplier,objpath,okpath,otfolder,stopprofit=None,stoploss=None):
        self.nbuyfee=nbuyfee
        self.nsellfee=nsellfee
        self.obuyfee=obuyfee
        self.osellfee=osellfee
        self.omultiplier=omultiplier
        self.oquery=OptionQuery(objpath=objpath,okpath=okpath,otfolder=otfolder)
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate']=pd.to_datetime(data['tradedate'])
        data=data.set_index('tradedate',drop=True)
        data = data.sort_index(ascending=True)
        status = 'close'
        trades = []
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    hedgek,eprice=self.oquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    orevcalc=OptionShortRevenue(eprice=orderinfo['eprice'],optcost=orderinfo['optcost'],buyfee=self.obuyfee,sellfee=self.osellfee,multiplier=self.omultiplier,tmultiplier=(1+self.nbuyfee))
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    orevenue=orevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=nrevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='maturity':
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx,'refer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue']=nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                ocost = orevcalc.cost()
                orderinfo['cost'] = ncost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['ordersell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['ordersell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = ncost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status = 'close'
        trades = []
        for inx, row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status = 'open'
                    hedgek,eprice=self.oquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    hedgek,eprice=self.oquery.selectk(startdate=inx,period=row['period'])
                    if type(hedgek)!=pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    nrevcalc=NormalRevenue(buybid=orderinfo['buybid'],buyfee=self.nbuyfee,sellfee=self.nsellfee)
                    orevcalc=OptionShortRevenue(eprice=orderinfo['eprice'],optcost=orderinfo['optcost'],buyfee=self.obuyfee,sellfee=self.osellfee,multiplier=self.omultiplier,tmultiplier=(1+self.nbuyfee))
                    nrevenue=nrevcalc.calculation(refer=row['refer'])
                    orevenue=orevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=nrevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                nrevenue = nrevcalc.calculation(refer=row['refer'])
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif status=='maturity':
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx,'refer']
                nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue']=nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                ocost = orevcalc.cost()
                orderinfo['cost'] = ncost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status=='selling':
                orderday+=1
                if row['callsell']<=row['open']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                elif row['consell']<=row['high']:
                    orderinfo['sellinx']=inx
                    orderinfo['sellday']=orderday
                    orderinfo['sellbid']=max(row['consell'],row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                if status=='close':
                    nrevenue = nrevcalc.calculation(refer=orderinfo['sellbid'])
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    ncost = nrevcalc.cost(sellbid=orderinfo['sellbid'])
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = ncost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    nrevenue = nrevcalc.calculation(refer=row['refer'])
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = nrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class MarginOptionHedge:
    def __init__(self,mbuyfee,msellfee,minterest,mmargin,mguarantee,obuyfee,osellfee,omultiplier,objpath,okpath,otfolder,stopprofit=None,stoploss=None):
        self.mbuyfee=mbuyfee
        self.msellfee=msellfee
        self.minterest=minterest
        self.mmargin=mmargin
        self.mguarantee=mguarantee
        self.obuyfee=obuyfee
        self.osellfee=osellfee
        self.omultiplier=omultiplier
        self.oquery=OptionQuery(objpath=objpath,okpath=okpath,otfolder=otfolder)
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['orderbuy']>=row['low']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['orderbuy'],row['high']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                    mrevcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    orevcalc = OptionShortRevenue(eprice=orderinfo['eprice'], optcost=orderinfo['optcost'], buyfee=self.obuyfee, sellfee=self.osellfee, multiplier=self.omultiplier, tmultiplier=(self.mmargin + self.mbuyfee))
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['refer'],holdday=(inx - orderinfo['buyinx']).days)
                    orevenue=orevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=mrevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if (mguarantee < self.mguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if (mguarantee<self.mguarantee):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status == 'mco')|(status == 'maturity'):
                orderday +=1
                orderinfo['sellinx']=inx
                orderinfo['sellday']=orderday
                orderinfo['sellbid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                mrevenue, orderinfo['guarantee']=mrevcalc.calculation(refer=orderinfo['sellbid'],holdday=(inx - orderinfo['buyinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                mcost=mrevcalc.cost(sellbid=orderinfo['sellbid'],holdday=(inx - orderinfo['buyinx']).days)
                ocost=orevcalc.cost()
                orderinfo['cost']=mcost*orevcalc.tradequota+ocost*orevcalc.hedgequota
                if status == 'mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['ordersell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['ordersell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = mcost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if (mguarantee < self.mguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self, data):
        if (set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','open','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='buying'
                    orderday=0
            elif status=='buying':
                orderday+=1
                if (row['callbuy']>=row['open']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':row['open'],'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['conbuy']>=row['low']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'buyinx':inx,'buyday':orderday,'buybid':min(row['conbuy'],row['high']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    mrevcalc=MarginRevenue(buybid=orderinfo['buybid'],buyfee=self.mbuyfee,sellfee=self.msellfee,margin=self.mmargin,interest=self.minterest)
                    orevcalc = OptionShortRevenue(eprice=orderinfo['eprice'], optcost=orderinfo['optcost'], buyfee=self.obuyfee, sellfee=self.osellfee, multiplier=self.omultiplier, tmultiplier=(self.mmargin + self.mbuyfee))
                    mrevenue,mguarantee=mrevcalc.calculation(refer=row['refer'],holdday=(inx - orderinfo['buyinx']).days)
                    orevenue=orevcalc.calculation(refer=hedgek.loc[inx,'settle'])
                    revenue=mrevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if (mguarantee < self.mguarantee) :
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'selling'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if (mguarantee<self.mguarantee):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'selling'
                        orderday = 0
            elif (status == 'mco')|(status == 'maturity'):
                orderday += 1
                orderinfo['sellinx'] = inx
                orderinfo['sellday'] = orderday
                orderinfo['sellbid'] = row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                orderinfo['revenue'] = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                ocost = orevcalc.cost()
                orderinfo['cost'] = mcost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                if status == 'mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status = 'close'
                if row['openlogic']:
                    status = 'buying'
                    orderday = 0
            elif status == 'selling':
                orderday += 1
                if row['callsell'] <= row['open']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status = 'close'
                elif row['consell'] <= row['high']:
                    orderinfo['sellinx'] = inx
                    orderinfo['sellday'] = orderday
                    orderinfo['sellbid'] = max(row['consell'], row['low'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status = 'close'
                if status == 'close':
                    mrevenue, orderinfo['guarantee'] = mrevcalc.calculation(refer=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'refer'])
                    orderinfo['revenue'] = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    mcost = mrevcalc.cost(sellbid=orderinfo['sellbid'], holdday=(inx - orderinfo['buyinx']).days)
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = mcost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'sell-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'buying'
                        orderday = 0
                else:
                    mrevenue, mguarantee = mrevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['buyinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = mrevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if (mguarantee < self.mguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['buyinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class ShortOptionHedge:
    def __init__(self,sbuyfee,ssellfee,sinterest,smargin,sguarantee,obuyfee,osellfee,omultiplier,objpath,okpath,otfolder,stopprofit=None,stoploss=None):
        self.sbuyfee=sbuyfee
        self.ssellfee=ssellfee
        self.sinterest=sinterest
        self.smargin=smargin
        self.sguarantee=sguarantee
        self.obuyfee=obuyfee
        self.osellfee=osellfee
        self.omultiplier=omultiplier
        self.oquery=OptionQuery(objpath=objpath,okpath=okpath,otfolder=otfolder)
        self.extralogics = []
        if stopprofit:
            extralogic=stopprofit_logic(stopprofit=stopprofit)
            self.extralogics.append(extralogic)
        if stoploss:
            extralogic=stoploss_logic(stoploss=stoploss)
            self.extralogics.append(extralogic)

    def statistics(self,data):
        if (set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['orderbuy','ordersell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['ordersell']<=row['high']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['ordersell'],row['low']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    orevcalc = OptionShortRevenue(eprice=orderinfo['eprice'], optcost=orderinfo['optcost'], buyfee=self.obuyfee, sellfee=self.osellfee, multiplier=self.omultiplier, tmultiplier=self.smargin)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if (sguarantee < self.sguarantee):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                orderinfo['revenue'] = srevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=(inx - orderinfo['sellinx']).days)
                ocost=orevcalc.cost()
                orderinfo['cost']=scost*orevcalc.tradequota+ocost*orevcalc.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                orderday += 1
                if row['orderbuy'] >= row['low']:
                    orderinfo['buyinx'] = inx
                    orderinfo['buyday'] = orderday
                    orderinfo['buybid'] = min(row['orderbuy'], row['high'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    orderinfo['revenue'] = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = scost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

    def statistics_with_callauction(self,data):
        if (set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic','tradedate','period'])<=set(data.columns))==False:
            print('缺少必要数据列',set(['conbuy','consell','callbuy','callsell','refer','high','low','openlogic','holdlogic','tradedate','period']).difference(set(data.columns)))
            return None
        data['tradedate'] = pd.to_datetime(data['tradedate'])
        data = data.set_index('tradedate', drop=True)
        data = data.sort_index(ascending=True)
        status='close'
        trades=[]
        for inx,row in data.iterrows():
            if status=='close':
                if row['openlogic']:
                    status='selling'
                    orderday=0
            elif status=='selling':
                orderday+=1
                if (row['callsell']<=row['open']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':row['open'],'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                elif (row['consell']<=row['high']):
                    status='open'
                    hedgek, eprice = self.oquery.selectk(startdate=inx, period=row['period'])
                    if type(hedgek) != pd.DataFrame:
                        break
                    orderinfo={'sellinx':inx,'sellday':orderday,'sellbid':max(row['consell'],row['low']),'eprice':eprice,'optcost':hedgek.loc[inx,'refer'],'period':row['period']}
                if status=='open':
                    srevcalc = ShortRevenue(sellbid=orderinfo['sellbid'], sellfee=self.ssellfee, buyfee=self.sbuyfee, margin=self.smargin, interest=self.sinterest)
                    orevcalc = OptionShortRevenue(eprice=orderinfo['eprice'], optcost=orderinfo['optcost'], buyfee=self.obuyfee, sellfee=self.osellfee, multiplier=self.omultiplier, tmultiplier=self.smargin)
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                    if (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days)>=orderinfo['period']:
                        status='maturity'
                        orderday=0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold==False:
                            status = 'buying'
                            orderday = 0
                else:
                    if row['openlogic']==False:
                        status='close'
            elif status=='open':
                srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                revenue = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                if (sguarantee < self.sguarantee):
                    status = 'mco'
                    orderday = 0
                elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                    status = 'maturity'
                    orderday = 0
                else:
                    hold = row['holdlogic']
                    for logic in self.extralogics:
                        hold = hold & logic.calc(revenue)
                    if hold == False:
                        status = 'buying'
                        orderday = 0
            elif (status == 'mco') | (status == 'maturity'):
                orderday +=1
                orderinfo['buyinx']=inx
                orderinfo['buyday']=orderday
                orderinfo['buybid']=row['refer']
                orderinfo['settle'] = hedgek.loc[inx, 'refer']
                srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                orderinfo['revenue'] = srevenue*orevcalc.tradequota+orevenue*orevcalc.hedgequota
                scost = srevcalc.cost(buybid=orderinfo['buybid'],holdday=(inx - orderinfo['sellinx']).days)
                ocost=orevcalc.cost()
                orderinfo['cost']=scost*orevcalc.tradequota+ocost*orevcalc.hedgequota
                if status=='mco':
                    orderinfo['closetype'] = 'margin-closeout'
                else:
                    orderinfo['closetype'] = 'maturity-close'
                trades.append(orderinfo)
                status='close'
                if row['openlogic']:
                    status = 'selling'
                    orderday = 0
            elif status == 'buying':
                orderday += 1
                if row['callbuy']>=row['open']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=row['open']
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                elif row['conbuy']>=row['low']:
                    orderinfo['buyinx']=inx
                    orderinfo['buyday']=orderday
                    orderinfo['buybid']=min(row['conbuy'],row['high'])
                    orderinfo['settle'] = hedgek.loc[inx, 'refer']
                    status='close'
                if status=='close':
                    srevenue, orderinfo['guarantee'] = srevcalc.calculation(refer=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    orderinfo['revenue'] = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    scost = srevcalc.cost(buybid=orderinfo['buybid'], holdday=(inx - orderinfo['sellinx']).days)
                    ocost = orevcalc.cost()
                    orderinfo['cost'] = scost * orevcalc.tradequota + ocost * orevcalc.hedgequota
                    orderinfo['closetype'] = 'buy-close'
                    trades.append(orderinfo)
                    status = 'close'
                    if row['openlogic']:
                        status = 'selling'
                        orderday = 0
                else:
                    srevenue, sguarantee = srevcalc.calculation(refer=row['refer'], holdday=(inx - orderinfo['sellinx']).days)
                    orevenue = orevcalc.calculation(refer=hedgek.loc[inx, 'settle'])
                    revenue = srevenue * orevcalc.tradequota + orevenue * orevcalc.hedgequota
                    if (sguarantee < self.sguarantee):
                        status = 'mco'
                        orderday = 0
                    elif ((data[data.index>inx].index.min() - orderinfo['sellinx']).days) >= orderinfo['period']:
                        status = 'maturity'
                        orderday = 0
                    else:
                        hold = row['holdlogic']
                        for logic in self.extralogics:
                            hold = hold & logic.calc(revenue)
                        if hold:
                            status = 'open'
            else:
                raise Exception("Illegal status!")
        if status != 'close':
            orderinfo['status'] = status
            trades.append(orderinfo)
        return trades

class stopprofit_logic:
    def __init__(self,stopprofit):
        self.stopprofit=stopprofit

    def calc(self,revenue):
        return revenue<self.stopprofit

class stoploss_logic:
    def __init__(self,stoploss):
        self.stoploss=stoploss

    def calc(self,revenue):
        return revenue>self.stoploss

class NormalRevenue:
    def __init__(self,buybid,buyfee,sellfee):
        self.buybid=buybid
        self.buyfee=buyfee
        self.sellfee=sellfee

    def calculation(self,refer):
        return (refer/self.buybid)*(1-self.sellfee)/(1+self.buyfee)-1

    def cost(self,sellbid):
        return (self.buyfee / (1 + self.buyfee)) + (sellbid / self.buybid) * self.sellfee / (1 + self.buyfee)

def NormalMaxMin(data,revcalc):
    highpiece = data['high']
    lowpiece = data['low']
    sppiece = data['ordersell']
    sppiece = (highpiece >= sppiece) * sppiece + (highpiece < sppiece) * highpiece
    sppiece = (lowpiece <= sppiece) * sppiece + (lowpiece > sppiece) * lowpiece
    spmax = sppiece.max()
    spmin = sppiece.min()
    return revcalc.calculation(refer=spmax),revcalc.calculation(refer=spmin)

class MarginRevenue:
    def __init__(self,buybid,buyfee,sellfee,margin,interest):
        self.buybid=buybid
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.margin=margin
        self.interest=interest

    def calculation(self,refer,holdday):
        revenue = ((refer / self.buybid) * (1 - self.sellfee) - (1 + self.interest * holdday)) / (self.margin + self.buyfee)
        guarantee = (refer / self.buybid) * (1 - self.sellfee) - self.interest * holdday + self.margin
        return revenue,guarantee

    def cost(self,sellbid,holdday):
        return (self.buyfee + (sellbid / self.buybid) * self.sellfee + self.interest * holdday) / (self.margin + self.buyfee)

def MarginMaxMin(data,revcalc):
    highpiece = data['high']
    lowpiece = data['low']
    sppiece = data['ordersell']
    sppiece = (highpiece >= sppiece) * sppiece + (highpiece < sppiece) * highpiece
    sppiece = (lowpiece <= sppiece) * sppiece + (lowpiece > sppiece) * lowpiece
    spdays = pd.Series(range(len(sppiece)), index=sppiece.index)
    revenues,guarantees=revcalc.calculation(refer=sppiece,holdday=spdays)
    return revenues.max(),revenues.min()

class ShortRevenue:
    def __init__(self,sellbid,sellfee,buyfee,margin,interest):
        self.sellbid=sellbid
        self.sellfee=sellfee
        self.buyfee=buyfee
        self.margin=margin
        self.interest=interest

    def calculation(self,refer,holdday):
        revenue = (1 - self.sellfee - (refer / self.sellbid) * (1 + self.buyfee) - self.interest * holdday) / self.margin
        guarantee = (1 - self.sellfee + self.margin) / ((refer / self.sellbid) * (1 + self.buyfee) + self.interest * holdday)
        return revenue,guarantee

    def cost(self,buybid,holdday):
        return (self.sellfee + (buybid / self.sellbid) * self.buyfee + self.interest * holdday) / self.margin

def ShortMaxMin(data,revcalc):
    highpiece = data['high']
    lowpiece = data['low']
    bppiece = data['orderbuy']
    bppiece = (highpiece >= bppiece) * bppiece + (highpiece < bppiece) * highpiece
    bppiece = (lowpiece <= bppiece) * bppiece + (lowpiece > bppiece) * lowpiece
    bpdays = pd.Series(range(len(bppiece)), index=bppiece.index)
    revenues,guarantees=revcalc.calculation(refer=bppiece,holdday=bpdays)
    return revenues.max(),revenues.min()

class FutureIndexContractQuery:
    def __init__(self,fkpath,ftfolder):
        contracts=pd.read_csv(fkpath,index_col=[0])
        if (set(['filename','listdate','delistdate']) <= set(contracts.columns)):
            self.contracts=contracts
            self.contracts['listdate']=pd.to_datetime(self.contracts['listdate'])
            self.contracts['delistdate']=pd.to_datetime(self.contracts['delistdate'])
            self.ftfolder=ftfolder
        else:
            self.contracts=None
            self.ftfolder=None

    def selectk(self,startdate,period):
        startdate=startdate
        enddate=startdate+pd.Timedelta(period,'d')
        selections=self.contracts[(self.contracts['listdate']<=startdate)&(self.contracts['delistdate']>=enddate)]
        kfile=self.ftfolder+selections['filename'][selections['delistdate'].idxmin()]
        if kfile[-4:]!='.csv':
            kfile=kfile+'.csv'
        kdata=pd.read_csv(kfile,index_col=[0])
        if (set(['tradedate','refer','settle'])<=set(kdata.columns)):
            kdata['tradedate']=pd.to_datetime(kdata['tradedate'])
            kdata=kdata.set_index('tradedate',drop=True)
            kdata = kdata.sort_index(ascending=True)
            return kdata.loc[startdate:enddate]
        else:
            return None

class FutureIndexLongRevenue:
    def __init__(self,kprice,buyfee,sellfee,available,margin):
        self.kprice=kprice
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.available=available
        self.margin=margin

    def calculation(self,refer):
        revenue=(refer*(1-self.sellfee)/self.kprice-1)/(self.margin+self.available+self.buyfee)
        acount=self.available+(refer*(1-self.sellfee)/self.kprice-1)
        return revenue,acount

    def cost(self,refer):
        return (self.buyfee + (refer / self.kprice) * self.sellfee) / (self.margin + self.available + self.buyfee)

class FutureIndexShortRevenue:
    def __init__(self,kprice,buyfee,sellfee,available,margin):
        self.kprice=kprice
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.available=available
        self.margin=margin

    def calculation(self,refer):
        revenue=(1-refer*(1+self.buyfee)/self.kprice)/(self.margin+self.available+self.sellfee)
        account=self.available+(1-refer*(1+self.buyfee)/self.kprice)
        return revenue,account

    def cost(self,refer):
        return (self.sellfee + (refer / self.kprice) * self.buyfee) / (self.margin + self.available + self.sellfee)

class OptionQuery:
    def __init__(self,objpath,okpath,otfolder):
        objdata=pd.read_csv(objpath,index_col=[0])
        if (set(['tradedate','refer'])<=set(objdata.columns)):
            objdata['tradedate']=pd.to_datetime(objdata['tradedate'])
            self.objdata=objdata.set_index('tradedate',drop=True).sort_index(ascending=True)
        else:
            self.objdata=None
        contracts=pd.read_csv(okpath,index_col=[0])
        if (set(['filename','listdate','delistdate','exerciseprice']) <= set(contracts.columns)):
            self.contracts=contracts
            self.contracts['listdate']=pd.to_datetime(self.contracts['listdate'])
            self.contracts['delistdate']=pd.to_datetime(self.contracts['delistdate'])
            self.otfolder=otfolder
        else:
            self.contracts=None
            self.otfolder=None

    def selectk(self,startdate,period):
        startdate=startdate
        enddate=startdate+pd.Timedelta(period,'d')
        selections = self.contracts[(self.contracts['listdate'] <= startdate) & (self.contracts['delistdate'] >= enddate)]
        kdelist=selections['delistdate'].min()
        selections=selections[selections['delistdate']==kdelist]
        ansdata=abs(selections['exerciseprice']-self.objdata.loc[startdate,'refer'])
        eminpoint=ansdata.idxmin()
        eprice=selections['exerciseprice'][eminpoint]
        kfile=self.otfolder+selections['filename'][eminpoint]
        if kfile[-4:]!='.csv':
            kfile=kfile+'.csv'
        kdata=pd.read_csv(kfile,index_col=[0])
        if (set(['tradedate','refer','settle'])<=set(kdata.columns)):
            kdata['tradedate']=pd.to_datetime(kdata['tradedate'])
            kdata=kdata.set_index('tradedate',drop=True).sort_index(ascending=True)
            return kdata.loc[startdate:enddate],eprice
        else:
            return None,None

class OptionLongRevenue:
    def __init__(self,eprice,optcost,buyfee,sellfee,multiplier,tmultiplier):
        self.eprice=eprice
        self.optcost=optcost
        self.buyfee=buyfee
        self.sellfee=sellfee
        self.multiplier=multiplier
        self.tradequota=tmultiplier*(eprice*multiplier)/(tmultiplier*(eprice*multiplier)+(optcost*multiplier+buyfee+sellfee))
        self.hedgequota=1-self.tradequota

    def calculation(self,refer):
        return (refer*self.multiplier)/(self.optcost*self.multiplier+self.buyfee+self.sellfee)-1

    def cost(self):
        return 1

class OptionShortRevenue:
    def __init__(self, eprice, optcost, buyfee, sellfee, multiplier, tmultiplier):
        self.eprice = eprice
        self.optcost = optcost
        self.buyfee = buyfee
        self.sellfee = sellfee
        self.multiplier = multiplier
        self.tradequota=tmultiplier*(eprice*multiplier)/(tmultiplier*(eprice*multiplier)+(optcost*multiplier+buyfee+sellfee))
        self.hedgequota=1-self.tradequota

    def calculation(self, refer):
        return (refer* self.multiplier) / (self.optcost * self.multiplier + self.buyfee + self.sellfee) - 1

    def cost(self):
        return 1

