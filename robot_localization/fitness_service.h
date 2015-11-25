/*
 TUIO C++ GUI Demo 
 
 Copyright (c) 2005-2012 Martin Kaltenbrunner <martin@tuio.org>
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#ifndef __FITNESS_SERVICE_H__
#define __FITNESS_SERVICE_H__

enum fitness_type {
    DISTANCE = 0,
    PATH = 1,
};

class FitnessService {
public:
    FitnessService(const std::string address, const int port);
    ~FitnessService();
    
    void start_listen();
    void set_verbouse(bool verbouse);
    
private:
    bool action_start(int id);
    float action_fitness(int id, fitness_type type);
    void action_position(int id); // TODO couple of floats returned
    
    const std::string address;
    const int port;
    bool verbose;
};

#endif /* __FITNESS_SERVICE_H__ */

