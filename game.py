#Ashwin Thirukkumaran, Surya Kamalakannan, Hargun Dosanjh & Eric Tran
#all the imports
import pygame
import random
from pygame import mixer
import time



# Initializing pygame/mxier
pygame.init()
mixer.init()

#variables to limit the speed in which the game can run at (fixes the frame rate):
clock = pygame.time.Clock()
FPS = 60

#game variables
GRAVITY = 0.38
TILE_SIZE = 40

SCREEN_WIDTH = 1000
# When you multiply it returns a float, you have to turn it back into an int
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Legends of the Arena')
#--------------------
#Defining movement variables
moving_left = False
moving_right = False
moving_left2 = False
moving_right2 = False
shoot = False
shoot2 = False
start_game = False
clicked = False


#loading music and sounds
#background music

pygame.mixer.music.load('music_sound/clean_music.mp3')
pygame.mixer.music.set_volume(0.3) #volume intensity
pygame.mixer.music.play(-1,0.1,6000) #arguments(amount of times u want to loop, delay, duration of fade)
                                                  #^ -1 means forever                       ^5000 = 5s
                                                  
#sound affects
slice_attack_fx = pygame.mixer.Sound('music_sound/slice_attack.mp3')
slice_attack_fx.set_volume(0.3)
jump_fx = pygame.mixer.Sound('music_sound/jump.mp3')
jump_fx.set_volume(0.3)
super_sayin_fx = pygame.mixer.Sound('music_sound/super_sayin_power_up.mp3')
super_sayin_fx.set_volume(0.7)
instant_T = pygame.mixer.Sound('music_sound/instant_T.mp3')
instant_T.set_volume(0.1)
healing_fx = pygame.mixer.Sound('music_sound/mini_healing.mp3')
healing_fx.set_volume(10)                                              






#loading images
# slice attack (zoro attack)
slice_img = pygame.image.load('shoot/zoro1_4.png').convert_alpha() # convert_alpha makes better images
aura_img = pygame.image.load('shoot/aura.png').convert_alpha() # convert_alpha makes better images
aura_img = pygame.transform.scale(aura_img, (int(aura_img.get_width() * 0.06), int(aura_img.get_height() * 0.06)))#scaling the image
#corono image
powerUp_1 = pygame.image.load('images/drink.png').convert_alpha() 
powerUp_1 = pygame.transform.scale(powerUp_1, (int(powerUp_1.get_width() * 0.2), int(powerUp_1.get_height() * 0.2)))#scaling the image
#rice image
powerUp_2 = pygame.image.load('images/rice.png').convert_alpha() 
powerUp_2 = pygame.transform.scale(powerUp_2, (int(powerUp_2.get_width() * 0.25), int(powerUp_2.get_height() * 0.25)))#scaling the image

#background image
#background_img = pygame.image.load('images/Background.png').convert_alpha()
background_img = pygame.image.load('images/BG.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (int(background_img.get_width() *2), int(background_img.get_height() *3.19)))#scaling the image

#starting screen images
title_img = pygame.image.load('images/title.png').convert_alpha()
zoro_start_img = pygame.image.load('images/zoro_player.png').convert_alpha()
zoro_start_img = pygame.transform.scale(zoro_start_img, (int(zoro_start_img.get_width() *0.8), int(zoro_start_img.get_height() *0.8)))#scaling the image
goku_start_img = pygame.image.load('images/goku_player.png').convert_alpha()
goku_start_img = pygame.transform.scale(goku_start_img, (int(goku_start_img.get_width() *0.8), int(goku_start_img.get_height() *0.8)))#scaling the image
vs_img = pygame.image.load('images/background.jpg').convert_alpha()
vs_img = pygame.transform.scale(vs_img, (int(vs_img.get_width() *1.3), int(vs_img.get_height() *1.3)))#scaling the image





#power up dictionary
item_powerUp = {
    'Drink'     : powerUp_1,
    'Rice'      : powerUp_2

}

#power Up image






#define colors:
background_color = (100, 30, 0)
beige = (245,245,220)
blueish = (148, 224, 224)
red = (247, 13, 26)
black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)


#function to refresh the screen rate
def draw_bg():
    screen.fill(background_color)
    screen.blit(background_img, (0, 0))
