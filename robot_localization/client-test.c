#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <assert.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <errno.h>

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

long int string_to_int(char *string) {
    if (string == NULL) {
        return -1;
    }
    
    long int result;
    char *c;
    for (c = string; *c != '\0'; c++) {
        if (*c < '0' || *c > '9')
            return -1;
    }

    result = atoi(string);
    return result;
}

ssize_t writen(int fd, const void *vptr, size_t n) {
    size_t nleft;
    ssize_t nwritten;
    const char *ptr;

    ptr = (const char * ) vptr;
    nleft = n;
    while(nleft > 0) {
        if ( (nwritten = write(fd, ptr, nleft)) <= 0 ) {
            if (errno == EINTR)
                nwritten = 0; // and call write() again
            else
                return -1; // error
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return n;
}

void writeData4(int socketfd, const void *data)
{
    int payload = htonl(*(unsigned int*)data);
    int *payload_pointer = &payload;
    ssize_t result = writen(socketfd, payload_pointer, sizeof(payload));
    
    if (result < 0 ) {
        perror("Error writing on the stream");
        exit(2);
    }
}

void readData4(int socketfd, void *data)
{
    int payload = -1;
    int *payload_pointer = &payload;
    int byte_read = read(socketfd, payload_pointer, sizeof(payload));
    if (byte_read < 0) {
        perror("Error reading from socket");
        exit(2);
    }
    
    *((int*) data) = ntohl(payload);
    return;
}

void do_start(int socketfd, int id) {
    writeData4(socketfd, &id);
}

void do_fitness(int socketfd, int id, int type) {
    writeData4(socketfd, &id);
    writeData4(socketfd, &type);
    
    float fitness;
    readData4(socketfd, &fitness);
    
    printf("Fitness result: %f\n", fitness);
}

void do_position(int socketfd, int id) {
    writeData4(socketfd, &id);
    
    float x, y;
    readData4(socketfd, &x);
    readData4(socketfd, &y);
    
    printf("Coordinate result: < %f %f >\n", x, y);
    
}

int main(int argc, char **argv) {
    int socketfd, err;
    struct sockaddr_in addr;

    if (argc < 5) {
        printf("missing parameter, usage:\n"
        "%s <ip_address> <port> <command> <parameters>\n\n"
        "Commands:\n"
        "\t1 <id>\treturns a single ERR value\n"
        "\t2 <id> <type>\treturns a single ERR value\n"
        "\t3 <id>\treturns a single ERR value\n"
        "\n", argv[0]);
        exit(1);
    }
    
    int port = string_to_int(argv[2]);
    if (port < 0) {
        fprintf(stderr, "Invalid port argument: %s\n", argv[2]);
        exit(1);
    }
    
    int command = string_to_int(argv[3]);
    if (command<1 || command>3) {
        fprintf(stderr, "Invalid command argument: %s\n", argv[3]);
        exit(1);
    }
    int id = string_to_int(argv[4]);
    if (id<0) {
        fprintf(stderr, "Invalid id argument: %s\n", argv[4]);
        exit(1);
    }
    int type;
    if (command == 2) {
        type = string_to_int(argv[5]);
        switch(type) {
            case DISPLACEMENT:
            case PATH:
                break;
            default:
                fprintf(stderr, "Invalid type argument: %d\n", type);
                exit(1);
        }
    }

    socketfd = socket(AF_INET, SOCK_STREAM, 0);
    if (socketfd < 0) {
        perror("Couldn't create the socket");
        exit(2);
    }

    struct hostent * host_entity = gethostbyname(argv[1]);
    if (host_entity == NULL) {
        perror("Error resolving hostname");
        close(socketfd);
        exit(3);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr = **((struct in_addr **)host_entity->h_addr_list);

    err = connect(socketfd, (struct sockaddr *) &addr, sizeof(struct sockaddr_in));
    if (err < 0) {
        perror("Error connecting to the server\n");
        close(socketfd);
        exit(4);
    }
    
    writeData4(socketfd, &command);
    switch(command) {
        case RPC_START:
            do_start(socketfd, id);
            break;
        case RPC_FITNESS:
            do_fitness(socketfd, id, type);
            break;
        case RPC_POSITION:
            do_position(socketfd, id);
            break;
        default:
            fprintf(stderr, "Invalid command %d\n", command);
            exit(1);
            break;
    }
    

    int return_code = -1;
    if (read(socketfd, &return_code, sizeof(return_code)) < 0) {
        perror("Error reading from socket\n");
        close(socketfd);
        exit(2);
    } else {
        return_code = ntohl(return_code);
        printf("Return code: %d\n", return_code);
    }

    close(socketfd);
    return 0;
}

