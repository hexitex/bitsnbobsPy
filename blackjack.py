import random
import time

class Player(object):
    The_Deck=None
    
    def __init__(self,name,deck):
        self.name=name
        self.The_Deck=deck
        self.cards_in_hand=[]
        self.money_in_wallet=100
        self.is_dealer=False

    def calculate_card_values(self):
        value=[0,0]
        for i in self.cards_in_hand:
            split=self.The_Deck.card_value(i)
            value[0]+=split[0]
            value[1]+=split[1]
        return value
    
    def get_cards(self):
        return self.cards_in_hand
    
    def get_money_in_wallet(self):
        return self.money_in_wallet
    
    def get_name(self):
        return self.name
    
    def take_card(self,card_number):
        self.cards_in_hand.append(card_number)

    def pay_money(self,amount,Other_Player):
        if amount>self.money_in_wallet:
            return False
        else:
            Other_Player.take_money(amount)
            self.money_in_wallet-=amount
            return True
        
    def take_money(self,amount):
        if amount<=0:
            return False
        else:
            self.money_in_wallet+=amount
            return True
        
    def make_dealer(self):
        self.is_dealer=True
       
    def make_player(self):
        self.is_dealer=False
        
class Deck(object):
    deck=[]  #cards are just numbers 1 through 52 starting with hearts,clubs,diamonds and finally spades
    cards_in_play=[]
    
