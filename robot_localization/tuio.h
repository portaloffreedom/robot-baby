
#ifndef __TUIO_H__
#define __TUIO_H__

#include "TUIO/TuioListener.h"
#include "TUIO/TuioClient.h"
#include "TUIO/UdpReceiver.h"
#include "TUIO/TcpReceiver.h"
#include "shared_data.h"

using namespace TUIO;

class Tuio: public TuioListener { 

public:
    Tuio(int port, SharedData *shared_data);
    ~Tuio() {
        tuioClient->disconnect();
        delete tuioClient;
        delete osc_receiver;
    }

    void listen();
    void gentle_stop() { running = false; }
    std::tuple<float, float> getPositionFromId(const int id);

    
    // pay attention as all these functions will be called from another thread
    void addTuioObject(TuioObject *tobj);
    void updateTuioObject(TuioObject *tobj);
    void removeTuioObject(TuioObject *tobj);

    void addTuioCursor(TuioCursor *tcur);
    void updateTuioCursor(TuioCursor *tcur);
    void removeTuioCursor(TuioCursor *tcur);

    void addTuioBlob(TuioBlob *tblb);
    void updateTuioBlob(TuioBlob *tblb);
    void removeTuioBlob(TuioBlob *tblb);

    void refresh(TuioTime frameTime);

private:
    void run();
    void receiveObjects();
    bool verbose, running;

    int width, height;

    TuioClient *tuioClient;
    OscReceiver *osc_receiver;
    SharedData *shared_data;
    
    // pay attention as all these functions will be called from another thread
    void insetTuioObjectInData(TuioObject *tobj);
};


class IDNotFound {
public:
    IDNotFound(const int id)
      : id(id) {};
private:
    int id;
};

#endif /* __TUIO_H__ */
