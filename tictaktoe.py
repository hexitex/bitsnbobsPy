import random
import os
import copy
from _functools import reduce

master_grid=[[4,4,4],[4,4,4],[4,4,4]]
player1_score=0
player2_score=0
player1=''
player2=''
valid_first=('a','b','c') 
valid_second=('1','2','3')
abc_map={'a':0,'b':1,'c':2}
exit_flag=0             
cp=-1   
player=''
os.system('cls')  # For Windows
os.system('clear')  # For Linux/OS X            

def init():
    global player1
    global player2
    global player1_score
    global player2_score
    player1_score=0
    player2_score=0
    print ('/------------------------------------------------------------------------\\')
    print ('| ASCII ticTacToe - "q" to end game, and "r" to restart                   |')
    print ('| Targets are in the form of A1 or 1A, C2 or 2c. This allows bigger grids |')
    print ('\\------------------------------------------------------------------------/\n\n')
    player1=input('Enter Player 1 Name: ')+' (P1)'
    if len(player1)==0: player1='Lazy Brain (P1)'
    player2=input('Enter Player 2 Name: ')+' (P2)'
    if len(player2)==0: player2='Lazy Git (P2)'

def show_grid(cg):
    out='\n\n\n\n{p1} Score: {p1s} {p2} Score: {p2s}\n     A     B     C\n'.format(p1s=player1_score, p2s=player2_score,p1=player1,p2=player2)
    inc=0
    for x in cg:
        inc+=1
        out+='  +-----+-----+-----+\n'+str(inc)+' |'
        count=0
        for a in x: 
            if a==1: 
                out+='  X'
            elif a==0:
                out+='  O'
            else: 
                out+='   '
            count+=1
            if count<3:
                out+='  |'
            if count==3:
                out+='  |\n'
    print (out+'  +-----+-----+-----+')

def check_target(target,cg):
    if len(target)<2 and target.lower() not in['r','q']:#has restart or quit been requested?
        return [True,-1,-1]
    if target.lower()[0]=='q' :
        return [True,-5,-5]
    if target.lower()[0]=='r' :
        return [True,-2,-2]
    t1=target[0].lower()
    t2=target[1].lower()
    
    if (t1 in valid_first) and (t2 in valid_second): #allow both '1a' and 'a1' to be valid as input
        v1=abc_map[t1]
        v2=int(t2)-1
    elif (t2 in valid_first) and (t1 in valid_second):
        v2=int(t1)-1
        v1=abc_map[t2]
    else:
        return [True,-1,-1]
   
    if cg[v2][v1]==4:
        return [False,v2,v1]
    else:
        return [True,-3,-3]
    
    return [True,v2,v1]

def is_finished(cg):
    
    who_won = list(map(lambda x,y,z: x+y+z,cg[0],cg[1],cg[2])) #vertical wins
    a=check_line(who_won)
    if a[0]==1:
        return a

    new_list=list(zip(cg[0],cg[1],cg[2])) # horizontal wins
    who_won = list(map(lambda x,y,z: x+y+z,new_list[0],new_list[1],new_list[2]))
    a=check_line(who_won)
    if a[0]==1:
        return a
    
    a=check_line([cg[0][0]+cg[1][1]+cg[2][2],cg[1][1]+cg[0][2]+cg[2][0],4]) # diagonal wins
    if a[0]==1:
        return a
   
    pos_count=0 # full grid
    for x in cg:
        for a in x:
            if a==1 or a==0:
                pos_count+=1
    if pos_count>=9:
        return [1,'Full Board',1]
      
    return [0,'Game in Progress',0]

def check_line(line):
    global player1_score
    global player2_score
    if line[0]==0 or line[1]==0 or line[2]==0:
        player1_score+=1
        return [1,'Player 1 Wins ',1]
    if line[0]==3 or line[1]==3 or line[2]==3:
        player2_score+=1
        return [1,'Player 2 Wins ',1]
    return[0,'',0]
        
def take_turn(cp):
    global player1
    global player2
    player=''
    if cp==0:
        player=player1
    else:
        player=player2
    
    return input(player+" enter your target.. ")

def run_game(cg):
    global exit_flag
    
    while not exit_flag:  # start of game
        if random.randrange(0,2)==0:
            cp=0
            player=player1
            print('\n\n\n'+player1+' goes first')
        else:
            cp=1
            player=player2
            print('\n\n\n'+player2+' goes first')
     
        run=is_finished(cg) # will tell us if we need to exit or the game is over
    
        while not run[0]:
            show_grid(cg)
            run=check_target(take_turn(cp),cg)
            if not run[0]:
                cg[run[1]][run[2]]=cp #make move
                fin=is_finished(cg)

                if fin[2]:
                    show_grid(cg)
                    print ('\n\n\n\n\n\n\n'+fin[1])
                    cg=copy.deepcopy(master_grid)
                    break
                os.system('cls')
                os.system('clear')
                cp= 0 if cp else 1 # flip player
     
            else:
              
                if run[1]==-1 or run[1]==-3:  #invalid?
                    print('\n\n\n\n\n'+player+' Try again!')#no target try again 
                    run[0]=0
                if run[1]==-2:#restart wanted
                    cg=copy.deepcopy(master_grid)
                    break
                if run[1]==-5: #quit wanted
                    if player1_score>player2_score:
                        player=player1  
                        print (player+' WINS!')
                    elif player2_score>player1_score:
                        player=player2
                        print (player+' WINS!')
                    else:
                        print ('DRAW!')
                    exit_flag=1
                    break
init()
run_game(copy.deepcopy(master_grid[:])) 
