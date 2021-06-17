import math 
import random
import time

"""
We will initialize the game board with:
#piles - a list of how many elements remain in pile
#player - 0 or 1 to indicate the player
#winner - None , 0, 1 to indicate who the winner is

"""
"""
#We will have two classes one for game and one for AI.
#game -> functions -> [Constructor, avail_action , otherP, switchP, move]
#AI -> functions -> [Constuctor, update, get, updateR, future, chooseBest]

"""
"""
#state = [1,3,5,7] or [1,2,4,0] or etc
#action = (row to remove from, how many to remove) or (i,j)

"""

class match():
    def __init__(self,initial = [1,3,5,7]):
        
        self.piles = initial.copy()
        self.player = 0
        self.winner = None
    @classmethod
    def available_actions(cls,piles):
        
        actions = set()
        #for i in range(piles)                    
        for i, pile in enumerate(piles):
            for j in range(1,pile+1):
                actions.add((i,j))
        return actions

    @classmethod
    def other_player(cls,player):

        return 0 if player == 1 else 1

    def switch_player(self):

        self.player = match.other_player(self.player)

    def move(self,action):
        
        pile, count = action #(i,j)
        
        #errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")
        
        self.piles[pile] -= count
        self.switch_player()

        if all(pile == 0 for pile in self.piles):
            self.winner = self.player

class matchAI():
    #AI -> functions -> [Constuctor, update, get, updateR, future, chooseBest]
    def __init__(self, alpha = 0.5 , epsilon = 0.1):
        
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):

        """
        Updated q value using old state, action and reward for the new state
        """
        
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state,action, old, reward, best_future)

    def get_q_value(self,state, action):

        if(tuple(state), action) not in self.q:
            return 0

        return self.q[tuple(state), action]

    def update_q_value(self, state, action, old_q, reward, future_rewards):

        val = old_q + self.alpha*((reward+future_rewards) - old_q)
        self.q[(tuple(state),action)] = val

    def best_future_reward(self, state):

        best_future = 0
        possibilities = list(match.available_actions(state))

        for option in possibilities:
            q_val = self.get_q_value(state, option)
            if q_val > best_future:
                best_future = q_val
            else:
                continue
        
        return best_future

    def choose_action(self, state, epsilon = True):

        best_action = None
        best_reward = 0

        actions = list(match.available_actions(list(state)))

        for action in actions:
            if best_action is None or self.get_q_value(state,action) > best_reward:
                best_reward = self.get_q_value(state,action)
                best_action = action
        
        if epsilon:
            
            weights = [(1-self.epsilon) if action == best_action else (self.epsilon/(len(actions) -1)) for action in actions]

            best_action = random.choices(actions,weights = weights, k=1)[0]

        return best_action

def train(n):
    player = matchAI()

    for i in range(n):
        print(f"Playing training game {i+1}")
        game = match()

        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        while True:
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            last[game.player]["state"] = state
            last[game.player]["action"] = action

            #Make move
            game.move(action)

            new_state = game.piles.copy()

            #When game is over, update q value with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            #if game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    #Return the trained computer/AI

    return player

def play(ai, human_player = None):

    if human_player is None:
        human_player = random.randint(0,1)

    game = match()

    #Game loop
    while True:
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")

        print()

        available_actions = match.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move

        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon = True) #Important please read this line
            
            print(f"AI chose to take {count} from pile {pile}.")


        #Make move

        game.move((pile, count))

        #Winner Check

        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return









































