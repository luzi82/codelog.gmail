from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pprint
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(inp.translate(dict(zip(map(ord, u'-_'), u'+/'))))

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # try refresh creds
    try:
        if creds and (not creds.valid) and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    except:
        creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', q='from: me').execute()
    pprint.pprint(results)

    message_list = results.get('messages', [])
    if len(message_list)<=0: return

    print('================================')
    
    message_id = message_list[0]['id']

    result = service.users().messages().get(userId='me', id=message_id).execute()
    pprint.pprint(result)

    print('================================')
    
    part_list = result['payload']['parts']
    part_list = filter(lambda p:p['mimeType']=='text/plain', part_list)
    part_list = list(part_list)
    
    for part in part_list:
        body_data = part['body']['data']
        body_data = base64_url_decode(body_data)
        body_data = body_data.decode('utf8')
        print(body_data)

if __name__ == '__main__':
    main()
