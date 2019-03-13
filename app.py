# A Sample Device Application
# This imports the Davra Device SDK
# Which connects to the Davra Device Agent
# and from there to the Davra server
#
import time, requests, os.path
from requests.auth import HTTPBasicAuth
import json 
from pprint import pprint
import sys
from datetime import datetime
import davra_sdk as davraSdk
import paho.mqtt.client as mqtt


# Configuration for the app should be available in config.txt.
# It should contain the application name and version
appConfig = davraSdk.loadAppConfiguration()



def getProcessListing(functionInfo):
    davraSdk.log('App received instruction to get process listing ')
    s = davraSdk.runCommandWithTimeout("ps -ef ", 10)
    davraSdk.sendMessageFromAppToAgent({"finishedFunctionOnApp": functionInfo["functionName"], \
    "status": "completed", \
    "response": str(s[1]) })
    return


# Just for demonstration purposes
# A callback for when any message is seen on the comms channel from the agent.
def onAnyMessageReceived(msg):
    payload = str(msg.payload)
    if(davraSdk.isJson(payload) == False):
        return
    msg = json.loads(payload)
    # Was this message from this app itself
    if("fromApp" in msg and msg['fromApp'] == appConfig["applicationName"]):
        return
    else:
        # Was this message from the Device Agent
        if("fromAgent" in msg):
            davraSdk.log("A message was received from Device Agent")
    return



    
    
###########################   MAIN LOOP

if __name__ == "__main__":
    
    davraSdk.log("Starting device application " + appConfig["applicationName"] + " " + appConfig["applicationVersion"])
    

    # Instruct the SDK to attach to the mqtt topic and call our function when a message is received
    # Also inform the SDK of the name of this Device Application
    davraSdk.connectToAgent(appConfig["applicationName"])
    # Wait (for a max of timeout seconds) until the agent is available to communicate
    davraSdk.waitUntilAgentIsConnected(600)
    
    # Inform the Agent and Platform server that this application can do tasks on the device
    davraSdk.registerCapability('agent-action-getProcessListing', { \
            "functionParameters": { }, \
            "functionLabel": "Get the list of processes running", \
            "functionDescription": "Get the list of processes running on the device" \
    }, getProcessListing)

    # Demonstration of how to listen to any communication on the device (the agent or other apps)
    davraSdk.listenToAllMessagesFromAgent(onAnyMessageReceived)

    # Demonstration of how to send a miscellaneous message to the agent
    davraSdk.sendMessageFromAppToAgent({"message": "test from app"})

    # Main loop to run forever. 
    countMainLoop = 0
    while True:
        # Only every n seconds
        if(countMainLoop % 60 == 0):
            davraSdk.log('Application running: ' + appConfig["applicationName"])
        if(countMainLoop % 30 == 0):
			# Demonstration of sending a simple metric reading to the server
            davraSdk.sendMetricValue("counter", countMainLoop)
        countMainLoop += 1
        time.sleep(1)
# End Main loop