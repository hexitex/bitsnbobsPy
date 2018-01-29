import random
import os
import copy

master_grid=[[4,4,4],[4,4,4],[4,4,4]]
empty_grid=copy.deepcopy(master_grid[:])
player1_score=0
player2_score=0
player1=''
player2=''
valid_first=('a','b','c') 
valid_second=('1','2','3')
abc_map={'a':0,'b':1,'c':2}
exit_flag=0             
#start by getting the grid5
cp=-1   
player=''
os.system('cls')  # For Windows
os.system('clear')  # For Linux/OS X            

def init():
    #empty_grid=list(copy.deepcopy(master_grid))
    global player1
    global player2
    global player1_score
    global player2_score
    #global empty_grid
    player1_score=0
    player2_score=0
    print ('/----------------------------------------------------------------------\\')
    print ('| Welcome to the awesome  gameplay feature of this ASCII ticTacToe  |')
    print ('| in the known universe. Targets are in the form of A1 or 1A, C2 or 2c. |')
    print ('| "Q", "q" or "quit" to end game, and "R", "r" or "restart" to restart  |')
    print ('\\----------------------------------------------------------------------/\n\n')
    player1=input('Enter Player 1 Name: ')+' (P1)'
    if len(player1)==0: player1='Lazy Brain (P1)'
    player2=input('Enter Player 2 Name: ')+' (P2)'
    if len(player2)==0: player2='Lazy Git (P2)'
    #cg=empty_grid
   # show_grid(cg)
    return empty_grid

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
    #has restart or quit beeen requested?
    if len(target)<2 and target.lower() not in['r','q']:
        return [True,-1,-1]
    if target.lower()[0]=='q' :
        return [True,-5,-5]
    if target.lower()[0]=='r' :
        return [True,-2,-2]
    t1=target[0].lower()
    t2=target[1].lower()
    
    #allow both '1a' and 'a1' to be valid as input
    if (t1 in valid_first) and (t2 in valid_second):
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
    global player1_score
    global player2_score
 
   
    for x in cg:
        p1won=0
        p2won=0
        for i in x:
            if i==0:
                p1won+=1
            elif i==1:
                p2won+=1
        if p1won==3:
            player1_score+=1
            return [1,'Player 1 Wins Horiz',1]
        if p2won==3:
            player2_score+=1
            return [1,'Player 2 Wins Horiz',1]
   
    for x in range(0,3):
        a1=0
        a2=0
        a3=0
        a1+=cg[0][x]
        a2+=cg[1][x]
        a3+=cg[2][x]

        #print (str(x)+str(a1)+str(a2)+str(a3))

        if a1+a2+a3==0:
            player1_score+=1
            return [1,'Player 1 Wins Vert',1]
        if a1+a2+a3==3:
            player2_score+=1
            return [1,'Player 2 Wins Vert',1]
    a1=0
    a2=0
    a3=0
    a4=0
    a5=0
   
    a1=cg[0][0]
    a2=cg[1][1]
    a3=cg[2][2]
    a4=cg[0][2]
    a5=cg[2][0]

    if a1+a2+a3==0:
            player1_score+=1
            return [1,'Player 1 Wins Diag LR',1]
    if a1+a2+a3==3:
            player2_score+=1
            return [1,'Player 2 Wins Diag LR',1]

    if a2+a4+a5==3:
            player2_score+=1
            return [1,'Player 2 Wins Diag RL',1]
    if a2+a4+a5==0:
            player1_score+=1
            return [1,'Player 1 Wins Diag RL',1]

    pos_count=0

    for x in cg:
        for a in x:
            if a==1 or a==0:
                pos_count+=1
        
    if pos_count>=9:
        return [1,'Full Board',1]
      
    return [0,'Game in Progress',0]
        
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
    
    while not exit_flag:
        # start of game
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
                # running
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
                
                #invalid?
                if run[1]==-1 or run[1]==-3:
                    #no target try again 
                    print('\n\n\n\n\n'+player+' Try again!')
                    run[0]=0
                if run[1]==-2:
                    #restart wanted
                    cg=copy.deepcopy(master_grid)
                    break
                if run[1]==-5:
                    #quit wanted
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
run_game(empty_grid) 
