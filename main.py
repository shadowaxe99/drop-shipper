from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import os
import base64
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    resp = MessagingResponse()

    # Extract the message body from the request
    incoming_msg = request.values.get('Body', '').lower()

    # If the incoming message is 'sick', cancel all events for the day and notify
    if 'sick' in incoming_msg:
        # Get today's date
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        # Get the events for today
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            # Cancel all events for today
            for event in events:
                service.events().delete(calendarId='primary', eventId=event['id']).execute()

            # Send an email to notify about the cancellation
            message = MIMEText('I am not feeling well today and will not be able to attend the scheduled events. I will reschedule them as soon as possible.')
            message['to'] = 'recipient@example.com'
            message['from'] = 'your-assistant-email@example.com'
            message['subject'] = 'Cancellation of today's events'
            raw_message = base64.urlsafe_b64encode(message.as_bytes())
            raw_message = raw_message.decode()
            message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()

            resp.message("All events for today have been cancelled.")
    else:
        resp.message("I didn't understand your message.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
