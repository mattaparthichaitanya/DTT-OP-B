from api_helper import ShoonyaApiPy
import credentials
import datetime
import DateTimeNow
import TOKEN
import time
api = ShoonyaApiPy()
#ret = api.login(userid=credentials.user, password=credentials.u_pwd, twoFA=credentials.factor2, vendor_code=credentials.vc, api_secret=credentials.app_key, imei=credentials.imei)
#ret = ret['susertoken']
#f = open('TOKEN','w+')
#f.write(ret)
#f.close() 
#######################################
#k = open('/home/ubuntu/DTT-OP-B/TOKEN','r')
l = TOKEN.TOKEN
#print(l)
ret = api.set_session(userid=credentials.user, password=credentials.u_pwd, usertoken=l)
token = api.get_quotes('NSE', 'Nifty Bank')['token']
lastBusDay = datetime.datetime.today()
lastBusDay = lastBusDay.replace(hour=DateTimeNow.hour, minute=DateTimeNow.minutes, second=0, microsecond=0)
ret = api.get_time_price_series(exchange='NSE', token=token, starttime=lastBusDay.timestamp(), interval=1)
twoopen = ret[0]['into']
# print(twoopen)
# exit()
option_ki_dari_edi = round((int(float(twoopen))), -2)
print("BANKNIFTY is at : ",option_ki_dari_edi)
selection = f'{"Nifty Bank"} {"PE"} {option_ki_dari_edi}'
selectionC = f'{"Nifty Bank"} {"CE"} {option_ki_dari_edi}'
print(selectionC)
print(selection)
# optionToken = api.get_quotes('NFO', 'BANKNIFTY24NOV22C42400')['token']
optionToken = api.searchscrip(exchange='NFO',searchtext=selection)['values'][0]['tsym']
optionTokenC = api.searchscrip(exchange='NFO',searchtext=selectionC)['values'][0]['tsym']
tokenC = api.get_quotes('NFO', optionTokenC)['token']
token = api.get_quotes('NFO', optionToken)['token']
optoken = api.get_quotes('NFO', token)['token']
optokenC = api.get_quotes('NFO', tokenC)['token']
lastBusDay1 = lastBusDay
lastBusDay2 = lastBusDay1.replace(hour=DateTimeNow.hour, minute=DateTimeNow.minutes, second=0, microsecond=0)
ret1 = api.get_time_price_series(exchange='NFO', token=optoken, starttime=lastBusDay2.timestamp(), interval=1)
lastBusDay3 = lastBusDay
lastBusDay4 = lastBusDay3.replace(hour=DateTimeNow.hour, minute=DateTimeNow.minutes, second=0, microsecond=0)
ret2 = api.get_time_price_series(exchange='NFO', token=optokenC, starttime=lastBusDay3.timestamp(), interval=1)
opopen = ret1[0]['into']
opopenC = ret2[0]['into']
print("CE ",round(int(float(opopenC))))
print("PE",round(int(float(opopen))))
###########################################
# PE ENTRY
mondayentry = round(float(opopen)*1.3)
mondaytarget = round(float(mondayentry)*1.15)
mondaystoploss = round(float(mondayentry)*0.85)
print("#######################################")

print("MON PE ENTRY : ",mondayentry)
print("*******")
print("MON PE TARGET : ",mondaytarget)
print("*******")
print("MON PE SL : ",mondaystoploss)
print("*******")
# CE ENTRY
mondayentryC = round(float(opopenC)*1.3)
mondaytargetC = round(float(mondayentryC)*1.15)
mondaystoplossC = round(float(mondayentryC)*0.85)
print("MON CE ENTRY : ",mondayentryC)
print("*******")
print("MON CE TARGET : ",mondaytargetC)
print("*******")
print("MON CE SL : ",mondaystoplossC)
print("*******")
print("#######################################")

# opltp = api.get_quotes(exchange='NFO', token=optoken)['lp']
# print(float(opltp))
feed_opened = False
feedJson = {}
socket_opened = False
orderJson = {}
def evert_handler_feed_update(message):
    # print(message)
    if (('lp' in message) & ('tk' in message)):
        feedJson[message['tk']] = {'ltp': float(message['lp'])}
def event_handler_order_update(inmessage):
    # print(inmessage)
    if (('norenordno' in inmessage) & ('status' in inmessage)):
        orderJson[inmessage['norenordno']] = {'status': inmessage['status']}
def open_callback():
    global feed_opened
    feed_opened = True
def setupWebSocket():
    global feed_opened
    api.start_websocket(order_update_callback=event_handler_order_update,
                        subscribe_callback=evert_handler_feed_update, socket_open_callback=open_callback)
    time.sleep(1)
    while (feed_opened == False):
        print("WAITING FOR WEBSOCKET TO OPEN MOWAA")
        pass
    return True
setupWebSocket()
api.subscribe([f'NFO|{optoken}',f'NFO|{optokenC}'])
time.sleep(1)
while True:
    opltp =float(feedJson[optoken]['ltp'])
    time.sleep(1)
    opltpC =float(feedJson[optokenC]['ltp'])
    time.sleep(1)
    print("CE :",opltpC,"  ", "PE :",opltp)
    if opltpC >= mondayentryC or opltp >= mondayentry :
        if opltp >= mondayentry:
            api.place_order(buy_or_sell='B', product_type='M',
                            exchange='NFO', tradingsymbol=optionToken,
                            quantity=25, discloseqty=0, price_type='MKT',
                            retention='DAY', remarks='PE ENTERED')
            print("PE ENTERED")
            while True:
                opltp = float(api.get_quotes(exchange='NFO', token=optoken)['lp'])
                # print("PE LTP :   ",opltp)
                
                if ((datetime.datetime.now()).time()).hour == 9 and ((datetime.datetime.now()).time()).minute >= 45:
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionToken,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='PE SQUARED OFF')
                    print("PE SQUARED OFF")
                    exit()
                if opltp >= mondaytarget:
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionToken,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='TARGET HIT')
                    print("PE TARGET HIT")
                    exit()
                if opltp <= mondaystoploss:
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionToken,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='STOPLOSS HIT')
                    print("PE SL HIT")
                    exit()
        if opltpC >= mondayentryC:
            api.place_order(buy_or_sell='B', product_type='M',
                            exchange='NFO', tradingsymbol=optionTokenC,
                            quantity=25, discloseqty=0, price_type='MKT',
                            retention='DAY', remarks='ENTRY BUY ORDER')
            print("CE ENTRY TRIGGERED")
            while True:
                opltpC = float(api.get_quotes(exchange='NFO', token=optokenC)['lp'])
                # print("CE LTP :   ",opltpC)
                if ((datetime.datetime.now()).time()).hour == 9 and ((datetime.datetime.now()).time()).minute >= 45:
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionTokenC,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='CE SQUARED OFF')
                    print("CE SQUARED OFF")
                    exit()
                if opltpC >= mondaytargetC :
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionTokenC,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='TARGET ORDER')
                    print("CE TARGET TRIGGERED")
                    exit()
                if opltpC <= mondaystoplossC:
                    api.place_order(buy_or_sell='S', product_type='M',
                                    exchange='NFO', tradingsymbol=optionTokenC,
                                    quantity=25, discloseqty=0, price_type='MKT',
                                    retention='DAY', remarks='SL ORDER')
                    print("CE STOPLOSS HIT")
                    exit()
    
    if ((datetime.datetime.now()).time()).hour == 9 and ((datetime.datetime.now()).time()).minute >= 45:
        print('Market Closed Mowaa')
        exit()
