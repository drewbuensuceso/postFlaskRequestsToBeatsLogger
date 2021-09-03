from flask import Flask, request
from TdSDK import TdSDK
import argparse
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def GetPostRequests():
    request_body = str(request.get_json())
    log.PostSingleData(request_body)    
    return request_body

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--ConectorName", help="Enter Connector/Module Name", required=True)
    parser.add_argument("-v", "--Vendor", help="Enter Vendor Name", required=True)
    parser.add_argument("-p","--flask_port", help="Enter which port the flask app should run", required=True)
    parser.add_argument("-H","--logstash_host", help="Enter Logstash Host")
    parser.add_argument("-P","--logstash_port", help="Enter Logstash Port")
    parser.add_argument("-t","--tenant", help="Enter tenant name")
    args = parser.parse_args()

    os.environ['ConectorName'] = args.ConectorName
    os.environ['Vendor'] = args.Vendor
    os.environ['flask_port'] = args.flask_port
    os.environ['logstash_host'] = args.logstash_host
    os.environ['logstash_port'] = args.logstash_port
    os.environ['TENANT'] = args.tenant

    log = TdSDK.LSM(CONNECTOR_NAME=os.environ["ConectorName"], VENDOR=os.environ["Vendor"])
    log.InitializeBeatsLogger()
    app.run(host='0.0.0.0', port=os.environ['flask_port'], debug=True)