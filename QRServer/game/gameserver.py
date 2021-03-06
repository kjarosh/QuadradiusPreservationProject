from threading import Lock

from QRServer.common.classes import MatchId, Match
from QRServer.game.gameclient import GameClientHandler


class GameServer:
    matches: dict[MatchId, Match]
    _lock: Lock

    def __init__(self):
        self._lock = Lock()
        self.matches = {}

    def register_client(self, client_handler: GameClientHandler):
        match_id = client_handler.match_id()
        with self._lock:
            if match_id not in self.matches:
                self.matches[match_id] = Match(match_id)

            self.matches[match_id].add_party(client_handler)

    def get_player_count(self, match_id: MatchId):
        if match_id in self.matches:
            return len(self.matches[match_id].parties)
        return 0

    def remove_client(self, client):
        match_id = client.match_id()
        with self._lock:
            if match_id in self.matches:
                match = self.matches[match_id]
                try:
                    match.remove_party(client)
                    if match.empty():
                        del self.matches[match_id]
                except Exception:
                    pass
                # TODO possibly should tell the other player that opponent left
