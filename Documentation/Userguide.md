# Userguide
This is the userguide to use the chess engine.

The chess engine can either be used via the cmd or (the recommended way) with a dedicated GUI.

## How to execute the program

### Command Line
To use the engine with the cmd, just execute `main.py`. As this engine uses the [uci]() interface
the commands to execute different functions are also uci conform.

The different available moves:
* `uci`: This is the first command which has to be executed. This signals the engine that the uci
standard should be used
* `isready`: This is used to tell the engine that a game can be started
* `ucinewgame`: This is used for the engine to start a new game
* `position`: This is used to put a position on the board
  * `position startpos`: This puts the starting position on board and initialized all other values
  * `position fen [fenstring]`: This tells the engine that the board that is defined by the "fenstring" should
  be put on the board
  * After that moves can be added too. So `position startpos a2a4 h7h5` describes the starting position
  followed by the moves "a2a4" and "h7h5".
* `go`: Tells the engine that it should execute search for the best move

If you want to put that move on the board afterwards you have to use the `position` command.

### Dedicated GUI
I strongly advise the use of [Arena](http://www.playwitharena.de). After downloading and starting the programm
a chess engine can be loaded by pressing `engines -> install new engine`. The enigine lays in
[main.exe](/dist/main.exe). If you want to build you own .exe if you changed things you can do this as folows:
* `pip install pyinstaller`
* `pyinstaller --onefile Application/main.py`

After that you can either play the engine by just making the first move or let the engine
play against itself by pressing the `<->` "demo" button.