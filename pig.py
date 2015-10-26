__author__ = 'Patrick Abejar'

import argparse
import random
import time

"""A PLAYER is created in order to keep score and take a turn. Keeping
score is done by class level variables, while taking a turn involves
the player rolling the dice and making decisions afterwards. Tests are
done to determine if the player has reached the 100 points required for
a win and also if the players' turn is finished.
"""


class Player:

    # Encapsulates all class variables of Player
    def __init__(self, identity):

        self.identityEnc = identity
        self.scoreEnc = 0     # Total number of points for player
        self.tempScore = 0    # Points earned only during current round
        self.tempScorePrev = 0    # Keeps previous rounds' temp score
        self.isWinnerEnc = False

    # Returns the encapsulated identity of the player
    def identity(self):

        return self.identityEnc

    # Returns the encapsulated total game score of the player
    def score(self):

        return self.scoreEnc

    # Needed for users who try to hold points after game ends as this will
    # subtract any added points to the total score. "sub" will be subtract-
    # ed from the score.
    def subtract_from_score(self, sub):

        self.scoreEnc -= sub

    # Returns how many points were held last hold turn
    def previous_hold_score(self):

        return self.tempScorePrev

    # Declares player winner if True
    def is_winner(self):

        return self.isWinnerEnc

    # Sets the encapsulated winner variable to True
    def make_winner(self):

        self.isWinnerEnc = True

    # Roll a 6-faced die and display the current results
    def roll_die(self):
        random.seed(time.time())
        current_roll = int(random.random() * 6) + 1
        self.tempScore += current_roll

        if current_roll == 1:
            print " _____\n|     | Rolled: 1\n|  *  | ALL POINTS LOST," \
                  " YOUR TURN IS OVER.\n|_____|\n"

        elif current_roll == 2:
            print " _____\n|     | Rolled: 2\n| * * | Points this " \
                  "Round: %i\n|_____|\n" % self.tempScore

        elif current_roll == 3:
            print " _____\n|    *| Rolled: 3\n|  *  | Points this " \
                  "Round: %i\n|*____|\n" % self.tempScore

        elif current_roll == 4:
            print " _____\n|*   *| Rolled: 4\n|     | Points this " \
                  "Round: %i\n|*___*|\n" % self.tempScore

        elif current_roll == 5:
            print " _____\n|*   *| Rolled: 5\n|  *  | Points this " \
                  "Round: %i\n|*___*|\n" % self.tempScore

        elif current_roll == 6:
            print " _____\n|*   *| Rolled: 6\n|*   *| Points this " \
                  "Round: %i\n|*___*|\n" % self.tempScore

        return current_roll

    """The decide() function tests if a player lost his turn or won the
    game. Then, if appropriate, it wil ask to roll or hold again. An
    integer will be returned based on the result/ decision. The following
    shows corresponding integer values:

    0 = won game; game will be finished
    1 = lose turn; give the other player a turn
    2 = hold; give the other player a turn
    3 = roll; turn is yielded back to current player
    4 = ran out of time; game will be finished
    """
    def decide(self, rolled_value):

        # Follow here if the player loses all holding points.
        if rolled_value == 1:
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 1

        # Keep checking if score is above 100 for a win.
        if self.tempScore + self.scoreEnc >= 100:
            print "Total points      : %i" % \
                  (self.tempScore+self.scoreEnc)
            print "\n********************\n      PLAYER %i      \n" \
                  "      %i points      \n   IS THE WINNER    \n" \
                  "********************" % (self.identity(),
                                            self.tempScore+self.scoreEnc)
            self.isWinnerEnc = True
            return 0

        decision = raw_input("Type 'r' for roll and 'h' for hold. "
                             "Decision: ")

        while decision != "r" and decision != "h":
            decision = raw_input("Error. Please only type 'r' for roll "
                                 "and 'h' for hold. Decision: ")

        # Hold will add the score to the player's total score and
        # yield turn to another player.
        if decision == "h":
            self.scoreEnc += self.tempScore
            # In case game is out of time, tempScorePrev will be taken
            # from total score.
            self.tempScorePrev = self.tempScore
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 2

        # Rolling again brings one back to the top of the while loop.
        if decision == "r":
            return 3

        print ""


"""This computer player class subclasses Player with a decide() method
that requires no user input. It functions based on an algorithm notated
below as stated in the assignment.
"""


