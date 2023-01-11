import pytest
from jose import jwt, JWTError
from datetime import datetime
import application as app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    return app.app.test_client()


test_authorization_key = '2f5ae96c-b558-4c7b-a590'
test_secret_key = '8083153b78e170dbf3deacf6351c0'
test_request_date = datetime(2023, 1, 6, 17, 57, 21, 956624)
test_token = {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2ptb250ZXJvLmNvbSIsImluZm8iOiJKb2IgQXBwbGljYXRpb24gUHJhY3RpY2FsIFRlc3QiLCJzdWIiOiIyZjVhZTk2Yy1iNTU4LTRjN2ItYTU5MCIsImlhdCI6MTY3MzA0MjI0Mn0.WJCiqlS34zz9Pt5U3paRtUgRQaGiBAJrphcpA70B4IE'}


def test_create_payload():
    test_iat = int(round(datetime.timestamp(test_request_date)))
    assert app.create_payload(test_authorization_key, test_request_date) == \
        {"iss": "https://jmontero.com",
        "info": "Job Application Practical Test",
        "sub": '2f5ae96c-b558-4c7b-a590',
        "iat": 1673042242
        }

def test_create_token():
    payload_to_encode = app.create_payload(test_authorization_key, test_request_date) 
    token =  jwt.encode(payload_to_encode, test_secret_key, 'HS256')
 
    assert {'token': token} == test_token

def test_validate_token():
    with pytest.raises(Exception):
        app.validate_token('INVALID_SECRET_KEY', test_token['token'])
    
    with pytest.raises(Exception):
        app.validate_token(test_secret_key, 'INVALID_TOKEN')

    assert app.validate_token(test_secret_key, test_token['token']) == 200

def test_post_message():
    test_payload = \
         { "message": "This is a test",
            "to": "Junior Montero",
            "from": "Helene Ruiz",
            "timeToLifeSec": 15 
            }
    test_message = app.message_to_post(test_payload)
    assert test_message == { "message" : "Hello Junior Montero your message will be sent." }

