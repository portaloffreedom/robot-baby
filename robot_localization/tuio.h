
#ifndef __TUIO_H__
#define __TUIO_H__

#include "TUIO/TuioListener.h"
#include "TUIO/TuioClient.h"
#include "TUIO/UdpReceiver.h"
#include "TUIO/TcpReceiver.h"

using namespace TUIO;

class Tuio: public TuioListener { 

public:
    Tuio(int port);
    ~Tuio() {
        tuioClient->disconnect();
        delete tuioClient;
        delete osc_receiver;
    }

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

    void listen();
    void gentle_stop() { running = false; }
    std::tuple<float, float> getPositionFromId(const int id);

private:
    void run();
    void receiveObjects();
    bool verbose, running;

    int width, height;

    TuioClient *tuioClient;
    OscReceiver *osc_receiver;
};

#endif /* __TUIO_H__ */
