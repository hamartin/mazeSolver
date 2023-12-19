# MAZESOLVER

This is a script/application for me <Hans Åge Martinsen> to learn a little more
about pygame and reinforcement learning/ML. The idea is to create something
that generates a maze and then lets an AI/ML train on that maze to solve it.

The maze stuff is a fork of StanislavPetrovV/Maze_Game with modifications of my
own. You can find an exact copy of the code i forked in the Maze_Game branch or
you can direct your browser to his repository
[https://github.com/StanislavPetrovV/Maze_Game](https://github.com/StanislavPetrovV/Maze_Game).
I suspect as time goes by, the maze game and maze generation stuff will change
quite a lot, but the basis of it all will be Stanislav's original project.

# The idea

So far the idea is to create a maze automatically which I use Stanislav's
code for. Using his code to also create a movable character and probably
something for the character to eat as well. I have created 2 surfaces. One for
the "game" itself, and one for the score stuff. That way, when I want to train
the AI, I can create an image only from the game surface.

This project becomes what ever it becomes.

In hindsight I realize, I could probably just have made minor changes to the
branched code and then have the AI train on that and it would have been a lot
less work, but I would also have understood pygame a lot less too. So it's all
good.
