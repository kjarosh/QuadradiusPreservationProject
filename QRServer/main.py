import socket
from multiprocessing import Process
from threading import Thread

from config import Config
from lobby import LobbyClient
from QRServer import lg

# TODO
# what server needs to store:
# list of people in lobby right now
# list of people who were online recently (like last one or smth)
# ranking for the month(s), retrieved by client based on date


def lobby_listener(conn_host, conn_port):
    gm_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gm_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    gm_s.bind((conn_host, conn_port))
    gm_s.listen(5)

    while True:
        (clientsocket, address) = gm_s.accept()
        ct = Thread(target=LobbyClient, args=(clientsocket, ))
        ct.run()


if __name__ == '__main__':
    lg.info('Server starting')
    lobby_process = Process(target=lobby_listener, args=(Config.HOST, Config.LOBBY_PORT,))
    lobby_process.start()

    # game_process = Process(target=game_listener, args=(Config.HOST, Config.GAME_PORT, game_handler))
    # game_process.start()

    lobby_process.join()
    # game_process.join()
