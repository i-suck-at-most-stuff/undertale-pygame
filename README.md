# Undertale Pygame Edition
### i made this for my CS Class Summative and decieded to track it cause i need to grind the hackclub highseas hours, i need that brick of fudge from the place next to hq, anyways this is the plan write up i had to write up for it
## also you can play the game here: [Click Here to go to CodeHS](https://codehs.com/sandbox/joshisyes/undertale-pygame-edition)

## the game plan
### import and setup pygame
this part starts with importing all the modules needed: pygame, sys, and random. pygame.init() is run to start up all pygame modules.

### define constants
here we set up basic variables like the window width and height (800 by 600), the color white (used later), and fps (frames per second) set to 60 for smooth gameplay.

### load images function
this function, load_image(), takes in a path and optional width/height. it loads the image from the file path, scales it down if needed to fit within the max dimensions, and returns the image.

### load specific images
we call load_image() to load in specific images for sans, the player’s heart, and bones with set maximum widths.

### screen setup and clock
we create the display screen with the set dimensions, give the game a title, and create a clock for frame rate control.

### draw_border function
this function just draws a rectangular border in white around the screen to frame the play area.

### difficulty selector function
this function lets the player pick between easy, medium, and hard difficulty. it highlights the current selection and allows switching with w/s keys and selection with enter. each difficulty has a different bone spawn rate (lower is harder). the selected rate is stored in the global variable BONE_SPAWN_RATE.

### global variable for bones and spawn rate
BONE_SPAWN_RATE is set to 40 by default (medium difficulty), and we make an empty list called bones to store each bone that will spawn.

### main_game function
this is the main gameplay function where the player can move around, bones spawn and move, and score is tracked. it includes:

-**player position and score:** player position is set to the middle, and score counters are reset.
-**game loop:** keeps running until the game is quit.
-**sans and player drawing:** displays sans at the top and lets the player move the heart icon with w/a/s/d keys.
-**bone spawning:** based on BONE_SPAWN_RATE, bones randomly spawn from one side and move across the screen.
-**bone movement and rotation:**bones move in a certain direction based on their spawn side, and they also rotate as they move.
-**collision detection:** checks if a bone collides with the player’s heart. if they do, the current score resets, and the bone disappears.
-**off-screen bones:** removes bones that go off-screen.
-**score update:** current score increases over time, and if it’s higher than the high score, it updates.
-**displaying scores**: draws the current and high scores on the screen.

### spawn_bone function
this function randomly picks a side for the bone to spawn from and returns its starting position and direction.

### check_collision function
this helper function checks if two rectangles (the player and a bone) collide using pygame’s colliderect().

### start the game
difficulty_selector() runs first so the player can pick a difficulty, then main_game() runs the actual game. finally, pygame quits after exiting.

overall, this sets up a basic game where the player moves around avoiding bones that spawn randomly from the edges. the goal is to survive as long as possible without getting hit, and the high score is tracked.
