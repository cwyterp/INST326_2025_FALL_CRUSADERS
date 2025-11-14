#Chris Section Boss Behavior 
import random
aggbehavior = {"health": 30,
                "phase1": [1, 1, 1, 1, 1, 2, 2, 3], 
                "phase2" :[1, 1, 1, 1, 1, 2, 3, 3],
                "phase3": [1, 1, 1, 1, 1, 3, 3, 3]}

defbehavior = {"health": 30,
                "phase1": [1, 1, 1, 1, 2, 2, 2, 3], 
                "phase2" :[1, 1, 2, 2, 2, 2, 3, 3],
                "phase3": [1, 2, 2, 2, 2, 3, 3, 3]}

passbehavior = {"health": 30,
                "phase1": [1, 1, 1, 2, 2, 3, 3, 3], 
                "phase2" :[1, 1, 1, 2, 3, 3, 3, 3],
                "phase3": [1, 1, 1, 3, 3, 3, 3, 3]}

def boss_behavior(health, behaviordict, skill = False):
    """Changes boss behavior based on health status, some always choices like using skill
    if it's charged and set 3 phases of 50% health, 25% health, then below 25%
    
    Args:
        health(int): current health of the boss
        behaviordict(dictionary): inserts the specific behaviro ratios of a certain  boss
        skill(value): tells function if the skill charged enough to be used
        
    Returns:
        Move choice based on the health and ratio or charged skill
    """
    move = Movement()
    choicedict = {1: move.attack(), 2: move.defend(), 
                  3: move.charge(), 4: move.skill()}
    if skill:
        return choicedict[4]
    if health > aggbehavior["health"]/2:
        return choicedict[random.choice(behaviordict["phase1"])]
    elif health > aggbehavior["health"]/4:
        return choicedict[random.choice(behaviordict["phase2"])]
    else:
        return choicedict[random.choice(behaviordict["phase3"])]
    
def special_boss_behavior(health, aggbehavior, defbehavior, passbehavior, playerchoice, skill = False):
    """Works as a special adaptable boss based on player choices
    
    Args:
        health(int): health of boss
        aggbehavior(dict): dictionary of aggressive boss behavior
        defbehavior(dict): dictionary of defensive boss behavior
        passbehavior(dict): dictionary of passive boss behavior
        playerchoice(var): player's most recent choice 
        
    Returns:
        Bosses move based on the behavior of the player character
    """
    playerhistory = [move.attack(), move.attack(),]
    playerhistory.append(playerchoice)
    move = Movement()
    choicedict = {1: move.attack(), 2: move.defend(), 
                  3: move.charge(), 4: move.skill()}
    if skill == True:
        return choicedict[4]
    if playerhistory[:-2] == [move.attack(), move.attack()]:
        return boss_behavior(health, defbehavior)
    elif playerhistory[:-2] == [move.defend(), move.attack()] or playerhistory[:-2] == [move.attack(), move.defend()]:
        return boss_behavior(health, aggbehavior)
    else:
        return boss_behavior(health, passbehavior)
    
# Jahnavi's Section: Story Function
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
def storyline(filepath):
    with open(filepath, 'r', encoding="UTF-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            print(line)
            if line[-1] == "?":
                choice = input("Choose your destiny.")
                if choice not in alphabet:
                    raise ValueError("Invalid choice. Enter a letter corresponding to your choice.")
            else:
                input("Press 'space' to continue...")