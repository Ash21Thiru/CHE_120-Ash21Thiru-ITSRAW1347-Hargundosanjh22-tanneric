import pygame




# Initializing pygame
pygame.init()


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
pygame.display.set_caption('Panadabuy Flash')
#--------------------
#Defining movement variables
moving_left = False
moving_right = False
moving_left2 = False
moving_right2 = False
start_game = False
clicked = False





#background image in loading screen
background_img = pygame.image.load('images/background.jpg').convert_alpha()
background_img = pygame.transform.scale(background_img, (int(background_img.get_width() * 4), int(background_img.get_height() * 4)))#scaling the image








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
       

        #giving speed:
        self.speed = speed

        
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
        self.is_super_cooldown = 0
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
        for i in range(6):
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
        for i in range(12):
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


        #gravity
        self.jump_velocity += GRAVITY
        if self.jump_velocity > 10:
            self.jump_velocity
        
        delta_y += self.jump_velocity

        #check if on floor
        if self.rect.bottom + delta_y > 730: #if it is airborn then:
            delta_y = 730 - self.rect.bottom #this stops them at the floor
            self.air_born = False  #resets and says character is no longer in the air
            




        #changing the character postion (final return):
        self.rect.x += delta_x
        self.rect.y += delta_y
    

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

        #background
        background_img = pygame.image.load('images/BG.png').convert_alpha()
        background_img = pygame.transform.scale(background_img, (int(background_img.get_width() * 4), int(background_img.get_height() * 4)))#scaling the image

        pygame.draw.rect(screen, beige, self.rect, 1) #remove/delete later (puts border around players)


    def update_action(self, new_action):
        #check if new action is different
        if new_action != self.action:
            self.action = new_action
            #updating animation
            self.index_frame = 0
            self.update_time = pygame.time.get_ticks()

   
#------------------------
#inilizing characters (name of character, x, y, scale, speed)
player1 = Character('zoro1', 1, 200, 200, 2, 5) #zoro
player2 = Character('goku1', 2, 600, 200, 2, 5) #goku







