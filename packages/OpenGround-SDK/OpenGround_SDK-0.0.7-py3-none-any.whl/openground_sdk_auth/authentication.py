from flask import request, redirect, session, Flask
from requests_oauthlib import OAuth2Session


import base64
import hashlib
import json
import logging
import os
import re
import requests
import urllib.parse
import webbrowser
import pkgutil

code_verifier = "";
code_challenge = "";
accessToken = "";
refreshToken = "";
client_id = "";
authorization_base_url = 'https://imsoidc.bentley.com/connect/authorize'
token_url = 'https://imsoidc.bentley.com/connect/token'
scope = "openground email openid profile offline_access"
redirect_uri = "http://localhost:8080"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def callback():
    print("callback")

    # Exchange code for access token.
    response = getAuthenticationResponse()    
    response.raise_for_status()
        
    if response.status_code == requests.codes.ok:    
        global accessToken 
        global refreshToken
        accessToken = response.json()["access_token"];
        refreshToken = response.json()["refresh_token"];                    
    else:
        raise RuntimeError('Invalid authentication response')

    #open text file in read mode
    data = pkgutil.get_data(__name__, "callback.html")
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the flask Server')
    func()

    return data

def getAuthenticationResponse():
    print("getAuthenticationResponse")
    # Exchange the code for an access token.
    
    query = urllib.parse.urlparse(request.url).query
    redirect_params = urllib.parse.parse_qs(query)
    code = redirect_params["code"][0]
    state = redirect_params["state"][0]
    
    headers = getHeaders("application/x-www-form-urlencoded")

    body = dict (
        grant_type = "authorization_code",
        code = code,
        code_verifier = code_verifier,
        client_id = client_id,
        state = state,
        redirect_uri = redirect_uri,
        client_secret = ""
    )
          
    response = requests.post(token_url, data = body, headers = headers)
    
    return response

def getHeaders(contentType = None, accept = "*/*", accessToken = None, instanceId = None):

    # Returns standard headers which may have additional entries depending on the passed parameters.
    headers = {
        "Content-Type" : contentType,
        "User-Agent" : "openground-python-demo",
        "Accept" : accept,
        "Cache-Control" : "no-cache",
        "Accept-Encoding" : "gzip, deflate, br"   
    }

    if (contentType != None):
        headers["Content-Type"] = contentType               

    return headers  

def Authenticate(clientid = "openground-cloud-connector"):
    
    global client_id
    global code_verifier
    global code_challenge

    client_id = clientid

    logging.basicConfig(level="DEBUG")

    # PKCE parameters
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
    code_verifier = code_verifier[:128]

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')

    oauthSession = OAuth2Session(
        client_id, 
        redirect_uri = redirect_uri, 
        scope = scope)

    authorization_url, state = oauthSession.authorization_url(
        authorization_base_url, 
        code_challenge = code_challenge, 
        code_challenge_method = "S256")
            
    #session['oauth_state'] = state
    webbrowser.open_new_tab(authorization_url)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(100)
    app.run(debug=True, host = "localhost", port = 8080, use_reloader=False)    
    return accessToken;
  
