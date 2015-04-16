//
//  main.cpp
//  RobotController
//
//  Created by Berend Weel on 08/04/15.
//  Copyright (c) 2015 Berend Weel. All rights reserved.
//

#include <iostream>
#include "UDPTransceiver.h"

int main(int argc, const char * argv[]) {
    UDPTransceiver transceiver("Hello World!");
    
    transceiver.step();
        
    return 0;
}
