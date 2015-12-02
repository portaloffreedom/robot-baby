#include "connection_listener.h"

#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>


#define CONNECTION_QUEUE_SIZE 20


ConnectionListener::ConnectionListener(const int port)
  : port(port)
{
    socketfd = socket(AF_INET, SOCK_STREAM, 0);
    if (socketfd < 0) {
        std::cerr<<"Couldn't create the TCP socket"<<std::endl;
        //TODO raise error
        exit(1);
    }
    
    
    sockaddr_in addr;
    
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    
    linger linger_options;
    linger_options.l_onoff = 1;
    linger_options.l_linger = 10;
    
    setsockopt(socketfd, SOL_SOCKET, SO_LINGER, &linger_options, sizeof(struct linger));
    
    int reuse_addr_options = 1;
    setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, &reuse_addr_options, sizeof(reuse_addr_options));
    
    int err = bind(socketfd, (struct sockaddr *) &addr, sizeof(struct sockaddr_in));
    if (err < 0) {
        std::cerr<<"Couldn't bind the socket on port "<<port<<std::endl;
        //TODO raise error
        exit(1);
    }
    
    err = listen(socketfd, CONNECTION_QUEUE_SIZE);
    if (err < 0) {
        std::cerr<<"Error transforming to server socket"<<std::endl;
        //TODO raise error
        exit(1);
    }
}

ConnectionListener::~ConnectionListener()
{
    close(this->socketfd);
}

Connection ConnectionListener::accept()
{
    sockaddr_in client_info;
    socklen_t addrlen = sizeof(client_info);
    int client_connection;

    std::memset(&client_info, 0, sizeof(client_info));

    client_connection = ::accept(this->socketfd, (sockaddr *) &client_info, &addrlen);
    if (client_connection < 0) {
        perror("Error while accepting new client");
        //TODO raise error
        exit(1);
    }
    
    return Connection(client_connection, client_info);
}