class ComputerPlayer(Player):

    # This will first roll the die and then follow the assignment strategy.
    def decide(self, rolled_value):

        # Follow here if the player loses all holding points.
        if rolled_value == 1:
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % \
                  (self.identity(), self.scoreEnc)
            return 1

        # Keep checking if score is above 100 for a win.
        if self.tempScore+self.scoreEnc >= 100:
            print "\n********************\n      PLAYER %i      \n" \
                  "      %i points      \n   IS THE WINNER    \n" \
                  "********************" % (self.identity(),
                                            self.tempScore+self.scoreEnc)
            self.isWinnerEnc = True
            return 0

        decision = "h"

        """While the score is below 75, hold whenever the computer player
        reaches 25 and above. While the score is 75 and above, hold when-
        ever the computer player's score reaches 100 - (temporary round
        score)."""
        if (100 - self.scoreEnc) >= 25:
            if self.tempScore < 25:
                decision = "r"
        else:
            if self.tempScore < (100 - self.scoreEnc):
                decision = "r"

        """Hold will add the score to the player's total score and yield
        the turn to another player."""
        if decision == "h":
            print "  Computer has decided to HOLD."
            self.scoreEnc += self.tempScore
            # In case game is out of time, tempScorePrev will be taken
            # from total score.
            self.tempScorePrev = self.tempScore
            self.tempScore = 0
            print "PLAYER %i'S SCORE IS NOW %i\n" % (self.identity(),
                                                     self.scoreEnc)
            return 2

        # Rolling again brings one back to the top of the while loop.
        if decision == "r":
            print "  Computer has decided to ROLL."
            return 3

        print ""


""" This class serves as the factory class that determines whether a
player is human or a computer player based on user input.
"""


class PlayerFactory:

    # This requires the identity of the player and if the player is a
    # human or a computer as its parameters. The object will be
    # instantiated dependent on being human/ computer.
    def get_player(self, identity, type_of_player):

        if type_of_player == "computer":
            return ComputerPlayer(identity)

        if type_of_player == "human":
            return Player(identity)


""" A GAME is the interaction between the two players along that provide
for two steps of each round that occur in the GAME. For Pig, it is roll-
ing the die and deciding whether to hold or roll again. GAME also keeps
a list of the two players. The parameters passed into the construtor of
GAME are required, as these are both the players participating in the
GAME.
"""


class Game:

    # The class variables of Game store the players in a list.
    def __init__(self, player1, player2):

        self.listOfPlayers = []
        self.listOfPlayers.append(player1)
        self.listOfPlayers.append(player2)

    # Returns the number of players currently playing
    def number_of_players(self):

        return len(self.listOfPlayers)

    # Returns the list of players currently playing
    def player_list(self):

        return self.listOfPlayers

    # Returns a random number from 1 to 6, based on the 6-faced die
    # Takes in the player rolling the die
    def roll_game_die(self, player):

        return player.roll_die()

    # Tests previous roll_game_die result through the first parameter
    # if the player, second input, has won the game
    def decide(self, roll_die_value, player):

        return player.decide(roll_die_value)

    # Removes all the current players from the list
    def reset_game(self):

        for x in range(0,len(self.listOfPlayers)):
            self.listOfPlayers.pop()


"""TimedGameProxy subclasses Game, and acts as an intermediate between
the GAME class and the user interface. Information travels back and
forth between GAME and the user via TimeGameProxy. While traveling
through this proxy, time is checked to ensure the game is limited to
only one minute. TimeGameProxy will end the GAME if the game has
existed for more than one minute.
"""


