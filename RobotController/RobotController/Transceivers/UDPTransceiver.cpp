//
//  UDPTransceiver.cpp
//  RobotController
//
//  Created by Berend Weel on 10/04/15.
//  Copyright (c) 2015 Berend Weel. All rights reserved.
//

#include "UDPTransceiver.h"
using namespace boost::asio;

UDPTransceiver::UDPTransceiver () :
    socket(io, ip::udp::endpoint(ip::udp::v4(),1337)) {
}

void UDPTransceiver::send(ip::address address) {
    
}