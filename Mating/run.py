from robot import EvolutionaryRobot

r1 = EvolutionaryRobot('r1-baby')
r2 = EvolutionaryRobot('r2-baby')

while True:
    command = raw_input()
    if command == 'exit':
        break
