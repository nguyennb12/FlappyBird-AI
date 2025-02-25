import neat.statistics
import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 550
WIN_HEIGHT = 800

# Global Variable generation count
GEN = 0

BIRD_IMS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STATE_FONT = pygame.font.SysFont("comicsans", 50)


# Class Bird has all the properties of the flappy bird
#Defines a Bird class that simulates jumping and movement in a game by updating position, 
# velocity, and tilt angles based on physics calculations, handling upward 
# and downward motion with rotation limits.
class Bird: 
    IMGS = BIRD_IMS 
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self,x,y):
        self.x = x 
        self.y = y
        self.tilt = 0
        self.tick_count = 0 
        self.vel = 0 
        self.height = self.y
        self.img_count = 0 
        self.img = self.IMGS[0]
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0 
        self.height = self.y 
        
    def move(self):
        self.tick_count += 1
        
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if d >= 16:
            d = 16 
        
        if d < 0: 
            d -= 2
            
        self.y = self.y + d
        
        if d < 0 or self.y < self.height + 50: 
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90:
                self.tilt == self.ROT_VEL
                
# Check to see what image should be shown based on img count.         
#Defines a draw method that animates the bird by cycling through images based on img_count and tilt, 
# rotates the image, and renders it on the window. The get_mask method returns a 
# mask for collision detection. 
    def draw(self, win):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        if  self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
#Defines a Pipe class to create moving pipe obstacles for the game. It initializes pipes with random heights,
# moves them leftward, draws them on the screen, and checks for 
# collisions with the bird using masks for precise detection.
class Pipe: 
    GAP = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
    
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)  
        self.PIPE_BOTTOM = PIPE_IMG  
    
        self.passed = False
        self.set_height()

        
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self): 
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

        
    def collide(self, bird):
        bird_mask = bird.get_mask()  
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # bottom point
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        # top point
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

#Defines a Base class representing the moving ground in the game. 
# It uses two images to create a seamless scrolling effect by moving them leftward and resetting their positions when off-screen, 
# then draws them onto the window to simulate continuous motion.
class Base: 
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self, y):
        self.y = y 
        self.x1 = 0
        self.x2 = self.WIDTH 
    
    def move(self):
        self.x1 -= self.VEL  
        self.x2 -= self.VEL  
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

#Defines a draw_window function that renders the game's visuals 
# by drawing the background, pipes, score, generation number, 
# base, and birds onto the window, then updates the display.        
def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    
    text = STATE_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))    
    
    text = STATE_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))
        
    base.draw(win)
    for bird in birds:
        bird.draw(win) 
    pygame.display.update()


#Defines a Base class representing the moving ground in the game.
# It uses two images to create a seamless scrolling effect by moving them leftward and resetting their positions when off-screen, 
# then draws them onto the window to simulate continuous motion.
def main(genomes, config):
    global GEN 
    GEN += 1
    nets = []
    ge = []
    birds = []
    
    for _, g in genomes: 
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)
    
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
                
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                bird.jump()
        
        add_pipe = False
        rem = []
        
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                    
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            pipe.move()
        
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        if score > 10000: 
            break
        
        base.move()             
        draw_window(win, birds, pipes, base, score, GEN)

# Call the NEAT run function
# Defines a run function that configures and initiates the NEAT algorithm to evolve neural networks over 
# 50 generations using main as the fitness function, 
# and starts the process when executed directly.

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
