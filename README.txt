== codelog.gmail

Refer to https://developers.google.com/gmail/api/quickstart/python

Enable Gmail API
https://console.cloud.google.com/apis/library/gmail.googleapis.com
> Enable API
> CREATE CREDENTIALS
  > Which API are you using? > Gmail API
  > Where will you be calling the API from? > Other UI
  > What data will you be accessing? > User data
> Download client_id.json.  Rename to credentials.json.

python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
