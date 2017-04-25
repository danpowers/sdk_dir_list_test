#!/usr/bin/python
#for ticket 307471

import globus_sdk
import time

CLIENT_ID = 'b21de7ea-af4c-4458-a71a-6c63eaa4c8f6'
EP_UUID = ''
top_level_dir = ''

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

TRANSFER_TOKEN = globus_transfer_data['access_token']

authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

for directory in tc.operation_ls(EP_UUID, path=top_level_dir):
    subdir_list = tc.operation_ls(EP_UUID, path=top_level_dir+directory['name'])
    print(subdir_list)
    time.sleep(0.5)