class TimedGameProxy(Game):

    # Almost similar to the Game constructor, but with an additional
    # startTime class variable to keep track of start of game
    def __init__(self, playerA, playerB):

        self.listOfPlayers = []
        self.startTime = time.time()
        self.listOfPlayers.append(playerA)
        self.listOfPlayers.append(playerB)

    # Starts a timed loop of the game for each player.
    def start_game(self):

        winner = 0

        # These two results allows for entry into the below loop.
        result = 3
        exists_no_winner = True

        # The while loop will check for BOTH a winner and time over.
        while exists_no_winner and (60 - (time.time()-self.startTime)) > 0:

            for player in self.listOfPlayers:

                print "********************\n      PLAYER %i      " \
                      "\n      %i points\n********************" % \
                      (player.identity(), player.score())

                """From PLAYER's decide() function:

                0 = won game; game will be finished
                1 = lose turn; give the other player a turn
                2 = hold; give the other player a turn
                3 = roll; turn is yielded back to current player
                4 = ran out of time; game will be finished
                """
                while result == 3:
                    # Check time before rolling die.
                    print "SECONDS LEFT: %f" % (60 - (time.time()
                                                      -self.startTime))
                    if (60 - (time.time()-self.startTime)) < 0:
                        result = 4
                        print "GAME OVER: Time is up!"
                        break
                    else:
                        # Roll the die.
                        resulting_face = self.roll_game_die(player)

                    # Check time before deciding after roll.
                    print "SECONDS LEFT: %f" % (60 - (time.time()
                                                      -self.startTime))
                    if (60 - (time.time()-self.startTime)) < 0:
                        result = 4
                        print "GAME OVER: Time is up!"
                        break
                    else:
                        # Gather if the user wants to roll or hold.
                        result = self.decide(resulting_face, player)

                        # Check time after deciding to roll.
                        if (60 - (time.time()-self.startTime)) < 0:
                            print "GAME OVER: Time is up!"

                            # Subtract the most recent hold if the user
                            # attempted to add hold points to the score.
                            if result == 2:
                                prev_score = player.previous_hold_score()
                                overtime = (time.time()-self.startTime) - 60
                                print "ALERT: Cannot add %i points since" \
                                      " game is already over by %f secon" \
                                      "ds." % (prev_score, overtime)
                                player.subtract_from_score(
                                    player.previous_hold_score())

                            result = 4
                            break

                # In the case of a tie, both players are winners.
                if result == 4:
                    if self.listOfPlayers[0].score() > \
                            self.listOfPlayers[1].score():
                        self.listOfPlayers[0].make_winner()
                        winner = "1"
                    elif self.listOfPlayers[0].score() < \
                            self.listOfPlayers[1].score():
                        self.listOfPlayers[1].make_winner()
                        winner = "2"
                    else:
                        self.listOfPlayers[0].make_winner()
                        self.listOfPlayers[1].make_winner()
                        winner = "1 & 2"
                    exists_no_winner = False
                    print "\n********************\n      PLAYER %s      " \
                          "\n   IS THE WINNER    \n********************" \
                          "\nPlayer 1 Points: %i\nPlayer 2 Points: %i" % \
                          (winner, self.listOfPlayers[0].score(),
                           self.listOfPlayers[1].score())
                    break

                # 0 is triggered by earning 100 or more points.
                if result == 0:
                    exists_no_winner = False
                    break

                # Reset the result to 3 for future iterations.
                result = 3


""" Main shall collect data containing the number of players that are
participating in the game. The game will also be started and shall be
reset when needed.
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", help="Indicate if player 1 is 'human'"
                                          " or 'computer'.")
    parser.add_argument("--player2", help="Indicate if player 2 is 'human'"
                                          " or 'computer'.")
    parser.add_argument("--timed", help="Indicate if game is timed to 60"
                                        " seconds. Type 'yes' or 'no'.")

    args = parser.parse_args()

    try:
        player1_choice = args.player1.lower()
        player2_choice = args.player2.lower()
        timed_game = args.timed.lower()

    except AttributeError:
        print "ALERT: You need to choose 'human' or 'computer' for " \
              "players and 'yes' or 'no' for a timed version."
        exit(1)

    if player1_choice != "human" and player1_choice != "computer":
        print "ALERT: You need to type 'human' or 'player' for --player1."
        exit(1)
    if player2_choice != "human" and player2_choice != "computer":
        print "ALERT: You need to type 'human' or 'player' for --player2."
        exit(1)
    if timed_game != "yes" and timed_game != "no":
        print "ALERT: You need to type 'yes' or 'no' for --timed. "
        exit(1)

    factory = PlayerFactory()
    player1 = factory.get_player(1, player1_choice)
    player2 = factory.get_player(2, player2_choice)

    print "\n==================================================\n" \
          "                BEGINNING PIG GAME                \n" \
          "=================================================="

    # This is the timed version of Pig.
    if timed_game == "yes":
        print "TIMED VERSION\n"
        timed_game = TimedGameProxy(player1, player2)
        timed_game.start_game()
        timed_game.reset_game()

    # This version of Pig is not timed.
    elif timed_game == "no":
        game1 = Game(player1, player2)

        exists_no_winner = True
        result = 3

        while exists_no_winner:

            for player in game1.player_list():
                print "********************\n      PLAYER %i      " \
                      "\n      %i points\n********************" % \
                      (player.identity(), player.score())

                # Rolling and deciding without the timers.
                while result == 3:
                    resulting_face = game1.roll_game_die(player)
                    result = game1.decide(resulting_face, player)

                if result == 0:
                    exists_no_winner = False
                    break

                result = 3

        game1.reset_game()

    print "\n==================================================\n" \
          "                     GAME END                     \n" \
          "==================================================\n"


if __name__ == "__main__":
    main()
