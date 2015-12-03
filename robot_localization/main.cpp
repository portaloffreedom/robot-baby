#include <iostream>

#include "fitness_service.h"
#include "tuio.h"
#include "connection.h"
#include "shared_data.h"

int main(int argc, char **argv) {
    SharedData shared_data;
    
    Tuio tuio(3333, &shared_data);
    //tuio.listen();
    
    try {
        FitnessService fitness_service("", 7890, &tuio, &shared_data);
        fitness_service.start_listen();
    } catch(ConnectionException &ex) {
        std::cerr<<ex.reason<<std::endl;
        exit(1);
    }
    
    
    return 0;
}
