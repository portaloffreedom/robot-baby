#ifndef __CONNECTION_H__
#define __CONNECTION_H__

#include <string>
struct sockaddr_in;


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