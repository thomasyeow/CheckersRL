# CheckersRL
PyGame Checkers for testing the Q-Learning RL algorithm

WHAT IS THIS
This repo comes with 2 programs: qLearning.exe & CheckersSUML.exe.

qLearning.exe trains a q-Learning agent to play checkers over 5000 iterations, against an opposing agent that makes totally random moves.
After 5000 iterations, it dumps a .pkl file containing the model. Currently, the model reaches about 58% winrate against the random agent.

CheckersSUML.exe allows a human to play against the created model.

HOW TO USE
1) Run qLearning.exe - it will run 5000 iterations by default; this will take some time, but you can track the training progress on the console.
2) Run CheckersSUML.exe - this lets you play aginst the created model. Doesn't work if you didn't run qLearning.exe for the full 5000 iterations beforehand.
