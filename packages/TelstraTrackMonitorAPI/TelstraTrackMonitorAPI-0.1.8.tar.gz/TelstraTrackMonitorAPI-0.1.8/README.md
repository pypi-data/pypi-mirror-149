# TelstraTrackMonitorAPI
Intended to be a Structured way to interface with Telstra's Track & Monitor API.\

It mostly focuses on devices for now.

Has classes and methods for:
* Token Management - Get/Load/save/update
* Getting Devices with specified params

# Usage
Firstly you need to make up an instance of the TokenManager Class.\
This Class will be used to pass the retrieved Token to other methods later
~~~python
ttm_token = TelstraTrackMonitorAPI.TokenManager(
	server='https://tapi.telstra.com'
	client_id='XXXXXXXXXXXXXXXXXXXXX'
	client_secret='XXXXXXXXXXXXXXXXXXXXX'
	save_location='ttm_token.json'
)
ttm_token.load_token() #Loads any token information in the save_location json file
ttm_token.update_token() # Check if the token is expired and renews if so.
~~~
Once the above is done we can actually pull some information from Track & Monitor API
~~~python
with TelstraTrackMonitorAPI.Sessions(ttm_token.server,ttm_token.access_token) as TTM:
    ttm_devices=TTM.devices_get(
        {'$filter':'not(deviceFriendlyName eq null)'}
    )
~~~
The above method will get all devices in Track & Monitor API that have a Device Friendly name.


# Installation

`pip install TelstraTrackMonitorAPI`
