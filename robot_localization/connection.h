#ifndef __CONNECTION_H__
#define __CONNECTION_H__

#include <string>
#include <cstring>
#include <sstream>
struct sockaddr_in;

class ConnectionException {
public:
    ConnectionException(std::string reason, int _errno)
    {
        std::stringstream ss;
        ss << reason << ": " <<strerror(_errno);
        this->reason = ss.str();
    }
    
    ConnectionException(std::string reason)
        : ConnectionException(reason, errno) {};
        
    ConnectionException() {
        reason = strerror(errno);
    }
    
    std::string reason;
};

class Connection {
public:
    Connection(int client_connection, sockaddr_in client_info);
    ~Connection();
    
    int readInt4();
    void writeInt4(const int data);
    
    float readFloat4();
    void writeFloat4(const float data);
    
    void flush();
    void close();
    
private:
    /**
     * Assuming void* data is point to 4 bytes of valid data
     */
    void writeData4(const void *data);
    
    /**
     * Assuming void* data is point to 4 bytes of valid data
     */
    void readData4(void *data);
    
    std::string address;
    int port;
    int socketfd;
};


#endif /* __CONNECTION_H__ */