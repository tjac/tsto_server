import base64
import datetime
import hashlib
import json
import logging
import os
import random
import string
import sys
import time
import threading
from typing import Any, Dict
import uuid

# pip install dnserver
#from dnserver import DNSServer
#from dnserver.load_records import Records, Zone

# pip install flask
from flask import Flask, abort, jsonify, make_response, request, send_file
from flask_inflate import Inflate       # pip install flask-inflate
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

# The Simpson's Tapped Out protobufs
from proto import *

# midddleware to fix tsto apk patches that produces multiple slashes
import re
from werkzeug.wrappers import Request
class GameassetsRewriteMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if '/gameassets/' in request.path:  # we only target the gameassets URL and reduce multiple /'s to just one each
            environ['PATH_INFO'] = re.sub(r'/+', '/', request.path)
        return self.app(environ, start_response)

class TheSimpsonsTappedOutLocalServer:
  
  def __init__(self, server_url: str):
    # Generate the Flask application object
    self.app = Flask(__name__)
    Inflate(self.app)     # Enable ability to auto decompress gzip responses
    self.app.wsgi_app = GameassetsRewriteMiddleware(self.app.wsgi_app)
    
    # Load the configuration first
    self.CONFIG_FILENAME = "config.json"
    self.config: dict = {}
    self.load_config()

    # Set the initial configuration
    self.server_url: bool = server_url
    self.debug: bool = self.config.get("debug", False)
    self.run_tutorial: bool = self.config.get("debug", False)
    self.dlc_dir: str = self.config.get("dlc_dir")
    self.towns_dir: str = self.config.get("towns_dir")
    self.town_filename: str = self.config.get("active_town")
    self.reverse_proxy: bool = self.config.get("reverse_proxy", False)

    self.session_key: str = str(uuid.uuid4())
    self.land_token: str = str(uuid.uuid4())
    self.user_user_id: str = "".join([chr(random.randint(0x30,0x39)) for x in range(38)])
    self.user_telemtry_id: str = "".join([chr(random.randint(0x30,0x39)) for x in range(11)])
    self.token_session_key: str = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()
    self.token_user_id: str = str(random.randint(1000000000000, 99999999999999))
    self.token_authenticator_pid_id: int = random.randint(1000000000000, 99999999999999)
    self.token_persona_id: int = random.randint(1000000000000, 99999999999999)
    self.token_telemetry_id: str = str(random.randint(1000000000000, 99999999999999))
    self.personal_id: str = str(random.randint(1000000000000, 99999999999999))
    self.display_name: str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(5,12)))
    self.persona_name: str = self.display_name.lower()
    self.me_persona_pid_id: str = str(random.randint(1000000000000, 99999999999999))
    self.me_persona_display_name: str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(random.randint(5,12)))
    self.me_persona_name: str = self.me_persona_display_name.lower()
    self.me_persona_anonymous_id: str = base64.b64encode(hashlib.md5(self.me_persona_name.encode("utf-8")).digest()).decode("utf-8")
    self.device_id: str = hashlib.sha256(str(datetime.datetime.now()).encode("utf-8")).hexdigest()
    self.auth_code: str = ""

    # Generate a blank world (LandMessage) then attempt to load the active town
    self.land_proto: LandData_pb2.LandMessage = LandData_pb2.LandMessage()
    self.load_town()

    # if behind a reverse proxy setup so that the correct IP is recorded
    if self.reverse_proxy:
      self.app.wsgi_app = ProxyFix(
        self.app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
      )
    
    # Add the URL routes for Flask
    self.add_routes()

  def load_config(self) -> bool:
    """Load server configuration from json file"""
    self.config = {}
    with open(self.CONFIG_FILENAME, "r") as f:
      self.config = json.load(f)
    return True
    
  def save_config(self) -> bool:
    """Save server configuration to json file"""
    with open(self.CONFIG_FILENAME, "w") as f:
      json.save(self.config, f)
    return True

  def load_town(self) -> bool:
    """Attempts to load the current town_filename."""
    
    print(f"Attempting to load {self.town_filename}")

    # If the town_filename is not specified, just use a blank world and
    # set the run_tutorial to true.
    if not self.town_filename:
      # This is for loading a blank/tutorial town
      print("No town found. Generating blank world.")
      self.land_proto: LandData_pb2.LandMessage = LandData_pb2.LandMessage()
      self.land_proto.friendData.dataVersion = 72
      self.land_proto.friendData.hasLemonTree = False
      self.land_proto.friendData.language = 0
      self.land_proto.friendData.level = 0
      self.land_proto.friendData.name = "tsto_server_blank"
      self.land_proto.friendData.rating = 0
      self.land_proto.friendData.boardwalkTileCount = 0
      self.run_tutorial = True
      print(f"[r]land_proto is {len(self.land_proto.SerializeToString())} bytes")

      return True
    
    # Try to load the specified world from disk
    town_file_path = os.path.join(self.towns_dir, self.town_filename)
    if not os.path.isfile(town_file_path):
      # Unable to find the file, so generate a blank town and save it
      print(f"{town_file_path} wasn't found")
      self.land_proto: LandData_pb2.LandMessage = LandData_pb2.LandMessage()
      self.land_proto.friendData.dataVersion = 72
      self.land_proto.friendData.hasLemonTree = False
      self.land_proto.friendData.language = 0
      self.land_proto.friendData.level = 0
      self.land_proto.friendData.name = "tsto_server_blank"
      self.land_proto.friendData.rating = 0
      self.land_proto.friendData.boardwalkTileCount = 0
      self.run_tutorial = True
      print(f"[r]land_proto is {len(self.land_proto.SerializeToString())} bytes")
      return self.save_town()

    # Try to load the specified town...
    with open(town_file_path, "rb") as f:
      # Check if we have a teamtsto.org backup.
      try:
        self.land_proto.ParseFromString(f.read())
      except google.protobuf.message.DecodeError:
        try:
          # Check if we have a teamtsto.org backup.
          header = f.read(2)
          if header in (b'\x0a\x26', b'\x0a\x27', b'\x0a\x28'):
            f.seek(0)
          else:
            f.seek(0x0c)  # strip the header off the protobuf if we do.
          self.land_proto.ParseFromString(f.read())          
        except google.protobuf.message.DecodeError:
          print("[error] Unable to load {self.town_filename} town.")
          return False
      if self.land_proto.HasField("id"):
        self.user_user_id = self.land_proto.id
      if self.debug:
        print(f"[r]land_proto is {len(self.land_proto.SerializeToString())} bytes") 
        print(f"   land id is now {self.user_user_id}")     

    return True

  def save_town(self) -> bool:
    """Save the current .land_proto to disk as .town_filename."""
    # If there somehow isn't an active .land_proto, return error.
    if not self.land_proto:
      print(f"[error] .land_proto is None. Unable to save.")
      return False
    
    # If there isn't a name for the town, return error.
    if not self.town_filename:
      print(f"[error] .town_filename is None. Unable to save.")
      return False

    # Construct the full path/name
    town_file_path = os.path.join(self.towns_dir, self.town_filename)
    with open(town_file_path, "wb") as f:
      f.write(self.land_proto.SerializeToString())
      print(f"[w]land_proto is {len(self.land_proto.SerializeToString())} bytes")


    return True

  def add_routes(self):
    """Add the routes and map their handler functions."""
    
    # server: syn-dir.sn.eamobile.com
    self.app.add_url_rule("/director/api/<string:platform>/getDirectionByPackage",
                            view_func = self.get_direction_by_bundle)  # android
    self.app.add_url_rule("/director/api/<string:platform>/getDirectionByBundle",
                            view_func = self.get_direction_by_bundle)  # ios

    # server: oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com
    self.app.add_url_rule(# "/netstorage/gameasset/direct/simpsons/dlc/<string:filename>",
                          "/gameassets/<string:directory>/<string:filename>",
                            view_func = self.dlc_download)

    # server: user.sn.eamobile.com
    self.app.add_url_rule("/user/api/android/validateDeviceID",
                            view_func = self.validate_device_id)
    self.app.add_url_rule("/user/api/android/getDeviceID",
                            view_func = self.get_device_id)
    self.app.add_url_rule("/user/api/android/getAnonUid",
                            view_func = self.get_anon_uid)

    # server: gateway.ea.com
    self.app.add_url_rule("/proxy/identity/pids/me/personas/<string:user_id>",
                            view_func = self.me_personas)
    self.app.add_url_rule("/proxy/identity/pids/<string:pid>/personas",
                            view_func = self.pid_personas)
    self.app.add_url_rule("/proxy/identity/progreg/code", methods=["POST"],
                            view_func = self.progreg_code)

    # server: accounts.ea.com
    self.app.add_url_rule("/connect/auth", view_func = self.connect_auth)
    self.app.add_url_rule("/connect/token", methods=["POST"],
                            view_func = self.connect_token)
    self.app.add_url_rule("/connect/tokeninfo",
                            view_func = self.connect_tokeninfo)
    self.app.add_url_rule("/proxy/identity/geoagerequirements",
                            view_func = self.geoagerequirements)
    self.app.add_url_rule("/probe", view_func = self.probe)

    # server: pn.tnt-ea.com
    self.app.add_url_rule("/rest/v1/games/<game_id>/devices", methods=["POST"],
                            view_func = self.game_devices)
    self.app.add_url_rule("/games/<game_id>/devices", methods=["POST"],
                            view_func = self.game_devices)
   
    # server river-mobile.data.ea.com
    self.app.add_url_rule("/tracking/api/core/logEvent", methods=["POST"],
                            view_func = self.core_logEvent)
  
    # server: pin-river.data.ea.com
    self.app.add_url_rule("/pinEvents", methods=["POST"],
                            view_func = self.pinEvents)

    # server: prod.simpsons-ea.com
    self.app.add_url_rule("/mh/gameplayconfig", view_func = self.gameplayconfig)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/trackinglog/",
                            methods=["POST"], view_func = self.tracking_log)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/protoClientConfig/",
                            view_func = self.protoClientConfig)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/protoWholeLandToken/<land_id>/", 
                            methods=["POST"],
                            view_func = self.protoWholeLandToken)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/checkToken/<token>/protoWholeLandToken/",
                            view_func = self.checkToken)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/trackingmetrics/",
                            methods=["POST"], view_func = self.trackingmetrics)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/protoland/<land_id>/",
                            methods=["POST", "GET"],
                            view_func = self.bg_gameserver_plugin_protoland)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/protocurrency/<land_id>/",
                            view_func = self.protocurrency)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/extraLandUpdate/<land_id>/protoland/",
                            methods=["POST"],
                            view_func = self.extraLandUpdate)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/event/<land_id>/protoland/",
                            view_func = self.plugin_event)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/friendData",
                            methods=["POST"], view_func = self.friend_data)
    self.app.add_url_rule("/mh/games/bg_gameserver_plugin/friendData/origin",
                            methods=["GET"], view_func = self.friend_data)
    self.app.add_url_rule("/mh/games/lobby/time", view_func = self.lobby_time)
    self.app.add_url_rule("/mh/users", methods=["PUT", "GET"],
                            view_func = self.mh_user)
    self.app.add_url_rule("/mh/userstats", methods=["POST"],
                            view_func = self.userstats)



    # server: any (generic rule)

    self.app.add_url_rule("/", view_func = self.default_root)

  def run(self):
    """Activates the Flask server."""

    # start dns server
    """
    dnsserver = DNSServer(port=53)
    ipv4_parts = list(map(int, self.server_ip.split('.')))
    local_ipv6 = '::ffff:{:02x}{:02x}:{:02x}{:02x}'.format(*ipv4_parts)
    print(local_ipv6)

    # Disable to the logging noise from the dnserver
    dnserver_logger = logging.getLogger('dnserver')
    dnserver_logger.setLevel(logging.ERROR)
    
    dnsserver.add_record(Zone(host="syn-dir.sn.eamobile.com", type="A", answer=self.server_ip))
    dnsserver.add_record(Zone(host="syn-dir.sn.eamobile.com", type="AAAA", answer=local_ipv6))
    dnsserver.start()
    assert dnsserver.is_running
    """
    
    # start server: http version
    self.app.run(debug=True, host="0.0.0.0", port=9000) #443, ssl_context=("mydomain.com.crt", "mydomain.com.key"))
    #threading.Thread(target=lambda: self.app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)).start()
    
    # start server: https version
    #cert_key = os.path.join("certs", "syn-dir.sn.eamobile.com-key.pem")
    #cert = os.path.join("certs", "syn-dir.sn.eamobile.com.pem")
    #self.app.run(debug=True, host="0.0.0.0", port=443, ssl_context=(cert, cert_key))


  ##############################################################################
  # Server route handlers
  ##############################################################################

  # server: syn-dir.sn.eamobile.com
  
  def get_direction_by_bundle(self, platform: str):
    """Handler for the URLs:
      syn-dir.sn.eamobile.com/director/api/<string:platform>/getDirectionByPackage
      syn-dir.sn.eamobile.com/director/api/<string:platform>/getDirectionByBundle
    """
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
                      "value": f"{self.server_url}"
                  },
                  {
                      "key": "applecert.url",
                      "value": "https://www.apple.com/appleca/AppleIncRootCertificate.cer"
                  },
                  {
                      "key": "origincasualapp.url",
                      "value": f"{self.server_url}/loader/mobile/ios/"
                  },
                  {
                      "key": "akamai.url",
                      "value": f"{self.server_url}/skumasset/gameasset/" #"http://cdn.skum.eamobile.com/skumasset/gameasset/"
                  }
              ],
              "telemetryFreq": 300
          }

    # Setup URL redirects to our server
    for key in self.config["server_redirects"]:
      resp["serverData"].append({"key": key, "value": f"{self.server_url}"})

    return jsonify(resp)


  # server: oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com

  def dlc_download(self, directory: str, filename: str):
    """Handler for oct2018-4-35-0-uam5h44a.tstodlc.eamobile.com/netstorage/gameasset/direct/simpsons/<string:directory>/<string:filename>"""
    try:
      directory = secure_filename(directory)    # Sanitize the directory
      filename = secure_filename(filename)      # Sanitize the filename
      file_path = os.path.join(self.dlc_dir, directory, filename)
      if self.debug:
        print(f"requested file: {file_path}")
      if os.path.isfile(file_path):
          return send_file(file_path, mimetype="application/zip")#, as_attachment=True)
      else:
          return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
      if self.debug:
        print(f"Exception: {e}")
      return make_response(f"Error: {str(e)}", 500) 


  # server: user.sn.eamobile.com

  def get_anon_uid(self):
    """Handler for user.sn.eamobile.com/user/api/android/getAnonUid"""
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

  def get_device_id(self):
    """Handler for user.sn.eamobile.com/user/api/android/getDeviceID"""
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

  def validate_device_id(self):
    """Handler for user.sn.eamobile.com/user/api/android/validateDeviceID"""
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

  # server: gateway.ea.com

  def me_personas(self, user_id: str):
    """Handler for gateway.ea.com/proxy/identity/pids/me/personas/<user_id>"""
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
              "lastAuthenticated": "2024-12-28T5:25Z",
              "anonymousId": self.me_persona_anonymous_id
          }
      }
    )

  def pid_personas(self, pid: str):
    """Handler for gateway.ea.com/proxy/identity/pids/<pid>/personas"""
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

  def progreg_code(self):
    """Handler for gateway.ea.com/proxy/identity/progreg/code"""

    if self.debug: print(f"code request: {request.data}")

    # Try to parse the request data
    request_data = {}
    try:
      request_data = json.loads(request.data)
    except Exception as e:
      print(f"Failure to jsonify request: {request.data}")
      abort(500)
    
    filename: str = None
    code_type: str = request_data["codeType"]
    if code_type == "EMAIL":
      filename = request_data["email"]
      # town_filename is empty, fill in with a dummy name
      if not filename:
        filename = "blank_name@email.com"
      # Reduce the email to a filename by stripping everything after @
      filename = filename.split("@")[0]

    elif code_type == "SMS":
      filename = request_data["phoneNumber"]

    else:
      printf("Unknown codeType: {request_data}")
      abort(500)

    self.town_filename = filename

    # Attempt to load the town
    self.load_town()

    return ""

  def friend_data(self):
    """Handler for gateway.simpsons-ea.com/mh/games/bg_gameserver_plugin/friendData[/origin]"""
    friend_data = GetFriendData_pb2.GetFriendDataResponse()
    response = make_response(friend_data.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response  

  # server: accounts.ea.com

  def connect_auth(self):
    """Handler for accounts.ea.com/connect/auth"""
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

    # Is this the first stage of an authention request? The "verify" code stage.
    if request.args.get("authenticator_login_type") == "mobile_ea_account":
      
      # Decode the sig argument
      sig = request.args.get("sig")
      if sig:
        # Decompse the sig into its body and hash
        body, body_hash = sig.split(".")
        if not body:
          about(403)
      
      # Build a long lived token
      # This is taken from an actual session. Once de-base64'd, it looks like:
      #    AT0:2.0:3.0:86400:KpnQGZO2SIxD0xKZEL9pBauVdBJYRO0NYD2:47082:riqac
      #    ^            ^        ^                                 ^    ^--- ?
      #    |            |        |                                  ---- game id?
      #    |            |         --- actual token?
      #    |             ------ token life (in seconds)
      #     ------ header ("AuthToken0"?)
      self.lnglv_token = "QVQwOjIuMDozLjA6ODY0MDA6S3BuUUdaTzJTSXhEMHhLWkVMOXBCYXVWZEJKWVJPME5ZRDI6NDcwODI6cmlxYWM"
      
      # Build the response json
      return jsonify(
        {
          "code": "QUOgAOq3MMhJN3hQu3WMxVKvNbDKwgSQoVX3d0YS",
          "lnglv_token": self.lnglv_token
        }
      ) 
     
    # If we are getting an anonymous token, just return one...
    # TODO: programmatically generate this
    return jsonify({"code": "QUOgAP3pKNGNI71KH72KdKjMkkFE5sO1nWWi34qGAQ"})


  def connect_token(self):
    """Handler for accounts.ea.com/connect/token"""
    if self.debug: 
      print(f"client_id: {request.args.get('client_id')}")
      print(f"client_secret: {request.args.get('client_secret')}")
      print(f"code: {request.args.get('code')}")
      print(f"grant_type: {request.args.get('grant_type')}")
      print(f"redirect_uri: {request.args.get('redirect_uri')}")
      print(f"release_type: {request.args.get('release_type')}")

    # TODO: properly generate the access and refresh tokens
    self.access_token = base64.b64encode(
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
        "access_token": self.access_token,
        "token_type": "Bearer",
        "expires_in": 86400,     # 43199,
        "refresh_token": refresh_token,
        "refresh_token_expires_in": 86400, # 86399
        "id_token": id_token
      }
    )

  def connect_tokeninfo(self):
    """Handler for accounts.ea.com/connect/tokeninfo"""
    if self.debug: print(request.headers.get("access_token"))

    access_token = request.headers.get('access_token')
    # If we don't have an access token, we are looking at an anonymous login
    if not access_token:
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
    
    # If this is the long lived token, response with details about that token
    if access_token == self.lnglv_token:
      return jsonify(
        {
          "client_id": "long_live_token",
          "scope": "basic.identity basic.persona",
          "expires_in": 5184000,      # 60 days (in seconds))
          "pid_id": "1020010147082",
          "pid_type": "NUCLEUS",
          "user_id": "1020010147082",
          "persona_id": None
        }
      )
    
    # If this is the access_token, respond to that
    if access_token == self.access_token:
      return jsonify(
        {
          "client_id": "simpsons4-ios-client",
          "scope": "offline basic.antelope.links.bulk openid signin antelope-rtm-readwrite search.identity basic.antelope basic.identity basic.persona antelope-inbox-readwrite",
          "expires_in": 43199,
          "pid_id": self.me_persona_pid_id,
          "pid_type": "AUTHENTICATOR_ANONYMOUS",
          "user_id": self.token_user_id,
          "persona_id": self.token_persona_id,
          "authenticators": [
              {
                  "authenticator_type": "AUTHENTICATOR_ANONYMOUS",
                  "authenticator_pid_id": self.token_authenticator_pid_id
              },
              {
                  "authenticator_type": "NUCLEUS",
                  "authenticator_pid_id": self.token_authenticator_pid_id + 1
              }
          ],
          "is_underage": false,
          "stopProcess": "OFF",
          "telemetry_id": self.token_telemetry_id
        }
      )
    
    # otherwise, just error out
    abort(403)

  def geoagerequirements(self):
    """Handler for accounts.ea.com/proxy/identity/geoagerequirements"""
    return jsonify(
      {
        "geoAgeRequirements": {
          "minLegalRegAge": 13,
          "minAgeWithConsent": "3",
          "minLegalContactAge": 13,
          "country": "US"             # TODO: make configurable
        }
      }
    )

  def probe(self):
    """Handler for accounts.ea.com/probe"""
    return ""

  # server: pn.tnt-ea.com

  def game_devices(self, game_id: str):
    """Handler for pn.tnt-ea.com/games/<game_id>/devices and 
       pn.tnt-ea.com/rest/v1/games/<game_id>/devices"""
    # Expect game_id to be 48302, but doesn't matter if it changes
    req_json = request.get_json()
    if not req_json:
      abort(500)

    if self.debug:
      print(f"Body: {req_json}")

    resp_json = {
      "deviceIdentifier": req_json.get("deviceIdentifier"),
      "userAlias": req_json.get("userAlias"),
      "appId": req_json.get("appId"),
      "deviceType": req_json.get("deviceType"),
      "operatingSystem": req_json.get("operatingSystem").lower(),
      "manufacturer": req_json.get("manufacturer"),
      "model": req_json.get("model"),
      "appVersion": req_json.get("appVersion"),
      "locale": req_json.get("locale"),
      "timezone": req_json.get("timezone"),
      "disabled": True if req_json.get("disabled") == "True" else False,
      "disableReason": req_json.get("disableReason"),
      "dateOfBirth": req_json.get("dateOfBirth"),
      "sandbox": True if req_json.get("") == "True" else False,  
      "silentIntervalStart": -1,
      "silentIntervalEnd": -1,
      "country": self.config.get("country"),
      "legacy": False
    }
    return jsonify(resp_json)

  # server river-mobile.data.ea.com

  def core_logEvent(self):
    """river-mobile.data.ea.com/tracking/api/core/logEvent"""
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

  # server: pin-river.data.ea.com

  def pinEvents(self):
    """Handler for pin-river.data.ea.com/pinEvents"""
    if self.debug: print(request.get_json())   # get_json handles gzip decompression automatically
    resp = '{"status": "ok"}'
    response = make_response(resp)
    response.headers['Content-Type'] = 'application/json'
    return response
   
  # server: prod.simpsons-ea.com

  def lobby_time(self):
    xml = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Time><epochMilliseconds>{int(round(time.time() * 1000))}</epochMilliseconds></Time>'
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

  def tracking_log(self):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/trackinglog/"""
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

  def protoClientConfig(self):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/protoClientConfig/"""
    if self.debug: print(f"id: {request.args.get('id')}")

    client_config = ClientConfigData_pb2.ClientConfigResponse()

    for entry in self.config.get("protoClientConfig"):
      item = client_config.items.add()
      item.clientConfigId = entry[0]
      item.name = entry[1]
      item.value = entry[2]

    # Generate the response object
    response = make_response(client_config.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response

  def gameplayconfig(self):
    """Handler for prod.simpsons-ea.com/mh/gameplayconfig"""

    # NOTE: if this returns an empty config, the app still loads.

    client_config = GameplayConfigData_pb2.GameplayConfigResponse()

    for config_item in self.config.get("gameplayconfig"):
      item = client_config.item.add()
      item.name = config_item[0]
      item.value = config_item[1]

    response = make_response(client_config.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response

  def mh_user(self):
    """Handler for prod.simpsons-ea.com/mh/users"""
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

  def userstats(self):
    """Handler for prod.simpsons-ea.com/mh/userstats"""
    if self.debug: 
      print(f"device_id: {request.args.get('device_id')}")
      print(f"synergy_id: {request.args.get('synergy_id')}")
    # This always returns 409 
    abort(409)

  def protoWholeLandToken(self, land_id):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/protoWholeLandToken/<land_id>/"""
    if self.debug:
      print(f"force: {request.args.get('force')}")

    req = WholeLandTokenData_pb2.WholeLandTokenRequest()
    req.ParseFromString(request.data)
    if self.debug: 
      print(f"\trequestId: {req.requestId}")

    data = WholeLandTokenData_pb2.WholeLandTokenResponse()
    data.token = self.land_token
    data.conflict = False
    
    response = make_response(data.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response
 
  def checkToken(self, token):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/checkToken/<token>/protoWholeLandToken/"""
    if self.debug: 
      print(f"\ttoken: {token}")

    data = AuthData_pb2.TokenData()
    data.sessionKey = self.session_key
    data.expirationDate = 0
    
    response = make_response(data.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response

  def trackingmetrics(self):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/trackingmetrics/"""
    
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

  def bg_gameserver_plugin_protoland(self, land_id: str):
    """Handler prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/protoland/<land_id>/"""
    if self.debug:
      print(f"\tland id: {land_id}")
      
    if request.method == 'GET':
      # Load town
      self.load_town()
      response = make_response(self.land_proto.SerializeToString())
      response.headers['Content-Type'] = 'application/x-protobuf'
      return response

    if request.method != "POST":
      abort(500)

    # Deserialize the current town state
    self.land_proto.ParseFromString(request.data)

    # Save town
    self.save_town()

    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><WholeLandUpdateResponse/>'
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response
 
  def protocurrency(self, land_id: str):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/protocurrency/<land_id>/"""
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
 
  def extraLandUpdate(self, land_id: str):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/extraLandUpdate/<land_id>/protoland/"""
    # TODO: process the incoming update
    req = LandData_pb2.ExtraLandMessage()
    req.ParseFromString(request.data)
    
    if self.debug or 1:
      print(req)
      """"
      if req.hasField("currencyDelta"): 
    
    message ExtraLandMessage {
      repeated .Data.ExtraLandMessage.CurrencyDelta currencyDelta = 1;
      repeated .Data.EventMessage event = 2;
      repeated .Data.ExtraLandMessage.PushNotification pushNotification = 3;
      repeated .Data.ExtraLandMessage.CommunityGoalDelta communityGoalDelta = 4;
      repeated .Data.ExtraLandMessage.MatchmakingRegistration matchmakingRegistration = 5;
      repeated .Data.PurchaseRequestMessage.DeviceIds deviceIds = 6;
      optional .Data.PurchaseRequestMessage.ApplicationInfo applicationInfo = 7;
      optional .Data.PurchaseRequestMessage.DeviceInfo deviceInfo = 8;
      message CurrencyDelta {
        optional int32 id = 1;
        optional string reason = 2;
        optional int32 amount = 3;
        optional int64 updatedAt = 4;
        optional string productId = 5;
      }
      message PushNotification {
        optional string id = 1;
        optional string toPlayerId = 2;
        optional int32 scheduledIn = 3;
        optional string templateName = 4;
        optional string message = 5;
      }
      message CommunityGoalDelta {
        optional string category = 1;
        optional int64 amount = 2;
      }
      message MatchmakingRegistration {
        optional string category = 1;
        repeated .Data.NameValue params = 2;
      }
    }
"""

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

  def plugin_event(self, land_id: str):
    """Handler for prod.simpsons-ea.com/mh/games/bg_gameserver_plugin/event/<land_id>/protoland/"""

    # TODO: figure out the use of this.
    event = LandData_pb2.EventsMessage()
    response = make_response(event.SerializeToString())
    response.headers['Content-Type'] = 'application/x-protobuf'
    return response


  # Generic default route handler

  def default_root(self):
    """Handler for default '/' routes"""
    if self.debug:
      print("/ called")
    return ""


def start_server():
  print("starting web server")
  server = TheSimpsonsTappedOutLocalServer(sys.argv[1])
  server.run()


if __name__ == "__main__":
  start_server()
