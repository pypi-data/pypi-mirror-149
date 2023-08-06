'''
Created on May 6, 2022

@author: cjm10
'''
'''
Created on May 3, 2022

@author: cjm10
'''

from django.shortcuts import redirect as djangoRedirect
from flask import make_response, redirect
import jwt
import logging
import requests
import rsa
import traceback
import urllib.parse

class Auth():
    # if get or post vars contain "b2fSetup" or "B2F_AUTHN" save them to cookies of the same name
    # run b2f
    secureUrl = "https://secure.blue2factor.com"
    logoutUrl = ""
    SUCCESS = 0
    setup = None
    b2fCookie = None
    redirect = None

    def getEndpoint(self, companyId):
        return self.secureUrl + "/SAML2/SSO/" + companyId + "/Token"
    
    def getFailureUrl(self, companyId):#/failure/{CompanyID}/recheck
        return self.secureUrl + "/failure/" + companyId + "/recheck"
    
    def getResetUrl(self, companyId):
        return self.secureUrl + "/failure/" + companyId + "/reset"
    
    def getIssuer(self, companyId):
        return self.secureUrl + "/SAML2/SSO/" + companyId + "/EntityId"
    
    def getSignout(self, companyId):
        return self.secureUrl + "/SAML2/SSO/" + companyId + "/Signout"
    
    def authenticateFlaskRequest(self, request, companyId, loginUrl, privateKeyStr):
        jwt = request.form.get("B2F_AUTHN") or request.cookies.get("B2F_AUTHN")
        b2fSetup = request.form.get("b2fSetup")
        auth, b2fCookie, reject, b2fSetup = self.authenticate(request.url, jwt, companyId, loginUrl,
                                                              b2fSetup, privateKeyStr)
        self.b2fCookie = b2fCookie
        self.redirect = make_response(redirect(reject, 302))
        self.setup = b2fSetup
        return auth
    
    def authenticateDjangoRequest(self, request, companyId, loginUrl, privateKeyStr):
        jwt = None
        if request.method == 'POST':
            jwt = request.POST["B2F_AUTHN"] 
        if not jwt:
            jwt = request.COOKIES["B2F_AUTHN"]
        b2fSetup = request.POST["b2fSetup"]
        auth, b2fCookie, reject, b2fSetup = self.authenticate(request.url, jwt, companyId, loginUrl,
                                                              b2fSetup, privateKeyStr)
        self.b2fCookie = b2fCookie
        self.redirect = djangoRedirect(reject)
        self.setup = b2fSetup
        return auth
    
    def authenticate(self, url, jwt, companyId, loginUrl, b2fSetup, privateKeyStr):
        if jwt:
            success, newToken = self.b2fAuthorized(jwt, companyId, loginUrl, privateKeyStr)
            logging.error("success: " + str(success))
            if success:
                return True, newToken, None, b2fSetup
            else:
                url = url.split("?")[0]
                logging.error("redirecting to: " + self.getFailureUrl(companyId) + "?url=" + urllib.parse.quote(url))
                return False, newToken, self.getFailureUrl(companyId) + "?url=" + urllib.parse.quote(url), b2fSetup
        else:
            logging.error("jwt was empty")
            redirectSite = self.getResetUrl(companyId) + "?url=" + urllib.parse.quote(url)
            logging.error("setting referrer to " + url)
            return False, "", redirectSite, b2fSetup
        
    def b2fAuthorized(self, jwt, companyId, loginUrl, privateKeyStr):
        success = False
        newToken = None
        try:
            if self.tokenIsValid(jwt, companyId, loginUrl):
                newToken = jwt
                logging.error("token was valid")
                success = True
            else:
                logging.error("token wasn't valid, will attempt to get a new one")
                success, newToken = self.getNewToken(jwt, companyId, loginUrl, privateKeyStr);
        except:
            logging.error(traceback.format_exc())
        return success, newToken
    
    def getNewToken(self, jwt, companyId, loginUrl, privateKeyStr):
        success = False
        newJwt = None
        try:
            logging.error("checking: " + self.getEndpoint(companyId))
            signature = self.getJwtSignature(jwt, privateKeyStr)
            response = requests.get(url=self.getEndpoint(companyId), auth=BearerAuth(jwt + "&" + signature))
            logging.error("response: " + str(response.status_code))
            if response.status_code == 200:
                jsonResponse = response.json()
                logging.error(jsonResponse)
                if jsonResponse is not None:
                    logging.error("success: " + str(jsonResponse["outcome"]))
                    if int(jsonResponse["outcome"]) == self.SUCCESS:
                        newJwt = jsonResponse["token"]
                        success = self.tokenIsValid(newJwt, companyId, loginUrl)
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(str(e))
        return success, newJwt
    
    def getJwtSignature(self, jwt, privateKeyStr):
        pemPrefix = '-----BEGIN RSA PRIVATE KEY-----'
        pemSuffix = '-----END RSA PRIVATE KEY-----'
        privateKeyStr = privateKeyStr.replace("\n", "").replace("\r", "");
        privateKeyStr = privateKeyStr.replace(pemSuffix, "").replace(pemPrefix, "")
        privateKeyStr = self.addNewLinesToKeyString(privateKeyStr)
        privateKeyStr = pemPrefix + "\n" + privateKeyStr + "\n" + pemSuffix
        privateKey = rsa.PrivateKey.load_pkcs1(privateKeyStr)
        signature = rsa.sign(jwt.encode('utf-8'), privateKey, 'SHA-256')
        return signature
    
    def tokenIsValid(self, authToken, companyId, loginUrl):
        valid = False
        if authToken is not None:
            logging.warn("authToken: " + authToken)
            try:
                headers = jwt.get_unverified_header(authToken)
                url = headers.get("x5u")
                logging.warn("url: " + url)
                publicKey = self.getPublicKeyFromUrl(url)
                if publicKey is not None:
                    decoded = jwt.decode(
                        authToken,
                        publicKey,
                        issuer=self.getIssuer(companyId),
                        audience=loginUrl,
                        algorithms=["RS256"])
                    valid = True
                    logging.warn("decoded: " + str(decoded))
                    logging.warn("token is valid")
            except jwt.ExpiredSignatureError:
                logging.error("signature expired")
            except jwt.InvalidIssuerError:
                logging.error("invalid issuer")
            except Exception as e:
                logging.error("invalid jwt")
                logging.error(traceback.format_exc())
                logging.error(str(e))
        else:
            logging.error("token was null")
        return valid
        
    def getPublicKeyFromUrl(self, url):
        publicKey = None
        resp = requests.get(url)
        if resp.status_code == 200:
            logging.warn("***url response: " + resp.text)
            publicKey = ("-----BEGIN PUBLIC KEY-----\n" + self.addNewLinesToKeyString(resp.text) + 
                   "\n-----END PUBLIC KEY-----")
        else:
            logging.warn("status code: " + str(resp.status_code))
        return publicKey
    
    def addNewLinesToKeyString(self, keyStr):
        lines = []
        for i in range(0, len(keyStr), 64):
            lines.append(str(keyStr[i:i + 64]))
        return '\n'.join(lines)
    
    def setB2fCookie(self, response):
        try:
            if (self.setup != None):
                response.set_cookie('b2fSetup', self.setup, samesite='Lax', max_age=60*60, secure=True)
            if (self.b2fCookie != None):
                response.set_cookie('B2F_AUTHN', self.b2fCookie, samesite='Lax', max_age=60*60*24*90, secure=True)
        except:
            logging.error(traceback.format_exc())
        return response;
    
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
