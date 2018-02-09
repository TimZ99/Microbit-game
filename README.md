# Microbit-game
Dodge the obstacles, a game made for the Micro:Bit. 

The display failing and all the pixels are falling down. You, a pixel on the bottom, have survived your fall. 
Sadly the other pixels are still falling and you need to dodge them to stay alive. 
Go left or right and try to stay alive until the last pixels has fallen! 

Rescue is on the way! Good luck!

## How to use
- Press 0 + GND to start the game.
- The pixel on the bottom row is the player.
- Use A en B to move the player en to dodge the pixels that are comming down.
- Press 2 + GND to stop the game or just hit a falling pixel.

## Levels
There are 5 levels.
- Level 1
  - Speed: 1000ms
  - Empty row between falling pixels
- Level 2
  - Speed: 800ms
  - Empty row between falling pixels
- Level 3
  - Speed: 600ms
  - Empty row between falling pixels
- Level 4
  - Speed: 400ms
  - Empty row between falling pixels
- Level 5
  - Speed: 200ms
  - Empty row between falling pixels
  
The maximum score is 100 points! After that, you 
  
The empty row can be removed, but it makes it very unlikely that you survive the level. 
Every row is randomly generated, but there is always 1 escape hole.
When there is no empty row between 2 falling pixels, it could happen that there is no way to get to the escape hole of the next row.

## Next step
Whats next:
- The code is a bit messy and could use a rewrite.
- Code could be written in less code.
