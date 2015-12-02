
#include "fitness_service.h"
#include <iostream>

FitnessService::FitnessService(const std::string address, const int port)
  : address(address)
  , port(port)
  , connection_listener(port)
  , verbose (false)
{
    
}

FitnessService::~FitnessService()
{
}


void FitnessService::set_verbouse(bool verbouse)
{
    this->verbose = verbouse;
}

void FitnessService::start_listen()
{
    bool poweroff = false;
    while (!poweroff) {
        Connection client = connection_listener.accept();
        int methodID = client.readInt4();
        std::cout<<"method "<<methodID<<" called!"<<std::endl;
        switch (methodID) {
            case RPC_START:
                rpc_start(client);
                break;
                
            case RPC_FITNESS:
                rpc_fitness(client);
                break;
                
            case RPC_POSITION:
                rpc_position(client);
                break;
                
            default:
                std::cerr<<"id "<<methodID<<" not implemented"<<std::endl;
        }
    }
}

void FitnessService::action_start(const int id)
{
    std::cout<<"start on id "<< id <<std::endl;
}

float FitnessService::action_fitness(const int id, const fitness_type type)
{
    std::cout<<"fitness on id "<< id <<" fitness type "<<type<<std::endl;
    return 42.42;
}

coordinate FitnessService::action_position(const int id)
{
    std::cout<<"position on id "<< id <<std::endl;
    return {5.3,3.2};
}

void FitnessService::rpc_start(Connection& client)
{
    int id = client.readInt4();
    action_start(id);
    
    client.writeInt4(SUCCESS);
    return;
}

void FitnessService::rpc_fitness(Connection& client)
{
    int id = client.readInt4();
    fitness_type type = (fitness_type) client.readInt4();
    
    float fitness = action_fitness(id, type);
    
    client.writeFloat4(fitness);
    
    client.writeInt4(SUCCESS);
    return;
}

void FitnessService::rpc_position(Connection& client)
{
    int id = client.readInt4();
    
    coordinate position = action_position(id);
    
    client.writeFloat4(position.x);
    client.writeFloat4(position.y);
    
    client.writeInt4(SUCCESS);
    return;
}




