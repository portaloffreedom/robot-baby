#include <iostream>

#include "fitness_service.h"
#include "tuio.h"

int main(int argc, char **argv) {
    //Tuio tuio(3333);
    //tuio.listen();
    
    FitnessService fitness_service("", 7890);
    fitness_service.start_listen();
    
    return 0;
}
