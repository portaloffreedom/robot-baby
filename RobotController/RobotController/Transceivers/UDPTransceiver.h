//
//  UDPTransceiver.h
//  RobotController
//
//  Created by Berend Weel on 10/04/15.
//  Copyright (c) 2015 Berend Weel. All rights reserved.
//

#ifndef __RobotController__UDPTransceiver__
#define __RobotController__UDPTransceiver__

#include "GenomeTransceiver.h"
#include <boost/asio.hpp>

using namespace boost::asio;

class UDPTransceiver : public GenomeTransceiver {
public:
    UDPTransceiver();
    
    virtual void broadcastGenome();
    
    virtual void send(ip::address address);
    virtual void receive();
    
private:
    io_service io;
    ip::udp::socket socket;
};

#endif /* defined(__RobotController__UDPTransceiver__) */
