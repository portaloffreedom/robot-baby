#ifndef __CONNECTION_LISTENER_H__
#define __CONNECTION_LISTENER_H__

#include <string>

#include "connection.h"

class ConnectionListener {
public:
    ConnectionListener(const int port);
    ~ConnectionListener();
    
    Connection accept();
    
private:
    int port;
    int socketfd;
};

#endif /* __CONNECTION_LISTENER_H__ */
