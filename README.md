# GearHeads RoboCupJuniors Egypt 2018 Code

This year's RescuMaze challenge was about rescuing victims in a maze.
The robot is placed in a random area by the judge. Its tasks are to explore all possible areas, find victims, which are letters on walls or a hot area on the floor- and spot them, and finally got back to the first point (the random starting area.)
The algorithm is to use a recursive function that considers each intersection a parent node which has ways leading to child nodes and explore each child node until it reaches a dead-end point. Then, it plans to explore each sibling node by going back to the parent node and going into each way other than the one that has a dead-end point. This algorithm leads the robot to the starting point after exploring the maze entirely.