#strings for showing cards#
    card_pic_small={13:'<3',26:'~&',39:'<>',52:'<}'} 
    card_str={ 1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
    card_pic={ 1:{1:'|   @@    |   ',2:'|  @  @   |   ',3:'| @AAAA@  |   ',4:'| @    @  |   ',5:'| @    @  |   '},\
               2:{1:'|         |   ',2:'|   xx    |   ',3:'|         |   ',4:'|   xx    |   ',5:'|         |   '},\
               3:{1:'|   xx    |   ',2:'|         |   ',3:'|   xx    |   ',4:'|         |   ',5:'|   xx    |   '},\
               4:{1:'|         |   ',2:'| xx  xx  |   ',3:'|         |   ',4:'| xx  xx  |   ',5:'|         |   '},\
               5:{1:'| xx  xx  |   ',2:'|         |   ',3:'|   xx    |   ',4:'|         |   ',5:'| xx  xx  |   '},\
               6:{1:'| xx  xx  |   ',2:'|         |   ',3:'| xx  xx  |   ',4:'|         |   ',5:'| xx  xx  |   '},\
               7:{1:'| xx  xx  |   ',2:'|   xx    |   ',3:'| xx  xx  |   ',4:'|         |   ',5:'| xx  xx  |   '},\
               8:{1:'| xx  xx  |   ',2:'| xx  xx  |   ',3:'|         |   ',4:'| xx  xx  |   ',5:'| xx  xx  |   '},\
               9:{1:'| xx  xx  |   ',2:'| xx  xx  |   ',3:'| xx  xx  |   ',4:'|   xx    |   ',5:'| xx  xx  |   '},\
              10:{1:'| xx  xx  |   ',2:'| xx  xx  |   ',3:'| xx  xx  |   ',4:'| xx  xx  |   ',5:'| xx  xx  |   '},\
              11:{1:'| |||||   |   ',2:'| ~~  <)  |   ',3:'|~~(   _\\ |   ',4:'|~~~   <  |   ',5:'| \\..../  |   '},\
              12:{1:'|  v_v_v  |   ',2:'| &&  <)  |   ',3:'|&&&@   > |   ',4:'|&&&\' (<  |   ',5:'|&&&&../  |   '},\
              13:{1:'| MMMMM   |   ',2:'| /~  <)  |   ',3:'|///{  _\\ |   ',4:'|///  (<  |   ',5:'| \\..../  |   '}}
                 
    card_top=",---------,   "
    card_bot="'---------'   "
    card_pad='|         |   '
      
    def __init__(self):
        self.deck=self.reset_deck()
       
    def reset_deck(self):
        self.deck.clear()
        self.cards_in_play.clear()
        for i in range(1,53):
            self.deck.append(i)
        return self.deck

    def suit_number(self,cn): # get the suit number of the card and the key for the card pic
       
        if cn in range(1,14):
            return [cn,13]
        elif cn in range(14,27):
            return [cn-13,26]
        elif cn in range(27,40):
            return [cn-26,39]
        else:
            return [cn-39,52]
        
    def card_value(self,cn): # value of card in blackjack
        if cn<14:
            cn=cn
        elif cn>13 and cn <27:
            cn=cn-13
        elif cn>26 and cn <40:
            cn=cn-26
        else:
            cn=cn-39
        if cn==1:
            return [11,1]
        elif cn in range(2,10):
            return [cn,0]
        else:
            return [10,0]
        
    def get_card_str(self,cn):
        tval1=''
        suit_no=self.suit_number(cn)[0]
        suit_key=self.suit_number(cn)[1]
        if suit_no<=10 and suit_no>1:
            tval1=str(suit_no)
        else:
            tval1=str(self.ctype_val_str[suit_no])
            
        return tval1+self.pic_str[suit_key]
        
    def get_card_pics(self,cnl):   # very elaborate printing of cards so they display side by side, OCD strikes again!
       
            card_pic=''
            
            for i in cnl:  # tops of cards
                card_pic+=self.card_top
            card_pic+='\n'
            
            for x in cnl:  # id of card
                suit_no=self.suit_number(x)[0]
                suit_key=self.suit_number(x)[1]
                lp=' '
                if suit_no==10:
                    lp=''
                card_pic+='|'+self.card_str[suit_no]+\
                self.card_pic_small[suit_key]+lp+'     |   '
            card_pic+='\n'
            
            for x in cnl: #empty space
                card_pic+=self.card_pad
                
            card_pic+='\n'
            
            for x in range(1,6): # 5 sections make up a card pic
                                
                for pn in cnl: # pics of cards
                    suit_no=self.suit_number(pn)[0]
                    suit_key=self.suit_number(pn)[1]
                    card_pic+=self.card_pic[suit_no][x]
                    card_pic=card_pic.replace('xx',self.card_pic_small[suit_key])
                card_pic+='\n'    
                    
            for x in cnl: # empty space
                card_pic+=self.card_pad
            card_pic+='\n'    
            
            for x in cnl:  # bottom id of card
                suit_no=self.suit_number(x)[0]
                suit_key=self.suit_number(x)[1]
                lp=' '
                
                if suit_no==10:
                    lp=''
                card_pic+='|     '+lp+self.card_str[suit_no]+self.card_pic_small[suit_key]+'|   '
            
            card_pic+='\n'
            
            for x in cnl:   # bottom of card
                card_pic+=self.card_bot
            
            card_pic+='\n'
            return card_pic            

    def print_cards(self,card_number_list):
            print(self.get_card_pics(card_number_list))
           
    def get_random_card(self):
        val=random.randrange(0,len(self.deck))
        card=self.deck[val]
        self.cards_in_play.append(card)  #put card in inplay cards
        self.deck.remove(card) #remove from deck
        return card
    
print('To Quit the Game enter "Q" at any prompt')
end_flag=1
d=Deck()
p1=Player('Robert',d)
p2=Player('Dealer',d)
p2.make_dealer()
p2.take_money(50000)
p1.make_player()
current_player=p1
dealer=p2

def do_player_calc(player):
    
    c1Val=player.calculate_card_values()[0]
    c2Val=player.calculate_card_values()[1]
    number_of_cards=len(player.get_cards())
    number_of_aces=c2Val
    
    if c1Val==21:
        print(player.get_name()+' has 21!')
        return [1,number_of_cards,21] # seems to be a winner 
    elif (c1Val-(11*number_of_aces))+c2Val==21:
            return [2,number_of_cards,21] # could be out-ranked by dealer
    if c1Val>21:
        if c2Val==0:
            print(player.get_name()+' is a Looser!!.......')
            return [4,number_of_cards,c1Val] # bust 
        elif c2Val>0: # aces
            c1Val-=c2Val*10 # number of aces     
            if c1Val>21:
                print(player.get_name()+' is Still a Looser!')
                return [4,number_of_cards,c1Val] # bust
            else: return [5,number_of_cards,c1Val]
    else: return [5,number_of_cards,c1Val] # still playing    
    
while end_flag:
    dealer.cards_in_hand=[]
    current_player.cards_in_hand=[]
    d.reset_deck()
    no_winner=True # next while
    print(p1.get_name()+' has '+str(p1.get_money_in_wallet())+' credits')
    if p1.get_money_in_wallet()<=0:
        end_flag=0;
        print('sorry you loose - bye')
        break
    ok=1
    while ok:
        strbet=input('Enter the amount for your bet')
    
        bet=int(strbet)
        if bet>p1.get_money_in_wallet():
            print('You don\'t have that much, you have ' +str(p1.get_money_in_wallet()) )
        else:
            ok=0
    
    current_player.pay_money(bet,dealer)
    current_player.take_card(d.get_random_card())
    current_player.take_card(d.get_random_card())
    dealer.take_card(d.get_random_card())
    print(p1.get_name()+' has '+str(p1.get_money_in_wallet())+' credits')
    d.print_cards(current_player.get_cards())
    d.print_cards(dealer.get_cards())
    
    while no_winner:
        while True:
            calc=do_player_calc(current_player)
            stat=calc[0]
            val=calc[2]
            print(current_player.get_name()+' '+str(val))
            
            if stat<3: #21:
                if current_player.is_dealer==False:
                    current_player=dealer
                    stat=0 
                    break
            if stat==4: # bust
                no_winner=False
                if  current_player.is_dealer==True:
                    current_player.pay_money(bet*2, p1)
                    current_player=p1
                break
            if  current_player.is_dealer==True and val>=do_player_calc(p1)[2]:
                    no_winner=False
                    print('Dealer Wins')
                    current_player=p1
                    break
            
            if current_player.is_dealer==False:
                action=input("What to Do? Enter 'S' to stick, 'H' to hit")
                if action.lower()=='s':
                    current_player=dealer
                elif action.lower()=='h':
                        current_player.take_card(d.get_random_card())
                        d.print_cards(current_player.get_cards())
                elif action.lower()=='q':
                    no_winner=False
                    end_flag=False
                    break
            else:
                print(current_player.get_name()+' turn')  
                time.sleep(2.2)  
                current_player.take_card(d.get_random_card())
                d.print_cards(dealer.get_cards())
