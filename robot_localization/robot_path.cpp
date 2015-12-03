#include "robot_path.h"

#include <cmath>

float distance(const float x1, const float y1, const float x2, const float y2)
{
    float a,b;
    a = (x1-x2);
    b = (y1-y2);
    
    return std::sqrt(a*a + b*b);
}

RobotPath::RobotPath()
{
}

void RobotPath::insertElem(const long time, const float x, const float y)
{
    std::lock_guard<std::mutex> lock(this->mutex);
    path.push_back(PathElem(time, x, y));
}

void RobotPath::reset()
{
    std::lock_guard<std::mutex> lock(this->mutex);
    path.clear();
}

RobotPath::PathElem::PathElem(const long time, const float x, const float y)
  : time(time)
  , x(x)
  , y(y)
{
}

float RobotPath::pointDistance(const RobotPath::PathElem &a, const RobotPath::PathElem &b)
{
    return distance(a.x, a.y, b.x, b.y);
}

float RobotPath::calculate_displacement()
{
    std::lock_guard<std::mutex> lock(this->mutex);
    return pointDistance(path.front(), path.back());
}

float RobotPath::calculate_path()
{
    float total = 0;
    
    std::lock_guard<std::mutex> lock(this->mutex);
    std::list<PathElem>::const_iterator iter = path.begin();
    if (iter == path.end())
        return 0;
    
    std::list<PathElem>::const_iterator next = path.begin();
    next++;
    
    while (next!= path.end()) {
        total += pointDistance(*iter, *next);
        
        iter++;
        next++;
    }
    
    return total;
}


