![](https://github.com/zwang1600/backgammon/blob/main/ui/images/backgammon-board-light.png)

## What is in this repo?
This repo is an implementation of the solved version of the game [backgammon](https://en.wikipedia.org/wiki/Backgammon). The methods used to implement the agents are [Minimax Search](https://en.wikipedia.org/wiki/Minimax), [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), and [Expectiminimax Search](https://en.wikipedia.org/wiki/Expectiminimax).

There are two versions of the game: "Deterministic Simplified Backgammon" (DSBG) and "Stochastic Simplified Backgammon" (SSBG) and the rules are explained below.

In both versions, several of the rules of normal Backgammon are removed or simplified so that the new versions are easier to play.

## DSBG
The game of backgammon normally involves rolling dice. However, in the "Deterministic Simplified Backgammon" version, there is no dice-rolling. Instead, it's as if one die had only 1s on all six of its faces and the other die had only 6s on all six if its faces. This adaptation removes the stochastic element of Backgammon, and it allows **Minimax** and **Alpha-Beta pruning** to be the appropriate techniques of choice for an agent.

## SSBG
In this, the dice rolling works normally, and the method of **expectiminimax search** is used. We'll call this variation of the game "Stochastic Simplified Backgammon".

## How to run the game?

**With GUI**:

First install pygame: 
```bash
pip3 install pygame
```
Then run the client file:
```bash
python3 client.py
```
If you want to run one of your own agents (SSBG or DSBG) you need to change one of the players (in the imports) to be your BackgammonPlayer. If you run SSBG, make sure to change the value of DETERMINISTIC to Fals

**Without GUI**:

Run
```bash
bash run.sh
```

The game result will be in log.txt

## Acknowledgements
This is a project from the class [CSE 415: Introduction to Artificial Intelligence](https://courses.cs.washington.edu/courses/cse415/23wi/) from the University of Washington.