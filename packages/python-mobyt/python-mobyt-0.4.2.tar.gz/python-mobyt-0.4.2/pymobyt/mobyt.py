import requests
import json
import datetime
import base64

BASEURL = "https://app.mobyt.it/API/v1.0/REST/"

MESSAGE_HIGH_QUALITY = "N"
MESSAGE_MEDIUM_QUALITY = "L"
MESSAGE_LOW_QUALITY = "LL"


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

    raise TypeError ("Type not serializable")


class Mobyt(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        auth = self.login()
        if not auth:
            raise Exception('Can not authenticate with provided credentials')
    
    def login(self):
        """Authenticates the user given it's username and password. Returns a
        couple (user_key, session_key)
        """
        auth_string = "%s:%s" % (self.username, self.password)
        auth_token = base64.b64encode(auth_string.encode('UTF-8'))
        headers = {
            'Authorization': 'Basic %s' % auth_token.decode('UTF-8'),
            'Content-type' : 'application/json'
        }


        r = requests.get("%slogin" % BASEURL, headers=headers)
        if r.status_code != 200:
            return None

        user_key, session_key = r.text.split(';')
        self.user_key = user_key 
        self.session_key = session_key

        return True
    

    def send_sms(self, message, recipients, 
                 message_type=MESSAGE_MEDIUM_QUALITY, 
                 return_credits=False,
                 sender=None,
                 order_id=None,
                 allow_longer=False,
                 scheduled_delivery_time=None):
        """Sends an SMS"""
        if isinstance(recipients, str):
            recipients = [recipients]

        if not allow_longer and len(message) > 160:
            message = message[:160]

        data = {
            "message" : message,
            "message_type" : message_type,
            "returnCredits" : return_credits,
            "recipient": recipients,
            "sender": sender,
        }


        if scheduled_delivery_time:
            data['scheduled_delivery_time'] = scheduled_delivery_time
        
        if order_id:
            data['order_id'] = order_id

        headers = { 'user_key': self.user_key,
                    'Session_key': self.session_key,
                    'Content-type' : 'application/json' }

        r = requests.post("%ssms" % BASEURL,
                        headers=headers,
                        data=json.dumps(data, default=json_serial))

        print("DAdasdas")
        print(r.text)
        r.raise_for_status()

        return r.json()
    

    