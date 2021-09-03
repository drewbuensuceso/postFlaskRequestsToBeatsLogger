from logstash_async.transport import BeatsTransport
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from datetime import datetime, timedelta
import logging, logging.handlers, os


class TdSDK():
    class LSM(object):
        def __init__(self, CONNECTOR_NAME, VENDOR):
            try:
                self.CONNECTOR_NAME = CONNECTOR_NAME
                self.VENDOR = VENDOR
                self.TENANT = os.environ["TENANT"]
                """beatHost"""
                self.BeatHost = os.environ["logstash_host"]
                self.BeatPort = int(os.environ["logstash_port"]) #put into my system
            except OSError as e:
                return {"Error": e}

        def InitializeBeatsLogger(self): #initialize beats logger
            """Beats logging"""
            logger = logging.getLogger(self.CONNECTOR_NAME) #Defined by me depending on the service (TM or SvcNow)
            logger.setLevel(logging.INFO)
            """Beats transport"""
            transport = BeatsTransport(self.BeatHost, self.BeatPort, timeout=5.0, ssl_enable=False, ssl_verify=False, keyfile="", certfile="", ca_certs="")
            handler = AsynchronousLogstashHandler(
                self.BeatHost, 
                self.BeatPort, 
                transport=transport, 
                database_path= None
                )
            extra_ls_fields = {}
            extra_ls_fields["event"] = {}
            extra_ls_fields["event"]["module"] = self.CONNECTOR_NAME #Module name.
            extra_ls_fields["tenant"] = self.TENANT
            formatter = LogstashFormatter(extra_prefix=None, extra=None, message_type=self.VENDOR) #Get the integration name like servicenow or trendmicro email security)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            self.ExtraLSFields = extra_ls_fields
            self.BeatsLogger = logger
            return(self)
        
        def PostData(self, APIData, AttributeName=None):
            for record in APIData.get(f"{AttributeName}"):
                self.BeatsLogger.info(record, extra=self.ExtraLSFields)
        def PostSingleData(self, APIData):
            self.BeatsLogger.info(APIData, extra=self.ExtraLSFields)
    
    class ESM(object):
        def __init__(self,CONNECTOR_NAME, VENDOR):
            #Variables
            try:
                self.CONNECTOR_NAME = CONNECTOR_NAME
                self.VENDOR = VENDOR
                self.TENANT = os.environ["TENANT"]
                self.ES_USER = os.environ["ES_USER"]
                self.ES_PASS = os.environ["ES_PASS"]
                self.ES_HOST = os.environ["ES_HOST"]
                self.verify = True
            except OSError as e:
                return {"Error": e}

        def CheckESConn(self):
            #First Check ES works
            creds = self.ES_USER + ":" + self.ES_PASS
            ESConnect="https://"+creds+"@"+self.ES_HOST
            ES=Elasticsearch(ESConnect,timeout=10, verify_certs=self.verify, connection_class=RequestsHttpConnection)
            return ES

        def Post(self, index, doc):
            ES = self.CheckESConn()
            id = self.TENANT + "_" + self.CONNECTOR_NAME
            try:
                res = ES.index(index=index, body=doc, id=id)
                print("Posted the doc successfully.", res)
                return res
            except Exception as e:
                return e
        
        def Search(self, index, search_param):
            ES = self.CheckESConn()
            res = ES.search(index=index, body=search_param, size=1)
            return res

    class TSM(object):
        def __init__(self, CONNECTOR_NAME, VENDOR):
            try:
                self.CONNECTOR_NAME = CONNECTOR_NAME
                self.VENDOR = VENDOR
                self.TENANT = os.environ["TENANT"]
                self.TSLogFile = f"{CONNECTOR_NAME}_{self.TENANT}"
                self.current_timestamp = datetime.utcnow().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]
            except OSError as e:
                return {"Error": e}

        def GetLatestTs(self):
            try:
                file = open(self.TSLogFile, "r")
                lines = file.readlines()
                latest_timestamp = lines[-1]
                file.close()
                
                date_time_obj = datetime.strptime(latest_timestamp, r"%Y-%m-%d %H:%M:%S.%f")
                latest_timestamp = date_time_obj + + timedelta(milliseconds=1)
                latest_timestamp = latest_timestamp.strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.latest_timestamp = latest_timestamp
            except:
                self.latest_timestamp = None

        def PushTs(self):
            with open(self.TSLogFile, "a+") as file_object:
                file_object.seek(0)
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                file_object.write(self.current_timestamp)