#ifndef __ROBOT_PATH_H__
#define __ROBOT_PATH_H__

#include <list>
#include <mutex>

class RobotPath {
public:
    RobotPath();
    ~RobotPath() {};
    
    /**
     * function is thread safe
     */
    void reset();
    
    /**
     * function is thread safe
     */
    void insertElem(const long time, const float x, const float y);
    
    /**
     * function is thread safe
     */
    float calculate_displacement();
    
    /**
     * function is thread safe
     */
    float calculate_path();

private:
    class PathElem {
    public:
        const long time;
        const float x,y;
        
        PathElem(const long time, const float x, const float y);
    };

    std::list<PathElem> path;
    std::mutex mutex;
    
    static float pointDistance(const PathElem &a, const PathElem &b);
};

#endif /* __ROBOT_PATH_H__ */

