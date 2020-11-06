import sys
import numpy as np
import random
import numpy.random
import matplotlib.pyplot as plt
import matplotlib.figure
import time


def display_board(state, winning, col):
    #this function displays the graphics
    plt.show()
    fig, ax = plt.subplots()
    ax.cla()
    ax.set_xlim((0, 8))
    ax.set_ylim((0, 7))
    plt.xticks([1,2,3,4,5,6,7])
    ax.get_yaxis().set_visible(False)
    
    human_color = '#A50808'
    computer_color = col
    
    for i in range(6):
        for j in range(7):
            if state[i][j] == 1: 
                plt.gcf().gca().add_artist(plt.Circle((j+1,6-i), 0.4, color=human_color, fill=True))
            elif state[i][j] == -1:
                plt.gcf().gca().add_artist(plt.Circle((j+1,6-i), 0.4, color=computer_color, fill=True))

    if winning == 1:
        plt.text(0.25,6, 'Congratulations you have won!', fontsize=20)
    elif winning == -1:
        plt.text(1,6, '   Sorry you have lost!', fontsize=20)
    elif winning == -2:
        plt.text(1,6, '   The game is a tie', fontsize=20)
        
def greedy_reward(score):
    if score == 4: #first choice: do the win
        return 100000
    elif score == 31: #block a win
        return 1000
    else:
        return 0

def reward(score):
    #translates a raw score fron the board into a value
    #LOCAL reward function, NOT a global reward function
    
    #One weakness of our program is that we are using a local reward function, where
    #we are giving a aligned sequences that we can create by playing in each slot, 
    #as opposed to a global reward function where we might consider the state of the entire board
    #An example of this weakness is that an opponent could possibly stack pieces on either side of 
    #a column and force a win 
    #later in the game
    
    #however we inbtroduce some randomness as a tie-breaker which often appears to help the computer
    #play better in fact, and orevents the human player from creating a sequence of steps that wins every time.
    
    
    if score == 4: #first choice: do the win
        return 100000
    elif score == 31: #2nd choice: block a win
        return 1000
    elif score == 21: #3rd choice: place chip next to two lone opponent chips
        return 100
    elif score == 22: #sandwich two opponent chips
        return 10
    elif score == 13 or score == 3: #line up 3
        return 1
    elif score == 2: #line up 2
        return 0.1
    else:
        return 0

def generate_copy(state):
    #makes a copy to avoid Python creasting a pointer
    new_state = np.zeros((6,7))
    for i in range(6):
        for j in range(7):
            new_state[i][j] = state[i][j]
    return new_state

def check_computer_win(state):
    #returns True if the board state contains a computer win
    new_state = generate_copy(state)
    
    #check horizontal victory
    for i in range(6):
        for j in range(4):
            score = sum(new_state[i][j+k] for k in range(4))
            if score == -4:
                return True
    
    #check vertical victory
    for i in range(3):
        for j in range(7):
            score = sum(new_state[i+k][j] for k in range(4))
            if score == -4:
                return True
            
    #check backward diagonal victory
    for i in range(3):
        for j in range(4):
            score = sum(new_state[i+k][j+k] for k in range(4))
            if score == -4:
                return True

    #check forward diagonal victory
    for i in range(3):
        for j in range(3,7):
            score = sum(new_state[i+k][j-k] for k in range(4))
            if score == -4:
                return True
                
    return False
    
def check_human_win(state):
    #returns True if the board state contains a human win
    new_state = generate_copy(state)
    

    #check horizontal victory
    for i in range(6):
        for j in range(4):
            score = sum(new_state[i][j+k] for k in range(4))
            if score == 4:
                return True
    
    #check vertical victory
    for i in range(3):
        for j in range(7):
            score = sum(new_state[i+k][j] for k in range(4))
            if score == 4:
                return True
            
    #check backward diagonal victory
    for i in range(3):
        for j in range(4):
            score = sum(new_state[i+k][j+k] for k in range(4))
            if score == 4:
                return True

    #check forward diagonal victory
    for i in range(3):
        for j in range(3,7):
            score = sum(new_state[i+k][j-k] for k in range(4))
            if score == 4:
                return True
                
    return False
        
