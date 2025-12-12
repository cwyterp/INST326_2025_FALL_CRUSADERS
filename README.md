# INST326_2025_FALL_CRUSADERS
326 Final Project repository

## Purpose of Each File in the Program: 

.gitignore: provide a list of files for git to ignore

collab_exercise.py: class exercise

LICENSE: Copyright; explaining how other people can use our work

README.md: provide documenation for our project

rpg_game.py: the main file that runs our project

storyA.txt: a story file for a single path

storyB.txt: a story file for a single path

storyC.txt: a story file for a single path

mainstory.txt: provide an overall storyline

storyline.json: tried a json file, didn't like it, can't delete it

## How to Run Our Program

The script takes four command-line arguments, each one is a path to a text file. This is how you'd run the script on a Windows machine:  

> python rpg_game.py mainstory story1 story2 story3

Using the story files located in this directory, the script could also run with the following: 

> python rpg_game.py mainstory.txt storyA.txt storyB.txt storyC.txt

## Attribution:
| Method/function | Primary Author | Techniques Demonstrated |
| :-------: | :------: | :-------: |
| Player.take_action | Heyson garcia | **min** & **max** Statements |
| Player.update_history | Heyson Garcia | Conditional Expression | 
| round | Breanna Doyle | f-strings with an expression |
| define_boss_type | Breanna Doyle | regular expressions |
| storyline  | Jahnavi Vemuri  | **with** Statements  |
| Game.end_results  | Jahnavi Vemuri  | Sequence Unpacking  |
| boss_behavior | Christopher Yeung | Optional Parameters |
| parse_args | Christopher Yeung | Argument Parser |