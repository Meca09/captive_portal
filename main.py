counter = 0
def main():
    access_point()
    # captive_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    captive_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    captive_server.bind(('', 80))
    captive_server.listen(2)
    
    while True:
    #print(counter)
        client_sock, client_addr = captive_server.accept()
        handle_request(client_sock)

main()