def find_greedy_reward(state,action,player):
    #Given a board state, and an action that is to be played by 'player',
    #return the expected immediate reward
    
    new_state = generate_copy(state)
    new_state[action[0],action[1]] = player
    #print('checking horizontal points')
    #print('checking action ' + str(action))
    #print(new_state)
    scores = []

    #check horizontal
    for i in range(6):
        for j in range(4):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i and action[1] == j+k:
                    count +=1
            if count > 0:
                score = 0
                #print(str(action) + ' is gonna get checked for horizontal victory slots ' + str(j) +str(j+1) + str(j+2) + str(j+3))
                #then calculate a score
                for k in range(4):
                    if new_state[i][j+k] == -player:
                        #print('adding 10 like i should')
                        score += 10
                    elif new_state[i][j+k] == player:
                        #print('adding 1 like i should')
                        score += 1
                #print('raw score is ' + str(score))
                #print('point score is ' + str(reward(score)))

                scores.append(greedy_reward(score))   
                          
    #check vertical
    for i in range(3):
        for j in range(7):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j] == -player:
                        score += 10
                    elif new_state[i+k][j] == player:
                        score += 1
                scores.append(greedy_reward(score))
            
    #check backward diagonal
    for i in range(3):
        for j in range(4):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j+k:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j+k] == -player:
                        score += 10
                    elif new_state[i+k][j+k] == player:
                        score += 1
                scores.append(greedy_reward(score))

    #check forward diagonal
    for i in range(3):
        for j in range(3,7):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j-k:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j-k] == -player:
                        score += 10
                    elif new_state[i+k][j-k] == player:
                        score += 1
                scores.append(greedy_reward(score))
                
    return max(scores)

def find_reward(state,action,player):
    #Given a board state, and an action that is to be played by 'player',
    #return the expected immediate reward
    
    new_state = generate_copy(state)
    new_state[action[0],action[1]] = player
    #print('checking horizontal points')
    #print('checking action ' + str(action))
    #print(new_state)
    scores = []

    #check horizontal
    for i in range(6):
        for j in range(4):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i and action[1] == j+k:
                    count +=1
            if count > 0:
                score = 0
                #print(str(action) + ' is gonna get checked for horizontal victory slots ' + str(j) +str(j+1) + str(j+2) + str(j+3))
                #then calculate a score
                for k in range(4):
                    if new_state[i][j+k] == -player:
                        #print('adding 10 like i should')
                        score += 10
                    elif new_state[i][j+k] == player:
                        #print('adding 1 like i should')
                        score += 1
                #print('raw score is ' + str(score))
                #print('point score is ' + str(reward(score)))
                             
                if j < 3 and score != 31:
                    #print('we went into the check condition with a score of ' + str(score) + ' and j = ' + str(j))
                    #check for really bad moves
                    if new_state[i][j] == player and new_state[i][j+1] == 0 and\
                        new_state[i][j+2] == -player and new_state[i][j+3] == -player and\
                            new_state[i][j+4] == 0:
                            #rint('i found a really bad move in ' + str(j))
                            scores.append(0)
                    elif new_state[i][j] == 0 and new_state[i][j+1] == -player and\
                        new_state[i][j+2] == -player and new_state[i][j+3] == 0 and\
                            new_state[i][j+4] == player:
                            #print('i found a really bad move in ' +str(j+4))
                            scores.append(0)      
                    else:
                        #print('######## appending score inside check condition' + str(score))
                        scores.append(reward(score))
                else:
                    #print('@@@@@@@@ appending score outside check condition' + str(score))
                    scores.append(reward(score))   
                          
    #check vertical
    for i in range(3):
        for j in range(7):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j] == -player:
                        score += 10
                    elif new_state[i+k][j] == player:
                        score += 1
                scores.append(reward(score))
            
    #check backward diagonal
    for i in range(3):
        for j in range(4):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j+k:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j+k] == -player:
                        score += 10
                    elif new_state[i+k][j+k] == player:
                        score += 1
                scores.append(reward(score))

    #check forward diagonal
    for i in range(3):
        for j in range(3,7):
            #check if sequence contains action
            count = 0
            for k in range(4):
                if action[0] == i+k and action[1] == j-k:
                    count +=1
            if count > 0:
                score = 0
                #then calculate a score
                for k in range(4):
                    if new_state[i+k][j-k] == -player:
                        score += 10
                    elif new_state[i+k][j-k] == player:
                        score += 1
                scores.append(reward(score))
                
    return max(scores)
        
