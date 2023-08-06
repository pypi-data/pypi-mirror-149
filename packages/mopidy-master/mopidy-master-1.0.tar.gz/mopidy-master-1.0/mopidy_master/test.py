from websocket import create_connection
import json
def uri_to_master(uri):
        params = uri.split(':')
        params.pop(0)
        params.pop(0)
        uri = ":".join(params)
        return uri

print(uri_to_master('mopidymopidy:track:yandexmusic:track:23602860'))

payload = {
  "method": "core.playback.get_time_position",
  "jsonrpc": "2.0",
  "params":{},
          "id": 0
}
ws = create_connection("ws://192.168.2.238:6680/master/socketapi/ws")
#ws = create_connection("ws://192.168.2.109:6680/mopidy/ws")
ws.send(json.dumps({'message':'list'}))
#ws.send(json.dumps(payload))
print(ws.recv())



