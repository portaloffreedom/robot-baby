#include <iostream>

#include "fitness_service.h"
#include "tuio.h"
#include "connection.h"

int main(int argc, char **argv) {
    Tuio tuio(3333);
    //tuio.listen();
    
    try {
        FitnessService fitness_service("", 7890, &tuio);
        fitness_service.start_listen();
    } catch(ConnectionException ex) {
        std::cerr<<ex.reason<<std::endl;
        exit(1);
    }
    
    
    return 0;
}
