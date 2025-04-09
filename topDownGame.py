# Benjamin Kellman
# 3/18/25

# look at 
# move_with_walls
# maze_runner

import pygame
import random # for testing

class Box(pygame.sprite.Sprite):
    maxSpeed = 10
    # describe self as the object, the instance of the class
    def __init__ (self, dx, dy, img, imageScalel=1): 
        super().__init__() # Box is a child class calling its parent pygame.sprite.Sprite

        self.dx = dx
        self.dy = dy
        # x pos, y pos, x velocity, y velocity
        self.imageScale = 0.05
        self.imageWidth = (pygame.image.load(img).get_width())*self.imageScale
        self.imageHeight = (pygame.image.load(img).get_height())*self.imageScale
        self.image = pygame.transform.scale_by(pygame.image.load(img), self.imageScale).convert()
        self.rect = self.image.get_rect(center = (200, 200))

        #self.visualHitbox = pygame.Surface([self.imageWidth, self.imageHeight])


    def __str__(self):
        return f"({self.rect.x}, {self.rect.y})   <{self.dx}, {self.dy}>"

    def update(self, dt=1):

        # bounce off of screen walls
        if (self.rect.x>1200 or self.rect.x<0):
            self.dx *= -1
        if (self.rect.y>800 or self.rect.y<0):
            self.dy *= -1

        # move
        self.rect.x+=dt*self.dx
        self.rect.y+=dt*self.dy

        # max speed
        if (self.dx>self.maxSpeed):
            self.dx=self.maxSpeed
        elif (self.dx<-self.maxSpeed):
            self.dx= -self.maxSpeed

        if (self.dy>self.maxSpeed):
            self.dy=self.maxSpeed
        elif (self.dy<-self.maxSpeed):
            self.dy= -self.maxSpeed
        


        


    


        

background_colour = (234, 212, 252) 
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height]) 
pygame.display.set_caption('Window Caption') 

# list of sprites
# each Box is added
block_list = pygame.sprite.Group()

# list of every sprites
all_sprites_list = pygame.sprite.Group()

img = "theBox.png"
for i in range(10):
    block = Box(1, 1, img)
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    block_list.add(block)
    all_sprites_list.add(block)

player = Box(0, 0, img)
all_sprites_list.add(player)

clock = pygame.time.Clock()

pygame.key.set_repeat(1, 20)
score = 0
while True: 
    
# for loop through the event queue   
    for event in pygame.event.get(): 
        
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                player.dx-=1
                
            if keys[pygame.K_RIGHT]:
                player.dx+=1
                
            if keys[pygame.K_UP]:
                player.dy-=1
                
            if keys[pygame.K_DOWN]:
                player.dy+=1
    
    

    print(player.dx,player.dy)


    screen.fill(background_colour) 

    # pos = pygame.mouse.get_pos()

    # player.rect.x = pos[0]
    # player.rect.y = pos[1]
    player.update()

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)  # True deletes hit items, false doesn't

    for block in blocks_hit_list:
        score += 1
        print(score)

    for block in block_list:
        block.update()
    all_sprites_list.draw(screen)


    
    pygame.display.flip()
    clock.tick(60)

