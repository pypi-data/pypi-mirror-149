import csv
import json
import os
import errno
import socket
import sys
import urllib
import zipfile
from os import path
import requests
import logging
import configparser

logging.basicConfig(filename = 'edlwsapi.log',
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
LOGGER = logging.getLogger('EdelweissAPIConnect')

LOG_LEVELS = {
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

def init_logger(conf):
    """
    Method to initialize logger configuration via provided configuration object.
    - Parameters:
        conf : ConfigParser object of provided settings.ini file.
    """

    LOG_LEVEL=None
    LOG_FILE=None
    if 'LOG_LEVEL' in conf['GLOBAL'] and conf['GLOBAL']['LOG_LEVEL'] in LOG_LEVELS:
        LOG_LEVEL = LOG_LEVELS[conf['GLOBAL']['LOG_LEVEL']]
    if 'LOG_FILE' in conf['GLOBAL']:
        LOG_FILE = conf['GLOBAL']['LOG_FILE']
    if LOG_FILE or LOG_LEVEL:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        LOG_FILE = LOG_FILE if LOG_FILE else 'edlwsapi.log'
        LOG_LEVEL = LOG_LEVEL if LOG_LEVEL else logging.INFO
        logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        LOGGER = logging.getLogger('EdelweissAPI')
        return LOGGER

def init_proxies(conf):
    """
    Method to load proxy parameters from configuration file.
    - Parameter:
        conf: ConfigParser object of provided configuration file.
    """

    if conf and 'PROXY' in conf:
        if conf['PROXY'].get('HTTPS_PROXY') and conf['PROXY'].get('HTTP_PROXY'):
            LOGGER.info("Found proxy related configurations.")
            return {
                    'http': conf['PROXY'].get('HTTP_PROXY'),
                    'https': conf['PROXY'].get('HTTPS_PROXY'),
                }
    return {}


class EdelweissAPIConnect:

    def __init__(self, ApiKey, Password, reqID, downloadContract: bool, conf=None):
        self.conf = None
        self.__init_logger = init_logger
        if conf:
            self.conf = configparser.ConfigParser()
            try:
                if path.exists(conf):
                    self.conf.read(conf)
                    self.__init_logger(self.conf)
                    LOGGER.info("Loggers initiated with provided configuration.")
                else:
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), conf)
            except Exception as ex:
                LOGGER.exception("Error occurred while parsing provided configuaration file: %s", ex)
                raise ex
        else:
            LOGGER.info("Logger initiated with default values.")

        self.proxies = {}
        self.version = '1.0.2'
        self.dc = downloadContract
        self.instruments = []
        self.mfInstruments = []
        self.filename = "data_" + ApiKey + '.txt'
        self.__config = self.__Config(self.conf)
        self.__constants = self.__Constants()
        self.__init_proxies = init_proxies
        self.proxies = self.__init_proxies(self.conf)
        self.__http = self.__Http(self.__constants, self.proxies)
        self.__constants.set_Filename(self.filename)
        self.__constants.set_ApiKey(ApiKey)
        AppIdKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImZmIjoiVyIsImJkIjoid2ViLXBjIiwibmJmIjoxNjQ5MDc0MTE2LCJzcmMiOiJlbXRtdyIsImF2IjoiMS4wLjIiLCJhcHBpZCI6ImEyMTRmMjBiNjkxM2VjMjUxZjdjMjA1MGJiYWY2MDk4IiwiaXNzIjoiZW10IiwiZXhwIjoxNjQ5MDk3MDAwLCJpYXQiOjE2NDkwNzQ0MTZ9.Ci4uGuc41mXkkBw-Wp3mxkCCDSpoiXZ8V0R_x4eIl78"

        if conf and self.conf['GLOBAL'].get('AppIdKey'):
            AppIdKey = self.conf['GLOBAL'].get('AppIdKey')
        self.__constants.set_AppIdKey(AppIdKey)

        if path.exists(self.filename):
            LOGGER.info("User data file found, loading data.")
            read = open(self.filename, 'r').read()
            j = json.loads(read)
            self.__constants.set_VendorSession(j['vt'])
            self.__constants.set_JSession(j['auth'])
            self.__constants.set_eqAccId(j['eqaccid'])
            self.__constants.set_coAccId(j['coaccid'])
            self.__constants.set_Data(j['data'])
            self.__constants.set_AppIdKey(j['appidkey'])
        else:
            self.__VendorSession = self.__GenerateVendorSession(ApiKey, Password)
            self.__Authorization = self.__GetAuthorization(reqID)

        self.__CheckUpdate()

        self.__Instruments()

        self.exchanges = ['NSE', 'BSE', 'NFO', 'CDS', 'MCX', 'NCDEX']

        self.orderType = ['LIMIT', 'MARKET', 'STOP_LIMIT', 'STOP_MARKET']

        self.productType = ['BO', 'CO', 'CNC', 'MIS', 'NRML', 'MTF']

        self.validity = ['DAY', 'IOC', 'EOS', 'GTC', 'GTD']

    def __Instruments(self):
        try:
            if self.dc:
                url = self.__config.EquityContractURL
                if self.proxies:
                    proxy = urllib.request.ProxyHandler(self.proxies)
                    opener = urllib.request.build_opener(proxy)
                    urllib.request.install_opener(opener)
                    import ssl
                    ssl._create_default_https_context = ssl._create_unverified_context
                urllib.request.urlretrieve(url, 'instruments.zip')
                LOGGER.info("Downloaded instruments.zip")
                url = self.__config.MFContractURL
                urllib.request.urlretrieve(url, 'mfInstruments.zip')
                LOGGER.info("Downloaded mfInstruments.zip")

            with zipfile.ZipFile('instruments.zip', 'r') as zip_ref:
                zip_ref.extractall('instruments')
                LOGGER.info("Extracted instruments.csv")
            with open('instruments/instruments.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.instruments.append(row)
                LOGGER.info("Loaded instruments.csv")

            with zipfile.ZipFile('mfInstruments.zip', 'r') as zip_ref:
                zip_ref.extractall('mfInstruments')
                LOGGER.info("Extracted mfInstruments.csv")
            with open('mfInstruments/mfInstruments.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.mfInstruments.append(row)
                LOGGER.info("Loaded mfInstruments.csv")

        except Exception as ex:
            LOGGER.exception("Error occurred while downloading/ reading instruments: %s", ex)
            print("Error Download/Reading Instruments")

    def __CheckUpdate(self):
        LOGGER.info("Checking for new update.")
        url = self.__config.CheckUpdateURl()
        rep = self.__http.PostMethod(url, json.dumps({"lib": "EAC_PYTHON", "vsn": self.version}))
        if rep['data']['msg'] == 'MANDATORY':
            print("Mandatory Update. New version " + rep['data']['vsn'] + '. Update to new version to continue. Check changelog in documentation for details.')
            LOGGER.info("New mandatory update found. Please update to new version. Check changelog in documentation for details.")
            sys.exit(0)
        if rep['data']['msg'] == 'OPTIONAL':
            LOGGER.info("New optional update found.")
            print("New version " + rep['data']['vsn'] + " is available. Stay up to date for better experience. Check changelog in documentation for details.")

    def quantityDataValidation(self, quantity):
        '''
        Method to alidate data type of Order Quantity to be integer only.
        '''
        try:
            quantity = int(quantity)
            return quantity
        except ValueError as e:
            print("Error Occured : Quantity needs to be integer!")
            LOGGER.exception("Error occurred: %s", e)
            raise


    def GetLoginData(self):
        """

        Get Login Info.

        """
        return json.dumps(self.__constants.get_Data())

    def __GenerateVendorSession(self, ApiKey, Password) -> str:
        """

        Get Login Info.

        ApiKey : Key provided by Edelweiss

        Password : Password provided by Edelweiss

        """
        self.__Login(ApiKey, Password)
        LOGGER.info("Vendor session generated.")

    def __GetAuthorization(self, reqId) -> str:
        """

        Get Login Info.

        reqId : Request ID generated during re-direction to a url

        """
        self.__Token(reqId)
        LOGGER.info("Authorization done succesfully.")

    def OrderBook(self):
        """

        This method will retrieve the equity Order Book. Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        """
        LOGGER.info("OrderBook method is called.")
        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.OrderBookURL().format(userid=self.__constants.get_eqAccId())
            LOGGER.debug("OrderBook method is called for 'EQ' account type")
            eq = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.OrderBookURL_comm().format(userid=self.__constants.get_coAccId(), reqtype='COMFNO')
            LOGGER.debug("OrderBook method is called for 'CO' account type")
            comm = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.OrderBookURL().format(userid=self.__constants.get_eqAccId())
            LOGGER.debug("OrderBook method is called for 'COMEQ' account type")
            url_comm = self.__config.OrderBookURL_comm().format(userid=self.__constants.get_coAccId(), reqtype='COMFNO')
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def TradeBook(self):

        """

          This method will retrieve the Trade Book. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

        """
        LOGGER.info("TradeBook method is called.")
        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.TradeBookURL().format(userid=self.__constants.get_eqAccId())
            LOGGER.debug("TradeBook method is called for 'EQ' account type")
            eq = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.TradeBookURL_comm().format(userid=self.__constants.get_coAccId())
            LOGGER.debug("TradeBook method is called for 'CO' account type")
            comm = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.TradeBookURL().format(userid=self.__constants.get_eqAccId())
            url_comm = self.__config.TradeBookURL_comm().format(userid=self.__constants.get_coAccId())
            LOGGER.debug("TradeBook method is called for 'COMEQ' account type")
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def NetPosition(self):
        """
        Net position usually is referred to in context of trades placed during the day in case of Equity, or can refer to carry forward positions in case of Derivatives, Currency and Commodity. It indicates the net obligation (either buy or sell) for the given day in a given symbol. Usually you monitor the net positions screen to track the profit or loss made from the given trades and will have options to square off your entire position and book the entire profit and loss.


       This method will retrieve the Net position. Typical trade book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

          """
        LOGGER.info("NetPosition method is called.")
        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.NetPositionURL().format(userid=self.__constants.get_eqAccId())
            LOGGER.debug("NetPosition method is called for 'EQ' account type")
            eq = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", eq)
            return json.dumps({"eq": eq, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.NetPositionURL_comm().format(userid=self.__constants.get_coAccId())
            LOGGER.debug("NetPosition method is called for 'CO' account type")
            comm = self.__http.GetMethod(url)
            LOGGER.debug("Response received: %s", comm)
            return json.dumps({"eq": "", "comm": comm})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.NetPositionURL().format(userid=self.__constants.get_eqAccId())
            url_comm = self.__config.NetPositionURL_comm().format(userid=self.__constants.get_coAccId())
            LOGGER.debug("TradeBook method is called for 'COMEQ' account type")
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def OrderDetails(self, OrderId, Exchange):
        """

          Please use this method to retrive the details of single order.
          Response Fields :
           - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Trade ID
            - Trade Status

        """
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            LOGGER.info("OrderDetails method is called for MCX/NCDEX.")
            LOGGER.debug("OrderDetails method is called for MCX/NCDEX.")
            url = self.__config.OrderDetailsURL_comm().format(userid=self.__constants.get_coAccId(), orderid=OrderId)
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)
        else:
            LOGGER.info("OrderDetails method is called.")
            LOGGER.debug("OrderDetails method is called.")
            url = self.__config.OrderDetailsURL().format(userid=self.__constants.get_eqAccId(), orderid=OrderId)
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)

    def OrderHistory(self, StartDate, EndDate):
        """

          This method will retrive all the historical orders placed from `StartDate` to `EndDate`

          StartDate : Start Date of Search

          EndDate : End Date of search

        """
        LOGGER.info("OrderHistory method is called.")

        LOGGER.debug("OrderHistory method is called with account type: %s",
            self.__constants.get_Data()['data']['lgnData']['accTyp'])

        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.OrderHistoryURL().format(userid=self.__constants.get_eqAccId(), StartDate=StartDate,
                                                         EndDate=EndDate)
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": rep, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.OrderHistoryURL_comm().format(userid=self.__constants.get_coAccId(),
                                                              StartDate=StartDate,
                                                              EndDate=EndDate)
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": "", "comm": rep})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.OrderHistoryURL().format(userid=self.__constants.get_eqAccId(), StartDate=StartDate,
                                                         EndDate=EndDate)
            url_comm = self.__config.OrderHistoryURL_comm().format(userid=self.__constants.get_coAccId(),
                                                                   StartDate=StartDate,
                                                                   EndDate=EndDate)
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response receieved for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def Holdings(self):
        """
        Holdings comprises of the user's portfolio of long-term equity delivery stocks. An instrument in a holding's portfolio remains there indefinitely until its sold or is delisted or changed by the exchanges. Underneath it all, instruments in the holdings reside in the user's DEMAT account, as settled by exchanges and clearing institutions.
        """
        LOGGER.info("Holdings method is called.")
        LOGGER.debug("Holdings method is called with account type: %s",
            self.__constants.get_Data()['data']['lgnData']['accTyp'])

        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.HoldingURL().format(userid=self.__constants.get_eqAccId())
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            return json.dumps({"eq": rep, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            LOGGER.debug("Holdings not available for 'CO' account type.")
            return json.dumps({"eq": "", "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.HoldingURL().format(userid=self.__constants.get_eqAccId())
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response receieved: %s", rep)
            LOGGER.debug("Holdings not available for 'CO' account type.")
            combine = {"eq": rep, "comm": ""}
            return json.dumps(combine)

    def PlaceTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                   Streaming_Symbol,
                   Limit_Price,
                   Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):

        """
        Order placement refers to the function by which you as a user can place an order to respective exchanges. Order placement allows you to set various parameters like the symbol, action (buy, sell, stop loss buy, stop loss sell), product type, validity period and few other custom parameters and then finally place the order. Any order placed will first go through a risk validation in our internal systems and will then be sent to exchange. Usually any order successfully placed will have OrderID and ExchangeOrderID fields populated. If ExchangeOrderID is blank it usually means that the order has not been sent and accepted at respective exchange.

        Order placement method

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceTrade method is called.")

        self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration,
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "N",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0"}

        LOGGER.debug("PlaceTrade method is called with data: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.PlaceTradeURL_comm().format(userid=self.__constants.get_coAccId())
            reply = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response received for MCX/NCDEX: %s", reply)
            return json.dumps(reply)
        else:
            url = self.__config.PlaceTradeURL().format(userid=self.__constants.get_eqAccId())
            reply = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", reply)
            return json.dumps(reply)

    def PlaceCoverTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                        Streaming_Symbol,
                        Limit_Price,
                        Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):

        """

        A Cover Order is an order type for intraday trades. A Cover Order lets you to place trades with very high leverage of up to 20 times the available limits (Cash/Stocks collateral limits)

        Pay a fraction of total order amount (10% or Rs. 20) to own the shares. In case it falls below the following price, sell it off to prevent me losing money from sharp price drops.

        - `Trading_Symbol` : Trading Symbol of the Scrip

        - `Exchange` : Exchange

        - `Action` : BUY/SELL

        - `Duration` : DAY/IOC/EOS(for BSE)

        - `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        - `Quantity` : Quantity of the scrip

        - `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        - `Limit_Price` : Limit price of scrip

        - `Disclosed_Quantity` : Quantity to be disclosed while order placement

        - `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        - `ProdcutCode` : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceCoverTrade is method is called.")
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation is disabled for commodities.")
            return

        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration,
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': '', 'flQty': "0", }

        LOGGER.debug("PlaceCoverTrade method is called with data: %s", data)
        url = self.__config.PlaceCoverTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PostMethod(url, json.dumps(data))
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)

    def PlaceGtcGtdTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity, streaming_symbol,
                         Limit_Price,
                         Product_Code, DTDays):
        LOGGER.info("PlaceGtcGtdTrade method is called.")

        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'ordTyp': Order_Type,
                'qty': Quantity, 'lmPrc': Limit_Price, 'prdCode': Product_Code,
                'dtDays': DTDays, 'ordSrc': 'API', 'vnCode': '', 'oprtn': '<=', 'srcExp': '', 'tgtId': '',
                'brnchNm': '', 'vlDt': DTDays, 'sym': streaming_symbol,
                'brk': '', }

        LOGGER.debug("PlaceGtcGtdTrade method is called with data: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.PlaceTradeURL_comm().format(userid=self.__constants.get_coAccId())
            reply = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", reply)
            return json.dumps(reply)
        else:
            url = self.__config.PlaceGtcGtdTradeURL().format(userid=self.__constants.get_eqAccId())
            reply = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", reply)
            return json.dumps(reply)

    def ModifyTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                    Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                    ProductCode="CNC"):
        """
        Modify orders allows a user to change certain aspects of the order once it is placed. Depending on the execution state of the order (i.e. either completely open, partially open) there are various levels of modification allowed. As a user you can edit the product type, order quantity, order validity and certain other parameters. Please note that any modifications made to an order will be sent back to the risk system for validation before being submitted and there are chances that an already placed order may get rejected in case of a modification.

        Modify Order

        `Trading_Symbol` : Trading Symbol of the Scrip

        `Exchange` : Exchange

        `Action` : BUY/SELL

        `Duration` : DAY/IOC/EOS(for BSE)

        `Order_Type`: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        `Quantity` : Quantity of the scrip

        `Streaming_Symbol` : companycode_exchange to be obtained from Contract file downloaded

        `Limit_Price` : Limit price of scrip

        `Disclosed_Quantity` : Quantity to be disclosed while order placement

        `TriggerPrice` : Trigger Price applicable for SL/SL-M Orders

        `ProductCode` : CNC/MIS/NRML/MTF


        """
        LOGGER.info("ModifyTrade method is called.")

        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyTrade method is called with method: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.ModifyTradeURL_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__config.ModifyTradeURL().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

    def ModifyCoverTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                         Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                         ProductCode="CNC"):

        """

        Modify Cover Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("ModifyCoverTrade method is called")
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation is blocked for commodities.")
            return


        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyCoverTrade method is called with data: %s", data)
        url = self.__config.ModifyCoverTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PutMethod(url, json.dumps(data))
        LOGGER.debug("Response recieved: %s", resp)
        return json.dumps(resp)

    def CancelTrade(self, OrderId, Exchange, Order_Type, Product_Code):
        """

        An order can be cancelled, as long as on order is open or pending in the system

        Cancel Order

        OrderId : Nest OrderId

        """
        LOGGER.info("CancelTrade method is called.")

        data = {"nstOID": OrderId, "exc": Exchange, "prdCode": Product_Code, "ordTyp": Order_Type}
        LOGGER.debug("CancelTrade method is called with data: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.CancelTradeURL_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__config.CancelTradeURL().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response recieved: %s", resp)
            return json.dumps(resp)

    def MFOrderBook(self, fromDate, toDate):
        '''

        This method will retrieve the MF Order Book.
         fromDate: From Date
         toDate: To Date
         :return: MF Order Book

         Typical order book response will be a nested JSON containing below fields
            - Symbol
            - Product Type
            - Order type
            - Quantity
            - Price
            - Validity
            - Order ID
            - Order Status

        '''
        LOGGER.info("MFOrderBook method is called.")
        url = self.__config.OrderBookMFURL().format(userid=self.__constants.get_eqAccId(), fromDate=fromDate,
                                                    toDate=toDate)
        rep = self.__http.GetMethod(url)
        LOGGER.debug("MFOrderBook method is called. Receieved response: %s", rep)
        return json.dumps(rep)

    def ExitCoverTrade(self, OrderId):
        """
        This functionality allows you to completely exit a cover order which includes cancelling any unplaced orders and also completely squaring off any executed orders. For the orders which were executed it will usually modify the stop loss order leg and place it as a market order to ensure execution, while any non executed quantity order will get cancelled.

       Exit Cover Order

       OrderId : Nest OrderId

        """
        LOGGER.info("ExitCoverTrade method is called.")
        url = self.__config.ExitCoverTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PutMethod(url, json.dumps({"nstOID": OrderId}))
        LOGGER.debug("ExitCoverTrade method is called for nstOID: %s", OrderId)
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)

    def ExitBracketTrade(self, Order_Id, Syom_Id, Status):
        """
        Similar to Exit Cover order the functionality will ensure that any non executed open order will be cancelled. However for any orders which are executed it will automatically cancel one of the target or stop loss legs and modify the other leg to be placed as a market order. This will ensure that any executed orders will be squared off in position terms.

       Exit Bracket Order

       OrderId : Nest OrderId

       Syom_Id : Syom_Id obtained post placing Bracket Order

       Status: Current Status of the Bracket Order

       """
        LOGGER.info("ExitBracketTrade method is called.")
        data = {'nstOrdNo': Order_Id, 'syomID': Syom_Id, 'sts': Status}
        params = locals()
        LOGGER.debug("ExitBracketTrade method is called with data: %s", data)
        url = self.__config.ExitBracketTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.DeleteMethod(url, json.dumps(data))
        del (params["self"])
        LOGGER.debug("Response receieved: %s", resp)
        return json.dumps(resp)

    def PlaceBracketTrade(self, Exchange, Streaming_Symbol, Transaction_Type, Quantity, Duration, Disclosed_Quantity,
                          Limit_Price, Target, StopLoss, Trailing_Stop_Loss='Y', Trailing_Stop_Loss_Value="1"):

        """

        Bracket Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        Target : Absolute Target value

        StopLoss :Absolute Stop Loss value

        Trailing_Stop_Loss : Y/N

        Trailing_Stop_Loss_Value : Number

        """
        LOGGER.info("PlaceBracketTrade method is called.")
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            print('Operation invalid for Commodities')
            LOGGER.debug("Operation invalid for commodities.")
            return

        Quantity = self.quantityDataValidation(Quantity)

        data = {'exc': Exchange, 'sym': Streaming_Symbol,
                'trnsTyp': Transaction_Type, 'qty': Quantity, 'dur': Duration, 'dsQty': Disclosed_Quantity,
                'prc': Limit_Price, 'trdBsdOn': "LTP", 'sqOffBsdOn': 'Absolute', 'sqOffVal': Target,
                'slBsdOn': 'Absolute', 'slVal': StopLoss, 'trlSl': Trailing_Stop_Loss,
                'trlSlVal': Trailing_Stop_Loss_Value, 'ordSrc': 'API'}
        LOGGER.debug("PlaceBracketTrade method is called with data: %s", data)
        url = self.__config.PlaceBracketTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PostMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)

    def PlaceBasketTrade(self, orderlist):
        """

        Basket order allows user to place multiple orders at one time. User can place orders for multiple scrips all at once. One just creates multiple orders for same or different securities and club these orders together to be placed in one go. This helps save time.

        orderlist : List of Order to be placed, Refer: Order Class

        """
        LOGGER.info("PlaceBasketTrade method is called.")
        isComm = False
        lst = []
        for x in orderlist:
            if x.exc == 'MCX' or x.exc == 'NCDEX':
                isComm = True
                continue

            x.qty = self.quantityDataValidation(x.qty)

            data = {'trdSym': x.trdSym, 'exc': x.exc, 'action': x.action, 'dur': x.dur,
                    'ordTyp': x.ordTyp, 'qty': x.qty, 'dscQty': x.dscQty,
                    'price': x.price, 'trgPrc': x.trgPrc, 'prdCode': x.prdCode, 'vnCode': '',
                    'rmk': ''}
            lst.append(data)

        fd = {
            "ordLst": lst,
            "ordSrc": "API"
        }
        if isComm == True:
            print('Basket Order not available for Commodity')
        LOGGER.debug("PlaceBasketTrade method is called with data: %s", fd)
        url = self.__config.PlaceBasketTradeURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PostMethod(url, json.dumps(fd))
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)

    def Limits(self):
        """
        Limits refers to the cumulative margins available in your account which can be used for trading and investing in various products. Limits is a combination of the free cash you have (i.e. un-utilized cash), cash equivalent securities (usually margin pledged securities), any money which is in transit (T1/T2 day sell transaction values) and others, all of which can be used for placing orders. Usually whenever you place an order in a given asset and product type our risk management system assesses your limits available and then lets the orders go through or blocks the orders. Limits are dynamic in nature and can be influenced by the Mark to Markets in your positions and sometimes even by the LTP of your holdings.

        Get limits


        """
        LOGGER.info("Limits method is called.")
        LOGGER.debug("Limits method is called for accout type: %s",
                self.__constants.get_Data()['data']['lgnData']['accTyp'])
        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.LimitsURL().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.LimitsURL_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": resp})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.LimitsURL().format(userid=self.__constants.get_eqAccId())
            url_comm = self.__config.LimitsURL_comm().format(userid=self.__constants.get_coAccId())
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response recevied for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def GetAMOStatus(self):
        """

        Get AMO status

        """
        LOGGER.info("Limits method is called.")
        LOGGER.debug("Limits method is called for accout type: %s",
                self.__constants.get_Data()['data']['lgnData']['accTyp'])

        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.GetAMOFlag()
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": resp, "comm": ""})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.GetAMOFlag_comm()
            resp = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied: %s", resp)
            return json.dumps({"eq": "", "comm": resp})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.GetAMOFlag()
            url_comm = self.__config.GetAMOFlag_comm()
            rep = self.__http.GetMethod(url)
            LOGGER.debug("Response recevied for eq: %s", rep)
            rep_comm = self.__http.GetMethod(url_comm)
            LOGGER.debug("Response recevied for comm: %s", rep_comm)
            combine = {"eq": rep, "comm": rep_comm}
            return json.dumps(combine)

    def PlaceAMOTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                      Streaming_Symbol, Limit_Price, Disclosed_Quantity="0", TriggerPrice="0", ProductCode="CNC"):

        """
        After market order or AMO in short refers to orders which can be placed once the markets or exchanges are closed for trading. You can place AMO post market hours which will result in the order in question being placed automatically by 9:15 AM - 9:30 AM the next business day. AMO orders usually need to be limit orders in order to prevent inadvertent execution in case of adverse price movement in markets at beginning of day. AMO is a useful way to place your orders in case you do not have time to place orders during market hours.

        After Market Order trade

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("PlaceAMOTrade method is called.")

        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'posSqr': "false",
                'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}

        LOGGER.debug("PlaceAMOTrade method is called with data: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.PlaceAMOTrade_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

        else:
            url = self.__config.PlaceAMOTrade().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PostMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

    def ModifyAMOTrade(self, Trading_Symbol, Exchange, Action, Duration, Order_Type, Quantity,
                       Streaming_Symbol, Limit_Price, Order_ID, Disclosed_Quantity="0", TriggerPrice="0",
                       ProductCode="CNC"):

        """

        Modify After Market Order

        Trading_Symbol : Trading Symbol of the Scrip

        Exchange : Exchange

        Action : BUY/SELL

        Duration : DAY/IOC/EOS(for BSE)

        Order_Type: LIMIT/MARKET/STOP_LIMIT/STOP_MARKET

        Quantity : Quantity of the scrip

        Streaming_Symbol : companycode_exchange to be obtained from Contract file downloaded

        Limit_Price : Limit price of scrip

        Disclosed_Quantity : Quantity to be disclosed while order placement

        TriggerPrice : Trigger Price applicable for SL/SL-M Orders

        ProductCode : CNC/MIS/NRML/MTF

        """
        LOGGER.info("ModifyAMOTrade method is called.")

        Quantity = self.quantityDataValidation(Quantity)

        data = {'trdSym': Trading_Symbol, 'exc': Exchange, 'action': Action, 'dur': Duration, 'flQty': "0",
                'ordTyp': Order_Type, 'qty': Quantity, 'dscQty': Disclosed_Quantity, 'sym': Streaming_Symbol,
                'mktPro': "",
                'lmPrc': Limit_Price, 'trgPrc': TriggerPrice, 'prdCode': ProductCode, 'dtDays': '', 'nstOID': Order_ID}
        LOGGER.debug("ModifyAMOTrade method is called with data: %s", data)

        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.ModifyAMOTrade_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

        else:
            url = self.__config.ModifyAMOTrade().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s",resp)
            return json.dumps(resp)

    def CancelAMOTrade(self, OrderId, Exchange, Order_Type, Product_Code):
        """

        Cancel After Market Order

        OrderId : Nest Order Id

        """
        LOGGER.info("CancelAMOTrade method is called.")
        data = {"nstOID": OrderId, "exc": Exchange, "prdCode": Product_Code, "ordTyp": Order_Type}
        LOGGER.debug("CancelAMOTrade method is called with data: %s", data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.CancelAMOTrade_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", resp)
            return json.dumps(resp)

        else:
            url = self.__config.CancelAMOTrade().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response received: %s", resp)
            return json.dumps(resp)

    def PositionSquareOff(self, orderlist):
        """

        Square off is a term used in intraday and simply means closing all open positions by the end of the trading day

        orderList : List of orders to be Squared Off. Refer : Orders class.

        """
        lst_eq = []
        lst_comm = []
        LOGGER.info("PositionSquareOff method is called.")
        for x in orderlist:

            x.qty = self.quantityDataValidation(x.qty)

            if x.exc == 'MCX' or x.exc == "NCDEX":
                data = {'trdSym': x.trdSym, 'exc': x.exc, 'action': x.action, 'dur': x.dur, 'flQty': "0",
                        'ordTyp': x.ordTyp, 'qty': x.qty, 'dscQty': x.dscQty, 'sym': x.sym,
                        'mktPro': "",
                        'lmPrc': x.price, 'trgPrc': x.trgPrc, 'prdCode': x.prdCode, 'dtDays': '', 'posSqr': "true",
                        'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}
                lst_comm.append(data)
            else:
                data = {'trdSym': x.trdSym, 'exc': x.exc, 'action': x.action, 'dur': x.dur, 'flQty': "0",
                        'ordTyp': x.ordTyp, 'qty': x.qty, 'dscQty': x.dscQty, 'sym': x.sym,
                        'mktPro': "",
                        'lmPrc': x.price, 'trgPrc': x.trgPrc, 'prdCode': x.prdCode, 'dtDays': '', 'posSqr': "true",
                        'minQty': "0", 'ordSrc': "API", 'vnCode': '', 'rmk': ''}
                lst_eq.append(data)

        resp_eq = ""
        resp_comm = ""

        if len(lst_eq) > 0:
            url = self.__config.PositionSqOffURL().format(userid=self.__constants.get_eqAccId())
            LOGGER.debug("PositionSquareOff method is called with data: %s.", lst_eq)
            resp_eq = self.__http.PostMethod(url, json.dumps(lst_eq))

        if len(lst_comm) > 0:
            url_comm = self.__config.PositionSqOffURL().format(userid=self.__constants.get_coAccId())
            LOGGER.debug("PositionSquareOff method is called with data: %s.", lst_comm)
            resp_comm = self.__http.PostMethod(url_comm, json.dumps(lst_comm))

        resp = {"eq": resp_eq, "comm": resp_comm}
        LOGGER.debug("Response received: %s", resp)
        return json.dumps(resp)


    def ConvertPosition(self, Order_Id, Fill_Id, New_Product_Code, Old_Product_Code, Exchange, orderType):
        """

        Convert Position : converts your holding position from MIS to CNC and vice-versa

        Order_Id : Nest Order id

        Fill_Id : Fill Id of the trade obtained from Trade API

        New_Product_Code: New Product code of the trade

        Old_Product_Code : Existing Product Code of the trade

        """
        LOGGER.info("ConvertPosition method is called.")
        data = {'nstOID': Order_Id, 'flID': Fill_Id,
                'prdCodeCh': New_Product_Code, 'prdCode': Old_Product_Code,
                'exc': Exchange, 'ordTyp': orderType}

        LOGGER.debug("ConvertPosition method is called with data %s",data)
        if Exchange == 'MCX' or Exchange == 'NCDEX':
            url = self.__config.ConvertPositionURL_comm().format(userid=self.__constants.get_coAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)
        else:
            url = self.__config.ConvertPositionURL().format(userid=self.__constants.get_eqAccId())
            resp = self.__http.PutMethod(url, json.dumps(data))
            LOGGER.debug("Response receieved: %s", resp)
            return json.dumps(resp)
    # MF Methods

    def PlaceMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                ReInv_Flag, Folio_Number,
                Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Mandate_Id):

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''
        LOGGER.info("PlaceMF method is called.")
        data = {'currentOrdSts': '', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.get_eqAccId(), 'folioNo': Folio_Number,
                'ordTyp': 'FRESH', 'txnId': '0', 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': Mandate_Id, 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D'}

        LOGGER.info("PlaceMF method is called with data: %s.", data)
        url = self.__config.PlaceMFURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PostMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp )
        return json.dumps(resp)

    def ModifyMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                 ReInv_Flag, Folio_Number,
                 Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                 Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id, Mandate_Id):

        '''

        certain attributes of a MF order may be modified., as long as on order is open or pending in the system

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Order_Type:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:


        '''
        LOGGER.info("ModifyMF method is called.")
        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.get_eqAccId(), 'folioNo': Folio_Number,
                'ordTyp': 'MODIFY', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D', 'mdtId':Mandate_Id}

        LOGGER.debug("PlaceMF method is called with data: %s.", data)
        url = self.__config.PlaceMFURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PutMethod(url, json.dumps(data))
        LOGGER.debug("Response received: %s", resp )
        return json.dumps(resp)


    def CancelMF(self, Token, ISIN_Code, Transaction_Type, Client_Code, Quantity, Amount,
                 ReInv_Flag, Folio_Number,
                 Scheme_Name, Start_Date, End_Date, SIP_Frequency,
                 Generate_First_Order_Today, Scheme_Plan, Scheme_Code, Transaction_Id):

        '''

        Token:

        ISIN_Code:

        Transaction_Type:

        Client_Code:

        Quantity:

        Amount:

        ReInv_Flag:

        Folio_Number:

        Scheme_Name:

        Start_Date:

        End_Date:

        SIP_Frequency:

        Generate_First_Order_Today:

        Scheme_Plan:

        Scheme_Code:

        '''
        LOGGER.info("CancelMF method is called.")
        data = {'currentOrdSts': 'ACCEPTED', 'token': Token, 'isin': ISIN_Code, 'txnTyp': Transaction_Type,
                'clientCode': Client_Code, 'qty': Quantity, 'amt': Amount, 'reInvFlg': ReInv_Flag,
                'reqstdBy': self.__constants.get_eqAccId(), 'folioNo': Folio_Number,
                'ordTyp': 'CANCEL', 'txnId': Transaction_Id, 'schemeName': Scheme_Name, 'rmrk': '',
                'mnRdmFlg': '', 'ordSrc': 'API', 'strtDy': "1", 'strtDt': Start_Date, 'endDt': End_Date,
                'sipFrq': SIP_Frequency, 'gfot': Generate_First_Order_Today, 'tnr': '999',
                'mdtId': '', 'sipregno': '', 'siporderno': '',
                'schemePlan': Scheme_Plan, 'schemeCode': Scheme_Code, 'euinnumber': '', 'dpc': 'Y',
                'closeAccountFlag': 'N',
                'kycflag': '1', 'euinflag': 'N', 'physicalFlag': 'D'}

        LOGGER.debug("CancelMF with data %s", data)
        url = self.__config.CancelMFURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.PutMethod(url, json.dumps(data))
        LOGGER.debug("Response recevied: %s", resp)
        return json.dumps(resp)

    def HoldingsMF(self):
        LOGGER.info("HoldingsMF method is called.")
        params = locals()
        del (params["self"])
        url = self.__config.HoldingsMFURL().format(userid=self.__constants.get_eqAccId())
        resp = self.__http.GetMethod(url)
        LOGGER.info("HoldingsMF method is called. Response recevied: %s",resp)
        return json.dumps(resp)

    # MF methods

    def __Login(self, source, password):
        params = locals()
        del (params["self"])
        url = self.__config.LoginURL().format(vendorId=source)
        rep = self.__http.PostMethod(url, json.dumps({"pwd": password}))
        if rep != "":
            vt = rep['msg']
            self.__constants.set_VendorSession(vt)
            LOGGER.info("User logged in successfully.")
        else:
            LOGGER.info("User unable to login.")
            LOGGER.debug("User unable to login.")
            sys.exit()

    def __Token(self, reqId):
        params = locals()
        del (params["self"])
        url = self.__config.TokenURL()
        rep = self.__http.PostMethod(url, json.dumps({"reqId": reqId}), False)

        if rep != "":
            self.__constants.set_Data(rep)
            if rep['data']['lgnData']['accTyp'] == 'EQ':
                self.__constants.set_eqAccId(rep['data']['lgnData']['accs']['eqAccID'])
            elif rep['data']['lgnData']['accTyp'] == 'CO':
                self.__constants.set_coAccId(rep['data']['lgnData']['accs']['coAccID'])
            elif rep['data']['lgnData']['accTyp'] == 'COMEQ':
                self.__constants.set_eqAccId(rep['data']['lgnData']['accs']['eqAccID'])
                self.__constants.set_coAccId(rep['data']['lgnData']['accs']['coAccID'])

            self.__constants.set_JSession(rep['data']['auth'])

            prop = json.dumps({'vt': self.__constants.get_VendorSession(),
                               'auth': self.__constants.get_JSession(),
                               'eqaccid': self.__constants.get_eqAccId(),
                               'coaccid': self.__constants.get_coAccId(),
                               'data': self.__constants.get_Data(),
                               'appidkey': self.__constants.get_AppIdKey()})
            writetofile = open(self.filename, 'w').write(prop)
            LOGGER.debug("Login details are pickled in file.")
        else:
            print("\nYour login Request ID has expired, kindly regenerate it and try again!")
            LOGGER.debug("Login request id has expired. Need to regenerate.")
            sys.exit()

    def Logout(self):
        LOGGER.info("Logout method called.")
        LOGGER.debug("Logout method called with account type: %s",
            self.__constants.get_Data()['data']['lgnData']['accTyp'])
        params = locals()
        del (params["self"])
        if self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'EQ':
            url = self.__config.LogoutURL().format(userid=self.__constants.get_eqAccId())
            rep = self.__http.PutMethod(url, {})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'CO':
            url = self.__config.LogoutURL().format(userid=self.__constants.get_coAccId())
            rep = self.__http.PutMethod(url, {})

        elif self.__constants.get_Data()['data']['lgnData']['accTyp'] == 'COMEQ':
            url = self.__config.LogoutURL().format(userid=self.__constants.get_eqAccId())
            rep = self.__http.PutMethod(url, {})

        if rep != "":
            if path.exists(self.filename):
                LOGGER.debug("File with account related details is removed.")
                os.remove(self.filename)
            self.__constants.set_Data("")

    class __Constants:

        def __init__(self):
            self.__VendorSession = ""
            self.__ApiKey = ""
            self.__eqAccId = ""
            self.__coAccId = ""
            self.__JSessionId = ""
            self.__AppIdKey = ""
            self.__Data = ""
            self.__Filename = ""

        def set_VendorSession(self, val):
            self.__VendorSession = val

        def get_VendorSession(self):
            return self.__VendorSession

        def set_ApiKey(self, val):
            self.__ApiKey = val

        def get_ApiKey(self):
            return self.__ApiKey

        def set_eqAccId(self, val):
            self.__eqAccId = val

        def set_coAccId(self, val):
            self.__coAccId = val

        def get_eqAccId(self):
            return self.__eqAccId

        def get_coAccId(self):
            return self.__coAccId

        def set_JSession(self, val):
            self.__JSessionId = val

        def get_JSession(self):
            return self.__JSessionId

        def set_AppIdKey(self, val):
            self.__AppIdKey = val

        def get_AppIdKey(self):
            return self.__AppIdKey

        def set_Data(self, val):
            self.__Data = val

        def get_Data(self):
            return self.__Data

        def set_Filename(self, val):
            self.__Filename = val

        def get_Filename(self):
            return self.__Filename

    class __Config:

        def __init__(self, conf=None):

            self.baseurleq = "https://client.edelweiss.in/edelmw-eq/eq/"
            self.baseurlcomm = "https://client.edelweiss.in/edelmw-comm/comm/"
            self.baseurlcontent = "https://client.edelweiss.in/edelmw-content/content/"
            self.baseurllogin = "https://client.edelweiss.in/edelmw-login/login/"
            self.basemflogin = "https://client.edelweiss.in/edelmw-mf/mf/"
            self.EquityContractURL = "https://client.edelweiss.in/app/toccontracts/instruments.zip"
            self.MFContractURL = "https://client.edelweiss.in/app/toccontracts/mfInstruments.zip"

            if conf and 'GLOBAL' in conf:
                if conf['GLOBAL'].get('BasePathLogin'):
                    self.baseurllogin = conf['GLOBAL']['BasePathLogin']
                if conf['GLOBAL'].get('BasePathEq'):
                    self.baseurleq = conf['GLOBAL']['BasePathEq']
                if conf['GLOBAL'].get('BasePathComm'):
                    self.baseurlcomm = conf['GLOBAL']['BasePathComm']
                if conf['GLOBAL'].get('BasePathContent'):
                    self.baseurlcontent = conf['GLOBAL']['BasePathContent']
                if conf['GLOBAL'].get('BasePathMf'):
                    self.basemflogin = conf['GLOBAL']['BasePathMf']
                if conf['GLOBAL'].get('EquityContractURL'):
                    self.EquityContractURL = conf['GLOBAL']['EquityContractURL']
                if conf['GLOBAL'].get('MFContractURL'):
                    self.MFContractURL = conf['GLOBAL']['MFContractURL']
                if conf['GLOBAL'].get('AppIdKey'):
                    self._AppIdKey = conf['GLOBAL']['AppIdKey']
                LOGGER.info("URL constants loaded with provided configuration file.")

        def CheckUpdateURl(self):
            return urllib.parse.urljoin(self.baseurlcontent, "adhoc/lib/version/")

        def OrderBookURL(self):
            return urllib.parse.urljoin(self.baseurleq, "order/book/{userid}/v1/")

        def OrderBookURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "orderbook/{userid}?rTyp={reqtype}/")

        def TradeBookURL(self):
            return urllib.parse.urljoin(self.baseurleq, "tradebook/v1/{userid}/")

        def TradeBookURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "tradebook/{userid}/")

        def NetPositionURL(self):
            return urllib.parse.urljoin(self.baseurleq, "positions/net/{userid}/")

        def NetPositionURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "positions/{userid}/")

        def PlaceTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/placetrade/{userid}/")

        def PlaceTradeURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/placetrade/{userid}/")

        def PlaceBracketTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/placebrackettrade/{userid}/")

        def PlaceCoverTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/covertrade/{userid}/")

        def ModifyCoverTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/modifycovertrade/{userid}/")

        def ExitCoverTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/exitcovertrade/{userid}/")

        def PlaceBasketTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/basketorder/{userid}/")

        def ExitBracketTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/exitbrackettrade/{userid}/")

        def PlaceGtcGtdTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/placegtcgtdtrade/{userid}/")

        def PlaceGtcGtdTradeURL_comm(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/placegtcgtdtrade/{userid}/")

        def OrderDetailsURL(self):
            return urllib.parse.urljoin(self.baseurleq, "order/details/{userid}?nOID={orderid}")

        def OrderDetailsURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "orderdetails/{userid}?oID={orderid}")

        def OrderHistoryURL(self):
            return urllib.parse.urljoin(self.baseurleq, "order/history/{userid}?sDt={StartDate}&eDt={EndDate}/")

        def OrderHistoryURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "orderhistory/{userid}?sDt={StartDate}&eDt={EndDate}/")

        def ModifyTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/modifytrade/{userid}/")

        def ModifyTradeURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/modifytrade/{userid}/")

        def CancelTradeURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/canceltrade/v1/{userid}/")

        def CancelTradeURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/canceltrade/v1/{userid}/")

        def HoldingURL(self):
            return urllib.parse.urljoin(self.baseurleq, "holdings/v1/rmsholdings/{userid}/")

        def HoldingURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "reports/detail/{userid}/")

        def LimitsURL(self):
            return urllib.parse.urljoin(self.baseurleq, "limits/rmssublimits/{userid}/")

        def LimitsURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "limits/{userid}/")

        def GetAMOFlag(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/amoflag/")

        def GetAMOFlag_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/amoflag/")

        def PositionSqOffURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/position/sqroff/{userid}/")

        def ConvertPositionURL(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/convertposition/v1/{userid}/")

        def ConvertPositionURL_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/convertposition/v1/{userid}/")

        def PlaceAMOTrade(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/amo/placetrade/{userid}/")

        def PlaceAMOTrade_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/amo/placetrade/{userid}/")

        def ModifyAMOTrade(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/amo/modifytrade/{userid}/")

        def ModifyAMOTrade_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/amo/modifytrade/{userid}/")

        def CancelAMOTrade(self):
            return urllib.parse.urljoin(self.baseurleq, "trade/amo/canceltrade/v1/{userid}/")

        def CancelAMOTrade_comm(self):
            return urllib.parse.urljoin(self.baseurlcomm, "trade/amo/canceltrade/v1/{userid}/")

        # MF Related APIs

        def PlaceMFURL(self):
            return urllib.parse.urljoin(self.basemflogin, "trade/{userid}/")

        def ModifyMFURL(self):
            return urllib.parse.urljoin(self.basemflogin, "trade/{userid}/")

        def CancelMFURL(self):
            return urllib.parse.urljoin(self.basemflogin, "trade/{userid}/")

        def HoldingsMFURL(self):
            return urllib.parse.urljoin(self.basemflogin, "holding/{userid}/")

        def OrderBookMFURL(self):
            return urllib.parse.urljoin(self.basemflogin, "order/{userid}?frDt={fromDate}&toDt={toDate}/")

        # Login related APIs

        def LoginURL(self):
            return urllib.parse.urljoin(self.baseurllogin, "accounts/loginvendor/{vendorId}/")

        def TokenURL(self):
            return urllib.parse.urljoin(self.baseurllogin, "accounts/logindata/")

        def LogoutURL(self):
            return urllib.parse.urljoin(self.baseurllogin, "accounts/{userid}/logout/")

    class __Http:
        def __init__(self, constants, proxies, ssl_verify=False):
            self.__constants = constants
            self.requests = requests.session()
            if proxies:
                LOGGER.debug("Proxies are setup for HTTP requests.")
                self.requests.proxies.update(proxies)
                self.requests.verify = ssl_verify

        def GetMethod(self, url, sendSource=True):
            if sendSource:
                LOGGER.debug("Request to url: %s", url)
                response = self.requests.get(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "Source": self.__constants.get_ApiKey(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey()
                })
            else:
                LOGGER.debug("Request to url: %s", url)
                response = self.requests.get(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey()
                })
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')

            if response.status_code == 200:
                return json.loads(response.content)
            elif 200 < response.status_code <= 299:
                LOGGER.debug("Response received with status code != 200.")
                LOGGER.debug("Error response: %s", response.content.decode('UTF-8'))
                return ""
            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    print(json.dumps(json.loads(response.content.decode('UTF-8'))))
                    if path.exists(self.__constants.get_Filename()):
                        os.remove(self.__constants.get_Filename())
                        sys.exit()
                    print("Expired session.")
                print(response.content.decode('UTF-8'))
                LOGGER.debug("Error response: %s", response.content.decode('UTF-8'))
                return ""

        def PostMethod(self, url, data, sendSource=True):
            if sendSource:
                response = self.requests.post(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "Source": self.__constants.get_ApiKey(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey(),
                    "Content-type": "application/json"}, data=data)

            else:
                response = self.requests.post(url, headers={
                    "Authorization": self.__constants.get_JSession(),
                    "SourceToken": self.__constants.get_VendorSession(),
                    "AppIdKey": self.__constants.get_AppIdKey(),
                    "Content-type": "application/json"}, data=data)

            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)
            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    print(json.dumps(json.loads(response.content.decode('UTF-8'))))
                    if path.exists(self.__constants.get_Filename()):
                        os.remove(self.__constants.get_Filename())
                    print("Expired session.")
                LOGGER.debug("Error response: %s", response.content.decode('UTF-8'))
                return ""

        def PutMethod(self, url, data: json):
            response = self.requests.put(url, headers={"Authorization": self.__constants.get_JSession(),
                                                  "Source": self.__constants.get_ApiKey(),
                                                  "SourceToken": self.__constants.get_VendorSession(),
                                                  "Content-type": "application/json"}, data=data)
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)

            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists(self.__constants.get_Filename()):
                        os.remove(self.__constants.get_Filename())
                    print("Expired session.")
                LOGGER.debug("Error response: %s", response.content.decode('UTF-8'))
                return ""

        def DeleteMethod(self, url, data: json):
            response = self.requests.delete(url, headers={"Authorization": self.__constants.get_JSession(),
                                                     "Source": self.__constants.get_ApiKey(),
                                                     "SourceToken": self.__constants.get_VendorSession(),
                                                     "Content-type": "application/json"}, data=data)
            if response.headers.get('AppIdKey') != "":
                self.__constants.set_AppIdKey = response.headers.get('AppIdKey')
            if response.status_code == 200:
                return json.loads(response.content)

            else:
                if 'Expired' in response.content.decode('UTF-8'):
                    if path.exists(self.__constants.get_Filename()):
                        os.remove(self.__constants.get_Filename())
                    print("Expired session.")
                LOGGER.debug("Error response: %s", response.content.decode('UTF-8'))
                return ""


class Feed:

    def __init__(self, accid, userid, conf):

        '''
        Streamer

        To subscribe to the streamer, Create the single instance of this mentioning `callback` method. After successsful subscription, `callback` method will be called whenever packet is available at the streamer.

         - symbols: Symbol list for subscription : Symbol_exchange to be obtained from Contract File

         - accid: Customer Account ID

         - messageCallback: Callback to receive the Feed in

         - subscribe_order

         - subscribe_quote

        '''
        self.conf = None
        self.__init_logger = init_logger
        self.__appID = None
        if conf:
            self.conf = configparser.ConfigParser()
            try:
                if path.exists(conf):
                    self.conf.read(conf)
                    self.__init_logger(self.conf)
                    LOGGER.info("Loggers initiated with provided configuration.")
                    self.__appID = self.conf['GLOBAL'].get('AppIdKey')
                else:
                    raise FileNotFoundError(
                        errno.ENOENT, os.strerror(errno.ENOENT), conf)
            except Exception as ex:
                LOGGER.exception("Error occurred while parsing provided configuaration file: %s", ex)
                raise ex
        else:
            LOGGER.info("Feed object initiated with default values.")
        self.userid = userid
        self.accid = accid

        # New code TCP
        self.sock = socket.create_connection([
            self.conf['STREAM'].get('HOST'), self.conf['STREAM'].get('PORT')
        ], 10000)
        LOGGER.info("Connection established with subscriber.")


    def subscribe(self, sysmbls, callBack, subscribe_order: bool = True, subscribe_quote: bool = True):
        self.cb = callBack
        self.sysmbls = sysmbls
        # Send data
        if subscribe_quote:
            quote = self.__CreateMessage_quote(sysmbls)
            LOGGER.debug("Requesting subscriber with quote: %s", quote)
            self.sock.send(bytes(quote, 'UTF-8'))

        if subscribe_order:
            orderfiler = self.__CreateMessage_OrderFiler()
            LOGGER.debug("Requesting subscriber with order: %s", orderfiler)
            self.sock.send(bytes(orderfiler, "UTF-8"))

        while True:
            resp = self.sock.recv(2048).decode()
            LOGGER.debug("Response recevied: %s", resp)
            if resp:
                callBack(resp)

    def __CreateMessage_quote(self, symbols):

        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})

        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe"
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def __CreateMessage_OrderFiler(self):

        req = {
            "request":
                {
                    "streaming_type": "orderFiler",
                    "data":
                        {
                            "accType": "EQ",
                            "userID": self.userid,
                            "accID": self.accid,
                            "responseType": ["ORDER_UPDATE", "TRADE_UPDATE"]
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "subscribe",
                },
            "echo": {}
        }
        return json.dumps(req) + "\n"

    def unsubscribe(self, symbols=None):
        '''

         This method will unsubscribe the symbols from the streamer. After successful invokation of this, will stop the streamer packets of these symbols.

         symbols: `streaming symbol` for the scrips which need to be unsubscribed

         void
        '''
        symset = []
        for syms in symbols:
            symset.append({"symbol": syms})
        req = {
            "request":
                {
                    "streaming_type": "quote3",
                    "data":
                        {
                            "accType": "EQ",
                            "symbols": symset
                        },
                    "formFactor": "P",
                    "appID": self.__appID,
                    "response_format": "json",
                    "request_type": "unsubscribe"
                },
            "echo": {}
        }
        LOGGER.debug("Unsubscribing with request: %s", req)
        self.sock.send(bytes(json.dumps(req) + "\n", "UTF-8"))


class Order:

    def __init__(self, Exchange, TradingSymbol, StreamingSymbol, Action, ProductCode,
                 OrderType, Duration, Price, TriggerPrice, Quantity, DisclosedQuantity,
                 GTDDate, Remark):
        '''

         Exchange: Exchange of the scrip

         TradingSymbol: Trading Symbol, to be obtained from Contract Notes

         StreamingSymbol: ScripCode_exchange

         Action: BUY/SELL

         ProductCode: CNC/MIS/NRML

         OrderType: LIMIT/MARKET

         Duration: Validity DAY/IOC

         Price: Limit price of the scrip

         TriggerPrice: Trigger Price in case of SL/SL-M Order

         Quantity: Quantity of scrip to be purchased

         DisclosedQuantity: Disclosed Quantiy for the Order

         GTDDate: Good Till Date in dd/MM/yyyy format

         Remark: remark

        '''
        self.exc = Exchange
        self.trdSym = TradingSymbol
        self.sym = StreamingSymbol
        self.action = Action
        self.prdCode = ProductCode
        self.ordTyp = OrderType
        self.dur = Duration
        self.price = Price
        self.trgPrc = TriggerPrice
        self.qty = Quantity
        self.dscQty = DisclosedQuantity
        self.GTDDate = GTDDate
        self.rmk = Remark
