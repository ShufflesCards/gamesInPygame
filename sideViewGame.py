# Benjamin Kellman
# 3/18/25

# side view game
# I will finish this then topDownGame


# look at platform_moving


import pygame


# make entity class
# player extends from that

# spikes in a seperate class
# have that offset from a platform
# function update: rect.x rect.y offset from moving platform rect.x rect.y

class Player(pygame.sprite.Sprite):
    maxSpeed = 8
    # describe self as the object, the instance of the class
    def __init__ (self, img, mainCharachter, imageScalel=1): 
        super().__init__() # Box is a child class calling its parent pygame.sprite.Sprite
        self.score = 0

        self.dx = 0
        self.dy = 0
        self.mainCharachter = mainCharachter
        # x pos, y pos, x velocity, y velocity
        self.imageScale = 0.05

        
        self.imageWidth = (pygame.image.load(img).get_width())*self.imageScale
        self.imageHeight = (pygame.image.load(img).get_height())*self.imageScale

        self.image = pygame.transform.scale_by(pygame.image.load(img), self.imageScale).convert()
        self.rect = self.image.get_rect(center = (800, 200))

        # list of sprites we can collide with
        self.level = None

    def __str__(self):
        return f"({self.rect.x}, {self.rect.y})   <{self.dx}, {self.dy}>"

    def update(self):
        
        # gravity
        self.calc_grav()

        self.calc_friction()

        # move left and right
        self.rect.x+=self.dx
        

        '''
        if (self.dy>self.maxSpeed):
            self.dy=self.maxSpeed
        elif (self.dy<-self.maxSpeed):
            self.dy= -self.maxSpeed
        '''

        # check collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dx>0:
                # when moving right and hitting something. our right side hits the left side of the barrier
                self.rect.right = block.rect.left
            elif self.dx<0:
                self.rect.left = block.rect.right
            
            self.dx=0


        # move up and down
        self.rect.y+=self.dy

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.dy>0:
                # going down
                self.rect.bottom = block.rect.top
            elif self.dy<0:
                self.rect.top = block.rect.bottom
            
            # stop moving down because we hit a block 
            self.dy=0

            if isinstance(block, MovingPlatform):
                # checks if what we hit is a moving platform
                self.rect.x+=block.dx

        collectable_hit_list = pygame.sprite.spritecollide(self, self.level.collectable_list, True)
        for item in collectable_hit_list:
            self.score += 1
            print(self.score)
        

        # hitting an enemy
        if self.mainCharachter:
            enemys_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
            for enemy in enemys_hit_list:
                if self.rect.y >= enemy.rect.y: # remove the = to make it so you an go through enemys
                    if self.dx>0:
                        # when moving right and hitting something. our right side hits the left side of the enemy
                        #self.rect.right = enemy.rect.left
                        self.dx = -self.dx *1.1 - 15
                    elif self.dx<0:
                        #self.rect.left = enemy.rect.right
                        self.dx = -self.dx *1.1 + 15
                if self.dy>0:
                    # going down
                    #self.rect.bottom = enemy.rect.top
                    self.dy = -self.dy *1.1 - 2
                    if self.dy <= -15:
                        self.dy = -15


        
        
    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list)>0 or self.rect.bottom >= screen_height:
            self.dy = -11

    def calc_grav(self):
        
        # checking if we are on the Moon for low gravity
        if self.level.level_type == "Moon":
            if self.dy == 0:
                self.dy = 0.5
            else:
                self.dy+=0.4
        else:
            if self.dy==0:
                self.dy=1
            else:
                self.dy+=0.5

        # check if we are grounded
        if self.rect.y >= screen_height - self.rect.height and self.dy>=0:
            self.dy=0
            self.rect.y = screen_height - self.rect.height
    
    def calc_friction(self):
        if self.level.level_type == "Ice":
            print("ice")
        else:
            if self.dx<0.5 and self.dx > -0.5:
                self.dx = 0
            elif self.dx>=0.5:
                self.dx/=1.1
            elif self.dx<=-0.5:
                self.dx/=1.1

class Collectable(pygame.sprite.Sprite):
    def __init__(self, dx, dy):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.dx=dx
        self.dy=dy
    
    def update(self):
        self.rect.y+=self.dy
        self.rect.x+=self.dx

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """ # we get parameter of width and height, and the code will set rect.x and rect.y, and player to the platform
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    dx = 0
    dy = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    level = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """


        # left right 
        self.rect.x+=self.dx

        # check collision with player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.dx<0:
                # platform moving left
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
        
        # up down
        self.rect.y+=self.dy

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # we hit the player and are assuming we will not move the player into anything
            if self.dy<0:
                # moving up
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
        
        # Check the boundaries and see if we need to reverse direction
        if (not self.dy == 0) and (self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top):
            self.dy *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if (not self.dx == 0) and (cur_pos < self.boundary_left or cur_pos > self.boundary_right):
            self.dx *= -1

