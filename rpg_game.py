import random
from argparse import ArgumentParser
import sys


# Jahnavi's Section: Story Function
def storyline(main_story, path_A, path_B, path_C):
    alphabet = ["A", "B", "C", "a", "b", "c"]
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

    if choice in ["A", "a"]:
        with open(path_A, "r", encoding="UTF-8") as A:
            for raw_line in A:
                line = raw_line.strip()
                print(line)
                input("Press 'enter' to continue...")
                print()

    if choice in ["B", "b"]:
        with open(path_B, "r", encoding="UTF-8") as B:
            for raw_line in B:
                line = raw_line.strip()
                print(line)
                input("Press 'enter' to continue...")
                print()

    if choice in ["C", "c"]:
        with open(path_C, "r", encoding="UTF-8") as C:
            for raw_line in C:
                line = raw_line.strip()
                print(line)
                input("Press 'enter' to continue...")
                print()
    return choice


class Game:

    # Jahnavi's Section 2
    def __init__(self, player_name, player_skill):
        self.player = Player(player_name, player_skill)

        self.status = True
        self.winner = None

        self.player_stats = {
            "Name": self.player.name,
            "HP": self.player.hp,
            "Attack": self.player.attack,
            "Defense": self.player.defense,
            "Charge": self.player.charge,
        }

    def commence(self, boss):
        self.boss = boss
        round(self.player, self.boss)

        self.player.hp = self.player_stats["HP"]

        self.winner = "boss" if self.player_stats["HP"] <= 0 else "player"
        self.status = False

    def end_results(self):
        if self.status == False:
            if self.winner == "player":
                return (
                    f"Yayy you defeated the boss. Good Job :). \nHere were "
                    + f"the stats: \n{self.player_stats}\n{self.boss.hp}"
                )
            else:
                return (
                    f"Womp womp you lost :( \n...\n Here were the stats: "
                    + f"\n{self.player_stats}\n{self.boss.hp}"
                )

    def run_game(self, boss):
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

        # choose boss action:
        if boss.type == "aggressive" or "passive" or "defensive":
            boss.boss_behavior()
        else:
            boss.special_boss_behavior(
                boss.aggbehavior,
                boss.defbehavior,
                boss.passbehavior,
                boss.player_history[-2:],
            )

        # turn! update hp/charge status
        player.take_action(boss, action)
        # will continue until one or both character's hp dip below zero

    if player.hp <= 0:
        print("Unfortunately, you have have been defeated.")
    elif boss.hp <= 0:
        print(
            "Hooray! You have successfully defeated the boss and will move on"
            " to the next round."
        )


class Player:
    # Heyson's Section: Player section
    def update_history(self, choice):

        action_list = {"A": "attack", "D": "defend", "C": "charge", "S": "skill"}

        (
            self.player_history.append(action_list[choice])
            if choice in action_list
            else print("Invalid choice")
        )

    def __init__(self, name, skill_type):

        self.name = name
        self.hp = 20
        self.attack = 12
        self.defense = 5
        self.charge = 0
        self.max_charge = 5
        # heal, smite, shield
        self.skill_type = skill_type
        self.player_history = []

    def take_action(self, boss, action):

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
        self.type = type
        self.hp = 25
        self.defense = 6
        self.attack = 10
        self.charge = 1
        self.max_charge = 5
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
            behaviordict(dictionary): inserts the specific behaviro ratios of a certain  boss
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
            skill == True
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
            playerchoice(var): player's most recent choice

        Returns:
            Bosses move based on the behavior of the player character
        """
        choicedict = {
            1: "attack",
            2: "defend",
            3: "charge",
            4: "skill",
        }
        if self.charge == 5:
            skill == True
        if skill == True:
            return choicedict[4]
        if player_history[-2:] == ["attack", "attack"]:
            return self.boss_behavior(self.hp, defbehavior)
        elif player_history[-2:] == ["defend", "attack"] or player_history[-2:] == [
            "attack",
            "defend",
        ]:
            return self.boss_behavior(self.hp, aggbehavior)
        else:
            return self.boss_behavior(self.hp, passbehavior)


def main(mainstory, path1, path2, path3):
    """Runs game based on the file given

    Args:
        path (str): path to a text file. File should be split accordingly to be a
        readable story

    """

    # get player inputs: name, skill
    name = input("Hello Traveler! Please input your name here: ")
    print()
    print("To help you on your travels, you may choose one skill.")
    print(
        "These skills are:\nsmite, for extra attack damage\nshield, for a"
        " stronger defense\nheal, to boost your health"
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
        else:
            break
    choice = storyline(mainstory, path1, path2, path3)
    # deciding boss type
    boss_types = {
        "A" or "a": "passive",
        "B" or "b": "defensive",
        "C" or "c": "aggressive",
    }

    game = Game(name, skill)

    game.run_game(Boss(boss_types[choice]))


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
