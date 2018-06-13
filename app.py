from flask import Flask, request
import json
import requests
import os
import json

app = Flask(__name__)

PAT = os.environ["PAGE_ACCESS_TOKEN"]

@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
    print ("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print ("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print ("Handling Messages")
  payload = request.get_data()
  print (payload)
  msgType = Helper().get_message_type(payload)
  if not msgType:
    send_message(PAT, Helper().get_sender_id(payload), "I did not get what you said :(")
  if msgType == "getting_started":
    first_time_message(payload)
  if msgType == "message":
    for sender, message in messaging_events(payload):
      print ("Incoming from %s: %s" % (sender, message))
      send_message(PAT, sender, message)
  return "ok"

class Helper:
  def get_message_type(self,payload):
    data = json.loads(payload)
    if "postback" in data["entry"][0]["messaging"][0]:
      return "getting_started"
    elif "message" in data["entry"][0]["messaging"][0]:
      return "message"
    else:
      return None

  def get_sender_id(self,payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"][0]
    return messaging_events["sender"]["id"]

def first_time_message(payload):
  send_message(PAT, Helper().get_sender_id(payload), "First Time message")

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
  secret = os.environ['SECRET']
  if request.args.get('secret') != secret:
    return "incorrect secret. Send the secret as GET parameter.\nHint: what do you want?"
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
    print (result)
    print ('\n\n')
    print (json.dumps(result,indent=4))
    send_message(PAT,sender_id,json.dumps(result,indent=4))
    return json.dumps(result,indent=4)


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """
  text = text.replace('\\"','"')
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print (r.text)


# @app.route('database',methods = ['GET','POST'])
# def database():
#     print ('database')

if __name__ == '__main__':
  app.run()