/*
 TUIO C++ GUI Demo 
 
 Copyright (c) 2005-2012 Martin Kaltenbrunner <martin@tuio.org>
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#ifndef __FITNESS_SERVICE_H__
#define __FITNESS_SERVICE_H__

#include <tuple>
#include "connection_listener.h"
#include "tuio.h"
#include "shared_data.h"

enum err {
    SUCCESS = 0,
    ERROR = -1,
};

enum rpcID {
    RPC_START = 1,    // int -> err
    RPC_FITNESS = 2,  // (int,int) -> (float, err)
    RPC_POSITION = 3, // (int) -> (float, float, err)
};

enum fitness_type {
    DISPLACEMENT = 1, // DISPLACEMENT
    PATH = 2,         // DISTANCE
};

class FitnessService {
public:
    FitnessService(const std::string address, const int port, Tuio *tuio, SharedData *shared_data);
    ~FitnessService();
    
    void start_listen();
    void set_verbouse(bool verbouse);
    
private:
    void action_start(const int id);
    float action_fitness(const int id, const fitness_type type);
    std::tuple<float, float> action_position(const int id);
    
    void rpc_start(Connection &client);
    void rpc_fitness(Connection &client);
    void rpc_position(Connection &client);
    
    const std::string address;
    const int port;
    ConnectionListener connection_listener;
    Tuio *tuio;
    SharedData *shared_data;
    
    bool verbose;
};

#endif /* __FITNESS_SERVICE_H__ */

