import base64
from dataclasses import dataclass, field
import datetime
import hashlib
import hmac
import random
from typing import Union

# pip install pyjwt
import jwt

@dataclass
class AuthCode:
  _type: str                  # e.g. "authorization_code"
  expiration: int             # Expiration timestamp (unix format)


@dataclass
class AccessToken:
  expiration: int             # Expiration timestamp (unix format)
  client_id: str = ""
  persona: "Persona" = None   # Persona set associated with token
  authenticators: list = field(default_factory=list)  # pid_id list 


@dataclass
class RefreshToken:
  expiration: int             # Expiration timestamp (unix format)
  client_id: str = ""
  persona: "Persona" = None   # Persona set associated with token


@dataclass
class IdToken:
  expiration: int             # Expiration timestamp (unix format)
  body: dict = field(default_factory=dict)  # Body of the token in dict form
  client_id: str = ""
  persona: "Persona" = None   # Persona set associated with token


@dataclass
class Authenticator:
  _type: str
  persona: "Persona"
  access_token: str
  expires_in: int
  access_token_expires: int
  refresh_token: str
  refresh_token_expires_in: int
  refresh_token_expires: int
  token_type: str = "Bearer"
  id_token: Union[str, None] = None

  def to_dict(self) -> dict:
    return {
      "type": self._type,
      "persona_id": self.persona.persona_id,
      "access_token": self.access_token,
      "expires_in": self.expires_in,
      "access_token_expires": self.access_token_expires,
      "refresh_token": self.refresh_token,
      "refresh_token_expires_in": self.refresh_token_expires_in,
      "refresh_token_expires": self.refresh_token_expires,
      "token_type": self.token_type,
      "id_token": self.id_token,
    }

@dataclass
class AccessProfile:
  client_id: str
  persona_id: int
  pid_id: int
  user_id: int
  authenticators: list = field(default_factory=list)
  
  