#drawing the background for starting screen
def VS_BG():
    screen.blit(vs_img,(-400,-500))







#--------------------
#Craete the character
#this class has general property for all characters
class Character(pygame.sprite.Sprite):
    def __init__(self, char_name, which_character, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.alive = True
        #seting up which character   
        self.char_name = char_name
        #goku super sayin:
        self.is_super = False
        #health stat:
        self.health = 100
        self.max_health = self.health
        #giving speed:
        self.speed = speed
        #shooting cooldown timer 
        self.attack_cooldown = 0
        #direction (1 means right; -1 means left)            
        self.direction = 1
        self.flip = False
        #jump physics and jump animation:
        self.jump = False
        self.jump_velocity = 0
        self.air_born = True        
        #creating a list for my animations
        self.zoro_animation_list = []
        self.goku_animation_list = []
        self.goku_super_animation_list = []
        self.which_character = which_character
        self.index_frame = 0
        #super sayin variables
        self.super_start_time = None
        #what action is currently running: 0->idle 1->run
        self.action = 0
        #as soon as this class is created the time will start, we use this as reference for the animation cooldown...etc
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        
#------------------------------------------------
        #-->ZORO ANIMATIONS
        #------------------------ Idle Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/zoro_images/idle/zoro1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.zoro_animation_list.append(temp_list)        
        temp_list = [] 
        #------------------------ Run Animation
        for i in range(8):
        # loading in character  
            img = pygame.image.load(f'animations/zoro_images/run/zoro1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.zoro_animation_list.append(temp_list)
        temp_list = []  #resets temp list
        #------------------------ Jumping Animation
        for i in range(6):
        # loading in character  
            img = pygame.image.load(f'animations/zoro_images/jump/zoro1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.zoro_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Attack Animation
        for i in range(9):
        # loading in character  
            img = pygame.image.load(f'animations/zoro_images/attack/zoro1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.zoro_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Dead Animation
        for i in range(7):
        # loading in character  
            img = pygame.image.load(f'animations/zoro_images/dead/zoro1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.zoro_animation_list.append(temp_list)  
        temp_list = []
#------------------------------------------------    

        #-->GOKU ANIMATIONS
        #------------------------ Idle Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_images/idle/goku1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_animation_list.append(temp_list)        
        temp_list = [] 
        #------------------------ Run Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_images/run/goku1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_animation_list.append(temp_list)
        temp_list = []  #resets temp list
        #------------------------ Jumping Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_images/jump/goku1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Attack Animation
        for i in range(8):
        # loading in character  
            img = pygame.image.load(f'animations/goku_images/attack/goku1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Dead Animation
        for i in range(5):
        # loading in character  
            img = pygame.image.load(f'animations/goku_images/dead/goku1_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_animation_list.append(temp_list)   
        temp_list = []  #resets temp list
#------------------------------------------------
        
        #-->GOKU SUPER SAYIN Animation:
        #------------------------ Idle Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_super_images/idle/goku1_super_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_super_animation_list.append(temp_list)        
        temp_list = [] 
        #------------------------ Run Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_super_images/run/goku1_super_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_super_animation_list.append(temp_list)
        temp_list = []  #resets temp list
        #------------------------ Jumping Animation
        for i in range(4):
        # loading in character  
            img = pygame.image.load(f'animations/goku_super_images/jump/goku1_super_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_super_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Attack Animation
        for i in range(8):
        # loading in character  
            img = pygame.image.load(f'animations/goku_super_images/attack/goku1_super_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_super_animation_list.append(temp_list)  
        temp_list = []  #resets temp list
        #------------------------ Dead Animation
        for i in range(5):
        # loading in character  
            img = pygame.image.load(f'animations/goku_super_images/dead/goku1_super_{i}.png').convert_alpha() #by doing \f'{self.char_name}\ we are able to put different names and use different images
        # scaling image size
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        #storing the animations in the self.animation_list
            temp_list.append(img) #this will add all out images into one array
        self.goku_super_animation_list.append(temp_list)   
         
            
            
            
            
            
            
            
            
            
            
            
            
        
            

            
        
        





#^^^^^^^^^^^^^^^^^^
#so we have a 2-D array to store 2 types of list, 
# first list is a series of images for idle animation, 
# second list is a series of images for run animation
#third list is a series of images for jump animation
#third list is a series of images for attack animation
#fourth list is a series of images for the death animation

        if which_character == 1:
            #setting up self.image
            self.image = self.zoro_animation_list[self.action][self.index_frame] #---> [which animation][which image in that animation list]
            # puts an invisible rectangle around the sprite
            self.rect = self.image.get_rect()
            # giving initial coordinates
            self.rect.center = (x, y) 
            #assigning speed
        elif which_character == 2:
            #setting up self.image
            self.image = self.goku_animation_list[self.action][self.index_frame] #---> [which animation][which image in that animation list]
            # puts an invisible rectangle around the sprite
            self.rect = self.image.get_rect()
            # giving initial coordinates
            self.rect.center = (x, y) 
            #assigning speed            



    def update(self):
        self.animation_update()
        self.check_alive()
        #update cooldown
        if self.attack_cooldown > 0:
            #if fired a shot it lower power shot
            self.attack_cooldown -= 1 
    #speed method
    def move(self, moving_left, moving_right):
        #change in distance variables
        delta_x = 0
        delta_y = 0
        
        #assignmennt movement variales if moving left or right
        if moving_left: 
            delta_x = -self.speed
            #changing the direction the character is facing
            self.flip = True
            self.direction = -1
        if moving_right:
            delta_x = self.speed
            #changing the direction the character is facing
            self.flip = False
            self.direction = 1






        #jump
        #if w is pressed and character is not airborn
        if self.jump == True and self.air_born == False:
            self.jump_velocity = -15
            self.jump = False
            self.air_born = True # reseting
            jump_fx.play()

        #gravity
        self.jump_velocity += GRAVITY
        if self.jump_velocity > 10:
            self.jump_velocity
        
        delta_y += self.jump_velocity

        #check if on floor
        if self.rect.bottom + delta_y > 730: #if it is airborn then:
            delta_y = 729 - self.rect.bottom #this stops them at the floor
            self.air_born = False  #resets and says character is no longer in the air
            
        #hitting the left walls
        if self.rect.left + delta_x <= 0:
            delta_x = 0.1
            
        #hitting the right walls
        if self.rect.right + delta_x > SCREEN_WIDTH:
            delta_x = SCREEN_WIDTH - self.rect.right




        #changing the character postion (final return):
        self.rect.x += delta_x
        self.rect.y += delta_y
    
    #attack methdod
    def shot(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 45
        #sets a variable with the parameters of our class
            if self.char_name == 'zoro1':
                slice_attack = Attack(self.rect.centerx + (120*self.direction) - 10, self.rect.centery + (40), self.direction, self.char_name) #accessing the x ,y & direction of player1 (attributes which were already given to player1)
            elif self.char_name == 'goku1':
                slice_attack = Attack(self.rect.centerx + (120*self.direction) , self.rect.centery + (0), self.direction, self.char_name) #accessing the x ,y & direction of player1 (attributes which were already given to player1)
                                                         
            Attack_group.add(slice_attack) #adding slice_attack to the group
             #sound FX
            slice_attack_fx.play()

# Super Saiyan 3 seconds methods:
    def activate_super(self, current_time):
        self.is_super = True  # Set the player's super state to active.
        self.super_start_time = current_time  # starts recording the time

    # Deactivates the "super" state for the player, resetting the relevant properties
    def deactivate_super(self):
        self.is_super = False  # player is no longer super
        self.super_start_time = None  # restarts time

    # checks if the player has been in super sayin for 5 seconds and then deactivates super
    def update_player_state(self, current_time):
        if self.is_super and self.super_start_time is not None:  # checks if player is super
            if current_time - self.super_start_time > 5:  # checks if player has been super for more than 5 seconds
                self.deactivate_super()  #deactivate the super
            




    #animation method
    def animation_update(self):
        #explnation: my flipping through all the images fast enough it will become an animation
        which_character = self.which_character
            #if this character is 1 (zoro)
        if which_character == 1:
            animation_cooldown = 70
            #updating image depening on the time
            self.image = self.zoro_animation_list[self.action][self.index_frame]    


            #check if enough time has passed since the last update
            #explnation of code---> so we take teh current time and subtract it from the last time we checked the time ---> if it is greater than the animation_cooldown(70) then...
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.index_frame += 1 #changing the image
                self.update_time = pygame.time.get_ticks() #reseting timer
            else:
                None #nothing happens

            #if the animation is finished, then set back to the start, acces a specfic list in the 2D array
            if self.index_frame >= len(self.zoro_animation_list[self.action]):
                if self.action == 4:
                    self.index_frame = len(self.zoro_animation_list[self.action]) - 1
                else:
                    self.index_frame = 0
            
                #if this character is 2 (goku)
        elif which_character == 2 and not(player2.is_super):
            animation_cooldown = 70
            #updating image depening on the time
            self.image = self.goku_animation_list[self.action][self.index_frame]    


            #check if enough time has passed since the last update
            #explnation of code---> so we take teh current time and subtract it from the last time we checked the time ---> if it is greater than the animation_cooldown(70) then...
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.index_frame += 1 #changing the image
                self.update_time = pygame.time.get_ticks() #reseting timer
            else:
                None #nothing happens

            #if the animation is finished, then set back to the start, acces a specfic list in the 2D array
            if self.index_frame >= len(self.goku_animation_list[self.action]):
                if self.action == 4:
                    self.index_frame = len(self.goku_animation_list[self.action]) - 1
                else:
                    self.index_frame = 0
                    
        
        elif which_character == 2 and player2.is_super:
            animation_cooldown = 70
            #updating image depening on the time
            self.image = self.goku_super_animation_list[self.action][self.index_frame]    


            #check if enough time has passed since the last update
            #explnation of code---> so we take teh current time and subtract it from the last time we checked the time ---> if it is greater than the animation_cooldown(70) then...
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.index_frame += 1 #changing the image
                self.update_time = pygame.time.get_ticks() #reseting timer
            else:
                None #nothing happens

            #if the animation is finished, then set back to the start, acces a specfic list in the 2D array
            if self.index_frame >= len(self.goku_super_animation_list[self.action]):
                if self.action == 4:
                    self.index_frame = len(self.goku_super_animation_list[self.action]) - 1
                else:
                    self.index_frame = 0
        
        else:
            None
            
        #super sayin transformation
    
            
            
            
            
            
            
        
        

    #method will put the image on the scnree
    def draw(self):
        #it will transform the image (in this case flipping) --> argument (what am i flipping, x directtion flip, y direction flip)
        screen.blit(pygame.transform.flip(self.image, self.flip,False),self.rect)
                                #self.image -> what image             self.rect -> location of the image


        





    def update_action(self, new_action):
        #check if new action is different
        if new_action != self.action:
            self.action = new_action
            #updating animation
            self.index_frame = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)
            screen.blit(text1, textRect1)
        
            
    

#------------------------

class Item(pygame.sprite.Sprite):
                    #item_type: feed a string that corrosponds with 'item_powerUp' dictionary, which will access images
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)#inheriting the methods from sprite class    
        self.item_type = item_type
        self.image = item_powerUp[item_type] #takes images from dictionary
        self.rect = self.image.get_rect()
        self.rect.midtop = x + TILE_SIZE//2, y - (TILE_SIZE - self.image.get_height())
    
    def update(self):    
            #pygame.sprite.collide_rect checks the collison between player
            
            #check if there is collision between item(self) rectangle and player1(zoro)
        if pygame.sprite.collide_rect(self, player1):
            #check which powerUp 
            if self.item_type == 'Drink':
                healing_fx.play()
                if player1.health >= 50:   #max health is 100
                    player1.health = player1.max_health
                else:
                    player1.health += 50
                print("gain to " , player1.health)    
            elif self.item_type == 'Rice':
                None
            else:
                None
            self.kill()
            
            #check if there is collision between item(self) rectangle and player2(goku)
        if pygame.sprite.collide_rect(self, player2):  
            #if goku collides with rice -> make super sayin
            if self.item_type == 'Rice':
                #sets player.is_super to True
                player2.is_super = True
                current_time = time.time()  #starts timer
                player2.activate_super(current_time) 
                self.kill()
                super_sayin_fx.play()
            if self.item_type == 'Drink':
                self.kill()
                #nothing happens
                
    
    






class HealthBar():
    def __init__(self, x, y, health, max_health, color, color1):
                            #health -> currrent health
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.color = color
        self.color1 = color1

    def draw(self, health):
        if player2.is_super:     
            #update with new healths
            self.health = health
            #health ration
            ratio = self.health / self.max_health 
            pygame.draw.rect(screen, black, (self.x - 5, self.y - 5, 160, 30)) #border pt
            pygame.draw.rect(screen, blueish, (self.x, self.y, 150, 20))
                                                            #^width and heigth

            #since we want our blue bar ontop of the red bar...we draw that after the red bar is created
            pygame.draw.rect(screen, self.color1, (self.x, self.y, 150 * ratio, 20))

        else:
            #update with new healths
            self.health = health
            #health ration
            ratio = self.health / self.max_health 

            pygame.draw.rect(screen, black, (self.x - 5, self.y - 5, 160, 30)) #border pt
            pygame.draw.rect(screen, blueish, (self.x, self.y, 150, 20))
                                                            #^width and heigth

            #since we want our blue bar ontop of the red bar...we draw that after the red bar is created
            pygame.draw.rect(screen, self.color, (self.x, self.y, 150 * ratio, 20))
                                                                    #^if your health is 80%, then by multiplying 150 by 0.8, it only displays 80% of the bar

                        





#slice class
class Attack(pygame.sprite.Sprite): 
    def __init__(self, x, y, direction, character):
        pygame.sprite.Sprite.__init__(self) #inheriting the methods from sprite class
        self.character = character

        if self.character == 'zoro1': #if zoro then image is:
            self.image = slice_img 
        elif self.character == 'goku1': #if goku then image is:
            self.image = aura_img
        
            
        self.speed = 7
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    
    
    def update(self):
      
        
        
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet is off screen
        if self.rect.right < 0 or self.rect.left > (SCREEN_WIDTH):
            self.kill()
        

        if pygame.sprite.spritecollide(player1, Attack_group, False): #detects if the attack has hit another player
            if player1.alive:
                player1.health -= 10
                print("p1" , player1.health)
                self.kill() #it will delete the attack if true
        
        if pygame.sprite.spritecollide(player2, Attack_group, False): #detects if the attack has hit another player
            if player2.alive:
                #If Goku is super sayin then he takes no damage
                if player2.is_super:
                    instant_T.play()
                    None
                else:
                    player2.health -= 10
                    print("p2" , player2.health)
                    self.kill() #it will delete the attack if true


#By putting my attack slices in a group so we can apply functions/methods to them all
Attack_group = pygame.sprite.Group()
powerUp_group = pygame.sprite.Group()



















#--------------
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 10000)
#inilizing characters (name of character, x, y, scale, speed)
player1 = Character('zoro1', 1, 200, 200, 2, 5)
player2 = Character('goku1', 2, 600, 200, 2, 5)
#inilizing characters (x, y , current health, max health)
health_bar = HealthBar(10, 10, player1.health, player1.health, red, red)
health_bar2 = HealthBar(840, 10, player2.health, player2.health, red, gold)
                                                                #first color is what color the health bar should be normally
                                                                #second color is the health bar's color when goku is super sayin


font = pygame.font.Font('freesansbold.ttf', 45)
 
# create a text surface object,
# on which text is drawn on it.
text = font.render('Press Enter/Return', True, beige)
textRect = text.get_rect()
textRect.center = (500, 700)

text1 = font.render('Press Escape', True, beige)
textRect1 = text1.get_rect()
textRect1.center = (500, 150)





#--------------------
run = True
# The loop will run until we set run = False

while run:
    if start_game == False:
        #draw meny
        #screen.fill((51, 51, 77))
        VS_BG()
        screen.blit(title_img, (40,50))
        screen.blit(goku_start_img, (600,300))
        screen.blit(zoro_start_img, (30,300))
        
        screen.blit(text, textRect)
        
            #in the draw method we have a code that checks if button is clicked it sets start_game to True (starts game)
        if clicked:
            start_game = True
            clicked = False
   

    else:

        #frame rate:
        clock.tick(FPS)
        draw_bg()

       #checking is goku is super:
        current_time = time.time() #getting current time
        player2.update_player_state(current_time)#checks if player2 is super



        #update and draw slice attack
        Attack_group.update()
        Attack_group.draw(screen)


        player1.draw()
        #arguments  (moving_left, moving_right)
        player1.move(moving_left,moving_right)
        player1.update()
        #player health bar
        health_bar.draw(player1.health)
        powerUp_group.draw(screen)
        powerUp_group.update()

        

        player2.draw()
        #arguments  (moving_left, moving_right)
        player2.move(moving_left2,moving_right2)
        player2.update()  
        #player health bar 
        health_bar2.draw(player2.health)

        if player1.alive: #only works if player is alive
            #checking if there is any movment:
            if shoot:
                player1.shot()
                player1.update_action(3)#3 -> means attack
            elif player1.air_born:
                player1.update_action(2)#2 -> means jump
            elif moving_left or moving_right:
                player1.update_action(1)#1 -> means run
            else:
                #if he is not moving
                player1.update_action(0) #0 -> means idle
            #player1.move(moving_left,moving_right)

        if player2.alive: #only works if player is alive
            #checking if there is any movment:
            if shoot2:
                player2.shot()
                player2.update_action(3)#3 -> means attack
            elif player2.air_born:
                player2.update_action(2)#2 -> means jump
            elif moving_left2 or moving_right2:
                player2.update_action(1)#1 -> means run
            else:
                #if he is not moving
                player2.update_action(0) #0 -> means idle
            #player1.move(moving_left,moving_right)









    # Whenever an action is performed, this will register it
    for event in pygame.event.get():
        # If we click the exit button, it will end the loop
        if event.type == pygame.QUIT:
            run = False
        elif event.type == SPAWN_EVENT:
            # Create and add items every 10 seconds
            item1 = Item('Drink', random.randint(0, SCREEN_WIDTH), 300)
            powerUp_group.add(item1)
            item2 = Item('Rice', random.randint(0, SCREEN_WIDTH), 300)
            powerUp_group.add(item2)
            
            
            
        #looks for any keyboard buttons being pressed
        if event.type == pygame.KEYDOWN:
            #if the a_key is pressed:
            if event.key == pygame.K_a:
                moving_left = True
            #if the d_key is pressed:
            if event.key == pygame.K_d:
                moving_right = True
            #if escape button is pressed ----> quit game
            if event.key == pygame.K_ESCAPE:
                run = False
            #checking if w is pressed and player is alive
            if event.key == pygame.K_w and player1.alive:
                player1.jump = True
                print("jump")
            #shoot button
            if event.key == pygame.K_SPACE:
                shoot = True
                print("shoot")              
            #if enter is pressed to start game
            if event.key == pygame.K_RETURN or event.key == pygame.K_BACKSPACE:
            
                clicked = True
                print("game start")
            
        #---------------------Player 2 controls
            if event.key == pygame.K_LEFT:
                moving_left2 = True
            #if the d_key is pressed:
            if event.key == pygame.K_RIGHT:
                moving_right2 = True
            #checking if w is pressed and player is alive
            if event.key == pygame.K_UP and player2.alive:
                player2.jump = True
                print("jump")
            #shoot button
            if event.key == pygame.K_RSHIFT:
                shoot2 = True
                print("shoot")

            
            
        #if keyboard button is release:
        if event.type == pygame.KEYUP:
            #if the a_key is up:
            if event.key == pygame.K_a:
                moving_left = False
            #if the d_key is up:
            if event.key == pygame.K_d:
                moving_right = False
            #if the space_key is up
            if event.key == pygame.K_SPACE:
                shoot = False
                
                
                
        #---------------------Player 2 controls
            #if the a_key is up:
            if event.key == pygame.K_LEFT:
                moving_left2 = False
            #if the d_key is up:
            if event.key == pygame.K_RIGHT:
                moving_right2 = False
            #if the space_key is up
            if event.key == pygame.K_RSHIFT:
                shoot2 = False
                
                 


    pygame.display.update()
# Clean up and exit the game
pygame.quit()
exit()


     
        
        


       
