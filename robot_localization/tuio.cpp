#include "tuio.h"
#include "common.h"
#include <iostream>
#include <cstdlib>

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
}

void Tuio::listen() {
    run();
}

void Tuio::run() {
    running=true;
    while (running) {
        receiveObjects();
    }
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

void Tuio::receiveObjects() {
    char id[5];
    std::list<TuioCursor*> cursorList = tuioClient->getTuioCursors();
    tuioClient->lockCursorList();
    for (std::list<TuioCursor*>::iterator iter = cursorList.begin(); iter!=cursorList.end(); iter++) {
        TuioCursor *tuioCursor = (*iter);
        std::list<TuioPoint> path = tuioCursor->getPath();
        if (path.size()>0) {
    
            TuioPoint last_point = path.front();
//             glBegin(GL_LINES);
//             glColor3f(0.0, 0.0, 1.0);
            
            for (std::list<TuioPoint>::iterator point = path.begin(); point!=path.end(); point++) {
//                 glVertex3f(last_point.getScreenX(width), last_point.getScreenY(height), 0.0f);
//                 glVertex3f(point->getScreenX(width), point->getScreenY(height), 0.0f);
                last_point.update(point->getX(),point->getY());
            }
//             glEnd();
            
            // draw the finger tip
//             glColor3f(0.75, 0.75, 0.75);
//             glPushMatrix();
//             glTranslatef(last_point.getScreenX(width), last_point.getScreenY(height), 0.0);
//             glBegin(GL_TRIANGLE_FAN);
            for(double a = 0.0f; a <= 2*M_PI; a += 0.2f) {
//                 glVertex2d(cos(a) * height/100.0f, sin(a) * height/100.0f);
            }
//             glEnd();
//             glPopMatrix();
            
//             glColor3f(0.0, 0.0, 0.0);
//             glRasterPos2f(tuioCursor->getScreenX(width),tuioCursor->getScreenY(height));
//             sprintf(id,"%d",tuioCursor->getCursorID());
//             drawString(id);
        }
    }
    tuioClient->unlockCursorList();
    
    // draw the objects
    std::list<TuioObject*> objectList = tuioClient->getTuioObjects();
    tuioClient->lockObjectList();
    for (std::list<TuioObject*>::iterator iter = objectList.begin(); iter!=objectList.end(); iter++) {
        TuioObject *tuioObject = (*iter);
        int pos_size = height/25.0f;
        int neg_size = -1*pos_size;
        float xpos  = tuioObject->getScreenX(width);
        float ypos  = tuioObject->getScreenY(height);
        float angle = tuioObject->getAngleDegrees();
        
//         glColor3f(0.0, 0.0, 0.0);
//         glPushMatrix();
//         glTranslatef(xpos, ypos, 0.0);
//         glRotatef(angle, 0.0, 0.0, 1.0);
//         glBegin(GL_QUADS);
//         glVertex2f(neg_size, neg_size);
//         glVertex2f(neg_size, pos_size);
//         glVertex2f(pos_size, pos_size);
//         glVertex2f(pos_size, neg_size);
//         glEnd();
//         glPopMatrix();
        
//         glColor3f(1.0, 1.0, 1.0);
//         glRasterPos2f(xpos,ypos+5);
//         sprintf(id,"%d",tuioObject->getSymbolID());
//         drawString(id);
    }
    tuioClient->unlockObjectList();
    
    // draw the blobs
    std::list<TuioBlob*> blobList = tuioClient->getTuioBlobs();
    tuioClient->lockBlobList();
    for (std::list<TuioBlob*>::iterator iter = blobList.begin(); iter!=blobList.end(); iter++) {
        TuioBlob *tuioBlob = (*iter);
        float blob_width = tuioBlob->getScreenWidth(width)/2;
        float blob_height = tuioBlob->getScreenHeight(height)/2;
        float xpos  = tuioBlob->getScreenX(width);
        float ypos  = tuioBlob->getScreenY(height);
        float angle = tuioBlob->getAngleDegrees();
        
//         glColor3f(0.25, 0.25, 0.25);
//         glPushMatrix();
//         glTranslatef(xpos, ypos, 0.0);
//         glRotatef(angle, 0.0, 0.0, 1.0);
        
        /*glBegin(GL_QUADS);
         glVertex2f(blob_width/-2, blob_height/-2);
         glVertex2f(blob_width/-2, blob_height/2);
         glVertex2f(blob_width/2, blob_height/2);
         glVertex2f(blob_width/2, blob_height/-2);
         glEnd();*/
        
//         glBegin(GL_TRIANGLE_FAN);
        for(double a = 0.0f; a <= 2*M_PI; a += 0.2f) {
//             glVertex2d(cos(a) * blob_width, sin(a) * blob_height);
        }
//         glEnd();
        
//         glPopMatrix();
        
//         glColor3f(1.0, 1.0, 1.0);
//         glRasterPos2f(xpos,ypos+5);
//         sprintf(id,"%d",tuioBlob->getBlobID());
//         drawString(id);
    }
    tuioClient->unlockBlobList();
}

void Tuio::insetTuioObjectInData(TuioObject *tobj) {
    RobotPath *path;
    try {
        path = shared_data->get(tobj->getSymbolID());
    } catch (std::out_of_range &e) {
        return;
    }
    
    path->insertElem(tobj->getTuioTime().getTotalMilliseconds(), tobj->getX(), tobj->getY());   
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
}


