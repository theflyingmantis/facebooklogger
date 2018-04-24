from flask import Flask, request
import json
import requests
import os
import json

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = os.environ["PAGE_ACCESS_TOKEN"]

@app.route('/', methods=['GET'])
def handle_verification():
    return '<h1>Welcome to the fb chat bot testing service of Abhinav Rai</h1>'

@app.route('/', methods=['POST'])
def handle_messages():
  print ("Handling Messages")
  payload = request.get_data()
  print (payload)
  for sender, message in messaging_events(payload):
    print ("Incoming from %s: %s" % (sender, message))
    send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

@app.route('/api/<service>',methods = ['GET','POST'])
def loggine_api(service):
  sender_id = os.environ['SENDER_ID']
  if request.method == 'GET':
    result = {
      'GET_PARAMS': request.args,
      'REQUEST_TYPE': 'GET',
      'SERVICE': service
    }
    send_message(PAT,sender_id,json.dumps(result,indent=4))
    return json.dumps(result,indent=4)
  if request.method == 'POST':
    result = {
      'RAW_DATA': request.get_data(),
      'REQUEST_TYPE': 'POST',
      'GET_PARAMS': request.args,
      'FORM_DATA': request.form,
      'SERVICE': service
    }
    send_message(PAT,sender_id,json.dumps(result,indent=4))
    return json.dumps(result,indent=4)


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.encode().decode()}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print (r.text)

if __name__ == '__main__':
  app.run()