def height(state,slot):
    #returns the height of a chip to be played, given the slot
    for i in range(0,6):
        if state[5-i][slot] == 0:
            return 5-i
    #return illegal move
    return 9
    
def transition_prob(state):
    #create a transition vector for what the computer expects the human to play next
    #the idea is that the transition vector is a human reward vector that is normalized
    #The computer expects the human to play with the same strategyu as itself
    
    transition_vector = []
    forbidden = [0,0,0,0,0,0,0]
    final_transition_vector = [0,0,0,0,0,0,0]
    for slot in range(7):
        if height(state,slot) == 9:
            forbidden[slot] = 1
            transition_vector.append(0)
        else:
            action = (height(state,slot),slot)           
            transition_vector.append(find_reward(state,action,1))
    
    #print(transition_vector)
            
    if sum(forbidden[i] for i in range(7)) == 0 and transition_vector == [0,0,0,0,0,0,0]:
        final_transition_vector = [1/7,1/7,1/7,1/7,1/7,1/7,1/7]
        #print(final_transition_vector)
        return final_transition_vector
    
    if transition_vector == [0,0,0,0,0,0,0]:
        for slot in range(7):
            if forbidden[slot] != 1:
                final_transition_vector[slot] = 1/(7-sum(forbidden[i] for i in range(7)))
        #print(transition_vector)
        return final_transition_vector
                
    for slot in range(7):
        if transition_vector[slot] == -1:
            transition_vector[slot] = 0
    
    final_transition_vector = [0,0,0,0,0,0,0]
    for slot in range(7):
        final_transition_vector[slot] = transition_vector[slot]/sum(transition_vector[i] for i in range(7))
        
   # print(final_transition_vector)
    return final_transition_vector
            

    
#generates a list of feasible actions
def generate_actions(state):
    actions = []
    for slot in range(7):
        if height(state,slot) != 9:
            actions.append((height(state,slot),slot))
            
    return actions

#update board state space with an action
def do_action(state,action,player):
    state[action[0],action[1]] = player
    return state
     
#returns true if the board is full and it's a tie
def tie(state):
    check = 0
    for i in range(6):
        for j in range(7):
            if state[i][j] == 0:
                check += 1
    if check == 0:
        return True
    else:
        return False
def greedy_lookahead(state, actions):
    #returns the best action and value for a state using depth = 1

    if actions == []:
        print('Game is a tie.')
        sys.exit()
        
    #print('Next round:')
    action_vec = []
    reward_vec = []
    maximum_so_far = -999999
    
    #level 1 computer action
    for action1 in actions:
        
        best_of_round = -9999999
        
        current = find_greedy_reward(generate_copy(state),action1,-1)
        new_state = do_action(generate_copy(state),action1,-1)
        
        if current > best_of_round:
            best_of_round = current
            action_of_round = action1
                
        if current == maximum_so_far:
            if np.random.rand() < 0.5:
                best_action_so_far = action1
                maximum_so_far = current
        elif current > maximum_so_far:
            best_action_so_far = action1
            maximum_so_far = current
                    
        reward_vec.append(best_of_round)
        action_vec.append(action_of_round)
                              
    #print('##################')
    #print(action_vec)
    #print(reward_vec)
    #print('computer selected action ' + str(best_action_so_far) + ' which has reward ' + str(maximum_so_far))
    return (best_action_so_far, maximum_so_far)

def lookahead(state, actions):
    #returns the best action and value for a state using depth = 1

    if actions == []:
        print('Game is a tie.')
        sys.exit()
        
    #print('Next round:')
    action_vec = []
    reward_vec = []
    maximum_so_far = -999999
    
    #level 1 computer action
    for action1 in actions:
        
        best_of_round = -9999999
        
        current = find_reward(generate_copy(state),action1,-1)
        new_state = do_action(generate_copy(state),action1,-1)
        
        if current > best_of_round:
            best_of_round = current
            action_of_round = action1
                
        if current == maximum_so_far:
            if np.random.rand() < 0.5:
                best_action_so_far = action1
                maximum_so_far = current
        elif current > maximum_so_far:
            best_action_so_far = action1
            maximum_so_far = current
                    
        reward_vec.append(best_of_round)
        action_vec.append(action_of_round)
                              
    #print('##################')
    #print(action_vec)
    #print(reward_vec)
    #print('computer selected action ' + str(best_action_so_far) + ' which has reward ' + str(maximum_so_far))
    return (best_action_so_far, maximum_so_far)


