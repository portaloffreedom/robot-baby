#include "shared_data.h"

SharedData::SharedData()
{
}

SharedData::~SharedData()
{
    std::lock_guard<std::mutex> lock(this->mutex);
    
    for (auto iter = map.begin(); iter != map.end(); iter++) {
        delete (*iter).second;
    }
}


RobotPath * SharedData::unblocked_get(const int id)
{
    return this->map.at(id);
}


RobotPath * SharedData::get(const int id)
{
    std::lock_guard<std::mutex> lock(this->mutex);
    return this->unblocked_get(id);
}

RobotPath * SharedData::operator[](const int id)
{
    return this->get(id);
}

RobotPath * SharedData::create(const int id)
{
    std::lock_guard<std::mutex> lock(this->mutex);
    RobotPath *robot_path;
    try {
        robot_path = this->unblocked_get(id);
        robot_path->reset();
    } catch(std::out_of_range) {
        robot_path = new RobotPath();
        map.insert(std::pair<char,RobotPath*>(id, robot_path) ); 
    }
    
    return robot_path;
}

void SharedData::reset(const int id)
{
    RobotPath * robot_path = this->get(id);
    
    robot_path->reset();
}
