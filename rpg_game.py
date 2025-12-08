import random
from argparse import ArgumentParser
import sys


class Story:
    # Jahnavi's Section: Story Function
    alphabet = ["A", "B", "C", "D", "a", "b", "c", "d"]

    def storyline(filepath="storyline.md"):
        with open(filepath, "r", encoding="UTF-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                print(line)
                if line[-1] == "?":
                    choice = input("Choose your destiny.")
                    if choice not in Story.alphabet:
                        raise ValueError("Invalid choice. Enter a letter a-d")
                else:
                    input("Press 'space' to continue...")


class Game:
    # Jahnavi's Section 2
    def __init__(self):
        self.player = Player(input("Choose name: "),input("Choose your skill(Smite,Heal,Sheild): ") )
        self.boss = Boss()

        self.status = True
        self.winner = None
        self.player_stats = {
            "name": self.player.name,
            "hp": self.player.hp,
            "attack": self.player.attack,
            "defense": self.player.defense,
            "charge": self.player.charge,
        }

        self.boss_stats = {
            "hp": self.boss.hp,
            "attack": self.boss.attack,
            "defense": self.boss.defense,
            "charge": self.boss.charge,
        }

    def commence(self):

        Moveset.round(self.player, self.boss)

        self.player.hp = self.player_stats["hp"]
        self.boss.hp = self.boss_stats["hp"]

        self.winner = "boss" if self.player_stats["hp"] <= 0 else "player"
        self.status = False

    def end_results(self):
        if self.status == False:
            if self.winner == "player":
                return (
                    f"Yayy you defeated the boss. Good Job :). \nHere were "
                    + f"the stats: \n{self.player_stats}\n{self.boss_stats}"
                )
            else:
                return (
                    f"Womp womp you lost :( \n...\n Here were the stats: "
                    + f"\n{self.player_stats}\n{self.boss_stats}"
                )

    def run_game(self):
        self.commence()
        self.end_results()


# Breanna Doyle, movement/round
class Moveset:
    def round(player, boss):
        """
        Simulates a round/fight between a player and boss. Characters take turns
        until one character has been defeated (their health reaches 0).

        Args:
            player (Player): The human player
            boss (Boss): The boss (opponent) of the round

        Side effects:
            Several print statements giving the player options, asking for
            input, and announcing if the player wins/loses.
        """
        while player.hp > 0 and boss.hp > 0:
            # tell player health status of both
            print(f"You have {player.hp} hp. Your opponent has {boss.hp} hp.")
            # give options
            print(
                "You can choose from one of the following options:\n\n"
                "A: Attack \nD: Defend \nC: Charge a skill \nS: Use a Skill"
            )
            # ask player what to do
            action_choice = input(
                f"{player.name}, which action would you like to take?"
            )
            # validate
            while True:
                if action_choice not in ["A", "D", "C", "S", "a", "d", "c", "s"]:
                    print(
                        "This is not a valid action. Please type one of the"
                        "specified letters."
                    )
                    print(
                        "You can choose from one of the following options:\n\n"
                        "A: Attack \nD: Defend \nC: Charge a skill \nS: Use a Skill"
                    )
                    action_choice = input(
                        f"{player.name}, which action would you like" "to take?"
                    )
                else:
                    action_dict = {
                        "A": "attack",
                        "a": "attack",
                        "D": "defend",
                        "d": "defend",
                        "C": "charge",
                        "c": "charge",
                        "S": "skill",
                        "s": "skill",
                    }
                    action = action_dict[action_choice]
                    break
            # update player history
            player.player_history.append[action]

            # choose boss action:
            if boss["type"] == "aggressive" or "passive" or "defensive":
                boss.boss_behavior(boss["hp"], boss["type"])
            else:
                boss.special_boss_behavior(
                    boss["hp"],
                    boss.aggbehavior,
                    boss.defbehavior,
                    boss.passbehavior,
                    boss.player_history[-1],
                )

            # turn! update hp/charge status
            player.take_action(boss, action)
            # will continue until one or both character's hp dip below zero

        if player["hp"] <= 0:
            print("Unfortunately, you have have been defeated.")
        elif boss["hp"] <= 0:
            print(
                "Hooray! You have successfully defeated the boss and will move on"
                " to the next round."
            )


class Player:
    # Heyson's Section: Player section
    def __init__(self,name,skill_type):
        
        self.name = name
        self.hp = 100
        self.attack = 12
        self.defense = 5
        self.charge = 0
        self.max_charge = 5
        # heal, smite, shield
        self.skill_type = skill_type
        self.player_history = []

    def take_action(self, state, action):
        boss = state.boss

        if action == "attack":
            damage = max(0, self.attack - boss.defense)
            boss.hp -= damage
            self.charge = min(self.charge + 1, self.max_charge)
            print(f"{self.name} attacked dealing {damage} damage.")

        elif action == "defend":
            self.defense += 3
            print(f"{self.name} raised their guard! Defense is now {self.defense}.")

        elif action == "charge":
            self.charge = min(self.charge + 2, self.max_charge)
            print(f"{self.name} charged their power! Charge is now:{self.max_charge}")

        elif action == "skill":
            if self.charge == self.max_charge:

                if self.skill_type == "heal":
                    self.hp += 20
                    print(
                        f"{self.name} uses HEAL! Restores 20 HP. " f"New HP: {self.hp}"
                    )

                elif self.skill_type == "smite":
                    dmg = max(0, (self.attack + 10) - boss.defense)
                    boss.hp -= dmg
                    print(f"{self.name} uses SMITE! Deals {dmg}")

                elif self.skill_type == "shield":
                    self.defense += 6
                    print(
                        f"{self.name} uses SHIELD! Defense increases by 6. "
                        f"New Defense: {self.defense}."
                    )

                print(f"Skill fully used — charge resets to 0.")
                self.charge = 0

            else:
                self.charge = min(self.charge + 1, self.max_charge)
                print(f"Skill not ready. {self.name} gains small charge ")

        return state


class Boss:
    # Chris Section Boss Behavior
    aggbehavior = {
        "phase1": [1, 1, 1, 1, 1, 2, 2, 3],
        "phase2": [1, 1, 1, 1, 1, 2, 3, 3],
        "phase3": [1, 1, 1, 1, 1, 3, 3, 3],
    }

    defbehavior = {
        "phase1": [1, 1, 1, 1, 2, 2, 2, 3],
        "phase2": [1, 1, 2, 2, 2, 2, 3, 3],
        "phase3": [1, 2, 2, 2, 2, 3, 3, 3],
    }

    passbehavior = {
        "phase1": [1, 1, 1, 2, 2, 3, 3, 3],
        "phase2": [1, 1, 1, 2, 3, 3, 3, 3],
        "phase3": [1, 1, 1, 3, 3, 3, 3, 3],
    }

    def __init__(self):
        self.hp = 150
        self.defense = 6
        self.attack = 10
        self.charge = 1
        self.max_charge = 5

    def boss_behavior(health, behaviordict, skill=False):
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
        choicedict = {
            1: move.attack(),
            2: move.defend(),
            3: move.charge(),
            4: move.skill(),
        }
        if skill:
            return choicedict[4]
        if health > behaviordict["health"] / 2:
            return choicedict[random.choice(behaviordict["phase1"])]
        elif health > behaviordict["health"] / 4:
            return choicedict[random.choice(behaviordict["phase2"])]
        else:
            return choicedict[random.choice(behaviordict["phase3"])]

    def special_boss_behavior(
        self, health, aggbehavior, defbehavior, passbehavior, playerchoice, skill=False
    ):
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
        playerhistory = [
            move.attack(),
            move.attack(),
        ]
        playerhistory.append(playerchoice)
        move = Movement()
        choicedict = {
            1: move.attack(),
            2: move.defend(),
            3: move.charge(),
            4: move.skill(),
        }
        if skill == True:
            return choicedict[4]
        if playerhistory[-2:] == [move.attack(), move.attack()]:
            return self.boss_behavior(health, defbehavior)
        elif playerhistory[-2:] == [move.defend(), move.attack()] or playerhistory[
            -2:
        ] == [move.attack(), move.defend()]:
            return self.boss_behavior(health, aggbehavior)
        else:
            return self.boss_behavior(health, passbehavior)


def main(path):
    """Runs game based on the file given

    Args:
        path (str): path to a text file. File should be split accordingly to be a
        readable story

    """
    # story = Story()
    # game = Game().run_game()

    # get player inputs: name, skill
    name = input("Hello Traveler! Please input your name here: ")
    print()
    print("To help you on your travels, you may choose one skill.")
    print("These skills are:\nsmite, for extra attack damage\nshield, for a"
          " stronger defense\nheal, to boost your health")
    skill = input("Please type the name of the skill you'd like here: ")
    
    #validate skill type
    while True:
        if skill not in ["smite", "shield", "heal"]:
            print(
                "This is not a valid action. Please type one of the "
                "listed skills."
            )
            print(
                "You can choose from one of the following options:\n"
                "smite\nshield\nheal"
            )
            skill = input("Please type the name of the skill you'd like here: ")
        else:
            break



def parse_args(arglist):
    """Parse command-line arguments.

    Expects four mandatory command-line argument: a main story file and the three branch story files.

    Args:
        arglist (list of str): a list of command-line arguments to parse.

    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("mainstory", help="file of storylines")
    parser.add_argument("story1", help="story1file")
    parser.add_argument("story2", help="story2file")
    parser.add_argument("story3", help="story3file")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
