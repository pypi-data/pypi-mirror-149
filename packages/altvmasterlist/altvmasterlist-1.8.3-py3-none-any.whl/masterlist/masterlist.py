#!/usr/bin/env python3
from urllib3 import PoolManager, exceptions
import json

pool = PoolManager()

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
        if (self.useCdn == False):
            print("[alt:V] This Server is not using a CDN.")
            return json.dumps({})
        else:
            return request(self.cdnUrl + "/connect.json")

def request(url):
    try:
        request = pool.request('GET', url, preload_content=False, headers={
            "User-Agent": "AltPublicAgent"
        })
        try:
            apijson = json.loads(request.data)
        except json.decoder.JSONDecodeError:
            apijson = json.dumps({})
        request.release_conn()
    except exceptions.MaxRetryError:
        apijson = json.dumps({})
    return apijson

def get_server_stats():
    return request(config.all_server_stats_link)

def get_servers():
    return_servers = []
    servers = request(config.all_servers_link)
    if (servers == "{}"):
        return []
    for server in servers:
        temp_server = Server("unknown", server["id"], server["maxPlayers"], server["players"], server["name"], server["locked"], server["host"], server["port"], server["gameMode"], server["website"], server["language"], server["description"], server["verified"], server["promoted"], server["useEarlyAuth"], server["earlyAuthUrl"], server["useCdn"], server["cdnUrl"], server["useVoiceChat"], server["tags"], server["bannerUrl"], server["branch"], server["build"], server["version"], server["lastUpdate"])
        return_servers.append(temp_server)
        
    return return_servers

def get_server_by_id(id):
    temp_data = request(config.server_link.format(id))
    if (temp_data == {}):
        return False
    else:
        if (temp_data["active"] == False):
            return_server = Server(temp_data["active"], id, 0, 0, "", False, "0.0.0.0", 7788, "", "", "", "", False, False, False, "", False, "", False, [], "", "release", -1, 0.0, 0)
        else:
            return_server = Server(temp_data["active"], id, temp_data["info"]["maxPlayers"], temp_data["info"]["players"], temp_data["info"]["name"], temp_data["info"]["locked"], temp_data["info"]["host"], temp_data["info"]["port"], temp_data["info"]["gameMode"], temp_data["info"]["website"], temp_data["info"]["language"], temp_data["info"]["description"], temp_data["info"]["verified"], temp_data["info"]["promoted"], temp_data["info"]["useEarlyAuth"], temp_data["info"]["earlyAuthUrl"], temp_data["info"]["useCdn"], temp_data["info"]["cdnUrl"], temp_data["info"]["useVoiceChat"], temp_data["info"]["tags"], temp_data["info"]["bannerUrl"], temp_data["info"]["branch"], temp_data["info"]["build"], temp_data["info"]["version"], temp_data["info"]["lastUpdate"])
        return return_server

def get_server_by_id_avg(id, time):
    return request(config.server_average_link.format(id, time))

def get_server_by_id_avg_result(id, time):
    response = get_server_by_id_avg(id, time)
    players_all = 0
    for entry in response:
        players_all = players_all + entry["c"]
    result = players_all / len(response)
    return round(result)

def get_server_by_id_max(id, time):
    return request(config.server_max_link.format(id, time))

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