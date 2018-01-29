import random
import time
class player(object):
    cards_in_hand=[]
    money_in_wallet=100
    is_dealer=False
    The_Deck=None
    name=''
    def __init__(self,name,deck):
        self.name=name
        self.The_Deck=deck

    def calculate_card_values():
        value=[0,0];
        for i in cards_in_hand:
           split=The_Deck.card_value(i)
           value[0]+=split[0]
           value[1]+=split[1]
       
        return value
    
    def get_cards():
        return self.cards_in_hand
    def get_money_in_wallet():
        return self.money_in_wallet
    def get_name():
        return self.name
    
    def take_card(card_number):
        cards_in_hand.append(card_number)
        calculate_value()

    def pay_money(amount,Other_Player):
        if amount>self.money_in_wallet:
            return False
        else:
            Other_Player.take_money(amount)
            self.money_in_wallet-=amount
            return True
    def take_money(amount):
        if amount<=0:
            return False
        else:
            self.money_in_wallet+=amount
            return True
        
    def make_dealer():
        self.is_dealer=True
       

    def make_player():
        self.is_dealer=False
        

class Deck(object):
    #cards are just numbers 1 through 52 starting with hearts,clubs,diamonds and finally spades
    deck=[]
    cards_in_play=[]
#strings for showing cards

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

    def suit_number(self,cn):
        # get the suit number of the card and the key for the card pic
        if cn in range(1,14):
            return [cn,13]
        elif cn in range(14,27):
            return [cn-13,26]
        elif cn in range(27,40):
            return [cn-26,39]
        else:
            return [cn-39,52]
        
    def card_value(self,cn):
        # value of card in blackjack
       
        if cn<14:
            cn=cn
        elif cn>13 and cn <27:
            cn=cn-13
        elif cn>26 and cn <40:
            cn=cn-26
        else:
            cn=cn-39
       
        if cn==1:
           
            return [1,11]
        elif cn in range(2,10):
            return [cn,0]
        else:
            return [10,0]
        
       
    def get_card_str(self,cn):
        tval1=''
        tval2=''
        suit_no=self.suit_number(cn)[0]
        suit_key=self.suit_number(cn)[1]
        if suit_no<=10 and suit_no>1:
            tval1=str(suit_no)
        else:
            tval1=str(self.ctype_val_str[suit_no])
            
        return tval1+self.pic_str[suit_key]
        
    def get_card_pics(self,cnl):
            # very elaborate printing of cards so they display side by side, OCD strikes again!! OCD update you can get a whole card image from unicode!
            card_pic=''
            
            for i in cnl:
                # tops of cards
                card_pic+=self.card_top
            card_pic+='\n'
            for x in cnl:
                # id of card
                suit_no=self.suit_number(x)[0]
                suit_key=self.suit_number(x)[1]
                lp=' '
                if suit_no==10:
                   lp=''
                card_pic+='|'+self.card_str[suit_no]+self.card_pic_small[suit_key]+lp+'     |   '
            card_pic+='\n'
            for x in cnl:
                #empty space
                card_pic+=self.card_pad
            card_pic+='\n'
            for x in range(1,6): # 5 sections make up a card pic
                                
                for pn in cnl:
                    # pics of cards
                    suit_no=self.suit_number(pn)[0]
                    suit_key=self.suit_number(pn)[1]
                    card_pic+=self.card_pic[suit_no][x]
                    card_pic=card_pic.replace('xx',self.card_pic_small[suit_key])
                card_pic+='\n'        
            for x in cnl:
                #empty space
                
                card_pic+=self.card_pad
            card_pic+='\n'    
            for x in cnl:
                #bottom id of card
                
                suit_no=self.suit_number(x)[0]
                suit_key=self.suit_number(x)[1]
                lp=' '
                if suit_no==10:
                   lp=''
                card_pic+='|     '+lp+self.card_str[suit_no]+self.card_pic_small[suit_key]+'|   '
            card_pic+='\n'
            for x in cnl:
                # bottom of card
                card_pic+=self.card_bot
            card_pic+='\n'
           
            return card_pic            

    def print_cards(self,card_number_list):
            print(self.get_card_pics(card_number_list))
           

    def get_random_card(self):
        val=random.randrange(0,len(self.deck))
        card=self.deck[val]
        
        #put card in inplay cards
        self.cards_in_play.append(card)
        #remove from deck
        self.deck.remove(card)
        return card
    
    
       
d=Deck()
p1=Player('Robert',d)
p2=Player('Dealer',d)
#print(d.deck)
cnl=[]

p2.make_dealer()
p1.make_player()
p1.pay_money(2,p2)
p1.take_card(d.get_random_card())
print(p1.get_name()+' has '+p1.get_money_in_wallet()+' credits')
print(d.print_cards(p1.get_cards())

"""
for i in range(1,3):
    card=d.get_random_card()
    cnl.append(card)
d.print_cards(cnl)

    
#d.print_card(i for i in range(1,53))
#print(d.deck)
#print(d.cards_in_play)
#d.reset_deck()
#print(d.deck)
#print(d.cards_in_play)
"""
