
#include "fitness_service.h"

FitnessService::FitnessService(const std::string address, const int port)
: verbose (false)
, address(address)
, port(port)
{
    
}

void FitnessService::set_verbouse(bool verbouse)
{
    this->verbose = verbouse;
}

void FitnessService::start_listen()
{
    
}