class AuthManager:

  def __init__(self, config: dict):
    self.config: dict = config

    self.debug: bool = self.config.get("debug", False)

    self.access_profiles: dict = {}     # the love profiles of access token
    self.auth_codes: dict = {}          # the authorization code
    self.auth_code_personas: dict = {}  # xref auth_code to persona
    self.access_tokens: dict = {}       # access tokens
    self.refresh_tokens: dict = {}      # maps refresh_token to persona set
    self.authenticators: dict = {}      # authenticator dictionaries
    self.id_tokens: dict = {}           # maps id_token to persona set
    self.persona_ids: dict = {}         # xref persona_id to access_token
    self.user_ids: dict = {}            # xref user_id to access_token
    self.pid_ids: dict = {}             # xref pid_id to access_token

    self.secret_key = self.config.get("secret_key")

  ##############################################################################
  # Utility functions
  ##############################################################################

  def log_debug(self, msg: str):
    if self.debug:
      print(msg)

  def now_int(self) -> int:
    """Returns the current time (UTC) as unix timestamp integer."""
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())

  def generate_counter_code(self, offset: int = 0) -> str:
    """Generates the base32hex-based timestamp string"""
    # Get the current timestamp plus any offset converted into minutes
    now: int = int(self.now_int() + offset) // 60

    # Encode the timestamp into a compressed Base32Hex format
    now_bin: str = bin(now)[2:]      # strip the leading "0b"
    
    alphabet = {
      "00000": "0", "00001": "1", "00010": "2", "00011": "3",
      "00100": "4", "00101": "5", "00110": "6", "00111": "7",
      "01000": "8", "01001": "9", "01010": "a", "01011": "b",
      "01100": "c", "01101": "d", "01110": "e", "01111": "f",
      "10000": "g", "10001": "h", "10010": "i", "10011": "j",
      "10100": "k", "10101": "l", "10110": "m", "10111": "n",
      "11000": "o", "11001": "p", "11010": "q", "11011": "r",
      "11100": "s", "11101": "t", "11110": "u", "11111": "v",
    }

    if len(now_bin) % 5:
      self.log_debug("generate_counter_code: invalid size: {now_bin}")
      return "00000"

    counter_code: str = ""
    for i in range(len(now_bin) // 5):
      sub_val = now_bin[i*5:(i+1)*5]
      if sub_val not in alphabet:
        self.log_debug("Invalid subvalue found: {sub_val}")
        return "00000"
      counter_code += alphabet[sub_val]

    # Return the result
    return counter_code

  def generate_random_bytes(self, length: int) -> bytes:
    """Generates a random sequence of bytes of length."""
    array = bytearray(length)
    for i in range(length):
      array[i] = random.randint(0,255)
    return array

  def b64encode_string(self, input_string: str) -> str:
    """Encode a string into a base64 encoded string without padding."""
    return base64.urlsafe_b64encode(
              input_string.encode("utf-8")
           ).decode("utf-8").replace("=", "")

  def b64encode_bytes(self, bytes_in: bytes) -> str:
    return base64.urlsafe_b64encode(bytes_in).decode("utf-8").replace("=", "")

  ##############################################################################
  # Code and Token Generation
  ##############################################################################
  def generate_access_code(self) -> str:
    """Generates a new acccess code."""
    access_code = self.generate_random_bytes(29)
    access_code[0:4] = b"AC\xA1\x00"    # prologue of the token
    access_code_str = self.b64encode_bytes(access_code)
    return access_code_str    

  def generate_access_token(self, id_base: int, expiry: int) -> str:
    """Generates an access token, returns token in Base64"""
    
    # An access token has the following format before being Base64 encoded:
    #
    #                                           id_base -------
    #                                                          v
    #  AT0:2.0:3.0:1440:KpnQGZO2SIxD0xKZEL9pBauVdBJYRO0NYD2:47082:riqac
    #  \_________/    ^        ^                                     ^
    #       ^         |        |                                     |
    #       |         |        |                        timestamp ---          
    #       |         |         --- token code (base64 encoded)
    #       |          ------ token life (in minutes)
    #        --- header ("AuthToken0")
    # 
    # The timestamp is a unix timestamp in minutes (// 60) stored in 
    # lowercase base32hex encoding
    #
    # The entire token is returned as a Base64 encoded string.

    # Build an access token
    timestamp = self.generate_counter_code()
    token_hash = self.b64encode_bytes(self.generate_random_bytes(26))
    access_token_body = f"AT0:2.0:3.0:{expiry}:{token_hash}:{id_base}:{timestamp}"
    access_token = self.b64encode_string(access_token_body)
    
    # Register the access_token
    self.access_tokens[access_token] = AccessToken(
                                          self.now_int() + (expiry * 60),
                                       )
    self.log_debug(f"Access token generated for {id_base}: {access_token_body}")
    self.log_debug(f"Access token is {access_token}")
    return access_token

  def generate_access_token_type1(self, id_base: int, expiry: int) -> str:
    """Generates an access token (type AT1), returns token in Base64"""
    
    # This is identical to generate_Access_token except it uses AT1 instead of
    # the AT0 type.

    # Build an access token
    timestamp = self.generate_counter_code()
    token_hash = self.b64encode_bytes(self.generate_random_bytes(26))
    access_token_body = f"AT1:2.0:3.0:{expiry}:{token_hash}:{id_base}:{timestamp}"
    access_token = self.b64encode_string(access_token_body)

    # Register the access_token
    self.access_tokens[access_token] = AccessToken(
                                          self.now_int() + (expiry * 60),
                                       )

    self.log_debug(f"Access token generated for {id_base}: {access_token_body}")
    self.log_debug(f"Access token is {access_token}")
    return access_token

  def generate_refresh_token(self, id_base: int, expiry: int) -> str:
    """Generates an refresh token, returns token in Base64"""

    # A refresh token has the following format before being Base64 encoded, a
    # format that is nearly identical to the access token format:
    #
    #                                           id_base -------
    #                                                          v
    #  RT0:2.0:3.0:1440:KpnQGZO2SIxD0xKZEL9pBauVdBJYRO0NYD2:47082:riqac
    #  \_________/    ^        ^                                     ^
    #       ^         |        |                                     |
    #       |         |        |                        timestamp ---          
    #       |         |         --- token code (base64 encoded)
    #       |          ------ token life (in minutes)
    #        --- header ("RefreshToken0")
    # 
    # The timestamp is a unix timestamp in minutes (// 60) stored in 
    # lowercase base32hex encoding
    #
    # The entire token is returned as a Base64 encoded string.    

    # Build a refresh token
    timestamp = self.generate_counter_code()
    token_hash = self.b64encode_bytes(self.generate_random_bytes(26))
    refresh_token_body = f"RT0:2.0:3.0:{expiry}:{token_hash}:{id_base}:{timestamp}"
    refresh_token = self.b64encode_string(refresh_token_body)

    # Register refresh_token
    self.refresh_tokens[refresh_token] = RefreshToken(
                                            self.now_int() + (expiry * 60),
                                         )

    self.log_debug(f"Refresh tkn generated for {id_base}: {refresh_token_body}")
    self.log_debug(f"Refresh token is {refresh_token}")
    return refresh_token

  def generate_id_token(self, persona_id: int, expiry: int) -> str:
    """Generates a signed id token"""

    # Find the persona by its id
    persona = self.user_manager.personas.get(persona_id)
    if not persona:
      return ""

    now = self.now_int()
    expiration = expiry + now

    id_token_body_json = {
          "aud": persona.client_id,
          "iss": "accounts.ea.com",
          "iat": now,
          "exp": expiration,
          "pid_id": str(persona.pid_id),
          "user_id": str(persona.user_id),
          "persona_id": persona.persona_id,
          "pid_type":"AUTHENTICATOR_ANONYMOUS",
          "auth_time": 0
        }
 
    id_token_body = jwt.encode(
                        id_token_body_json,
                        self.secret_key,
                        algorithm = "HS256"
                    )

    id_token_sig = base64.b64encode(
                     hmac.new(
                        self.secret_key.encode("utf-8"),
                        id_token_body.encode("utf-8"),
                        hashlib.sha256
                     ).digest()
                   ).decode("utf-8")

    id_token = f"{id_token_body}.{id_token_sig}"

    # Register the id_token 
    self.id_tokens[id_token] = IdToken(
                                  expiration,
                                  id_token_body_json,
                                  persona.client_id,
                                  persona
                               )

    self.log_debug(f"Id token generated for {persona_id}: {id_token_body_json}")
    self.log_debug(f"Id token is {id_token}")
    self.log_debug(f"{self.id_tokens[id_token]}")
    return id_token

  ##############################################################################
  # Code management
  ##############################################################################

  def new_authorization_code(self, code_type: str, lifetime: int = 600) -> str:
    """Generates a new authorization code."""
    # Generate a new code
    auth_code = self.generate_access_code()
    
    # Add the code the list of generated codes
    self.auth_codes[auth_code] = AuthCode(
                                    code_type,
                                    self.now_int() + lifetime
                                 )

    # Perform housekeeping on the auth codes
    self.remove_expired_authorization_codes()
    
    self.log_debug(f"New auth code: {auth_code}")
    # return the code
    return auth_code

  def is_valid_authorization_code(self, code: str) -> bool:
    """Returns True if code is in .auth_code and not expired."""
    info = self.auth_codes.get(code)
    if not info:
      self.log_debug(f"auth code {code} is unknown.")
      return False
    if info.expiration < self.now_int():
      self.log_debug(f"auth code {code} is expired.")
      return False

    self.log_debug(f"auth code {code} is valid.")
    return True

  def remove_expired_authorization_codes(self):
    """Clears any expired auth codes from .auth_codes"""
    code_list = [ac for ac in self.auth_codes.keys()]
    now = self.now_int()
    for ac in code_list:
      if self.auth_codes[ac].expiration < now:
        del self.auth_codes[ac]
        self.log_debug(f"auth code {ac} is expired and deleted.")
        if ac in self.auth_code_personas:
          del self.auth_code_personas[ac]
          self.log_debug(f"auth code {ac} removed from persona xref")

  ##############################################################################
  # Token management
  ##############################################################################

  def register_access_token_persona(self, access_token: str, persona: dict):
    """Registers the persona with the access_token"""
    if access_token not in self.access_tokens:
      self.log_debug(f"Unable to find access token {access_token}.")
      return

    self.access_tokens[access_token].persona = persona
    self.log_debug(f"{persona} registered to access token {access_token}")
 
  def register_refresh_token_persona(self, refresh_token: str, persona: dict):
    """Registers the persona with the refresh_token"""
    if refresh_token not in self.refresh_tokens:
      self.log_debug(f"Unable to find refresh token {refresh_token}.")
      return

    self.refresh_tokens[refresh_token].persona = persona
    self.log_debug(f"{persona} registered to refresh token {refresh_token}")

  def register_authenticator_to_access_token(self, 
                                              access_token: str, 
                                              pid_id: int
                                            ) -> bool:
    """Registers the authentication pid with the access token"""
    if access_token not in self.access_tokens:
      self.log_debug(f"Unable to find access token {access_token}.")
      return False

    self.access_tokens[access_token].authenticators.append(pid_id)
    self.log_debug(f"Authenicator {pid_id} registered to access token {access_token}")
    self.log_debug(self.access_tokens[access_token])
    return True

  def is_access_token_valid(self, access_token: str) -> bool:
    """Returns true if token is still valid"""
    # First remove any expired tokens
    self.remove_expired_access_tokens()
    
    # Next, see if our token still exists
    if not self.access_tokens.get(access_token):
      self.log_debug(f"Access token {access_token} does not exist, invalid")
      return False
    # Consider the access token valid
    self.log_debug(f"Access token {access_token} is valid")
    return True

  def remove_expired_access_tokens(self):
    """Removes any access token which has expired"""
    now = self.now_int()
    token_list = [acttok for acttok in self.access_tokens.keys()]
    for access_token in token_list:
      token_info = self.access_tokens.get(access_token)
      if not token_info:
        continue
      if token_info.expiration < now:
        del self.access_tokens[access_token]
        self.log_debug(f"Access token {access_token} expired and was deleted")
      
  def new_lnglv_token(self, username: str, client_id: str, auth_code: str) -> str:
    """Generate a new longlive token from login info"""
    # Find the user's persona set
    persona_set = self.user_manager.get_user_persona(username)
    if not persona_set:
      # Unknown user, so register one.
      persona_set = self.user_manager.register_new_user(username)
    if not persona_set:
      return ""
    
    # Generate the access token (this so registers the token)
    lnglv_token = self.generate_access_token_type1(persona_set.base_id, 
                                                   86400    # 60 days
                                                  )
    # Attach the persona to the token
    self.register_access_token_persona(lnglv_token, persona_set)
    
    # Attach the access code to the person 
    if auth_code:
      self.auth_code_personas[auth_code] = persona_set

    # return the token
    self.log_debug(f"New lnglv token generated: {lnglv_token}")
    return lnglv_token

  def is_lnglv_token(self, access_token: str) -> bool:
    """Returns true if the token is a valid lnglv token"""
    # Check validity of token first
    if not self.is_access_token_valid(access_token):
      self.log_debug(f"Access token {access_token} not found.")
      return False
    
    # Check if the token is a lnglv_token
    access_token_info = self.access_tokens.get(access_token)
    if not access_token_info:
      self.log_debug(f"Access token {access_token} not found (2).")
      return False
    if access_token_info.client_id != "lnglv_token":
      self.log_debug(f"Access token {access_token} is not a lnglv_token")
      self.log_debug(f"The token belongs to {access_token_info.client_id}")
      return False
    
    self.log_debug(f"Access token {access_token} is not a lnglv_token")
    return True

  ##############################################################################
  # Authenticator management
  ##############################################################################

  def new_authenticator(self, 
                        authenticator_type: str,
                        client_id: str
                       ) -> dict:
    """Generates a new authenticator type"""

    if authenticator_type not in ["AUTHENTICATOR_ANONYMOUS", "NUCLEUS"]:
      return {}

    # Generate a persona set for the authenticator
    persona_set = self.user_manager.generate_persona_id_set(
                                        authenticator_type,
                                        client_id = client_id
                                    )

    # Build the access and refresh tokens, register persona with each
    access_token = self.generate_access_token(persona_set.id_base, 720)
    self.access_tokens[access_token].client_id = client_id
    self.register_access_token_persona(access_token, persona_set)
    refresh_token = self.generate_refresh_token(persona_set.id_base, 1440)
    self.refresh_tokens[refresh_token].client_id = client_id
    self.register_refresh_token_persona(refresh_token, persona_set)

    # Authenicators are referenced primarily by the pid_id
    pid_id = persona_set.pid_id

    # Construct the authenticator
    now = self.now_int()
    authenticator = Authenticator(
                      authenticator_type,
                      persona_set,
                      access_token,
                      43200,
                      now + 43200,
                      refresh_token,
                      86400,
                      now + 86400,
                      "Bearer"
                    )

    # anonymous authenticators have the id_token
    if authenticator_type == "AUTHENTICATOR_ANONYMOUS":
      id_token = self.generate_id_token(persona_set.persona_id, 3600)
      authenticator.id_token = id_token

    # Add the authenticator to the list of authenticators
    self.authenticators[pid_id] = authenticator

    # Return the pid of the authenticator
    self.log_debug(f"New authenticator generated: {authenticator}")
    return authenticator

  def get_authenticator(self, pid_id: int) -> Authenticator:
    """Returns the type of authenticator for the pid or empty if not found."""
    if pid_id not in self.authenticators:
      self.log_debug(f"Authenticator {pid_id} is unknown/not found")
      return None
    return self.authenticators[pid_id]

  def get_access_token_profile(self, access_token: str) -> dict:
    """Returns details of the access token"""
    # Validate access token
    if not self.is_access_token_valid(access_token):
      self.log_debug(f"{access_token} not found")
      return {}

    # Get the person associated with the token
    token_details = self.access_tokens.get(access_token)
    if not token_details:
      self.log_debug(f"Failed to retrieve details of {access_token}")
      return {}

    persona = token_details.persona
    if not persona:
      self.log_debug(f"No persona attached to {access_token}")
      return {}
  
    expiration = token_details.expiration
    time_remaining = expiration - self.now_int()
    
    access_token_details = {
      "client_id": token_details.client_id,
      "expires_in": time_remaining,
      "persona_id": persona.persona_id,
      "pid_id": str(persona.pid_id),
      "pid_type": persona._type,
      "user_id": str(persona.user_id),
      "authenticators": []
    }
    
    for pid_id in token_details.authenticators:
      authenticator = self.get_authenticator(pid_id)
      if authenticator:
        access_token_details["authenticators"].append(authenticator.to_dict())

    self.log_debug(f"Access token {access_token}: {access_token_details}")
    return access_token_details

