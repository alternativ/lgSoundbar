import temescal, logging, time
from flask import Flask, request
from flask_api import status

logging.basicConfig(level=logging.DEBUG)

def initialize_connection(ip):
    global speaker
    global connectionSuccesful
    try:
        speaker = temescal.temescal(ip, callback=speaker_callback)
    except Exception as e:
        logging.error(f"failed to create a connection: {e}")
        connectionSuccesful = False
    else:
        logging.info("connection setup succesfully")
        connectionSuccesful =  True

def speaker_callback(response):
    global commandResponse
    if (response["data"]):
        logging.info(response["data"])
        commandResponse = response["data"]
    else:
        logging.info(response)
        commandResponse = False

app = Flask(__name__)

@app.route('/', methods=['GET'])
def returnhealth():
    return("nothing to see here, move along", status.HTTP_200_OK)

@app.route('/change/source', methods=['GET'])
def getinfo():
    if request.args.get("source"):
        requiredSource = (request.args.get("source"))
        try:
            initialize_connection("172.16.0.16")
            if requiredSource in ('KPN','Netflix','YouTube'):
                # speaker.set_func(0)
                speaker.set_func(15)
            else:
                logging.info("No action required")
            time.sleep(0.1)
            if connectionSuccesful:
                return(f"output: {commandResponse}", status.HTTP_200_OK)
            else:
                return(f"issue: {commandResponse}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            return(f"issue occured", status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return(f"issue occured", status.HTTP_400_BAD_REQUEST)
