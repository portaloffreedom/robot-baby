#ifndef __SHARED_DATA_H__
#define __SHARED_DATA_H__

#include <map>
#include <mutex>
#include "robot_path.h"

class SharedData {
public:
    SharedData();
    ~SharedData();

    
    /**
     * function is thread safe
     */
    RobotPath *create(const int id);
    
    /**
     * function is thread safe
     */
    void reset(const int id);
    
    /**
     * function is thread safe
     */
    RobotPath *get(const int id);

    // operators
    
    /**
     * function is thread safe
     */
    RobotPath *operator[](const int id);

private:
    std::map<int,RobotPath*> map;
    std::mutex mutex;

    RobotPath *unblocked_get(const int id);

};

#endif /* __SHARED_DATA_H__ */
