# Weekly Report 

## What did I do this week?
This week I mainly cared about two big topics:
* Implementing the rules of chess
* Implementing a basic MiniMax (I switched to NegaMax) Algorithm for searching for the best move.

For this I created two separate branches which also should be visible. I used a lot of time checking the code for
the basic moves. Also, I used alot of time thinking about how the calculation of checks and pins should work. I tried different
implementations but none of them worked.

My current idea is to not implement it as a rule but with the points a king would give if taken. In theory if the points of the king are high enough
the engine should prevent those moves and with a good move ordering the runtime overhead should be minimal.

## How has the project progressed?
The project has mostly progressed in regard to the MiniMax Algorithm. For that I created evaluation tables for the board as well
as a basic MiniMax algorithm. I use negaMax instead of MiniMax as it seems to be the default standard for chess engines.

The NegaMax implementation also works and I implemented a basic version of alpha-beta pruning for it.



## What did I learn this week?
I learned about differences between NegaMax and MiniMax algorithms as well as more details about alpha-beta pruning.
In addition, I learned how hard and complicated it can be to implement - what seems to be - easy rules of chess. The last day I read
alot about transposition tables, what hash functions to use in chess and what a transposition table should save.


## What has been unclear or problematic?
It is unclear if my idea of using the evaluation to prevent checks and pins can work or if I have to implement it in the rules myself.
Furthermore, the evaluation function seems to not work correctly for white and black, so I have to look into this too.

## What are my next steps?
My next steps are to implement transposition tables and a basic move ordering so that the engine can search deeper than right now.
Furthermore, I want to look into how to put the engine into lichess so one can actually play against the engine in a gui. But this
will be an extra topic if I have enough time.


## Weekly hours
22h