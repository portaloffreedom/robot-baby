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

UDPTransceiver::UDPTransceiver (std::string genome) :
    UDPTransceiver () {
    this->genome = genome;
}

void UDPTransceiver::broadcastGenome() {
    send(ip::address_v4::broadcast());
}

void UDPTransceiver::send(ip::address address) {
    boost::asio::const_buffer buffer(genome.c_str(), genome.length()+1);
    async_write(socket, buffer, address);
}

void UDPTransceiver::receive() {
    
}

void UDPTransceiver::step () {
    broadcastGenome();
    
    io.poll();
}