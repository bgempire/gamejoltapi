from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
import hashlib

from ast import literal_eval
from collections import OrderedDict
from pprint import pprint, pformat

_DEBUG = False
API_URL = "https://api.gamejolt.com/api/game/v1_2"
RETURN_FORMATS = ["json", "keypair", "dump", "xml"]
HTTP_METHODS = ["GET", "POST"]

class GameJoltDataRequired(Exception):
    def __init__(self, key):
        self.key = key
        self.message = "Value is required, cannot be None: " + repr(key)
        super().__init__(self.message)

class GameJoltAPI:
    def __init__(self, gameId, privateKey, username=None, userToken=None, responseFormat="json", submitRequests=True):
        self.gameId = str(gameId)
        self.privateKey = privateKey
        self.username = username
        self.userToken = userToken
        self.responseFormat = responseFormat if responseFormat in RETURN_FORMATS else "json"
        self.submitRequests = submitRequests
        self.operations = {
            "users/fetch" : API_URL + "/users/" + "?",
            "users/auth" : API_URL + "/users/auth/" + "?",
            "sessions/open" : API_URL + "/sessions/open/" + "?",
            "sessions/ping" : API_URL + "/sessions/ping/" + "?",
            "sessions/check" : API_URL + "/sessions/check/" + "?",
            "sessions/close" : API_URL + "/sessions/close/" + "?",
            "scores/fetch" : API_URL + "/scores/" + "?",
            "scores/tables" : API_URL + "/scores/tables/" + "?",
            "scores/add" : API_URL + "/scores/add/" + "?",
            "scores/get-rank" : API_URL + "/scores/get-rank/" + "?",
            "trophies/fetch" : API_URL + "/trophies/" + "?",
            "trophies/add-achieved" : API_URL + "/trophies/add-achieved/" + "?",
            "trophies/remove-achieved" : API_URL + "/trophies/remove-achieved/" + "?",
            "data-store/set" : API_URL + "/data-store/set/" + "?",
            "data-store/update" : API_URL + "/data-store/update/" + "?",
            "data-store/remove" : API_URL + "/data-store/remove/" + "?",
            "data-store/fetch" : API_URL + "/data-store/" + "?",
            "data-store/get-keys" : API_URL + "/data-store/get-keys/" + "?",
            "friends" : API_URL + "/friends/" + "?",
            "time" : API_URL + "/time/" + "?",
            "batch" : API_URL + "/batch/" + "?",
        }
        
    def _submit(self, operationUrl, data):
        orderedData = OrderedDict()
        isBatch = "batch" in operationUrl
        
        if not self.submitRequests and "format" in data.keys():
            data.pop("format")
        
        for key in sorted(data.keys()):
            orderedData[key] = data[key]
        data = orderedData
        
        requestUrls = data.pop("requests") if isBatch else []
        requestAsParams = "&".join(["requests[]=" + url for url in requestUrls]) if isBatch else ""
            
        urlParams = urlencode(data)
        urlParams += "&" + requestAsParams if isBatch else ""
        urlToSignature = operationUrl + urlParams + self.privateKey
        signature = hashlib.md5(urlToSignature.encode()).hexdigest()
        finalUrl = operationUrl + urlParams + "&signature=" + signature
        
        if self.submitRequests:
            if _DEBUG: print("Requesting URL:", finalUrl)
            response = urlopen(finalUrl).read().decode()
            
            if self.responseFormat == "json":
                return literal_eval(response)["response"]
            else:
                return response
        else:
            if _DEBUG: print("Generated URL:", finalUrl)
            return finalUrl

    def _validateRequiredData(self, data):
        for key in data.keys():
            if data[key] is None:
                raise GameJoltDataRequired(key)
        return True
        
    def _getValidData(self, data):
        validatedData = {}
        if self.responseFormat != "json":
            validatedData["format"] = self.responseFormat
        
        for key in data.keys():
            if data[key] is not None:
                validatedData[key] = data[key]
        return validatedData
    
    def _processBoolean(self, value):
        if value is not None:
            return str(value).lower()
    
    # Users
    def usersFetch(self, gameId=None, username=None, userId=None):
        """Returns a user's data."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId
        }
            
        if username is not None: 
            data["username"] = username
            
        elif userId is not None: 
            data["user_id"] = userId
        
        else:
            data["username"] = self.username
        
        self._validateRequiredData(data)
        return self._submit(self.operations["users/fetch"], data)
        
    def usersAuth(self, gameId=None, username=None, userToken=None):
        """Authenticates the user's information. This should be done before you make 
        any calls for the user, to make sure the user's credentials (username and 
        token) are valid."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["users/auth"], data)
    
    # Sessions
    def sessionsOpen(self, gameId=None, username=None, userToken=None):
        """Opens a game session for a particular user and allows you to tell Game Jolt 
        that a user is playing your game. You must ping the session to keep it active 
        and you must close it when you're done with it."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/open"], data)
        
    def sessionsPing(self, gameId=None, username=None, userToken=None, status=None):
        """Pings an open session to tell the system that it's still active. If the session 
        hasn't been pinged within 120 seconds, the system will close the session and you 
        will have to open another one. It's recommended that you ping about every 30 
        seconds or so to keep the system from clearing out your session.
        
        You can also let the system know whether the player is in an active or idle state 
        within your game."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Optional data
        optionalData = {
            "status" : status # active or idle
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["sessions/ping"], data)
    
    def sessionsCheck(self, gameId=None, username=None, userToken=None):
        """Checks to see if there is an open session for the user. Can be used to see 
        if a particular user account is active in the game."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/check"], data)
        
    def sessionsClose(self, gameId=None, username=None, userToken=None):
        """Closes the active session."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["sessions/close"], data)
        
    # Scores
    def scoresFetch(self, gameId=None, username=None, userToken=None, limit=None, tableId=None, guest=None, betterThan=None, worseThan=None):
        """Returns a list of scores either for a user or globally for a game."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken,
            "limit" : limit,
            "table_id" : tableId,
            "guest" : guest,
            "better_than" : betterThan,
            "worse_than" : worseThan,
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["scores/fetch"], data)
        
    def scoresTables(self, gameId=None):
        """Returns a list of high score tables for a game."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["scores/tables"], data)
        
    def scoresAdd(self, score, sort, gameId=None, username=None, userToken=None, tableId=None, guest=None, extraData=None):
        """Adds a score for a user or guest. """
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "score" : score,
            "sort" : sort
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken,
            "table_id" : tableId,
            "guest" : guest,
            "extra_data" : extraData,
        }
        
        # Add guest score if guest is provided
        if optionalData["guest"] is not None:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["scores/add"], data)
        
    def scoresGetRank(self, sort, gameId=None, tableId=None):
        """Returns the rank of a particular score on a score table."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "sort" : sort
        }
        
        # Optional data
        optionalData = {
            "table_id" : tableId,
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        return self._submit(self.operations["scores/get-rank"], data)
        
    # Trophies
    def trophiesFetch(self, achieved=None, trophyId=None, gameId=None, username=None, userToken=None):
        """Returns one trophy or multiple trophies, depending on the parameters passed in."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Optional data
        optionalData = {
            "achieved" : self._processBoolean(achieved),
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["trophies/fetch"], data)
        
    def trophiesAddAchieved(self, trophyId, gameId=None, username=None, userToken=None):
        """Sets a trophy as achieved for a particular user."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken,
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["trophies/add-achieved"], data)
        
    def trophiesRemoveAchieved(self, trophyId, gameId=None, username=None, userToken=None):
        """Remove a previously achieved trophy for a particular user."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken,
            "trophy_id" : trophyId
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["trophies/remove-achieved"], data)
    
    # Data Storage
    def dataStoreSet(self, key, data, gameId=None, username=None, userToken=None, globalData=False):
        """Sets data in the data store."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "key" : key,
            "data" : data
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/set"], data)
        
    def dataStoreUpdate(self, key, operation, value, gameId=None, username=None, userToken=None, globalData=False):
        """Updates data in the data store."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "key" : key,
            "operation" : operation,
            "value" : value
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/update"], data)
        
    def dataStoreRemove(self, key, gameId=None, username=None, userToken=None, globalData=False):
        """Removes data from the data store."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "key" : key
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/remove"], data)
        
    def dataStoreFetch(self, key, gameId=None, username=None, userToken=None, globalData=False):
        """Returns data from the data store."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "key" : key
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/fetch"], data)
        
    def dataStoreGetKeys(self, pattern, gameId=None, username=None, userToken=None, globalData=False):
        """Returns either all the keys in the game's global data store, 
        or all the keys in a user's data store."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "pattern" : pattern
        }
        
        # Optional data
        optionalData = {
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        # Process global data instead of user data
        if globalData:
            optionalData["username"] = None
            optionalData["user_token"] = None
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["data-store/get-keys"], data)
        
    # Friends
    def friends(self, gameId=None, username=None, userToken=None):
        """Returns the list of a user's friends."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "username" : username if username is not None else self.username,
            "user_token" : userToken if userToken is not None else self.userToken
        }
        
        self._validateRequiredData(data)
        
        return self._submit(self.operations["friends"], data)
    
    # Time
    def time(self, gameId=None):
        """Returns the time of the Game Jolt server."""
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId
        }
        
        self._validateRequiredData(data)
        return self._submit(self.operations["time"], data)
    
    # Batch Calls
    def batch(self, gameId=None, requests=[], parallel=None, breakOnError=None):
        """A batch request is a collection of sub-requests that enables developers to 
        send multiple API calls with one HTTP request. """
        
        for i in range(len(requests)):
            requests[i] = requests[i].replace(API_URL, "")
            requests[i] = requests[i].split("&signature=")[0]
            requests[i] += "&signature=" + hashlib.md5((requests[i] + self.privateKey).encode()).hexdigest()
            requests[i] = quote(requests[i].replace(API_URL, ""), safe="")
        
        # Required data
        data = {
            "game_id" : gameId if gameId is not None else self.gameId,
            "requests" : requests if len(requests) > 0 else None
        }
        
        # Optional data
        optionalData = {
            "parallel" : self._processBoolean(parallel),
            "break_on_error" : self._processBoolean(breakOnError)
        }
        
        self._validateRequiredData(data)
        data.update(self._getValidData(optionalData))
        
        return self._submit(self.operations["batch"], data)