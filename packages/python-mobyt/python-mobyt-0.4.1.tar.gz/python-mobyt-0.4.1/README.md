
# python-mobyt

## Send sms with Mobyt service

```
from pymobyt import Mobyt
from pymobyt.mobyt import MESSAGE_HIGH_QUALITY, MESSAGE_MEDIUM_QUALITY

class MobytGateway(object):
    def __init__(self, config):
        self.username = config.get('username')
        self.password = config.get('password')
        self.sender = config.get('sender')

        # Init mobyt service
        self.mobyt = Mobyt(self.username, self.password)
    
    def send(self, recipients_numbers, body, context={}):
        if len(body) > 160:
           message_type=MESSAGE_HIGH_QUALITY
        else:
           message_type=MESSAGE_MEDIUM_QUALITY

        # Send SMS
        response = self.mobyt.send_sms(body, recipients_numbers, sender=self.sender, message_type=message_type)

           
        if response['result'] != 'OK':
            raise Exception(response['result'])
        
        return True

```
