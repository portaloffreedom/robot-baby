#include "tuio.h"
#include "common.h"
#include <iostream>
#include <cstdlib>
#include <ctime>

Tuio::Tuio(int port, SharedData *shared_data)
  : shared_data(shared_data)
{
    osc_receiver = new UdpReceiver(port);
    //osc_receiver = new TcpReceiver("127.0.0.1",3333);
    //osc_receiver = new TcpReceiver("192.168.1.69",3333);
    tuioClient = new TuioClient(osc_receiver);
    tuioClient->addTuioListener(this);
    tuioClient->connect();
    
    if (!tuioClient->isConnected()) {
        std::cerr<<"Error connecting! (port: "<<port<<')'<<std::endl;
        std::exit(TUIO_ERROR_EXIT_CODE);
    }


    // current date/time based on current system
    time_t now = time(0);
    // convert now to string form
    char* dt = ctime(&now);

    // remove final '\n'
    size_t end = strlen(dt);
    dt[end-1] = '\0';

    position_log = std::ofstream("positions log " + std::string(dt) + ".csv");
    position_log << "ID, time, x, y, speed, orientation" << std::endl;
}

std::tuple<float, float> Tuio::getPositionFromId(const int id) {
    
    std::list<TuioObject*> objectList = tuioClient->getTuioObjects();
    tuioClient->lockObjectList();
    for (std::list<TuioObject*>::iterator iter = objectList.begin(); iter!=objectList.end(); iter++) {
        TuioObject *tuioObject = (*iter);
        if (tuioObject->getSymbolID() == id) {
            
            float x,y;
            /*
            std::list<TuioPoint> path = tuioObject->getPath();
            TuioPoint last_point = path.back();
            
            x = last_point.getX();
            y = last_point.getY();
            */
            TuioPoint position = tuioObject->getPosition();
            x = position.getX();
            y = position.getY();
            
            tuioClient->unlockObjectList();
            return std::make_tuple(x, y);
        }
    }
    tuioClient->unlockObjectList();
    
    throw IDNotFound(id);
}

void Tuio::insetTuioObjectInData(TuioObject *tobj) {
    RobotPath *path;
    try {
        path = shared_data->get(tobj->getSymbolID());
    } catch (std::out_of_range &e) {
        return;
    }
    
    path->insertElem(tobj->getTuioTime().getTotalMilliseconds(), tobj->getX(), tobj->getY());


    // ID
    position_log << tobj->getSymbolID() << ", ";
    // time
    position_log << tobj->getTuioTime().getTotalMilliseconds() << ", ";
    // x
    position_log << tobj->getX() << ", ";
    // y
    position_log << tobj->getY() << ", ";
    // speed x
    position_log << tobj->getMotionSpeed() << ", ";
    // orientation
    position_log << tobj->getAngleDegrees() << std::endl;
}

void Tuio::addTuioObject(TuioObject *tobj) {
    if (verbose)
        std::cout << "add obj " << tobj->getSymbolID() << " (" << tobj->getSessionID() << "/"<<  tobj->getTuioSourceID() << ") "<< tobj->getX() << " " << tobj->getY() << " " << tobj->getAngle() << std::endl;
    
    insetTuioObjectInData(tobj);
}

void Tuio::updateTuioObject(TuioObject *tobj) {
    if (verbose)
        std::cout << "set obj " << tobj->getSymbolID() << " (" << tobj->getSessionID() << "/"<<  tobj->getTuioSourceID() << ") "<< tobj->getX() << " " << tobj->getY() << " " << tobj->getAngle() 
        << " " << tobj->getMotionSpeed() << " " << tobj->getRotationSpeed() << " " << tobj->getMotionAccel() << " " << tobj->getRotationAccel() << std::endl;
    
    insetTuioObjectInData(tobj);
}

void Tuio::removeTuioObject(TuioObject *tobj) {
    
    if (verbose)
        std::cout << "del obj " << tobj->getSymbolID() << " (" << tobj->getSessionID() << "/"<<  tobj->getTuioSourceID() << ")" << std::endl;
}

void Tuio::addTuioCursor(TuioCursor *tcur) {
    
    if (verbose) 
        std::cout << "add cur " << tcur->getCursorID() << " (" <<  tcur->getSessionID() << "/"<<  tcur->getTuioSourceID() << ") " << tcur->getX() << " " << tcur->getY() << std::endl;
}

void Tuio::updateTuioCursor(TuioCursor *tcur) {
    
    if (verbose)
        std::cout << "set cur " << tcur->getCursorID() << " (" <<  tcur->getSessionID() << "/"<<  tcur->getTuioSourceID() << ") " << tcur->getX() << " " << tcur->getY() 
        << " " << tcur->getMotionSpeed() << " " << tcur->getMotionAccel() << " " << std::endl;
}

void Tuio::removeTuioCursor(TuioCursor *tcur) {
    
    if (verbose)
        std::cout << "del cur " << tcur->getCursorID() << " (" <<  tcur->getSessionID() << "/"<<  tcur->getTuioSourceID() << ")" << std::endl;
}

void Tuio::addTuioBlob(TuioBlob *tblb) {
    
    if (verbose)
        std::cout << "add blb " << tblb->getBlobID() << " (" << tblb->getSessionID()  << "/"<<  tblb->getTuioSourceID()<< ") "<< tblb->getX() << " " << tblb->getY() << " " << tblb->getAngle() << " " << tblb->getWidth() << " " << tblb->getHeight() << " " << tblb->getArea() << std::endl;
}

void Tuio::updateTuioBlob(TuioBlob *tblb) {
    
    if (verbose)
        std::cout << "set blb " << tblb->getBlobID() << " (" << tblb->getSessionID() << "/"<<  tblb->getTuioSourceID() << ") "<< tblb->getX() << " " << tblb->getY() << " " << tblb->getAngle() << " "<< tblb->getWidth() << " " << tblb->getHeight() << " " << tblb->getArea() 
        << " " << tblb->getMotionSpeed() << " " << tblb->getRotationSpeed() << " " << tblb->getMotionAccel() << " " << tblb->getRotationAccel() << std::endl;
}

void Tuio::removeTuioBlob(TuioBlob *tblb) {
    
    if (verbose)
        std::cout << "del blb " << tblb->getBlobID() << " (" << tblb->getSessionID() << "/"<<  tblb->getTuioSourceID() << ")" << std::endl;
}

void Tuio::refresh(TUIO::TuioTime frameTime)
{
    if (verbose)
        std::cout << "REFRESH? " << frameTime.getTotalMilliseconds() << std::endl;

    position_log.flush();
}


