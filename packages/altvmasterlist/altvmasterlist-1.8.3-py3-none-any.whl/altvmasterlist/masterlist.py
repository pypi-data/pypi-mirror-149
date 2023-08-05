#!/usr/bin/env python3

class config:
    base_link = "https://api.altv.mp"
    all_server_stats_link = "{}/servers".format(base_link)
    all_servers_link = "{}/servers/list".format(base_link)
    server_link = "{}/server".format(base_link) + "/{}"
    server_average_link = "{}/avg".format(base_link) + "/{}/{}"
    server_max_link = "{}/max".format(base_link) + "/{}/{}"

class Server:
    def __init__(self, active, id, maxPlayers, players, name, locked, host, port, gameMode, website, language, description, verified, promoted, useEarlyAuth, earlyAuthUrl, useCdn, cdnUrl, useVoiceChat, tags, bannerUrl, branch, build, version, lastUpdate):
        self.active = active
        self.id = id
        self.maxPlayers = maxPlayers
        self.players = players
        self.name = name
        self.locked = locked
        self.host = host
        self.port = port
        self.gameMode = gameMode
        self.website = website
        self.language = language
        self.description = description
        self.verified = verified
        self.promoted = promoted
        self.useEarlyAuth = useEarlyAuth
        self.earlyAuthUrl = earlyAuthUrl
        self.useCdn = useCdn
        self.cdnUrl = cdnUrl
        self.useVoiceChat = useVoiceChat
        self.tags = tags
        self.bannerUrl = bannerUrl
        self.branch = branch
        self.build = build
        self.version = version
        self.lastUpdate = lastUpdate

    def get_json(self):
        return {
            "active": self.active,
            "id": self.id,
            "maxPlayers": self.maxPlayers,
            "players": self.players,
            "name": self.name,
            "locked": self.locked,
            "host": self.host,
            "port": self.port,
            "gameMode": self.gameMode,
            "website": self.website,
            "language": self.language,
            "description": self.description,
            "verified": self.verified,
            "promoted": self.promoted,
            "useEarlyAuth": self.useEarlyAuth,
            "earlyAuthUrl": self.earlyAuthUrl,
            "useCdn": self.useCdn,
            "cdnUrl": self.cdnUrl,
            "useVoiceChat": self.useVoiceChat,
            "tags": self.tags,
            "bannerUrl": self.bannerUrl,
            "branch": self.branch,
            "build": self.build,
            "version": self.version,
            "lastUpdate": self.lastUpdate
        }

    def update(self):
        temp_server = get_server_by_id(self.id)
        if (temp_server != False):
            self.active = temp_server.active
            self.id = self.id
            self.maxPlayers = temp_server.maxPlayers
            self.players = temp_server.players
            self.name = temp_server.name
            self.locked = temp_server.locked
            self.host = temp_server.host
            self.port = temp_server.port
            self.gameMode = temp_server.gameMode
            self.website = temp_server.website
            self.language = temp_server.language
            self.description = temp_server.description
            self.verified = temp_server.verified
            self.promoted = temp_server.promoted
            self.useEarlyAuth = temp_server.useEarlyAuth
            self.earlyAuthUrl = temp_server.earlyAuthUrl
            self.useCdn = temp_server.useCdn
            self.cdnUrl = temp_server.cdnUrl
            self.useVoiceChat = temp_server.useVoiceChat
            self.tags = temp_server.tags
            self.bannerUrl = temp_server.bannerUrl
            self.branch = temp_server.branch
            self.build = temp_server.build
            self.version = temp_server.version
            self.lastUpdate = temp_server.lastUpdate

    def fetchconnectjson(self):
        from json import dumps
        if (self.useCdn == False):
            raise Exception("[alt:V] This Server is not using a CDN.")
        else:
            try:
                return request(self.cdnUrl + "/connect.json")
            except:
                raise Exception("Couldn`t get server CDN")

def request(url):
    from requests import get, exceptions
    from json import dumps, loads, decoder
    try:
        request = get(url, headers={
            "User-Agent": "AltPublicAgent"
        })
        try:
            return loads(request.content.decode("utf-8"))
        except decoder.JSONDecodeError:
            raise Exception("JSON Couldn`t be parsed") 
        del request
    except exceptions.RetryError():
        raise Exception("Couldn`t make request") 

def get_server_stats():
    try :
        return request(config.all_server_stats_link)
    except:
        raise Exception("Couldn`t get Server stats") 
    

def get_servers():
    return_servers = []
    try:
        servers = request(config.all_servers_link)
    except:
        raise Exception("Couldn`t get Servers") 
    
    if (servers == "{}"):
        return []
    for server in servers:
        temp_server = Server("unknown", server["id"], server["maxPlayers"], server["players"], server["name"], server["locked"], server["host"], server["port"], server["gameMode"], server["website"], server["language"], server["description"], server["verified"], server["promoted"], server["useEarlyAuth"], server["earlyAuthUrl"], server["useCdn"], server["cdnUrl"], server["useVoiceChat"], server["tags"], server["bannerUrl"], server["branch"], server["build"], server["version"], server["lastUpdate"])
        return_servers.append(temp_server)
        
    return return_servers

def get_server_by_id(id):
    try:
        temp_data = request(config.server_link.format(id))
    except:
        raise Exception("Couldn`t get server data") 
    
    if (temp_data == {}):
        return False
    else:
        if (temp_data["active"] == False):
            return_server = Server(False, id, 0, 0, "", False, "0.0.0.0", 7788, "", "", "", "", False, False, False, "", False, "", False, [], "", "release", -1, 0.0, 0)
        else:
            return_server = Server(temp_data["active"], id, temp_data["info"]["maxPlayers"], temp_data["info"]["players"], temp_data["info"]["name"], temp_data["info"]["locked"], temp_data["info"]["host"], temp_data["info"]["port"], temp_data["info"]["gameMode"], temp_data["info"]["website"], temp_data["info"]["language"], temp_data["info"]["description"], temp_data["info"]["verified"], temp_data["info"]["promoted"], temp_data["info"]["useEarlyAuth"], temp_data["info"]["earlyAuthUrl"], temp_data["info"]["useCdn"], temp_data["info"]["cdnUrl"], temp_data["info"]["useVoiceChat"], temp_data["info"]["tags"], temp_data["info"]["bannerUrl"], temp_data["info"]["branch"], temp_data["info"]["build"], temp_data["info"]["version"], temp_data["info"]["lastUpdate"])
        return return_server

def get_server_by_id_avg(id, time):
    try:
        return request(config.server_average_link.format(id, time))
    except:
        raise Exception("Couln`t get server data")
    

def get_server_by_id_avg_result(id, time):
    try:
        response = get_server_by_id_avg(id, time)
    except:
        raise Exception("Couln`t get server data")
    players_all = 0
    for entry in response:
        players_all = players_all + entry["c"]
    result = players_all / len(response)
    return round(result)

def get_server_by_id_max(id, time):
    try:
        return request(config.server_max_link.format(id, time))
    except:
        raise Exception("Couln`t get server data")

def validate_id(id):
    from re import compile
    regexraw = r"^[0-9a-zA-Z]{32}$"
    regex = compile(regexraw)
    result = regex.match(id)
    if (result != None):
        return True
    else:
        return False

if __name__ == "__main__":
    exit()