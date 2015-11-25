#include <iostream>

#include "fitness_service.h"
#include "tuio.h"

int main(int argc, char **argv) {
    std::cout << "Hello, world!" << std::endl;
    Tuio tuio(3333);
    tuio.listen();
    
    return 0;
}
