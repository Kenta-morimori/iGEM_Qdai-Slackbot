# coding: utf-8
from __future__ import print_function
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
import re


import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

#@listen_to("\$ (schedule|s)")
@respond_to("schedule")
def listen_func(message):
    tmp = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    try:
      from_tmp = sys.argv[1] or ""
      to_tmp = sys.argv[2] or ""
    except:
      from_tmp = ""
      to_tmp = ""
    timefrom = from_tmp or '2020/09/01'
    timeto = to_tmp or '2020/10/01'
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    timefrom = datetime.datetime.strptime(timefrom, '%Y/%m/%d').isoformat()+'Z'
    timeto = datetime.datetime.strptime(timeto, '%Y/%m/%d').isoformat()+'Z'
    events_result = service.events().list(calendarId="igem2021.qdai@gmail.com", # <- カレンダー取得元
                                        timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    replymessage = ""

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
        print(start, event['summary'])
        replymessage = replymessage + f"{start} {event['summary']}\n"
    
    message.send(replymessage)
    os.chdir(tmp)



