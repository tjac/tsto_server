import base64
import datetime
import hashlib
import json
import random
import random
import string
import sys
import time
from typing import Any, Dict
import uuid

# pip install flask
from flask import Flask, abort, jsonify, make_response, request
from flask_inflate import Inflate       # pip install flask-inflate

# pip install hexdump   -- this is for dev'ing, safe to ignore this import
#import hexdump

# The Simpson's Tapped Out protobufs
import AuthData_pb2
import ClientConfigData_pb2
import ClientLog_pb2
import ClientMetrics_pb2
import ClientTelemetry_pb2
import Common_pb2
import CustomerServiceData_pb2
import Error_pb2
import GambleData_pb2
import GameplayConfigData_pb2
import GetFriendData_pb2
import LandData_pb2
import MatchmakingData_pb2
import OffersData_pb2
import PurchaseData_pb2
import WholeLandTokenData_pb2


class TheSimpsonsTappedOutLocalServer:
  
  def __init__(self, server_ip: str):
    # Generate the Flask application object
    self.app = Flask(__name__)
    Inflate(self.app)     # Enable ability to auto decompress gzip responses

    # Set the initial configuration
    self.server_ip: bool = server_ip
    self.debug: bool = False
    self.run_tutorial: bool = False

    self.session_key: str = str(uuid.uuid4())         # 7e95ce80-db2b-4e09-9554-ca5171004335
    self.land_token: str = str(uuid.uuid4())          # b0687a40-3d16-49a6-ad81-c4524e997684
    self.user_user_id: str = "".join([chr(random.randint(0x30,0x39)) for x in range(38)])       # 27606208852049386642878482000969586141
    self.user_telemtry_id: str = "".join([chr(random.randint(0x30,0x39)) for x in range(11)])   # 11460983877
    self.token_session_key: str = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()         # b00d0e085c3f79f21f4e405f765575e6
    self.token_user_id: str = str(random.randint(1000000000000, 99999999999999))                # 1007072359901
    self.token_authenticator_pid_id: int = random.randint(1000000000000, 99999999999999)        # 1016288386758
    self.token_persona_id: int = random.randint(1000000000000, 99999999999999)                  # 1003650759901 (not a string)
    self.token_telemetry_id: str = str(random.randint(1000000000000, 99999999999999))           # 1006990259901
    self.personal_id: str = str(random.randint(1000000000000, 99999999999999))                  # 1009174947082
    self.display_name: str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(5,12))) # "gssincla-g"
    self.persona_name: str = self.display_name.lower()                                               # gssinclag
    self.me_persona_pid_id: str = str(random.randint(1000000000000, 99999999999999))            # 1007072559901
    self.me_persona_display_name: str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(5,12))) # "9BMtYCXtXKs3RSvD"
    self.me_persona_name: str = self.me_persona_display_name.lower()                                 # 9bmtycxtxks3rsvd
    self.me_persona_anonymous_id: str = base64.b64encode(hashlib.md5(self.me_persona_name.encode("utf-8")).digest()).decode("utf-8") # xdN+ZMOv2ykdR0rosKriDg==
    self.device_id: str = hashlib.sha256(str(datetime.datetime.now()).encode("utf-8")).hexdigest()              # "3be24cfa8a1beadfc8a18ee2c9691096bf38919bc9c34d2efcea0a8e8d5ce409"
  
    self.land_proto: LandData_pb2.LandMessage = LandData_pb2.LandMessage()
    if self.run_tutorial:
      # This is for loading a blank/tutorial town
      self.land_proto.friendData.dataVersion = 72
      self.land_proto.friendData.hasLemonTree = False
      self.land_proto.friendData.language = 0
      self.land_proto.friendData.level = 0
      self.land_proto.friendData.name = ""
      self.land_proto.friendData.rating = 0
      self.land_proto.friendData.boardwalkTileCount = 0
    else:
      with open("mytown.pb", "rb") as f:
        #f.read(12)      # strip header for teamtsto.org generated protobuf images
        self.land_proto.ParseFromString(f.read())


  def run(self):

    # server: syn-dir.sn.eamobile.com
    @self.app.route('/director/api/<platform>/getDirectionByPackage')  # android
    @self.app.route('/director/api/<platform>/getDirectionByBundle')   # ios
    def getDirectionByBundle(platform):
      if self.debug: 
        print(f"appVer: {request.args.get('appVer')}")
        print(f"deviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"appLang: {request.args.get('appLang')}")
        print(f"apiVer: {request.args.get('apiVer')}")
        print(f"serverEnvironment: {request.args.get('serverEnvironment')}")
        print(f"localization: {request.args.get('localization')}")
        print(f"hwId: {request.args.get('hwId')}")
        print(f"deviceLocale: {request.args.get('deviceLocale')}")
        print(f"bundleId: {request.args.get('bundleId')}")
        print(f"deviceString: {request.args.get('deviceString')}")

      server_keys = [
        "nexus.portal",
        "antelope.groups.url",
        "service.discovery.url",
        "synergy.tracking",
        "antelope.friends.url",
        "dmg.url",
        "avatars.url",
        "synergy.m2u",
        "akamai.url",
        "synergy.pns",
        "mayhem.url",
        "group.recommendations.url",
        "synergy.s2s",
        "friend.recommendations.url",
        "geoip.url",
        "river.pin",
        "origincasualserver.url",
        "ens.url",
        "eadp.friends.host",
        "synergy.product",
        "synergy.drm",
        "synergy.user",
        "antelope.inbox.url",
        "antelope.rtm.url",
        "friends.url",
        "aruba.url",
        "synergy.cipgl",
        "nexus.connect",
        "synergy.director",
        "pin.aruba.url",
        "nexus.proxy",
      ]

      resp = {
                "DMGId": 0,
                "appUpgrade": 0,
                "bundleId": "com.ea.simpsonssocial.inc2",
                "clientId": f"simpsons4-{platform}-client",
                "clientSecret": "D0fpQvaBKmAgBRCwGPvROmBf96zHnAuZmNepQht44SgyhbCdCfFgtUTdCezpWpbRI8N6oPtb38aOVg2y",
                "disabledFeatures": [],
                "facebookAPIKey": "43b9130333cc984c79d06aa0cad3a0c8",
                "facebookAppId": "185424538221919",
                "hwId": 2363,
                "mayhemGameCode": "bg_gameserver_plugin",
                "mdmAppKey": f"simpsons-4-{platform}",
                "millennialId": "",
                "packageId": "com.ea.game.simpsons4_row",
                "pollIntervals": [
                    {
                        "key": "badgePollInterval",
                        "value": "300"
                    }
                ],
                "productId": 48302,
                "resultCode": 0,
                "sellId": 857120,
                "serverApiVersion": "1.0.0",
                "serverData": [
                    {
                        "key": "antelope.rtm.host",
                        "value": f"http://{self.server_ip}:9000"
                    },
                    {
                        "key": "applecert.url",
                        "value": "https://www.apple.com/appleca/AppleIncRootCertificate.cer"
                    },
                    {
                        "key": "origincasualapp.url",
                        "value": f"http://{self.server_ip}/loader/mobile/ios/"
                    },
                    {
                        "key": "akamai.url",
                        "value": "http://cdn.skum.eamobile.com/skumasset/gameasset/"
                    }
                ],
                "telemetryFreq": 300
            }

      # Setup URL redirects to our server
      for key in server_keys:
        resp["serverData"].append({"key": key, "value": f"http://{self.server_ip}"})

      return jsonify(resp)


    # server: user.sn.eamobile.com
    @self.app.route("/user/api/android/getAnonUid")
    def get_anon_uid():
      if self.debug: 
        print(f"localization: {request.args.get('localization')}")
        print(f"appVer: {request.args.get('appVer')}")
        print(f"deviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"appLang: {request.args.get('appLang')}")
        print(f"apiVer: {request.args.get('apiVer')}")
        print(f"hwId: {request.args.get('hwId')}")
        print(f"deviceLocale: {request.args.get('deviceLocale')}")
        print(f"eadeviceid: {request.args.get('eadeviceid')}")
        print(f"updatePriority: {request.args.get('updatePriority')}")

      return jsonify(
        {
          "resultCode": 0,
          "serverApiVersion": "1.0.0",
          "uid": random.randint(10000000000, 99999999999)     # 17987306517
        }
      )
      
    # server: user.sn.eamobile.com
    @self.app.route("/user/api/android/getDeviceID")
    def get_device_id():
      if self.debug: 
        print(f"localization: {request.args.get('localization')}")
        print(f"appVer: {request.args.get('appVer')}")
        print(f"deviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"appLang: {request.args.get('appLang')}")
        print(f"apiVer: {request.args.get('apiVer')}")
        print(f"hwId: {request.args.get('hwId')}")
        print(f"deviceLocale: {request.args.get('deviceLocale')}")
        print(f"androidId: {request.args.get('androidId')}")

      return jsonify(
        {
          "deviceId": self.device_id,
          "resultCode": 0,
          "serverApiVersion": "1.0.0"
        }
      )

    # server: user.sn.eamobile.com
    @self.app.get("/user/api/android/validateDeviceID")
    def validate_device_id():
      if self.debug: 
        print(f"appVer: {request.args.get('appVer')}")
        print(f"deviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"appLang: {request.args.get('appLang')}")
        print(f"apiVer: {request.args.get('apiVer')}")
        print(f"serverEnvironment: {request.args.get('serverEnvironment')}")
        print(f"deviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"hwId: {request.args.get('hwId')}")
        print(f"deviceLocale: {request.args.get('deviceLocale')}")
        print(f"eadeviceid: {request.args.get('eadeviceid')}")
        print(f"androidId: {request.args.get('androidId')}")

      return jsonify(
          {
              "deviceId": self.device_id,
              "resultCode": 0,
              "serverApiVersion": "1.0.0"
          }
        )


    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/lobby/time")
    def lobby_time():
      xml = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Time><epochMilliseconds>{int(round(time.time() * 1000))}</epochMilliseconds></Time>'
      response = make_response(xml)
      response.headers['Content-Type'] = 'application/xml'
      return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/trackinglog/", methods=["POST"])
    def tracking_log():
      req = ClientLog_pb2.ClientLogMessage()
      req.ParseFromString(request.data)
      if self.debug: 
        print(f"\tTimestamp: {req.time_stamp}")
        print(f"\tSeverity: {req.severity}")
        print(f"\tSource: {req.source}")
        print(f"\tText: {req.text}")
        if req.HasField("userId"):
          print(f"\tUserId: {req.userId}")
        if req.HasField("connectionType"):
          print(f"\tConnection Type: {req.connectionType}")
        if req.HasField("serverLogFields"):
          print(f"\tServer Log Fields: {req.serverLogFields}")

      xml = f'<?xml version="1.0" encoding="UTF-8"?><Resources><URI>OK</URI></Resources>'
      response = make_response(xml)
      response.headers['Content-Type'] = 'application/xml'
      return response
      
    # server: accounts.ea.com
    @self.app.route("/connect/auth")
    def connect_auth():
      """
      ?client_id=simpsons4-ios-client
      &country=US
      &dob=1992-02-01
      &email=dude%40dude.dude
      &globalOptin=true
      &language=en
      &platform=iOS
      &prog_reg=true
      &redirect_uri=nucleus%3Arest
      &release_type=prod
      &response_type=code

      For logins, the verify code is sent using these parameters...
      authenticator_login_type=mobile_ea_account
      &client_id=simpsons4-android-client
      &nonce=2024-12-24%2004:30:37:000
      &redirect_uri=nucleus:rest
      &release_type=prod
      &response_type=code%20lnglv_token
      &sig=ewogICAiYXYiIDogInYxIiwKICAgImNyZWQiIDogIjExMTExMSIsCiAgICJlbWFpbCIgOiAiZHVkZUBkdWRlLmR1ZGUiLAogICAibSIgOiAiMSIsCiAgICJzdiIgOiAidjEiLAogICAidHMiIDogIjIwMjQtMTItMjQgMDQ6MzA6Mzc6MDAwIgp9Cg.RaJxDRmKhLZEtk98tYG8_E9gG83iBt1DNTerR04YGaQ
      """

      if self.debug: 
        print(f"authenticator_login_type: {request.args.get('authenticator_login_type')}")
        print(f"client_id: {request.args.get('client_id')}")
        print(f"apiVer: {request.args.get('apiVer')}")
        print(f"serverEnvironment: {request.args.get('serverEnvironment')}")
        print(f"redirect_uri: {request.args.get('redirect_uri')}")
        print(f"release_type: {request.args.get('release_type')}")
        print(f"response_type: {request.args.get('response_type')}")
        sig = request.args.get('sig')
        sig_parts = []
        if sig:
          try:
            sig_parts = sig.split(".")
            sig_parts[0] = base64.b64decode(sig_parts[0] + "=" * (len(sig_parts[0]) % 3))
            print(f"sig_parts: {sig_parts}")
          except Exception as e:
            print(f"sig: {sig}")

      # TODO: programmatically generate this
      response_json = {
        "code": "QUOgAP3pKNGNI71KH72KdKjMkkFE5sO1nWWi34qGAQ",
      }
      
      response_type = request.args.get("response_type")
      if response_type and response_type.find("lnglv_token") > -1:
        lnglv_token = base64.b64encode(
          "AT0:2.0:3.0:86400:BUr1cFqJ6P1cFhcrIbuyYAQuJ1X0kp4RwEw:47082:rhvos".encode("utf-8")
        ).decode("utf-8")
        response_json["lnglv_token"] = lnglv_token

      return jsonify(response_json)


    # server: accounts.ea.com
    @self.app.route("/connect/token", methods=["POST"])
    def connect_token():
      if self.debug: 
        print(f"client_id: {request.args.get('client_id')}")
        print(f"client_secret: {request.args.get('client_secret')}")
        print(f"code: {request.args.get('code')}")
        print(f"grant_type: {request.args.get('grant_type')}")
        print(f"redirect_uri: {request.args.get('redirect_uri')}")
        print(f"release_type: {request.args.get('release_type')}")

      # TODO: properly generate the access and refresh tokens
      access_token = base64.b64encode(
        "AT0:2.0:3.0:720:SHTNCm5XH18l7HfL0nefD8zQvjsNxlZF3vT:59901:rhal5".encode("utf-8")
      ).decode("utf-8")

      refresh_token_body = base64.b64encode(
        "RT0:2.0:3.0:1439:9WrwBPXBO03aH9mhN83m8NHkrpH5gyVcQ:59901:rhal5".encode("utf-8")
      ).decode("utf-8")
      # stealing a signature for now. TODO: calculate this
      refresh_token_sig = "MpDW6wVO8Ek79nu6jxMdSQwOqP"
      refresh_token = f"{refresh_token_body}.{refresh_token_sig}"

      id_token_header = base64.b64encode('{"typ":"JWT","alg":"HS256"}'.encode("utf-8")).decode("utf-8")
      id_token_body = base64.b64encode(
        json.dumps(
          { 
            "aud":"simpsons4-ios-client",
            "iss":"accounts.ea.com",
            "iat": int(round(time.time() * 1000)),
            "exp": int(round(time.time() * 1000)) + 3600,
            "pid_id": self.me_persona_pid_id,
            "user_id": self.token_user_id,
            "persona_id": self.token_persona_id,
            "pid_type":"AUTHENTICATOR_ANONYMOUS",
            "auth_time":0
          }
        ).encode("utf-8")
      ).decode("utf-8")
      # stealing a signature for now. TODO: calculate this
      id_token_sig = base64.b64encode(
        bytes.fromhex(
          "033b68a1deed4f9724690b1b69923bb719c56395128128dac76066713b1e"
        )
      ).decode("utf-8")
      id_token = f"{id_token_header}.{id_token_body}.{id_token_sig}"

      return jsonify(
        {
          "access_token": access_token,
          "token_type": "Bearer",
          "expires_in": 86400,     # 43199,
          "refresh_token": refresh_token,
          "refresh_token_expires_in": 86400, # 86399
          "id_token": id_token
        }
      )

    # server: accounts.ea.com
    @self.app.route("/connect/tokeninfo")
    def connect_tokeninfo():
      
      return jsonify(
        {
            "client_id": "simpsons4-android-client",
            "scope": "offline basic.antelope.links.bulk openid signin antelope-rtm-readwrite search.identity basic.antelope basic.identity basic.persona antelope-inbox-readwrite",
            "expires_in": 86400,        # 43199
            "pid_id": self.me_persona_pid_id,
            "pid_type": "AUTHENTICATOR_ANONYMOUS",
            "user_id": self.token_user_id,
            "persona_id": self.token_persona_id,
            "authenticators": [
                {
                    "authenticator_type": "AUTHENTICATOR_ANONYMOUS",
                    "authenticator_pid_id": self.token_authenticator_pid_id
                }
            ],
            "is_underage": False,
            "stopProcess": "OFF",
            "telemetry_id": self.token_telemetry_id
        }
      )

    # server: accounts.ea.com
    @self.app.route("/proxy/identity/geoagerequirements")
    def geoagerequirements():
      return jsonify({
        "geoAgeRequirements": {
            "minLegalRegAge": 13,
            "minAgeWithConsent": "3",
            "minLegalContactAge": 13,
            "country": "US"             # TODO: make configurable
        }
      })


    # server: accounts.ea.com
    @self.app.route("/proxy/identity/progreg/code", methods=["POST"])
    def progreg_code():
      if self.debug: print(f"code request: {request.data}")

      return ""

    # server: gateway.ea.com
    @self.app.route("/proxy/identity/pids/me/personas/<user_id>")
    def me_personas(user_id: str):
      return jsonify(
        {
            "persona": {
                "personaId": user_id,
                "pidId": self.me_persona_pid_id,
                "displayName": self.me_persona_display_name,
                "name": self.me_persona_name,
                "namespaceName": "gsp-redcrow-simpsons4",
                "isVisible": True,
                "status": "ACTIVE",
                "statusReasonCode": "",
                "showPersona": "EVERYONE",
                "dateCreated": "2012-02-29T0:00Z",
                "lastAuthenticated": "2024-11-28T5:25Z",
                "anonymousId": self.me_persona_anonymous_id
            }
        }
      )

    # server: gateway.ea.com
    @self.app.route("/proxy/identity/pids/<pid>/personas")
    def pid_personas(pid: str):
      
      json = {
        "personas": {
            "persona": [
                {
                    "personaId": self.personal_id,    # TODO: make configurable
                    "pidId": pid,
                    "displayName": self.display_name, # TODO: make configurable
                    "name": self.persona_name,        # TODO: make configurable
                    "namespaceName": "cem_ea_id",
                    "isVisible": True,
                    "status": "ACTIVE",
                    "statusReasonCode": "",
                    "showPersona": "FRIENDS",
                    "dateCreated": "2024-12-25T0:00Z",    # TODO: make configurable
                    "lastAuthenticated": ""
                }
            ]
        }
      }

      return jsonify(json)

    # server: accounts.ea.com
    @self.app.route("/probe")
    def probe():
      return ""

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/protoClientConfig/")
    def protoClientConfig():
      if self.debug: print(f"id: {request.args.get('id')}")

      client_config = ClientConfigData_pb2.ClientConfigResponse()
      
      config_entries = [
        (0,"AppUrl.ios.na","https://apps.apple.com/app/id497595276?ls=1&mt=8"),
        (1,"GameClient.MaxBundleSize","50"),
        (2,"MinimumVersion.ios","4.69.0"),
        (3,"CurrentVersion.ios","4.69.0"),
        (5,"LocalSaveInterval","10"),
        (6,"ServerSaveInterval","100"),
        (7,"AppUrl.ios.row","https://apps.apple.com/app/id498375892?ls=1&mt=8"),
        (8,"RateUrl.ios.na","https://apps.apple.com/app/id497595276?ls=1&mt=8"),
        (9,"RateUrl.ios.row","https://apps.apple.com/app/id498375892?ls=1&mt=8"),
        (10,"CheckDLCInterval","3600"),
        (13,"AppUrl.android.na","https://play.google.com/store/apps/details?id=com.ea.game.simpsons4_na"),
        (14,"AppUrl.android.row","https://play.google.com/store/apps/details?id=com.ea.game.simpsons4_row"),
        (15,"RateUrl.android.na","https://play.google.com/store/apps/details?id=com.ea.game.simpsons4_na"),
        (16,"RateUrl.android.row","https://play.google.com/store/apps/details?id=com.ea.game.simpsons4_row"),
        (20,"MinimumVersion.android","4.69.0"),
        (21,"CurrentVersion.android","4.69.0"),
        (22,"AppUrl.android.amazon.azn","amzn://apps/android?p=com.ea.game.simpsonsto_azn"),
        (23,"AppUrl.android.amazon.azn_row","amzn://apps/android?p=com.ea.game.simpsons4_azn_row"),
        (24,"RateUrl.android.amazon.azn","amzn://apps/android?p=com.ea.game.simpsonsto_azn"),
        (25,"RateUrl.android.amazon.azn_row","amzn://apps/android?p=com.ea.game.simpsons4_azn_row"),
        (26,"CoppaEnabledNa","1"),
        (27,"CoppaEnabledRow","1"),
        (28,"MaxBuildingSoftCapEnabled","1"),
        (29,"MaxBuildingSoftCapLimit","19500"),
        (30,"MaxBuildingSoftCapRepeatAmount","500"),
        (31,"MaxBuildingHardCapEnabled","1"),
        (32,"MaxBuildingHardCapLimit","24000"),
        (41,"ClientConfigInterval","300"),
        (43,"TelemetryEnabled.android","0"),
        (44,"TelemetryEnabled.ios","0"),
        (45,"TelemetryEnabled.android.amazon","0"),
        (47,"MinimumVersion.android.amazon","4.69.0"),
        (48,"CurrentVersion.android.amazon","4.69.0"),
        (52,"OriginAvatarsUrl","https://m.avatar.dm.origin.com"),
        (54,"TutorialDLCEnabled.io","1"),
        (55,"TutorialDLCEnabled.android","1"),
        (56,"TutorialDLCEnabled.android.amazon","1"),
        (57,"AppUrl.android.nokia.row","market://details?id=com.ea.game.simpsons4_nokia_row"),
        (58,"RateUrl.android.nokia.row","market://details?id=com.ea.game.simpsons4_nokia_row"),
        (59,"ParamUrl.android.nokia.row","market://details?id=com.ea.game.simpsons4_nokia_row"),
        (60,"TutorialDLCEnabled.android.nokia","1"),
        (67,"EnableVBOCache","1"),
        (68,"CoppaEnabledRow.ios.row.4.10.2","0"),
        (69,"CoppaEnabledRow.android.row.4.10.2","0"),
        (70,"CoppaEnabledRow.android.amazon.azn_row.4.10.2","0"),
        (71,"CoppaEnabledRow.ios.row.4.10.3","0"),
        (72,"CoppaEnabledRow.android.row.4.10.3","0"),
        (73,"CoppaEnabledRow.android.amazon.azn_row.4.10.3","0"),
        (74,"ExpiredTokenForcedLogoutEnabled","1"),
        (75,"SortEnableDAGAndTopo","2"),
        (76,"CustomFontEnabled.4.21.1","1"),
        (77,"CustomFontEnabled.4.21.2","1"),
        (82,"EnableOptAppSwitch.ios","1"),
        (83,"FullAppSwitchInterval","86400"),
        (85,"AkamaiClientEnabled.android","1"),
        (86,"CustomFontEnabled.ios.row.4.13.2","1"),
        (87,"CustomFontEnabled.ios.na.4.13.2","1"),
        (88,"CustomFontEnabled.android.row.4.13.2","1"),
        (89,"CustomFontEnabled.android.na.4.13.2","1"),
        (90,"CustomFontEnabled.android.amazon.azn.4.13.2","1"),
        (91,"CustomFontEnabled.android.amazon.azn_row.4.13.2","1"),
        (92,"EnableOptAppSwitch.android","1"),
        (93,"EnableOptAppSwitch.android.amazon","1"),
        (101,"TopUpGrindEnabled","1"),
        (102,"SynergySendAdditionalPurchaseFields.ios","1"),
        (103,"SynergySendAdditionalPurchaseFields.android","1"),
        (104,"SynergySendAdditionalPurchaseFields.android.amazon","0"),
        (105,"EnableRoadCacheOptimization","1"),
        (106,"FixNegativeObjectiveCount","1"),
        (107,"LandDataVersionUpgraderEnabled","1"),
        (108,"ConfigVersion","131"),
        (109,"Game:Enable:JobManagerEnabled","1"),
        (114,"MinimumOSVersion.ios","7.0.0"),
        (115,"MinimumOSVersion.android","3.0.0"),
        (116,"MinimumOSVersion.android.amazon","3.0.0"),
        (117,"XZeroSortFix", "1"),
        (118,"DefaultJobCensus","1"),
        (119,"TntForgotPassURL","https://signin.ea.com/p/originX/resetPassword"),
        (120,"Game:Enable:ShowRestorePurchases.ios","1"),
        (121,"CountriesWhereUpdatesUnavailable","CN"),
        (122,"Game:Enable:ShowRestorePurchases.ios.4.26.0","0"),
        (123,"FastQuestReload","0"),
        (124,"FastQuestReload.4.26.5","0"),
        (125,"DisableQuestAutostartBackups","0"),
        (126,"EnableCheckIndex","1"),
        (127,"CrashReportingIOSOn","1"),
        (128,"CrashReportingKindleOn","1"),
        (129,"CrashReportingAndroidOn","1"),
        (130,"CrashReportingNokiaOn","1","0"),
        (132,"UseNumPadCodeLogin","1"),
        (133,"DeleteUserEnabled","1"),
        (134,"EnableBGDownloadIos","0"),
        (135,"EnableBGDownloadAndroid","0"),
        (136,"EnableBGDownloadAmazon","0"),
        (137,"MaxSimultaneousBGDownloadsIos","5"),
        (138,"MaxSimultaneousBGDownloadsAndroid","1"),
        (139,"MaxSimultaneousBGDownloadsAmazon","1"),
        (140,"BGDownloadQuickCheckEnabled","0"),
        (1010,"MHVersion", "1"),
        (1011,"RequestsPerSecond","29"),
        (996,"GeolocationCountryCode","US"),
        (997,"GeolocationCountryName","United States"),
        (950,"TntAuthUrl", "https://auth.tnt-ea.com"),
        (951,"TntWalletUrl", "https://wallet.tnt-ea.com"),
        (952,"TntNucleusUrl","https://nucleus.tnt-ea.com"),
        (953,"OriginFriendUrl","https://m.friends.dm.origin.com"),
        (954,"SynergyUrl", "https://synergy.eamobile.com:443"),
        (1015,"FriendsProxyUrl","https://friends.simpsons-ea.com"),
        (949,"SynergyFormatUrl","https://%s.sn.eamobile.com"),
        (995,"KillswitchAllowFriends","0"),
        (994,"ServerVersion","local"),
        (1000,"Origin.AppId","febb96fb9f8eb468"),  
        (1001,"ParamUrl.ea.na","https://kaleidoscope.ea.com?tag=81c4640c68f5eee1"),  
        (1002,"ParamUrl.ea.row","https://kaleidoscope.ea.com?tag=4dada08e18133a83"),  
        (1003,"TntUrl","https://tnt-auth.ea.com?trackingKey=3e92a468de3d2c33"),  
        (1011,"MH_Version","2")   
      ]

      for entry in config_entries:
        
        item = client_config.items.add()
        item.clientConfigId = entry[0]
        item.name = entry[1]
        item.value = entry[2]


      response = make_response(client_config.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/gameplayconfig")
    def gameplayconfig():

      client_config = GameplayConfigData_pb2.GameplayConfigResponse()
      
      config_entries = [
        ("MysteryBoxUpgrade_GameConfig:Enable:GambleCall", "0"),
        ("System:Disable:DynamicSteamer", "1"),
        ("TouchPriority_GameConfig:Enable:TouchPriority", "true"),
        ("Casino_GameConfig:Gamblers:LocalTapped_CurrencyAmount", "20"),
        ("Casino_GameConfig:Gamblers:LocalTapped_TokenChance", "0.15"),
        ("Validator_GameConfig:VariablesValidator:Validator", "1"),
        ("Validator_GameConfig:VariablesValidator:ScriptedRequirements", "1"),
        ("Validator_GameConfig:VariablesValidator:ScriptedRequirements_Variables", "1"),
        ("WildWest_GameConfig:Dates:Wildwest_Start", "2016-04-19 8:00"),
        ("WildWest_GameConfig:Dates:Wildwest_ActOne", "2016-04-19 8:00"),
        ("WildWest_GameConfig:Dates:Wildwest_ActTwo", "2016-05-03 8:00"),
        ("WildWest_GameConfig:Dates:Wildwest_ActThree", "2016-05-17 8:00"),
        ("WildWest_GameConfig:Dates:Wildwest_End", "2016-05-30 23:59"),
        ("WildWest_GameConfig:Dates:Wildwest_LastChance", "2016-05-24 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_GeneralStoreStartTime", "2016-04-19 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_GeneralStorePrizeTrackOneEndTime", "2016-05-03 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_GeneralStorePrizeTrackTwoEndTime", "2016-05-17 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_GeneralStorePrizeTrackThreeEndTime", "2016-05-30 23:59"),
        ("WildWest_GameConfig:Dates:WildWest_ReturningContentWave1", "2016-04-26 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_ReturningContentWave2", "2016-05-10 8:00"),
        ("WildWest_GameConfig:Dates:WildWest_ReturningContentWave3", "2016-05-24 8:00"),
        ("WildWestPromo_GameConfig:Dates:WildWestPromo_End", "2016-05-04 08:00"),
        ("DSH_GameConfig:Dates:DSH_End", "2016-02-04 7:00:00"),
        ("DSH_GameConfig:Dates:DSH_OutroEnd", "2016-03-04 7:00:00"),
        ("Casino_GameConfig:Dates:Casino_StartDate", "2016-02-23 8:00"),
        ("Casino_GameConfig:Dates:Casino_ActTwo", "2016-03-07 8:00"),
        ("Casino_GameConfig:Dates:Casino_ActThree", "2016-03-17 8:00"),
        ("Casino_GameConfig:Dates:Casino_EndDate", "2016-03-29 8:00"),
        ("Casino_GameConfig:Dates:Casino_ActTwo_Quests", "2016-03-03 8:00"),
        ("Casino_GameConfig:Dates:Casino_ActThree_Quests", "2016-03-13 8:00"),
        ("Casino_GameConfig:Dates:PlatScratcher_WindowOne_Start", "2016-03-01 8:00"),
        ("Casino_GameConfig:Dates:PlatScratcher_WindowOne_End", "2016-03-04 8:00"),
        ("Casino_GameConfig:Dates:PlatScratcher_WindowTwo_Start", "2016-03-24 8:00"),
        ("Casino_GameConfig:Dates:PlatScratcher_WindowTwo_End", "2016-03-27 8:00"),
        ("Casino_GameConfig:Dates:ReferAFriendEnd", "2016-03-23 8:00"),
        ("Margeian_GameConfig:Dates:Margeian_Start", "2016-02-04 7:00:00"),
        ("Margeian_GameConfig:Dates:Margeian_End", "2016-03-16 8:00:00"),
        ("Margeian_GameConfig:Dates:Margeian_Kill", "2016-04-16 8:00:00"),
        ("Tailgate_GameConfig:Dates:Tailgate_Start", "2016-01-01 08:00"),
        ("Tailgate_GameConfig:Dates:Tailgate_End", "2016-02-09 08:00"),
        ("Superheroes_GameConfig:Dates:BeachHouseStartDate", "2015-03-29 8:00"),
        ("Superheroes_GameConfig:Dates:BeachHouseEndDate", "2015-04-07 8:00"),
        ("Superheroes_GameConfig:Dates:MilhouseStartDate", "2015-03-24 8:00"),
        ("Superheroes_GameConfig:Dates:MilhouseEndDate", "2015-03-31 8:00"),
        ("Superheroes_GameConfig:Dates:RadStationStartDate", "2015-03-29 8:00"),
        ("Superheroes_GameConfig:Dates:RadStationEndDate", "2015-04-07 8:00"),
        ("Superheroes_GameConfig:Dates:BartCaveStartDate", "2015-03-29 8:00"),
        ("Superheroes_GameConfig:Dates:BartCaveEndDate", "2015-04-07 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_ActOne_Start", "2014-01-01 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_ActTwo_Start", "2014-04-28 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_ActThree_Start", "2014-05-12 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_End", "2014-05-26 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_KillDate", "2014-06-04 8:00"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_5MinBeforeActTwo", "2014-04-28 7:55"),
        ("Terwilligers_GameConfig:Dates:Terwilligers_5MinBeforeActThree", "2014-05-12 7:55"),
        ("June2015_GameConfig:Dates:June2015_StartDate", "2015-05-23 8:00"),
        ("June2015_GameConfig:Dates:HomerballActOne", "2015-05-23 8:00"),
        ("June2015_GameConfig:Dates:HomerballActTwo", "2015-05-03 8:00"),
        ("June2015_GameConfig:Dates:HomerballActThree", "2015-05-13 8:00"),
        ("June2015_GameConfig:Dates:HomerballEnd", "2015-05-23 16:00"),
        ("June2015_GameConfig:Dates:HomerballActOneCrossover", "2015-05-01 8:00"),
        ("June2015_GameConfig:Dates:HomerballActTwoCrossover", "2015-05-11 8:00"),
        ("June2015_GameConfig:Dates:JuneStorePhaseTwoStart", "2015-05-03 8:00"),
        ("June2015_GameConfig:Dates:JuneStorePhaseThreeStart", "2015-05-13 8:00"),
        ("June2015_GameConfig:Dates:RevertToThreePanel", "2015-06-07 8:00"),
        ("June2015_GameConfig:Dates:SoccerCupStart", "2015-05-25 8:00"),
        ("June2015_GameConfig:Dates:SoccerCupEnd", "2015-05-30 8:00"),
        ("June2015_GameConfig:Dates:JuneTakedownEnd", "2015-07-28 8:00"),
        ("StEaster_GameConfig:Dates:StEaster_PromoEnd", "2016-03-20 8:00:00"),
        ("StEaster_GameConfig:Dates:StEaster_End", "2016-03-30 8:00:00"),
        ("StEaster_GameConfig:Dates:StEaster_Switch", "2016-03-23 8:00:00"),
        ("StEaster_GameConfig:Dates:StEaster_Kill", "2016-04-29 8:00:00"),
        ("StEaster_GameConfig:Dates:CruddySunday", "2016-03-27 8:00:00"),
        ("StEaster_GameConfig:Dates:CruddySunday_End", "2016-03-29 8:00:00"),
        ("StEaster_GameConfig:Dates:StPatsDay", "2016-03-17 8:00:00"),
        ("THOH2015_GameConfig:Dates:THOH2015ActOne", "2015-10-06 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015ActTwo", "2015-10-20 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015ActThree", "2015-11-04 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015ActEnd", "2015-11-17 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015ActKill", "2015-11-27 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015EventEndReminder", "2015-11-14 8:00"),
        ("THOH2015_GameConfig:Dates:THOH2015EventEndReminderEnd", "2015-11-14 23:59"),
        ("THOH2015_GameConfig:Dates:THOH2015LastDayReminder", "2015-11-17 1:00"),
        ("THOH2015_GameConfig:Dates:THOH2015TakedownActive", "2015-11-18 1:00"),
        ("THOH2015_GameConfig:Dates:THOH2015PrizeTrackActOneEnd", "2015-10-20 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_StartDate", "2014-12-08 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_ActOne", "2014-12-08 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_ActTwo", "2014-12-19 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_EndDate", "2015-01-02 8:00"),
        ("XMAS2015_GameConfig:Dates:Maggie_Early_StartDate", "2014-12-23 8:00"),
        ("XMAS2015_GameConfig:Dates:Maggie_StartDate", "2015-01-02 8:00"),
        ("XMAS2015_GameConfig:Dates:Maggie_EndDate", "2015-01-19 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_NewYearsDay", "2015-01-01 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_NewYearsStart", "2014-12-29 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_NewYearsFinale", "2014-12-31 8:00"),
        ("XMAS2015_GameConfig:Dates:XMASFifteen_NewYearsEnd", "2015-01-02 8:00"),
        ("OldJewishMan_GameConfig:Dates:RoshHashanah_StartDate", "2015-09-13 8:00"),
        ("OldJewishMan_GameConfig:Dates:EarlyAccess_OldJewishMan", "2015-09-17 8:00"),
        ("OldJewishMan_GameConfig:Dates:RoshHashanah_EndDate", "2015-09-16 8:00"),
        ("MathletesFeat_GameConfig:Dates:MathletesFeat_Air", "2015-05-18 0:00"),
        ("MathletesFeat_GameConfig:Dates:MathletesFeat_End", "2015-05-19 8:00"),
        ("MathletesFeat_GameConfig:Dates:MathletesFeat_Kill", "2015-06-19 8:00"),
        ("THOH2015_TieIn_GameConfig:Dates:THOH2015_TieIn_StartDate", "2015-10-21 8:00"),
        ("THOH2015_TieIn_GameConfig:Dates:THOH2015_TieIn_AirshipStartDate", "2015-10-23 8:00"),
        ("THOH2015_TieIn_GameConfig:Dates:THOH2015_TieIn_AirDate", "2015-10-25 8:00"),
        ("THOH2015_TieIn_GameConfig:Dates:THOH2015_TieIn_EndDate", "2015-10-26 8:00"),
        ("THOH2015_TieIn_GameConfig:Dates:THOH2015_TieIn_KillDate", "2015-11-26 8:00"),
        ("Valentines2016_GameConfig:Dates:Valentines2016_End", "2015-02-17 8:00:00"),
        ("Valentines2016_GameConfig:Dates:Valentines2016_Day", "2015-02-14 8:00:00"),
        ("Valentines2016_GameConfig:Dates:Valentines2016_Air", "2015-02-15 3:00:00"),
        ("Valentines2016_GameConfig:Dates:Valentines2016_DayEnd", "2015-02-15 8:00:00"),
        ("Valentines2016_GameConfig:Dates:Valentines2016_MaudeAvailability", "2015-02-24 8:00:00"),
        ("HalloweenOfHorror_GameConfig:Dates:THOH2015TieInStart", "2015-10-14 8:00"),
        ("HalloweenOfHorror_GameConfig:Dates:THOH2015TieInEnd", "2015-10-19 8:00"),
        ("HalloweenOfHorror_GameConfig:Dates:THOH2015TieInKill", "2014-11-19 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekOne", "2015-07-21 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekTwo", "2015-07-28 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekThree", "2015-08-04 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekFour", "2015-08-11 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekNine", "2015-09-15 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:SpringfieldHeightsWeekTen", "2015-09-22 8:00"),
        ("SpringfieldHeights_GameConfig:Dates:WealthyWednesday_EndTime", "2014-12-04 8:00"),
        ("WhackingDayPromo_GameConfig:Dates:WhackingDayPromo_Start", "2016-05-09 7:00"),
        ("WhackingDayPromo_GameConfig:Dates:WhackingDayPromo_End", "2016-05-12 7:00"),
        ("WhackingDayPromo_GameConfig:Dates:WhackingDayPromo_Kill", "2016-06-11 7:00"),
        ("WhackingDayPromo_GameConfig:Dates:HomerLivePromo_Start", "2016-05-09 7:00"),
        ("WhackingDayPromo_GameConfig:Dates:HomerLivePromo_End", "2016-05-15 7:00"),
        ("Superheroes2_GameConfig:Dates:SuperheroesTwo_QuickBattle", "2016-06-28 7:00"),
        ("SpringfieldGames_GameConfig:FirmwareMessage:Enabled", "1"),
        ("SciFi_GameConfig:Campaign:Reward1", "60"),
        ("SciFi_GameConfig:Campaign:Reward2", "15"),
        ("SciFi_GameConfig:Enable:Interactions", "1"),
        ("SciFi_SciFighterConfig:SciFighterPayouts:BaseReward_Event", "100"),
        ("SciFi_SciFighterConfig:SciFighterPayouts:CompletionReward_Event", "45"),
        ("SciFi_SciFighterConfig:SciFighterPayouts:PerSecondReward_Event", "5"),
        ("SeasonPremiere2016_GameConfig:Dates:SeasonPremiere2016_4X_End", "2016-10-04 17:00:00"),
        ("SeasonPremiere2016_GameConfig:Dates:SeasonPremiere2016_End", "2016-10-04 17:00:00"),
        ("NewUserBalancingConfig:XPTarget:Lvl60_TargetToNext", "500000"),
        ("NewUserBalancingConfig:XPTarget:PrestigeIncreaseBonusExp", "1000000"),
        ("FirstTimeMTX_GameConfig:FirstTimePacks:Enabled", "true"),
        ("AroundTheWorld_BalancingConfig:AirportJobs:TicketSpawnTimer", "20m"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerCount_Layer1_Base", "1"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerCount_Layer1_Range", "3"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerValue_Layer1_Base", "61"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerValue_Layer1_Range", "33"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerCount_Layer1_Base", "1"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerCount_Layer1_Range", "4"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerValue_Layer1_Base", "14"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerValue_Layer1_Range", "11"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerCount_Layer2_Base", "8"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerCount_Layer2_Range", "8"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:SpecimenLayerValue_Layer2_Base", "163"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerCount_Layer2_Base", "7"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerCount_Layer", "7"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerValue_Layer2_Base", "56"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:TachyonLayerValue_Layer2_Range", "44"),
        ("TimeTravellingToaster_BalancingConfig:ExcavationSiteRewards:PrizeTrackPerShovelValue", "31"),
        ("Music_Spreadsheet_Config:PrizeTrack3:Prize1", "14600"),
        ("Music_Spreadsheet_Config:PrizeTrack3:Prize2", "33600"),
        ("Music_Spreadsheet_Config:PrizeTrack3:Prize4", "83200"),
        ("Music_Spreadsheet_Config:PrizeTrack3:Prize5", "109500"),
        ("Music_Spreadsheet_Config:PrizeTrack3:Prize6", "146000"),
        ("THOH2017_Config:PrizeTrack2:Prize1", "900"),
        ("THOH2017_Config:PrizeTrack2:Prize2", "2800"),
        ("THOH2017_Config:PrizeTrack2:Prize3", "5600"),
        ("THOH2017_Config:PrizeTrack2:Prize4", "9400"),
        ("THOH2017_Config:PrizeTrack2:Prize5", "13200"),
        ("THOH2017_Config:PrizeTrack2:Prize6", "17000"),
        ("THOH2017_Config:PrizeTrack2:Prize7", "22700"),
        ("THOH2017_Config:PrizeTrack3:Prize1", "1300"),
        ("THOH2017_Config:PrizeTrack3:Prize2", "3900"),
        ("THOH2017_Config:PrizeTrack3:Prize3", "7800"),
        ("THOH2017_Config:PrizeTrack3:Prize4", "13000"),
        ("THOH2017_Config:PrizeTrack3:Prize5", "18200"),
        ("THOH2017_Config:PrizeTrack3:Prize6", "23400"),
        ("THOH2017_Config:PrizeTrack3:Prize7", "31200"),
        ("BFCM2017_GameConfig:Dates:BlackFriday2017_End", "2017-11-28 8:00"),
        ("BFCM2017_GameConfig:Dates:CyberMonday2017_End", "2017-11-28 8:00"),
        ("THOH2018_GameConfig:PremiumCosts:Hellscape", "199"),
        ("THOHXXX_GameConfig:EnableMTX:THOHXXX_iOSMTXOffersEnabled", "true"),
        ("THOHXXX_GameConfig:EnableMTX:THOHXXX_AndroidMTXOffersEnabled", "true"),
        ("THOHXXX_GameConfig:Dates:THOHXXX_MERCH_TenCommandments_End", "2019-11-20 14:00")
      ]
      
      for config_item in config_entries:
        item = client_config.item.add()
        item.name = config_item[0]
        item.value = config_item[1]

      response = make_response(client_config.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/users", methods=["PUT", "GET"])
    def mh_user():

      if self.debug: 
        print(f"appVer: {request.args.get('appVer')}")
        print(f"appLang: {request.args.get('appLang')}")
        print(f"application: {request.args.get('application')}")
        print(f"applicationUserId: {request.args.get('applicationUserId')}")

      data = AuthData_pb2.UsersResponseMessage()
      data.user.userId = self.user_user_id
      data.user.telemetryId = self.user_telemtry_id
      data.token.sessionKey = self.token_session_key
      
      response = make_response(data.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/protoWholeLandToken/<land_id>/", methods=["POST"])
    def protoWholeLandToken(land_id):
      if self.debug: print(f"force: {request.args.get('force')}")

      req = WholeLandTokenData_pb2.WholeLandTokenRequest()
      req.ParseFromString(request.data)
      if self.debug: print(f"\trequestId: {req.requestId}")

      data = WholeLandTokenData_pb2.WholeLandTokenResponse()
      data.token = self.land_token
      data.conflict = False
      
      response = make_response(data.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    # server prod.simpsons-ea.com
    @self.app.route("/mh/userstats", methods=["POST"])
    def userstats():
      if self.debug: 
        print(f"device_id: {request.args.get('device_id')}")
        print(f"synergy_id: {request.args.get('synergy_id')}")
      abort(409)

    # server river-mobile.data.ea.com
    @self.app.route("/tracking/api/core/logEvent", methods=["POST"])
    def core_logEvent():
      if self.debug: 
        print(f"\tlocalization: {request.args.get('localization')}")
        print(f"\tappLang: {request.args.get('appLang')}")
        print(f"\tdeviceLocale: {request.args.get('deviceLocale')}")
        print(f"\tdeviceLanguage: {request.args.get('deviceLanguage')}")
        print(f"\tappVer: {request.args.get('appVer')}")
        print(f"\thwId: {request.args.get('hwId')}")

        print(f"\tBody (json):")
        print(request.data)  

      return jsonify({"status": "ok"})


    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/checkToken/<token>/protoWholeLandToken/")
    def checkToken(token):
      if self.debug: print(f"\ttoken: {token}")

      data = AuthData_pb2.TokenData()
      data.sessionKey = self.session_key
      data.expirationDate = 0
      
      response = make_response(data.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/trackingmetrics/", methods=["POST"])
    def trackingmetrics():
      
      req = ClientMetrics_pb2.ClientMetricsMessage()
      req.ParseFromString(request.data)
      if self.debug: 
        print(f"\ttype: {req.type}")
        if req.HasField('severity'):
          print(f"\tSeverity: {req.severity}")
        print(f"\tName: {req.name}")
        print(f"\tValue: {req.value}")
     
      data = AuthData_pb2.TokenData()
      data.sessionKey = self.session_key
      data.expirationDate = 0
      
      xml = '<?xml version="1.0" encoding="UTF-8"?><Resources><URI>OK</URI></Resources>'
      response = make_response(xml)
      response.headers['Content-Type'] = 'application/xml'
      return response

    # server: gateway.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/friendData/origin")
    def friendData_origin():
      
      friend_data = GetFriendData_pb2.GetFriendDataResponse()
      response = make_response(friend_data.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response  

    # server: pin-river.data.ea.com
    @self.app.route("/pinEvents", methods=["POST"])
    def pinEvents():
      if self.debug: print(request.get_json())   # get_json handles gzip decompression automatically
      resp = '{"status": "ok"}'
      response = make_response(resp)
      response.headers['Content-Type'] = 'application/json'
      return response
   
    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/protoland/<land_id>/", methods=["POST", "GET"])
    def bg_gameserver_plugin_protoland(land_id: str):
      if self.debug: print(f"\tland id: {land_id}")
        
      if request.method == 'GET':
        response = make_response(self.land_proto.SerializeToString())
        response.headers['Content-Type'] = 'application/x-protobuf'
        return response

      elif request.method == "POST":
        # TODO: save updates to the town
        with open("mytown.pb", "wb") as f:
          f.write(self.land_proto.SerializeToString())
        
        
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><WholeLandUpdateResponse/>'
        response = make_response(xml)
        response.headers['Content-Type'] = 'application/xml'
        return response

    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/protocurrency/<land_id>/")
    def protocurrency(land_id: str):
      
      currency = PurchaseData_pb2.CurrencyData()
      currency.id = land_id
      currency.vcTotalPurchased = 0
      currency.vcTotalAwarded = 0
      currency.vcBalance = 1234567                    # number of donuts
      currency.createdAt = int(round(time.time() * 1000))
      currency.updatedAt = int(round(time.time() * 1000))

      response = make_response(currency.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

     
    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/extraLandUpdate/<land_id>/protoland/", methods=["POST"]) 
    def extraLandUpdate(land_id: str):
      
      # TODO: process the incoming update
      
      # TODO: figure out what the messages due
      extraland = LandData_pb2.ExtraLandResponse()
      response = make_response(extraland.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response
      
      """
      repeated .Data.ExtraLandMessage.CurrencyDelta processedCurrencyDelta = 1;
      repeated .Data.EventMessage processedEvent = 2;
      repeated .Data.EventMessage receivedEvent = 3;
      repeated .Data.ExtraLandResponse.CommunityGoal communityGoal = 4;
      message CommunityGoal {
        optional string category = 1;
        optional int64 progressTotal = 2;
        optional double progressRate = 3;
        repeated int64 awardThresholds = 4;
      }
      """
      
    # server: prod.simpsons-ea.com
    @self.app.route("/mh/games/bg_gameserver_plugin/event/<land_id>/protoland/")
    def plugin_event(land_id: str):

      # TODO: figure out the use of this.
      event = LandData_pb2.EventsMessage()
      response = make_response(event.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

     
    # Generic default route handler
    @self.app.get("/")
    def root():
      if self.debug: print("/ called")
      return ""

    # start server
    self.app.run(debug=True, host="0.0.0.0", port=80) #443, ssl_context=("mydomain.com.crt", "mydomain.com.key"))

def start_server():
  print("starting web server")
  server = TheSimpsonsTappedOutLocalServer(sys.argv[1])
  server.run()


if __name__ == "__main__":
  start_server()
