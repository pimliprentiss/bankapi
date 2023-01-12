from os import getenv
from time import time
from jose import jwt, JWTError
from flask import Flask, request, abort, jsonify

api_key = getenv('API_KEY')
secret_key = getenv('SECRET_KEY')

def create_payload(authorization_key, request_date):
    payload_data = {
            'iss': "https://jmontero.com",
            "info": "Job Application Practical Test",
            "sub": authorization_key,
            "iat": request_date
        }
    
    return payload_data


def create_token(encode_secret, authorization_key):
    request_date = int(time())
    payload_to_encode = create_payload(authorization_key, request_date).copy()
    token =  jwt.encode(payload_to_encode, encode_secret, algorithm='HS256')
    
    return {"token": token}


def validate_token(encode_secret, client_token):
    try:
        jwt.decode(client_token, encode_secret, algorithms='HS256')
        return 200
    except JWTError:
        abort(401, "ERROR: Unauthorized.")


def message_to_post(payload):
    formated_message = f"Hello {payload['to']} your message will be sent."
    
    return { "message": formated_message }


app = Flask(__name__)

#Added all methods because as per the requirements I need to print "ERROR if != POST"
@app.route('/get_token', methods = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def get_token():
 
    if request.method != 'POST': 
        return 'ERROR'

    client_authorization_key = request.headers.get('X-Parse-REST-API-Key')

    if client_authorization_key == api_key:
        return create_token(secret_key, client_authorization_key), 200
    else:
        return {'message': 'ERROR: Unauthorized, an API key must be provided'}, 401


@app.route("/DevOps", methods = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def post_message():

    if request.method != 'POST': 
        return 'ERROR'
    
    client_token = request.headers.get('X-JWT-KWY')
    validate_token(secret_key, client_token)

    return message_to_post(request.json)

@app.route("/healthcheck")
def healthcheck():
    
    return {'status': "running"}
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
