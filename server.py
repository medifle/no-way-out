import socket
import select


class Server(object):
    """ Simple socket server that listens to one single client. """

    def __init__(self, host="0.0.0.0", port=2222):
        """ Initialize the server with a host and port to listens to. """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.socket.bind((host, port))
        self.socket.listen(1)

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
        client_socket, client_address = self.socket.accept()
        print("Client {} connected".format(client_address))

        stop = False
        while not stop:
            if client_socket:
                # Check if the client is still connected and if data is available
                print("Waiting for client input")
                try:
                    rdy_read, rdy_write, socket_error = select.select(
                        [client_socket, ], [], [])
                except select.error:
                    print("Select() failed on socket with {}".format(client_address))
                    return -1

                print(len(rdy_read) > 0)
                if len(rdy_read) > 0:
                    read_data = client_socket.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print("{} closed the socket.".format(client_address))
                        stop = True
                    else:
                        print(">>> Received: %s" % read_data.rstrip())
                        if read_data.rstrip() == 'quit':
                            stop = True
                        else:
                            client_socket.send(read_data)
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True

        # Close socket
        print("Closing connection with {}".format(client_address))
        client_socket.close()
        return 0


if __name__ == "__main__":
    server = Server()
    server.run_server()
    print("Exiting")
