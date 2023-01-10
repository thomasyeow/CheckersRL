import torch
import random
import numpy as np
from collections import deque
from gameLogic import *
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.nrOfSets = 0
        self.epsilon = 0 #controls randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #if memory is exceeded, calls popleft()
        self.model = Linear_QNet(8,256,2)
        self.trainer = QTrainer(self.model, lr=LR, gamma = self.gamma)
        #TODO: model, trainer



    def get_state(self, game):
        gameState = [[EMPTY] * 8 for _ in range(8)]
        for x in range(8):
            for y in range(8):
                gameState[x][y] = game.boardArr[x][y]
        return gameState

    def remember(self, state, action, reward, next_state, gameOver):
        self.memory.append((state, action, reward, next_state, gameOver))#popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    #action is recorded as a tuple containing tuples (origin, destination)
    def get_action(self, game):
        print("id of board in agent is: ", id(game.boardArr))
        availableMoves, numberOfMoves = game.getAllAvailableMoves()
        self.epsilon = 80 - self.nrOfSets
        finalMove = ()
        #should random action be taken?
        random.seed()
        if random.randint(0, 100) < self.epsilon:
            print(numberOfMoves, " moves available to player" )
            randomMoveIndex = random.randint(0, numberOfMoves - 1)
            counter = 0
            for piece in availableMoves:
                for destination in piece[1]:
                    if counter == randomMoveIndex:
                        finalMove = (piece[0], destination)
                        return finalMove
                        counter = numberOfMoves
                    else:
                        counter += 1
        else:
            state0 = torch.tensor(game.boardArr)
            prediction = self.model(state0)
            finalMove = torch.argmax(prediction).item
            #are these moves even valid?
            valid = False
            for piece in availableMoves:
                for destination in piece[1]:
                    if finalMove == (piece[0], destination):
                        valid = True
                        print("VALID MOVE taken by AI")
            if not valid:
                print("invalid move taken by AI")
            return finalMove


        

#global function
def train():
    highScore = 0
    score = 0
    agent = Agent()
    setOf20 = 0
    game = Game()
    boardArr = game.reset()
    print("After reset, board looks like: " , boardArr)
    while True:
        done = False
        #get old state
        #CHECK if get_state() should just return boardArr instead of a copy
        state_old = agent.get_state(game)
        #get move 
        final_move = agent.get_action(game)
        #perform move and get new state and reward(if won)
        reward = game.makeMove(final_move[0], final_move[1])
        #if game isn't won
        if reward == 0:
            #pass to randomBot
            reward = game.randomBotTurn()
        state_new = agent.get_state(game)
        done = True if reward != 0 else False
        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        #if done(game was won/lost)
        if done:
            score += reward
            game.reset()
            setOf20 += 1
            #if finished set of 20 games, train long memory and increment nr of completed sets of 20
            if setOf20 == 20:
                agent.nrOfSets += 1
                print("Reached ", agent.nrOfSets, "th set")
                setOf20 = 0
                if score > highScore:
                    print("New high score: ", score)
                    highScore = score
                    agent.model.save()
                agent.train_long_memory()


if __name__ == '__main__':
    train()