import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Circles")

# Set up circle properties
circle_radius = 20
circle_color = (255, 0, 0)  # Red

# Set up initial circle position
circle_x = width // 2
circle_y = height // 2

#
circle_N = 1

# Set up clock to control the frame rate
clock = pygame.time.Clock()

class CircularObject:

    def __init__(self, radius=20, Vx = 10, Vy = 10, color = (255, 0, 0)):

        self.x = width // 2
        self.y = height // 2
        self.Vx = Vx
        self.Vy = Vy
        self.nnV = math.sqrt(self.Vx**2+self.Vy**2)
        self.mass = 20
        self.radius = radius
        self.color = color
        self.is_outside = False

    def update(self):

        self.x += self.Vx
        self.y += self.Vy

        if not self.is_outside and (( 0 < self.x < width and  0 < self.y < height)== False):

            self.Vy = math.cos(random.uniform(0,math.pi*2)) * 5
            self.Vx = math.sin(random.uniform(0,math.pi*2)) * 5

            self.is_outside = True

            self.x = circle_x
            self.y = circle_y

            self.duplicate()

        else:
            self.is_outside = False

    def duplicate(self):

        if random.randint(0,10) < 2:

            randomColor = []
            for i in range(3):
                randomColor.append(random.uniform(0,255))

            objects.append(CircularObject(self.radius*0.75, self.Vx/2, self.Vy/2, randomColor))
            objects.append(CircularObject(self.radius*0.75, -self.Vx/2, -self.Vy/2, randomColor))


circle1 = CircularObject()

objects = [circle1]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((255, 255, 255))  # White background

    for object in objects:
        pygame.draw.circle(screen, object.color, (object.x, object.y), object.radius)
    
    for object in objects: 
        object.update()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)  # Adjust the value to control the speed of the animation