class Level(object):
    """ This is a generic super-class used to define a level.
    Create a child class for each level with level-specific
    info. """
    # big parent to all levels made



    def __init__(self, player):
        # list of sprites for levels
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.collectable_list = pygame.sprite.Group()
        self.player = player

        # background image
        self.background = None

        # how far the world has shifted left and right
        self.world_shift = 0
        self.level_limit = -1000

        # adding level types to change things like friction and jump height for later
        self.level_type_list = ["Normal", "Ice", "Moon"]
        self.level_type = None

    def update(self):
        # update everything in this level
        self.platform_list.update()
        self.enemy_list.update()
        self.collectable_list.update()
    
    def draw(self, screen):
        # draw everything in this level

        screen.fill(BLUE)

        #draw all sprite lists part of the level (not player or stuff not just on this level)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.collectable_list.draw(screen)
    
    def shift_world(self, shift_x):
        # moving left and right moves the world

        self.world_shift += shift_x

        # go though all the sprite groups and shift them
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for collectable in self.collectable_list:
            collectable.rect.x += shift_x


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1500
        self.level_type = self.level_type_list[0]


        # level is 800x600
        # player starts at x=240
        # Array with width, height, x, and y of platform
        level = [[200, 70, 450, 530],
                 [200, 70, 800, 430],
                 [50, 50, 1300, 400],
                 [50, 50, 1500, 325],
                 [50, 50, 1300, 250],
                 [10, 600, 2600, 0] # level limit
                 ]

        # x, y, dx, dy
        collectables = [[1500,100,0,0]]
        

        # Array with width, height, x, y, left boundry, right boundry, top boundry, bottom boundry, dx, dy
        # if not moving vertically, set dy to 0
        # if not moving horizontally, set dx to 0
        # bounds will not matter
        movingplatforms = [[100, 50, 200, 300, 200, 500, None, None, 1, 0]]
        
        enemys = [[100, 100]]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        
        
        for moving in movingplatforms:
            block = MovingPlatform(moving[0], moving[1])
            block.rect.x = moving[2]
            block.rect.y = moving[3]
            block.boundary_left = moving[4]
            block.boundary_right = moving[5]
            block.boundary_top = moving[6]
            block.boundary_bottom = moving[7]
            block.dx = moving[8]
            block.dy = moving[9]
            block.player = self.player
            block.level = self
            self.platform_list.add(block)
        

        for collectable in collectables:
            item = Collectable(collectable[2],collectable[3])
            item.rect.x = collectable[0]
            item.rect.y = collectable[1]
            self.collectable_list.add(item)
        
        for enemy in enemys:
            dude = Player(img, False)
            dude.rect.x = enemy[0]
            dude.rect.y = enemy[1]
            dude.level = self
            self.enemy_list.add(dude)
            

class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000
        self.level_type = self.level_type_list[2]

        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
                   

background_colour = (234, 212, 252) 
screen_width = 800
screen_height = 600
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
screen = pygame.display.set_mode([screen_width, screen_height]) 
pygame.display.set_caption('Window Caption') 



img = "theBox.png"
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 20)
player = Player(img, True)

# Make all the levels
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))

# Set the current level 
current_level_no = 0
current_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = current_level


player.rect.x=240
player.rect.y=screen_height-player.rect.height
active_sprite_list.add(player)


while True: 
    # Figure out if it was an arrow key. If so
    # adjust speed.
    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if player.dx >= -player.maxSpeed:
            player.dx-=1
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if player.dx <= player.maxSpeed:
            player.dx+=1
        
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.jump()

    # for loop through the event queue   
    for event in pygame.event.get(): 
        
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()

    # update the player
    active_sprite_list.update()

    # update items in level
    current_level.update()
    
    # If the player gets near the right side, shift the world left (-x)
    if player.rect.right >= screen_width//1.4:
        diff = player.rect.right - screen_width//1.4
        player.rect.right = screen_width//1.4
        current_level.shift_world(-diff)

    # If the player gets near the left side, shift the world right (+x)
    if player.rect.left <= screen_width//3.5:
        diff = screen_width//3.5 - player.rect.left
        player.rect.left = screen_width//3.5
        current_level.shift_world(diff)


    # If we reach the end of the level, go to the next one
    current_positioin = player.rect.x + current_level.world_shift

    if current_positioin < current_level.level_limit:
        player.rect.x = screen_width//3.5
        if current_level_no < len(level_list)-1:
            current_level_no+=1
            current_level = level_list[current_level_no]
            player.level = current_level
        else:
            print("Game over") # add something better








    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    current_level.draw(screen)
    active_sprite_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()












    # pos = pygame.mouse.get_pos()

    # player.rect.x = pos[0]
    # player.rect.y = pos[1]
    
    


    
    


