# Snake-Game
This Python program is an advanced Snake Game using Pygame, integrating voice control, difficulty modes, and high score tracking with MySQL support.
Features
1. Game Modes
Easy: 1 apple, no walls, normal points.
Medium: 1 apple + 1 trap, 2x points, walls are passable.
Hard: 1 apple + 3 traps, 5x points, walls are deadly.

2. Controls
Keyboard:
Arrow keys or W/A/S/D to move the snake.
P to start the game.
Q to quit.

Mouse:
Click buttons on menus and pause.
Voice Commands:
Recognizes commands like "play", "easy", "medium", "hard", "rules", "score table", "back", and "quit".

3. Visuals
Custom snake head, body, and tail graphics.
Animated traps and fruits.
Grass background with alternating color cells.
Scoreboard with best score display.
Pause and game over screens with clickable options.

4. Sounds
Crunch sound when the snake eats an apple.
Voice feedback using pyttsx3.

5. Scoring
Easy: 1 point per apple.
Medium: 2 points per apple.
Hard: 5 points per apple.
High scores saved in score.txt and user scores in user_score.txt.

6. Database Integration
Connects to MySQL for storing user data.

7. Additional Features
Snake cannot move in the opposite direction instantly.
Traps reposition when the snake eats an apple.
Multi-line text rendering for rules and score tables.
Smooth game loop with adjustable snake speed per difficulty.

Installation
Install required packages:
pip install pygame mysql-connector-python SpeechRecognition pyttsx3
Make sure to have your MySQL server running and update credentials:
connection = mysql.connector.connect(
    host='localhost', user='root', port='3306',
    password='We1ih.Bu1ut', database='pythongui'
)
Place all required images in the same folder:
apple1.png, trap.png, cup.png, bg.jpg, snake_page.png
Snake head, body, tail images: head_up.png, head_down.png, etc.
Fonts:
PoetsenOne-Regular.ttf is required.

How to Play
Run the game:
python snake_game.py

Follow the menu:
Choose Play, Rules, Score Table, or Quit.
Select difficulty mode.
Control the snake with keyboard or voice commands.
Avoid traps and walls (depending on mode) while eating apples to gain points.
Pause the game using the pause button (top-right).
High scores are automatically saved.
