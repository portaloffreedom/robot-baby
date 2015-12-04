
#include "fitness_service.h"
#include <iostream>
#include <stdexcept>

FitnessService::FitnessService(const std::string address, const int port, Tuio *tuio, SharedData *shared_data)
  : address(address)
  , port(port)
  , connection_listener(port)
  , tuio(tuio)
  , shared_data(shared_data)
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
    
    shared_data->create(id);
}

float FitnessService::action_fitness(const int id, const fitness_type type)
{
    std::cout<<"fitness on id "<< id <<" fitness type "<<type<<std::endl;
    RobotPath *path = shared_data->get(id);
    
    float fitness = 0;
    
    switch(type) {
        case DISPLACEMENT:
            fitness = path->calculate_displacement();
            break;
        case PATH:
            fitness = path->calculate_path();
            break;
        default:
            std::cerr<<"unsupported fitness type: "<<type<<std::endl;
            throw std::invalid_argument("unsupported fitness type");
    }
    
    return fitness;
}

std::tuple<float, float> FitnessService::action_position(const int id)
{
    std::cout<<"position on id "<< id <<std::endl;
    
    return tuio->getPositionFromId(id);
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
    
    float fitness;
    try {
        fitness = action_fitness(id, type);
    } catch(std::invalid_argument &e) {
        client.writeFloat4(0);
        client.writeInt4(ERROR);
        return;
    } catch(std::out_of_range &e) {
        client.writeFloat4(0);
        client.writeInt4(ERROR);
        return;
    }
    
    client.writeFloat4(fitness);
    client.writeInt4(SUCCESS);
    return;
}

void FitnessService::rpc_position(Connection& client)
{
    int id = client.readInt4();
    
    std::tuple<float, float> position;
    
    try {
        position = action_position(id);
    } catch(IDNotFound &ex) {
        client.writeFloat4(0.0);
        client.writeFloat4(0.0);
        client.writeInt4(ERROR);
        return;
    }
    
    client.writeFloat4( std::get<0>(position) );
    client.writeFloat4( std::get<1>(position) );
    client.writeInt4(SUCCESS);
    
    return;
}




