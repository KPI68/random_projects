"""
This is a children's game. Shuffle and deal 4 cards from a deck. Compete
for the solution using all 4 cards, once each, applying addition, subtraction,
multiplication and division to come up the end result as 24. 
"""

import numpy as np
import random as rnd
        
seeds = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
suits = ['♠','♥','♣','♦']

# get_card and display_cards display the 4 cards
def get_card(card):
    suit = card[0]
    value = card[1:]  # 1: for '10'
    return (
        '┌─────────┐\n'
        '│{}       │\n'
        '│         │\n'
        '│    {}   │\n'
        '│         │\n'
        '│       {}│\n'
        '└─────────┘'
    ).format(
        format(value, ' <2'),
        format(suit, ' <2'),
        format(value, ' >2')
    ).splitlines()

def display_cards(cards):
    for lines in zip(*map(get_card, cards)):
        print(*lines)

# algorithm being to cover through all combinations in this way:
# In 4: 3+1 and 2+2; In 3: 2+1; In 2: +=*/
# since +-* both can have the operanes switch 
# as long as we cover the two directions with / 
# the upper levels need not mind the sequences

def toPlus(a,b):  
    return ['('+a[0]+'+'+b[0]+')',a[1]+b[1]]
def toMinus(a,b):
    return ['('+a[0]+'-'+b[0]+')',a[1]-b[1]]
def toTimes(a,b):
    return ['('+a[0]+'*'+b[0]+')',a[1]*b[1]]
def toDivide(a,b):
    if b[1]!=0 and int(a[1]/b[1])==a[1]/b[1]:
        return ['('+a[0]+'/'+b[0]+')',a[1]/b[1]]
    if a[1]!=0 and int(b[1]/a[1])==b[1]/a[1]:
        return ['('+b[0]+'/'+a[0]+')',b[1]/a[1]]

def calTwo(a,b):
    return [toPlus(a,b),toMinus(a,b),toTimes(a,b),toDivide(a,b)]

def calThree(a,b,c):
    ct = []
    for one in calTwo(b,c):
        if one!=None:
            ct += calTwo(a,one)
    for one in calTwo(a,b):
        if one!=None:
            ct += calTwo(c,one)
    for one in calTwo(a,c):
        if one!=None:
            ct += calTwo(b,one)
    return ct

def calThreeOne(a,b,c,d,verbose):
    cf=[]
    for one in calThree(a,b,c):
        if one!=None:
            for ct in calTwo(d,one):
                if ct!=None and (ct[1]==24 or ct[1]==-24 or verbose):
                    cf+=ct
    return cf

def calTwoTwo(a,b,c,d,verbose):
    cf=[]
    for one in calTwo(a,b):
        for two in calTwo(c,d):
            if one!=None and two!=None:
                for ct in calTwo(one,two):
                    if ct!=None and (ct[1]==24 or ct[1]==-24 or verbose):
                        cf+=ct
    return cf

class Cal24: 
    tried = []
    deck = []
    now4 = []
    for_one=False
    verbose=False
    
    #Two ways: 4 numbers provided in numbers or deal from a deck
    #To observe the algorithm we can use verbose=True
    def __init__ (self, numbers=[], verbose=False):
        self.for_one=len(numbers)==4
        self.verbose=verbose
        if self.for_one:
            self.now4=numbers
        else:
            for i in range(len(seeds)):
                for j in range(len(suits)):
                    self.deck.append(suits[j]+seeds[i])
        
    def shuffle(self):
        self.tried=[]
        self.deck=[]
        self.now4=[]
        self.__init__([], False)
        
    def deal(self):
    #each call deal 4 cards randomly, and return number of the remaining cards
        if len(self.deck)<4:
            print("All cards in the deck dealt.")
            return 0
        
        #pick 4 numbers randomly from 0-<number-of-cards-in-deck>
        rint=rnd.sample(range(0,len(self.deck)),4)
        
        #translate the random numbers into 4 cards <the_pick>
        #add the 4 cards to <tried>
        the_pick = []
        for i in range(4):
            self.tried.append(self.deck[rint[i]])
            the_pick.append(self.deck[rint[i]])
            
        #get the 4 numbers only from the cards
        self.now4=[seeds.index(i[1:])+1 for i in the_pick]
        
        #remove the 4 cards from the deck
        self.deck=[x for x in self.deck if x not in self.tried]
        
        #show the 4 cards
        display_cards(the_pick)
        
        #return the number of remaining cards
        return len(self.deck)

    def cal24(self):
        if len(self.now4)!=4:
            print("Deal or give 4 numbers 1-13 to play")
            return
        a=[str(self.now4[0]),self.now4[0]]
        b=[str(self.now4[1]),self.now4[1]]
        c=[str(self.now4[2]),self.now4[2]]
        d=[str(self.now4[3]),self.now4[3]]
        answer=(calThreeOne(a,b,c,d,self.verbose) +
                calThreeOne(a,b,d,c,self.verbose) +
                calThreeOne(a,c,d,b,self.verbose) +
                calThreeOne(b,c,d,a,self.verbose) +
                calTwoTwo(a,b,c,d,self.verbose) +
                calTwoTwo(a,c,b,d,self.verbose) +
                calTwoTwo(a,d,b,c,self.verbose)
               )
        if len(answer)==0:
            print("No solution.")
        else:
            print(answer)
    
#main
while 1==1:
    how=input("Give 4 card numbers(e.g.1 5 8 13) or Enter to deal from a deck: ")
    if how!='': #numbers input
        l4n=[int(i) for i in how.split(' ')]
        if len([n for n in l4n if n>=1 and n<=13])==len(l4n):
            Cal24(l4n).cal24() #show solution
        else:
            print("invalid numbers")
    else:
        break
    
#deal from deck
game=Cal24()
game.shuffle()

while 1==1:
    four_of=game.deal()
    input("Show answer")
    game.cal24()

    if four_of==0: 
        next_action=input("restart/quit: ")
        if next_action=="quit":
            break
        game.shuffle()
        continue
        
    if input(f"Next 4 of {four_of} /quit: ")=="quit":
        break
        