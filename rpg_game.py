import random
from argparse import ArgumentParser
import sys
import re


class Story:
    def storyline(main_story, path_A, path_B, path_C, game):
        alphabet = ["A", "B", "C", "a", "b", "c"]
        boss_types = {
            "A" or "a": "passive",
            "B" or "b": "defensive",
            "C" or "c": "aggressive",
        }

        with open(main_story, "r", encoding="UTF-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                print(line)
                input("Press 'enter' to continue...")
                print()
        choice = input("Choose your destiny: ").upper()
        # validate
        while True:
            if choice not in alphabet:
                choice = input("Invalid choice. Please choose a letter a-c: ").upper()
            else:
                break

        if choice == "A":
            path_file = path_A
        elif choice == "B":
            path_file = path_B
        else:
            path_file = path_C

        current_boss_type = boss_types[choice]
        fights_completed = 0

        with open(path_file, "r", encoding="UTF-8") as path_handle:
            for raw_line in path_handle:
                line_stripped = raw_line.strip()
                if line_stripped:
                    print(line_stripped)
                    input("Press 'enter' to continue...")
                    print()
                    continue

                if re.search(r"^\s", raw_line):

                    fights_completed += 1
                    boss = Boss(current_boss_type)
                    game.commence(boss)

                    if game.winner == "player":
                        game.status = True
                    else:
                        print(game.end_results())
                        return choice

        if fights_completed > 0 and game.winner == "player":
            print("Congratulations! You have successfully completed your journey!")
            print(game.end_results())

        return choice


class Game:
    """
    In charge of initiating a battle between the player and a type of boss.

    Attributes:
        player (Player): The player instanct that is participating in the
            battles.
        status (boolean): Indicates when the round or entire game has ended.
        winner (str or None): Stores who won (either "boss" or "player") or None.
        player_stats (set): A set containing the player's stats which includes...
            player.name (str)
            player.hp (int)
            player.attack (int)
            player.defense (int)
            player.charge (int)
    """

    def __init__(self, player_name, player_skill):
        """
        Initializes a Game object.

        Args:
            player_name (str): A string value that stores the name of the player.
            player_skill (str): A string value that stores their specialty skill.

        Side effects:
            Initializes player_name and player_skill attributes.
        """
        self.player = Player(player_name, player_skill)

        self.status = True
        self.winner = None

    def commence(self, boss):
        """
        Runs a full complete round between the player and the current boss. This
        is done by calling the round() function which takes care of the back and
        forth actions.

        Args:
            boss (Boss): An instance of a boss that the player will be fighting
                against.

        Side effects:
            Modifies the player's and the boss's stats like health, attack, etc.
            It also prints combat messages and determines the winner of the
            round which gets sent to the winner attribute. The status of the
            game will become false when the round ends.
        """
        self.boss = boss
        round(self.player, self.boss)

        self.winner = "boss" if self.player.hp <= 0 else "player"
        self.status = False

    def end_results(self):
        """
        This provides a summary of the game for the user at the end of their
        journey.

        Returns:
            str: A formatted summary which lets the player know who won and
                the stats of the player and the boss at the end of the game.
        """
        player_stats = (
            self.player.name,
            self.player.hp,
            self.player.attack,
            self.player.defense,
            self.player.charge,
        )
        p_name, p_health, p_attack, p_defense, p_charge = player_stats

        final_b_health = self.boss.hp

        if self.winner == "player":
            return (
                f"Yayy {p_name}! You defeated the boss. Good Job :). \nHere were "
                + f"the stats: \nYour Health: {p_health}\nYour Attack: {p_attack}"
                + f"\nYour Defense: {p_defense}\nYour Charge: {p_charge}"
                + f"\nBoss Health: {final_b_health}"
            )
        elif self.winner == "boss":
            return (
                f"Womp womp you lost :( \n...\n Here were the stats: "
                + f"\nYour Health: {p_health}\nYour Attack: {p_attack}"
                + f"\nYour Defense: {p_defense}\nYour Charge: {p_charge}"
                + f"\nBoss Health: {final_b_health}"
            )

    def run_game(self, boss):
        """
        Executes everything at once which should be used during the final boss
        battle. This method will run a battle using the commence() method and
        produce the end results by calling the end_results() method.

        Args:
            boss (Boss): An instance of a boss that the player will be fighting
                against.

        Side effects:
            Performs a round between the player and the boss which prints the
            combat messages in the round and generates a summary at the end.
        """
        self.commence(boss)
        self.end_results()


# Breanna Doyle, movement/round


def round(player, boss_type):
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
    # make boss
    boss = Boss(boss_type)

    while player.hp > 0 and boss.hp > 0:
        # tell player health status of both
        print(f"You have {player.hp} hp. Your opponent has {boss.hp} hp.")
        # give options
        print(
            "You can choose from one of the following options:\n\n"
            "A: Attack \nD: Defend \nC: Charge a skill \nS: Use a Skill\n"
        )
        # ask player what to do
        action_choice = input(
            f"{player.name}, which action would you like to " "take?\n"
        )
        # validate
        while True:
            if action_choice not in ["A", "D", "C", "S", "a", "d", "c", "s"]:
                print(
                    "This is not a valid action. Please type one of the "
                    "specified letters."
                )
                print(
                    "You can choose from one of the following options:\n\n"
                    "A: Attack \nD: Defend \nC: Charge a skill \nS: Use a Skill\n"
                )
                action_choice = input(
                    f"{player.name}, which action would you like to take?\n"
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
        player.player_history.append(action)

        player.take_action(boss, action)

        # choose boss action:
        if boss.type == "aggressive" or "passive" or "defensive":
            boss_action = boss.boss_behavior()
        else:
            boss_action = boss.special_boss_behavior(
                boss.aggbehavior,
                boss.defbehavior,
                boss.passbehavior,
                boss.player_history[-2:],
            )

        boss.take_action(player, boss_action)

    if player.hp <= 0:
        print("Unfortunately, you have have been defeated.")
    elif boss.hp <= 0:
        print("Hooray! Opponent defeated!!\n")


class Player:
    """
    Represents the player character in the game.

    Manages the player's stats, skill type, history of actions, and the logic
    for executing actions against a Boss opponent.

    Attributes:
        name (str): The name of the player.
        hp (int): Current health points.
        attack (int): Base attack damage value.
        defense (int): Base defense value.
        charge (int): Current charge level for the special skill.
        max_charge (int): The required charge level to use the skill.
        skill_type (str): The type of special skill.
        player_history (list): A history of actions taken by the player.
    """

    def update_history(self, choice):
        """
        Saves the player's action (A, D, C, S) in the player_history list.

        Args:
            choice (str): The input by the player


        Side effects:
            Appends the corresponding action string ('attack', 'defend', etc.)
            to self.player_history. Prints an error if the choice is invalid.
        """
        action_list = {"A": "attack", "D": "defend", "C": "charge", "S": "skill"}

        (
            self.player_history.append(action_list[choice])
            if choice in action_list
            else print("Invalid choice")
        )

    def __init__(self, name, skill_type):
        """
        Initializes a new Player instance with base stats and a chosen skill.

        Args:
            name (str): The name of the player.
            skill_type (str): The chosen skill.
        """
        self.name = name
        self.hp = 100
        self.attack = 12
        self.defense = 5
        self.charge = 0
        self.max_charge = 5
        # heal, smite, shield
        self.skill_type = skill_type
        self.player_history = []
        self.base_defense = 5

    def take_action(self, boss, action):
        """
        Executes the player's chosen action against the Boss opponent.

        The action affects the player's stats or the boss's health (hp).
        Defense buffs are assumed to be temporary.

        Args:
            boss (Boss): The Boss object the player is currently fighting.
            action (str): The action to perform.

        Side effects:
            Modifies self.hp, self.defense, self.charge, and
            boss.hp based on the action.
            Prints a description of the action taken.
        """
        # Reset defense to base if it was buffed in the last turn
        if self.defense != self.base_defense and action != "defend":
            self.defense = self.base_defense

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

        return


class Boss:
    # Chris Section Boss Behavior

    def __init__(self, type):
        """
        Initializes the stats for the boss.

        Args:
            type(str): type of boss that will be fighting

        """
        self.type = type
        self.hp = 20
        self.defense = 6
        self.attack = 10
        self.charge = 1
        self.max_charge = 5
        self.base_defense = 6
        self.aggbehavior = {
            "phase1": [1, 1, 1, 1, 1, 2, 2, 3],
            "phase2": [1, 1, 1, 1, 1, 2, 3, 3],
            "phase3": [1, 1, 1, 1, 1, 3, 3, 3],
        }
        self.defbehavior = {
            "phase1": [1, 1, 1, 1, 2, 2, 2, 3],
            "phase2": [1, 1, 2, 2, 2, 2, 3, 3],
            "phase3": [1, 2, 2, 2, 2, 3, 3, 3],
        }
        self.passbehavior = {
            "phase1": [1, 1, 1, 2, 2, 3, 3, 3],
            "phase2": [1, 1, 1, 2, 3, 3, 3, 3],
            "phase3": [1, 1, 1, 3, 3, 3, 3, 3],
        }

    def boss_behavior(self, skill=False):
        """Changes boss behavior based on health status, some always choices like using skill
        if it's charged and set 3 phases of 50% health, 25% health, then below 25%

        Args:
            health(int): current health of the boss
            skill(value): tells function if the skill charged enough to be used

        Returns:
            Move choice based on the health and ratio or charged skill
        """
        if self.type == "passive":
            behaviordict = self.passbehavior
        elif self.type == "aggressive":
            behaviordict = self.aggbehavior
        else:
            behaviordict = self.defbehavior

        choicedict = {
            1: "attack",
            2: "defend",
            3: "charge",
            4: "skill",
        }

        if self.charge == 5:
            skill = True
        if skill:
            return choicedict[4]
        if self.hp > 150 / 2:
            return choicedict[random.choice(behaviordict["phase1"])]
        elif self.hp > 150 / 4:
            return choicedict[random.choice(behaviordict["phase2"])]
        else:
            return choicedict[random.choice(behaviordict["phase3"])]

    def special_boss_behavior(
        self,
        aggbehavior,
        defbehavior,
        passbehavior,
        player_history,
        skill=False,
    ):
        """Works as a special adaptable boss based on player choices

        Args:
            health(int): health of boss
            aggbehavior(dict): dictionary of aggressive boss behavior
            defbehavior(dict): dictionary of defensive boss behavior
            passbehavior(dict): dictionary of passive boss behavior
            player_history(list): player's history of choices
            skill(value): tells function if the skill charged enough to be used

        Returns:
            Boss' move based on the behavior of the player character and behavior dictionary
        """
        choicedict = {
            1: "attack",
            2: "defend",
            3: "charge",
            4: "skill",
        }
        if self.charge == 5:
            skill = True
        if skill == True:
            return choicedict[4]
        if player_history[-2:] == ["attack", "attack"]:
            return choicedict[random.choice(defbehavior["phase1"])]
        elif player_history[-2:] == ["defend", "attack"] or player_history[-2:] == [
            "attack",
            "defend",
        ]:
            return choicedict[random.choice(aggbehavior["phase1"])]
        else:
            return choicedict[random.choice(passbehavior["phase1"])]

    def use_skill(self, player):
        damage = max(0, (self.attack + 15) - player.defense)
        player.hp -= damage
        self.charge = 0
        print(f"Boss uses special attack dealing {damage} damage to {player.name}!")

    def take_action(self, player, action):
        # Reset boss defense to base if it was buffed in the last turn
        if self.defense != self.base_defense and action != "defend":
            self.defense = self.base_defense
        # This prevents player defense from stacking infinitely.
        if player.defense != player.base_defense:
            player.defense = player.base_defense

        if action == "attack":
            damage = max(0, self.attack - player.defense)
            player.hp -= damage
            self.charge = min(self.charge + 1, self.max_charge)
            print(f"Boss attacked dealing {damage} damage to {player.name}.")

        elif action == "defend":
            self.defense += 3
            print(f"Boss raised its guard! Defense is now {self.defense}.")

        elif action == "charge":
            self.charge = min(self.charge + 2, self.max_charge)
            print(f"Boss charged its power! Charge is now:{self.charge}")

        elif action == "skill":
            self.use_skill(player)
            self.charge = 0


def main(mainstory, path1, path2, path3):
    """Runs game based on the file given

    Args:
        mainstory(str): path to a text file. File should be split accordingly to be a
        readable story
        path1(str): path to text file of story option 1
        path2(str): path to text file of story option 2
        path3(str): path to text file of story option 3

    Side effects:
        Prints and takes in the player name and type of skill.
    """

    # get player inputs: name, skill
    name = input("Hello Traveler! Please input your name here: ")
    print()
    print("To help you on your travels, you may choose one skill.")
    print(
        "These skills are:\nSmite: Extra attack damage\nShield: A"
        " stronger defense\nHeal: Boost your health"
    )
    skill = input("Please type the name of the skill you'd like here: ")

    # validate skill type
    while True:
        if skill not in ["smite", "shield", "heal"]:
            print(
                "This is not a valid action. Please type one of the " "listed skills."
            )
            print(
                "You can choose from one of the following options:\n"
                "smite\nshield\nheal"
            )
            skill = input("Please type the name of the skill you'd like here: ")
            print()
        else:
            break
    # choice = Story.storyline(mainstory, path1, path2, path3)
    # deciding boss type
    boss_types = {
        "A" or "a": "passive",
        "B" or "b": "defensive",
        "C" or "c": "aggressive",
    }

    game = Game(name, skill)

    Story.storyline(mainstory, path1, path2, path3, game)
    # game.run_game(Boss(boss_types[choice]))


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
    parser.add_argument("path1", help="story1file")
    parser.add_argument("path2", help="story2file")
    parser.add_argument("path3", help="story3file")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.mainstory, args.path1, args.path2, args.path3)
