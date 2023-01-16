BankApi
======

Token and Message service.

The app will be running on port 8080. The app expects an API_KEY and SECRET_KEY in the form of environment variables.


---
Running unit tests
```
pip install -r requirements.txt
python -m pytest tests
 
```

---
Running locally
```
pip install -r requirements.txt
python application.py
 
```
Local [Health Check](http://localhost:8080/healthcheck)
The local healthcheck is the only endpoint that accepts GET request, and will not be accesible facing when deploying to any environment.


---
We serve two endpoint, /get_token, which will provide a JWT, this endpoint expects and API_KEY header
```
curl -X POST -H "X-Parse-REST-API-Key: $KEY" $HOSTNAME/get_token 
```

You could pipe the command above to ```jq``` in order to save directly to a environment variable 

```
TOKEN=$(curl -X POST -H "X-Parse-REST-API-Key: $KEY" $HOSTNAME/get_token | jq -r .token)
```

The /DevOps endpoint provides the functionality for posting message and expect both the API_KEY and the JWT you can request at /get_token
```text
curl -X POST -H "X-Parse-REST-API-Key: $API_KEY" \
-H "X-JWT-KWY: $TOKEN" \
-H "Content-Type: application/json" -d '{ "message": "This is a test","to": "Juan Perez","from": "Rita Asturia","timeToLifeSec": 45 }' \
$HOSTNAME/DevOps
```
Both endpoints will return an error if a method other that POST is used.

---
The Chart/ folder contains the Kubernetes objects for deploying to EKS, this objects are a dependency to the [Argo Registry](https://github.com/pimliprentiss/bankapi-argo-registry)

