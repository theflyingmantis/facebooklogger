from flask import Flask, request, render_template
import json
import requests
import os
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]+"?sslmode=require"
db = SQLAlchemy(app)

PAT = os.environ["PAGE_ACCESS_TOKEN"]


class User(db.Model):
  __tablename__='userSenderIdMap'
  senderId = db.Column(db.String(17), unique=True, nullable=False, primary_key=True)
  userId = db.Column(db.String(17), nullable=False)
  def __repr__(self):
    return '<userId - %r, senderId - %r>' % self.userId, self.senderId

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
  payload = request.get_data()
  print (payload)
  senderId = Helper().get_sender_id(payload)
  msgType = Helper().get_message_type(payload)
  if not msgType:
    Message().send_message(PAT, Helper().get_sender_id(payload), "I did not get what you said :(")
  if msgType == "get_started":
    return first_time_message(senderId)
  if msgType == "message":
    senderId = Helper().get_sender_id(payload)
    if not Models().check_sender_id_in_db(senderId):
      return first_time_message(senderId)
    userId = Models().get_userId(senderId)
    Message().send_link_msg(senderId,userId)
    Message().send_id_msg(senderId,userId)
  return "ok"

class Helper:
  def get_message_type(self,payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"][0]
    if "postback" in messaging_events and messaging_events['postback']['payload']=="get_started":
      return "get_started"
    elif "message" in messaging_events:
      return "message"
    else:
      return None

  def get_sender_id(self,payload):
    data = json.loads(payload)
    messaging_event = data["entry"][0]["messaging"][0]
    return messaging_event["sender"]["id"]

  def get_random_string(self,length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

  

  def compose_msg(self,userId):
    return "You url is https://facebooklogger.herokuapp.com/api/"+str(userId)+"\nYour UserId is "+userId

class Message:
  def send_link_msg(self,senderId, userId):
    self.send_message(PAT, senderId, "You url is https://facebooklogger.herokuapp.com/api/"+str(userId))

  def send_id_msg(self,senderId, userId):
    self.send_message(PAT, senderId, "Unique Token is: "+str(userId))

  def send_message(self,token,recipient,text):
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


class Models:
  def check_sender_id_in_db(self, senderId):
    senderIdObj = User.query.filter_by(senderId=senderId).first()
    if senderIdObj:
      return True
    return False

  def add_sender_id_in_db(self, senderId):
    userId = Helper().get_random_string(16)
    if self.check_userId(userId):
      return self.add_sender_id_in_db(senderId)
    print userId, senderId
    Obj = User(senderId=senderId,userId=userId)
    db.session.add(Obj)
    db.session.commit()

  def get_userId(self, senderId):
    Obj = User.query.filter_by(senderId=senderId).first()
    if not Obj:
      raise Exception('UserId for '+senderId+' does not exist in db')
    return Obj.userId

  def check_userId(self, userId):
    Obj = User.query.filter_by(userId=userId).first()
    if Obj:
      return True
    return False

  def get_senderId(self,userId):
    Obj = User.query.filter_by(userId=userId).first()
    if not Obj:
      raise Exception('senderId for '+userId+' does not exist in db')
    return Obj.senderId



def first_time_message(senderId):
  if not Models().check_sender_id_in_db(senderId):
    Models().add_sender_id_in_db(senderId)
  try:
    userId = Models().get_userId(senderId)
    Message().send_link_msg(senderId, userId)
    Message().send_id_msg(senderId,UserId)
  except Exception as e:
    Message().send_message(PAT,senderId, "Something Wrong happened!")


@app.route('/api/<userId>',methods = ['GET','POST'])
def loggine_api(userId):
  if not Models().check_userId(userId):
    return render_template('404.html'), 404
  senderId = Models().get_senderId(userId)
  if request.method == 'GET':
    result = {
      'GET_PARAMS': request.args,
      'REQUEST_TYPE': 'GET',
    }
    Message().send_message(PAT,senderId,json.dumps(result,indent=4))
    return render_template('show_data.html', data=result)

  if request.method == 'POST':
    result = {
      'RAW_DATA': request.get_data(),
      'REQUEST_TYPE': 'POST',
      'GET_PARAMS': request.args,
      'FORM_DATA': request.form,
    }
    Message().send_message(PAT,senderId,json.dumps(result,indent=4))
    return render_template('show_data.html', data=result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




if __name__ == '__main__':
  app.run()