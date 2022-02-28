# About the project
This aplication is a visualizing tool for pathfinding and maze-generating algorithms built using Python3 with pygame.

# Guide
### Required setup
- Make sure you have installed [Python 3](https://www.python.org/downloads/) and [pygame](https://youtu.be/Y4Jn0UCqY28?t=163).
- Download the "main_script.py" file, navigate to its directory and run with "python main_script.py" (Windows & Linux) or "python3 main_script.py" (MacOS).
### Basic usage 
- On the top right you can see the node color legend.
- Use LEFT MOUSE BUTTON to select nodes and click buttons (the first click will select the start node and the second the end node).
- Use RIGHT MOUSE BUTTON to unselect nodes.
- If you want to generate a maze click any of the light green buttons ("Prim's, "Division", "Backtrack", "Random").
- To select a pathfinding algorithm click on it; selected button will change its color.
- To run the algorithm click "RUN" (green button).
- After running an algorithm you can clear clear the grid (click "CLEAR", yellow button) and you will keep your start and end nodes, as well as any barriers.
- You can also reset the grid (click "RESET", red button), to remove everything.
- To exit the program simply click "X" in the top right corner. **! If you do it while running an algorithm, session's settings will not be saved !**
### Additional info
- You can click "GRID OFF" button to toggle grid lines and click again on "GRID ON" to turn them off.
- You can change the size of the graph by clicking: "S" (small), "M" (medium) and "L" (large) buttons; selected button will change its color.
- You can change the animation speed by clicking: "S" (slow), "N" (normal) and "F" (fast) buttons; selected button will change its color.
- Current settings will be saved to "settings.txt" file.
