#!/usr/bin/python

import globus_sdk

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

globus_auth_data = token_response.by_resource_server['auth.globus.org']
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

AUTH_TOKEN = globus_auth_data['access_token']
TRANSFER_TOKEN = globus_transfer_data['access_token']

authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

for entry in tc.operation_ls(EP_UUID, path=top_level_dir):
    line = tc.operation_ls(EP_UUID, path=top_level_dir+entry['name'])
    print(line)
