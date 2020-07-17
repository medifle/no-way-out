import sys
import socket
from _thread import *
from no_way_out_game import NoWayOutGame, ENCODING


class Server(object):
    """ Simple socket server that listens to one single client. """

    def __init__(self, host="0.0.0.0", port=8888):
        """ Initialize the server with a host and port to listens to. """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
        self.host = host
        self.port = port
        try:
            self.socket.bind((host, port))
            print("Socket bind complete")
        except socket.error as err:
            print('Bind failed. Error Code : ' +
                  str(err[0]) + ' Message ' + err[1])
            sys.exit(-1)

        self.socket.listen(10)
        print('Socket now listening')

    def close(self):
        """ Close the server socket. """
        print("Closing server socket (host: %s, port %s)" %
              (self.host, self.port))
        if self.socket:
            self.socket.close()
            self.socket = None

    def run_server(self):
        """ Accept and handle an incoming connection. """
        print("Starting socket server (host %s, port %s)" %
              (self.host, self.port))
        # wait to accept a connection - blocking call
        while True:
            client_socket, client_address = self.socket.accept()
            print("Client {} connected".format(client_address))
            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(client_thread, (client_socket,))


def client_thread(socket):
    # Sending message to connected client
    # send only takes string
    socket.send(NoWayOutGame.GAME_START.encode(
        ENCODING) + "\n".encode(ENCODING))

    gameInstance = NoWayOutGame()

    # infinite loop so that function do not terminate and thread do not end.
    while True:
        socket.send("\n".encode(ENCODING) +
                    NoWayOutGame.REQUEST.encode(ENCODING))
        # Receiving from client
        data = socket.recv(1024).decode(ENCODING)
        print(">>> Received: {}".format(data))

        command = data.strip().split(" ")
        reply = gameInstance.run_action(command)

        if reply == "" or reply is None:
            reply = "Sorry, the command '%s' is not implemented yet." % command[0]

        socket.sendall(reply.encode(ENCODING))

        if gameInstance.game_ended:
            break

    # came out of loop
    socket.close()


if __name__ == "__main__":
    server = Server()
    server.run_server()
    print("Exiting")