def lookahead_d2(state, actions):
    #returns the best action and value for a state using depth = 1

    if actions == []:
        print('Game is a tie.')
        sys.exit()
        
    #print('Next round:')
    action_vec = []
    reward_vec = []
    bad_actions = []
    maximum_so_far = -9999999
    best_action_so_far = random.choice(actions)
    
    #level 1 computer action
    for action1 in actions:
        
        best_of_round = -9999999
        
        action_of_round = generate_actions(state)
        
        current = find_reward(generate_copy(state),action1,-1)
        new_state = do_action(generate_copy(state),action1,-1)
        
        #human response 1 
        human_actions = generate_actions(new_state)
        #transition_vec = transition_prob(new_state)
        
        #print(human_actions)
        #print(transition_vec)
    
        for h_action1 in human_actions:
            
            best_of_round = -9999999
            new_new_state = do_action(generate_copy(new_state),h_action1,1)            
            #h_reward = - (transition_vec[h_action1[1]] * find_reward(generate_copy(new_new_state),h_action1,1))
            #print('h_reward')

            if check_human_win(new_new_state):
                #human will win with that move
                current = -99999999999         
                bad_actions.append(action1)

        if current > best_of_round:
            best_of_round = current
            action_of_round = action1
                
        if current == maximum_so_far:
            if np.random.rand() < 0.5:
                best_action_so_far = action1
                maximum_so_far = current
        elif current > maximum_so_far:
            best_action_so_far = action1
            maximum_so_far = current
                    

        reward_vec.append(best_of_round)
        action_vec.append(action_of_round)

    count2 = 0
    while best_action_so_far in bad_actions and count2 < 30:
        best_action_do_far = random.choice(actions)
        count2 += 1
        
        if best_action_so_far not in bad_actions:
            return (best_action_so_far, maximum_so_far)

    return (best_action_so_far, maximum_so_far)     
        
    #print('##################')
    #print(action_vec)
    #print(reward_vec)
    #print('computer selected action ' + str(best_action_so_far) + ' which has reward ' + str(maximum_so_far))
    
def display_intro(col):
    #generates an intro screen

    state = [[-1,-1,-1,-1,-1,-1,-1],\
             [1,1,1,-1,1,-1,1],\
             [1,-1,-1,-1,1,-1,1],\
             [1,-1,-1,-1,1,1,1],\
             [1,1,1,-1,-1,-1,1],\
             [-1,-1,-1,-1,-1,-1,-1]]
        
    print('Welcome to the game of Connect 4,')
    print('where the first player to align 4 chips')
    print('wins the game.')
    print(' ')
    print('Human player is red and goes first')
    fig, ax = plt.subplots()
    display_board(state, 0, col)
    plt.show()
    input('- Press ENTER button to continue -')
    
    matplotlib.figure.Figure.clear(fig, ax)
    display_board(np.zeros((6,7)),0, col)
    plt.show()
    
