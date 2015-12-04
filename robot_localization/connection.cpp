
#include "connection.h"
#include <iostream>
#include <cerrno>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

Connection::Connection(int client_connection, sockaddr_in client_info)
  : socketfd(client_connection)
{
    address = inet_ntoa(client_info.sin_addr);
}

ssize_t writen(int fd, const void *vptr, size_t n) {
    size_t nleft;
    ssize_t nwritten;
    const char *ptr;

    ptr = (const char * ) vptr;
    nleft = n;
    while(nleft > 0) {
        if ( (nwritten = write(fd, ptr, nleft)) <= 0 ) {
            if (errno == EINTR)
                nwritten = 0; // and call write() again
            else
                return -1; // error
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return n;
}

Connection::~Connection()
{
    close();
}


void Connection::writeData4(const void *data)
{
    int payload = htonl(*(unsigned int*)data);
    int *payload_pointer = &payload;
    ssize_t result = writen(socketfd, payload_pointer, sizeof(payload));
    
    if (result < 0 ) {
        throw ConnectionException("Error writing on the stream");
    }
}

void Connection::readData4(void *data)
{
    int payload = -1;
    int *payload_pointer = &payload;
    int byte_read = read(socketfd, payload_pointer, sizeof(payload));
    if (byte_read < 0) {
        throw ConnectionException("Error reading from socket");
    }
    
    *((int*) data) = ntohl(payload);
    return;
}

void Connection::writeInt4(const int data)
{
    writeData4(&data);
}

void Connection::writeFloat4(const float data)
{
    writeData4(&data);
}

int Connection::readInt4()
{
    int data = 0;
    readData4(&data);
    return data;
}

float Connection::readFloat4()
{
    float data = 0;
    readData4(&data);
    return data;
}

void Connection::flush()
{
    fsync(this->socketfd);
}


void Connection::close()
{
    ::close(this->socketfd);
}



