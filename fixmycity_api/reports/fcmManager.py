import firebase_admin
from firebase_admin import credentials, messaging
from fixmycity_api import settings


cred = credentials.Certificate(settings.cred)
firebase_admin.initialize_app(cred)


def sendPush(title, msg, registration_token, dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title,
                                            body=msg,
                                            ),
        data=dataObject,
        tokens=registration_token
    )

    response = messaging.send_multicast(message)
    print('successfully sent message', response)