def run_performance_test_random_strategy(times, show_graphs):
    #function to have the computer AI an opponent with 
    #1) a random strategy
    #2) a greedy strategy
    
    run_time = time.time()
    num = np.random.rand()
    if num < 0.2:
        computer_color = '#FFD43B'
    elif num < 0.4:
        computer_color = '#4C0CFC'
    elif num < 0.6:
        computer_color = '#7FFF32'
    elif num < 0.8:
        computer_color = '#0AC5CC'
    else:
        computer_color = '#666666'
    
    state = np.zeros((6,7))
    #print(state)
    plt.show()
    fig, ax = plt.subplots()
    plt.show()
    matplotlib.figure.Figure.clear(fig, ax)    
    
    human_wins = 0
    computer_wins = 0
    ties = 0
    
    for iterate in range(times):
        
        state = np.zeros((6,7))      
        winning = 0
        
        while winning == 0:
            move = 0
            
            move = random.choice(generate_actions(state))
            state[move[0],move[1]] = 1
    
            #print(state)
            #print(' ')
            if check_human_win(state):
                #print('Congratulations, you have won!!')
                winning = 1
                
            
            #print(state)
            if show_graphs:
                display_board(state,winning, computer_color)
                plt.show()
            
            if winning != 1:
                
                    
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    ties += 1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
          
                state = generate_copy(state)
                computer_move = lookahead_d2(state,generate_actions(state))
                #print(computer_move[0])
                state = generate_copy(state)
                
                state[computer_move[0]] = -1
                #print(state)
                if show_graphs:
                    display_board(state, winning, computer_color)
                    plt.show()
                if check_computer_win(state):
                    #print('Sorry, the computer has won.')
                    winning = -1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    computer_wins += 1
                
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    ties += 1
                    
            else:
                human_wins += 1
                
    print('A total of ' + str(times) + ' games were simulated with a human playing a random strategy:')
    print('Computer (using 2-depth strategy) won ' + str(computer_wins) + ' games (' + \
          str(round(computer_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
    print('Random strategy player won ' + str(human_wins) + ' games (' + \
          str(round(human_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
    print('Games that were tied: ' + str(ties) + ' games (' + \
          str(round(ties/(human_wins+ties+computer_wins)*100,2)) + '% tie percentage).')
    print('total runtime: ' + str(round(time.time() - run_time, 2)) + ' seconds.')
    print(' ')
        
def run_performance_test_greedy_strategy(times, show_graphs):
    #function to have the computer AI an opponent with 
    #a random strategy
    
    run_time = time.time()
    
    num = np.random.rand()
    if num < 0.2:
        computer_color = '#FFD43B'
    elif num < 0.4:
        computer_color = '#4C0CFC'
    elif num < 0.6:
        computer_color = '#7FFF32'
    elif num < 0.8:
        computer_color = '#0AC5CC'
    else:
        computer_color = '#666666'
    
    state = np.zeros((6,7))
    #print(state)
    plt.show()
    fig, ax = plt.subplots()
    plt.show()
    matplotlib.figure.Figure.clear(fig, ax)    
    
    human_wins = 0
    computer_wins = 0
    ties = 0
    
    for iterate in range(times):
        
        state = np.zeros((6,7))      
        winning = 0
        
        while winning == 0:

            state = generate_copy(state)
            move = greedy_lookahead(state,generate_actions(state))
            #print('move')
            state[move[0]] = 1
    
            #print(state)
            #print(' ')
            if check_human_win(state):
                #print('Congratulations, you have won!!')
                winning = 1
                
            #print(state)
            if show_graphs:
                display_board(state,winning, computer_color)
                plt.show()
            
            if winning != 1:
                
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    ties += 1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
          
                state = generate_copy(state)
                computer_move = lookahead_d2(state,generate_actions(state))
                #print(computer_move[0])
                state = generate_copy(state)
                
                state[tuple(computer_move[0])] = -1
                #print(state)
                if show_graphs:
                    display_board(state, winning, computer_color)
                    plt.show()
                if check_computer_win(state):
                    #print('Sorry, the computer has won.')
                    winning = -1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    computer_wins += 1
                
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    ties += 1
                    
            else:
                human_wins += 1
                
    print('A total of ' + str(times) + ' games were simulated with a human playing a greedy strategy:')
    print('Computer (using 2-depth strategy) won ' + str(computer_wins) + ' games (' + \
          str(round(computer_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
    print('Greedy strategy player won ' + str(human_wins) + ' games (' + \
          str(round(human_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
   
    print('Games that were tied: ' + str(ties) + ' games (' + \
          str(round(ties/(human_wins+ties+computer_wins)*100,2)) + '% tie percentage).')
    print('total runtime: ' + str(round(time.time() - run_time, 2)) + ' seconds.')
    print(' ')
        
def run_performance_test_D1_strategy(times, show_graphs):
    #function to have the computer AI an opponent with 
    #a random strategy
    
    run_time = time.time()
    
    num = np.random.rand()
    if num < 0.2:
        computer_color = '#FFD43B'
    elif num < 0.4:
        computer_color = '#4C0CFC'
    elif num < 0.6:
        computer_color = '#7FFF32'
    elif num < 0.8:
        computer_color = '#0AC5CC'
    else:
        computer_color = '#666666'
    
    state = np.zeros((6,7))
    #print(state)
    plt.show()
    fig, ax = plt.subplots()
    plt.show()
    matplotlib.figure.Figure.clear(fig, ax)    
    
    human_wins = 0
    computer_wins = 0
    ties = 0
    
    for iterate in range(times):
        
        state = np.zeros((6,7))      
        winning = 0
        
        while winning == 0:

            state = generate_copy(state)
            move = lookahead(state,generate_actions(state))
            #print('move')
            state[move[0]] = 1
    
            #print(state)
            #print(' ')
            if check_human_win(state):
                #print('Congratulations, you have won!!')
                winning = 1
                
            #print(state)
            if show_graphs:
                display_board(state,winning, computer_color)
                plt.show()
            
            if winning != 1:
                
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    ties += 1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
          
                state = generate_copy(state)
                computer_move = lookahead_d2(state,generate_actions(state))
                #print(computer_move[0])
                state = generate_copy(state)
                
                state[tuple(computer_move[0])] = -1
                #print(state)
                if show_graphs:
                    display_board(state, winning, computer_color)
                    plt.show()
                if check_computer_win(state):
                    #print('Sorry, the computer has won.')
                    winning = -1
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    computer_wins += 1
                
                if tie(state):
                    #print('The game is a tie.')
                    winning = -2
                    if show_graphs:
                        display_board(state, winning, computer_color)
                        plt.show()
                    ties += 1
                    
            else:
                human_wins += 1
                
    print('A total of ' + str(times) + ' games were simulated with a human playing a 1-depth strategy:')
   
    print('Computer (using 2-depth strategy) won ' + str(computer_wins) + ' games (' + \
          str(round(computer_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
    print('1-Depth lookahead strategy player won ' + str(human_wins) + ' games (' + \
          str(round(human_wins/(human_wins+ties+computer_wins)*100,2)) + '% win percentage).')
    print('Games that were tied: ' + str(ties) + ' games (' + \
          str(round(ties/(human_wins+ties+computer_wins)*100,2)) + '% tie percentage).')
    print('total runtime: ' + str(round(time.time() - run_time, 2)) + ' seconds.')
    print(' ')
        
          
def main():
    num = np.random.rand()
    if num < 0.2:
        computer_color = '#FFD43B'
    elif num < 0.4:
        computer_color = '#4C0CFC'
    elif num < 0.6:
        computer_color = '#7FFF32'
    elif num < 0.8:
        computer_color = '#0AC5CC'
    else:
        computer_color = '#666666'
    
    state = np.zeros((6,7))
    #print(state)
    plt.show()
    fig, ax = plt.subplots()
    plt.show()
    matplotlib.figure.Figure.clear(fig, ax)
    display_intro(computer_color)
    
    winning = 0
    while winning == 0:
        move = 0
        
        while move <1 or move > 7 or height(state,move-1) > 8:
            m = input('Enter your move, red player: \n')
            move = int(m)
            
        move -= 1
            
        state[height(state,move),move] = 1
        #print(state)
        print(' ')
        if check_human_win(state):
            print('Congratulations, you have won!!')
            winning = 1
            
        
        #print(state)
        display_board(state,winning, computer_color)
        plt.show()
        
        if winning == 1:
            sys.exit()
            
        if tie(state):
            print('The game is a tie.')
            winning = -2
            display_board(state, winning, computer_color)
            plt.show()
            sys.exit()
        
        state = generate_copy(state)
        computer_move = lookahead_d2(state,generate_actions(state))
        #print(computer_move[0])
        state = generate_copy(state)
        
        state[computer_move[0]] = -1
        #print(state)
        display_board(state, winning, computer_color)
        plt.show()
        if check_computer_win(state):
            print('Sorry, the computer has won.')
            winning = -1
            display_board(state, winning, computer_color)
            plt.show()
        
    
        if tie(state):
            print('The game is a tie.')
            winning = -2
            display_board(state, winning, computer_color)
            plt.show()
            sys.exit()
    
#MAIN PROGRAM
main()
#run_performance_test_random_strategy(10, True)
#run_performance_test_greedy_strategy(1000, False)
#run_performance_test_D1_strategy(10, True)


