from calendar import c
from gameLogic import *
from agent import Agent
from collections import namedtuple
import numpy as np
import pickle
from CheckersSUML import CheckersSUML

np.random.seed()
Transition = namedtuple("Transition", ("state", "action", "reward", "next_state", "done"))

def run_qlearning(agent, game, nrOfEpisodes = 5000):
    actionsTaken = 0
    wins = 0
    losses = 0
    totalCorrectGuesses = 0
    totalMissedGuesses = 0
    for episode in range(nrOfEpisodes):
        print("NEW EPISODE")
        print(game.aiCorrectGuesses, " rule-adhering moves tried vs ", game.aiMissedGuesses, " illegal moves tried IN TOTAL." )
        totalCorrectGuesses += game.aiCorrectGuesses
        totalMissedGuesses += game.aiMissedGuesses
        game.aiCorrectGuesses = 0
        game.aiMissedGuesses = 0
        game.reset()
        while True:
            render.quitCheck()
            old_state = game.getStateCopy()
            actionIndex = agent.get_action()
            #NOTE if action is invalid, no action will be taken
            action = game.action_from_index(actionIndex)
            reward, actionTaken = game.makeMove(action)
            if actionTaken:
                render.render(game)
                actionsTaken += 1
                #if win
                if reward == 10:
                    print("WON")
                    wins +=1
                    print("Games played: ", episode+1, ". ", wins, " wins and ", losses, " losses")
                    if(episode >= 9):
                            print("Win ratio: ", format(wins/(wins+losses), '.2f'))
                    agent.learn(Transition(old_state, actionIndex, reward,
                                   game.getStateCopy(), True))
                    break
                else:
                    aiReward = game.randomBotTurn()
                    #if AI wins
                    if aiReward == -10:
                        print("LOST")
                        losses += 1
                        print("Games played: ", episode+1, ". ", wins, " wins and ", losses, " losses")
                        if(episode >= 9):
                            print("Win ratio: ", format(wins/(wins+losses), '.2f'))
                        agent.learn(Transition(old_state, actionIndex, reward,
                                   game.getStateCopy(), True))
                        break
                    else:
                        reward += aiReward
                        agent.learn(Transition(old_state, actionIndex, reward,
                                   game.getStateCopy(), False))
            else:
                #even if no action was taken, learn
                agent.learn(Transition(old_state, actionIndex, -0.1,
                                   game.getStateCopy(), False))
    
    filename = "checkersModel.pkl"
    file = open(filename, "wb")
    copyOfDict = dict(agent.q_table)
    pickle.dump(copyOfDict, file)
    file.close()
if __name__ == '__main__':
    
    game = Game()
    render = CheckersSUML(game)
    
    agent = Agent(game)
    run_qlearning(agent, game)