from robot import EvolutionaryRobot

r1 = EvolutionaryRobot('gecko')
r2 = EvolutionaryRobot('spider')

while True:
    command = raw_input()
    if command == 'exit':
        break
