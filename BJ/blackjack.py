import pygame
from deck import *
from constants import *
import sys
import time


pygame.init()

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('BlackJack')
gameDisplay.fill(background_color)
pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))

###text object render
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def end_text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


#game text display
def game_texts(text, x, y):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

 
def game_finish(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def black_jack(text, x, y, color):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    
#button display
def button(msg, x, y, w, h, ic, ac, action=None, *args):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 != None:
            action(*args)
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    TextSurf, TextRect = text_objects(msg, font)
    TextRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(TextSurf, TextRect)


class Play:
    #Set the initial parameters for the game to be played
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.card_coord = 672
        self.deal_coord = 672
        self.stand_pressed = 0
        self.has_hit = False
        self.can_split = False
        self.has_split = False
        
    
    #Function to see if a blackjack happened
    def blackjack(self):

        self.dealer.calc_hand()
        self.player.calc_hand()

        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.value == 21 and self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (672, 200))
            black_jack("Both with BlackJack!", 500, 80, grey)
            time.sleep(4)
            self.play_or_exit()
        elif self.player.value == 21:
            gameDisplay.blit(show_dealer_card, (672, 200))
            black_jack("You got BlackJack!", 500, 80, green)
            time.sleep(4)
            self.play_or_exit()
        elif self.dealer.value == 21:
            gameDisplay.blit(show_dealer_card, (672, 200))
            black_jack("Dealer has BlackJack!", 520, 80, red)
            time.sleep(4)
            self.play_or_exit()


    #Function to deal the hand
    def deal(self):
        #Add cards to the dealer and player hands
        for i in range(2):
            self.dealer.add_card(self.deck.deal())
            self.player.add_card(self.deck.deal())

        #Display the dealer card and player cards
        self.dealer.display_cards()
        self.player.display_cards()
        self.player_card = 1
        dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        game_texts("Dealer's hand:", 400, 150)

        gameDisplay.blit(dealer_card, (600, 200))
        gameDisplay.blit(dealer_card_2, (672, 200))

        game_texts("Your hand:", 400, 400)
        
        gameDisplay.blit(player_card, (600, 450))
        gameDisplay.blit(player_card_2, (672, 450))
        
        #Determine the player cards can be split
        if self.player.can_split():
            self.can_split = True
        
        #Check for a blackjack 
        self.blackjack()
            

    #Function to hit on the current hand
    def hit(self, hand = None, coord = None):
        if hand is None:
            hand = self.player
            coord = self.card_coord
    
        #Add a card to the hand and make sure to place it 
        # at the correct coordinate based on how many cards are in the hand
        if len(hand.cards) != 0:
            self.player_card = len(hand.card_img) - 1
            self.has_hit = True
            hand.add_card(self.deck.deal())
            coord += (len(hand.cards) - 2) * 72
            self.player_card += 1

            hand.calc_hand()
            hand.display_cards()
            player_card = pygame.image.load('img/' + hand.card_img[self.player_card] + '.png').convert()
            gameDisplay.blit(player_card, (coord, 450))

            #If the hit is a bust display a message and either end the game or
            # move to the next hand if the hand has been split
            if hand.value > 21:
                if not self.has_split:
                    show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
                    gameDisplay.blit(show_dealer_card, (672, 200))
                    game_finish("You Busted!", 500, 80, red)
                    time.sleep(4)
                    self.play_or_exit()
                elif self.has_split and self.stand_pressed == 0:
                    game_finish("You Busted!", 450, 650, red)
                    self.hand_1_bust = True
                    self.stand_split_hand()
                elif self.has_split and self.stand_pressed == 1:
                    game_finish("You Busted!", 1000, 650, red)
                    self.hand_2_bust = True
                    self.stand_split_hand()
            

    #Function to stand on the current cards and end the game 
    def stand(self):
        #Display the dealer hidden card
        if len(self.player.cards) != 0:
            show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            gameDisplay.blit(show_dealer_card, (672, 200))

            self.dealer.calc_hand()
            self.player.calc_hand()
            self.dealer_card = 1

            #Run out dealer cards until 17 is hit
            while self.dealer.value < 17:
                self.deal_coord += 72
                self.dealer_card += 1
                self.dealer.add_card(self.deck.deal())
                self.dealer.display_cards()
                dealer_card = pygame.image.load('img/' + self.dealer.card_img[self.dealer_card] + '.png').convert()
                gameDisplay.blit(dealer_card, (self.deal_coord, 200))
                self.dealer.calc_hand()

            #Display the results of the hand
            if self.dealer.value > 21:
                game_finish("Dealer Busts", 500, 80, green)
                time.sleep(4)
                self.play_or_exit()
            elif self.player.value > self.dealer.value:
                game_finish("You Won!", 500, 80, green)
                time.sleep(4)
                self.play_or_exit()
            elif self.player.value < self.dealer.value:
                game_finish("Dealer Wins!", 500, 80, red)
                time.sleep(4)
                self.play_or_exit()
            else:
                game_finish("It's a Tie!", 500, 80, grey)
                time.sleep(4)
                self.play_or_exit()


    #Function to double the bet
    def double(self, hand = None, coord = None):
        if hand is None:
            hand = self.player
            coord = self.card_coord

        #Make sure the player has not already hit on the cards
        if self.has_hit == False and len(hand.cards) != 0:
            #Deal only one card to the player and continue by calling the stand function
            hand.add_card(self.deck.deal())
            coord += 72
            self.player_card += 1

            hand.calc_hand()
            hand.display_cards()
            player_card = pygame.image.load('img/' + hand.card_img[self.player_card] + '.png').convert()
            gameDisplay.blit(player_card, (coord, 450))
                
            if hand.value > 21:
                show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
                gameDisplay.blit(show_dealer_card, (672, 200))
                game_finish("You Busted!", 500, 80, red)
                time.sleep(4)
                self.play_or_exit()
            else:
                self.stand()


    #Function to split the current cards
    def split(self):
        #See if hand is eligible for split
        if self.can_split and not self.has_hit:
            self.has_split = True
            self.hand_1_bust = False
            self.hand_2_bust = False
            gameDisplay.fill(background_color)
            pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
            pygame.display.update()

            #Create a second hand to play
            self.player2 = Hand()
            for i in range(2):
                self.player2.add_card(self.deck.deal())

            tmp = self.player.cards[1]
            self.player.cards[1] = self.player2.cards[0]
            self.player2.cards[0] = tmp

            self.player.display_cards()
            self.player2.display_cards()

            #Display the dealer and both player hands
            game_texts("Dealer's hand", 500, 150)
            game_texts("Your hand:", 500, 400)
            player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
            player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()
            player2_card = pygame.image.load('img/' + self.player2.card_img[0] + '.png').convert()
            player2_card_2 = pygame.image.load('img/' + self.player2.card_img[1] + '.png').convert()
            dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
            dealer_card_2 = pygame.image.load('img/back.png').convert()

            gameDisplay.blit(dealer_card, (600, 200))
            gameDisplay.blit(dealer_card_2, (672, 200))
            gameDisplay.blit(player_card, (300, 450))
            gameDisplay.blit(player_card_2, (372, 450))
            gameDisplay.blit(player2_card, (850, 450))
            gameDisplay.blit(player2_card_2, (922, 450))

            self.play_split_hand(hand_=self.player, coord_=372)
            self.play_split_hand(hand_=self.player2, coord_=922)


    #Play the split cards
    def play_split_hand(self, hand_, coord_):
        #Set up button clicks for when playing a split hand
        self.split_hands_played = 0
        while self.split_hands_played < 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #button("Deal", 30, 100, 150, 50, light_slat, dark_slat, self.deal)
                button("Hit", 30, 200, 150, 50, light_slat, dark_slat, self.hit, hand_, coord_)
                button("Stand", 30, 300, 150, 50, light_slat, dark_slat, self.stand_split_hand)
                #button("Double", 30, 400, 150, 50, light_slat, dark_slat, self.double, hand_, coord_)
                #button("Split", 30, 500, 150, 50, light_slat, dark_slat)
                button("EXIT", 30, 600, 150, 50, light_slat, dark_red, self.exit)

                #If both split hands have been played get out of this loop
                if self.stand_pressed == 2:
                    break

            pygame.display.flip()
            clock.tick(30)


    #Stand function for when the cards have been split
    def stand_split_hand(self):
        #Increment the amount of times the stand button was pressed
        #Increment the amount of split hands that have been played
        self.stand_pressed += 1
        self.split_hands_played += 1

        #If both split hands have been stood on, display the results
        if self.stand_pressed == 2:
            dealer_bust = False
            show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            gameDisplay.blit(show_dealer_card, (672, 200))

            self.dealer.calc_hand()
            self.player.calc_hand()
            self.player2.calc_hand()
            self.dealer_card = 1

            while self.dealer.value < 17:
                self.deal_coord += 72
                self.dealer_card += 1
                self.dealer.add_card(self.deck.deal())
                self.dealer.display_cards()
                dealer_card = pygame.image.load('img/' + self.dealer.card_img[self.dealer_card] + '.png').convert()
                gameDisplay.blit(dealer_card, (self.deal_coord, 200))
                self.dealer.calc_hand()

            #After displaying the dealer hidden card and rest of draw display
            # the results for both hands in the split
            if self.dealer.value > 21:
                game_finish("Dealer Busts", 500, 80, green)
                dealer_bust = True

            if self.player.value > self.dealer.value and not dealer_bust and not self.hand_1_bust:
                game_finish("You Won!", 400, 650, green)
            elif self.player.value < self.dealer.value and not dealer_bust and not self.hand_1_bust:
                game_finish("Dealer Wins!", 420, 650, red)
            elif self.player.value == self.dealer.value and not dealer_bust and not self.hand_1_bust:
                game_finish("It's a Tie!", 400, 650, grey)

            if self.player2.value > self.dealer.value and not dealer_bust and not self.hand_2_bust:
                game_finish("You Won!", 1000, 650, green)
            elif self.player2.value < self.dealer.value and not dealer_bust and not self.hand_2_bust:
                game_finish("Dealer Wins!", 1000, 650, red)
            elif self.player2.value == self.dealer.value and not dealer_bust and not self.hand_2_bust:
                game_finish("It's a Tie!", 1000, 650, grey)

            time.sleep(4)
            self.play_or_exit()


    #Exit the UI upon click of the exit button
    def exit(self):
        sys.exit()
    

    #Clean up the UI and values for the next hand
    def play_or_exit(self):
        self.player.value = 0
        self.dealer.value = 0
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.card_coord = 672
        self.deal_coord = 672
        self.has_hit = False
        self.can_split = False
        self.has_split = False
        self.stand_pressed = 0
        gameDisplay.fill(background_color)
        pygame.draw.rect(gameDisplay, grey, pygame.Rect(0, 0, 250, 700))
        pygame.display.update()

        
play_blackjack = Play()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        button("Deal", 30, 100, 150, 50, light_slat, dark_slat, play_blackjack.deal)
        button("Hit", 30, 200, 150, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Stand", 30, 300, 150, 50, light_slat, dark_slat, play_blackjack.stand)
        button("Double", 30, 400, 150, 50, light_slat, dark_slat, play_blackjack.double)
        button("Split", 30, 500, 150, 50, light_slat, dark_slat, play_blackjack.split)
        button("EXIT", 30, 600, 150, 50, light_slat, dark_red, play_blackjack.exit)
    
    pygame.display.flip()