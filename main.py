import pygame
import sys
import random
import numpy as np
import math
import pyautogui as pyag
import time
import threading

def calculate_centroid_np(points):
    points_array = np.array(points)
    centroid = np.mean(points_array, axis=0)
    return tuple(centroid)

def centroid_of_all_objects():
    points = []
    for object in objects:
        points.append([object.x,object.y])
    return calculate_centroid_np(points)

def percentage_change(chance):
    return random.uniform(0,1) < chance

WIDTH, HEIGHT = 1920, 1080
SCREEN_CENTER = [WIDTH // 2, HEIGHT // 2]
GRAVITY_STRENGTH = 1
AIR_RESISTANCE = 0.1

INITIAL_VELOCITY_VECTOR = [10,10]

class mouse_velocity_listener:

    def __init__(self):
        
        self.mouse_velocity = np.array([0,0])
        self.last_mouse_pos = np.array([0,0])

        self._listen_thread = threading.Thread(target=self._listener)
        self._listen_thread.start()

    def _listener(self):
        while True:
            new_mouse_pos = np.array(pyag.position())
            self.mouse_velocity = new_mouse_pos - self.last_mouse_pos
            time.sleep(0.01)
            self.last_mouse_pos = new_mouse_pos

mouseListener = mouse_velocity_listener()

#Objects
class CircularObject:

    def __init__(self, radius=100, Vx = 10, Vy = 10, color = (255, 0, 0), x = SCREEN_CENTER[0], y = SCREEN_CENTER[1]):

        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.mass = 20
        self.radius = radius
        self.color = color
        self.out_of_bounds = False
        self.alive = True
        self.bounces = 0

    def isInBounds(self):
        return 0 < self.x < WIDTH and 0 < self.y < HEIGHT
    
    def euclidian_velocity(self):
        return math.sqrt(self.x**2+self.y**2)
        
    def update(self):

        if self.isInBounds():
            self.out_of_bounds = False
        else:
            self.out_of_bounds = True
            self.reflect()
            if percentage_change(0.55) and self.euclidian_velocity() > 5:
                self.duplicate()

        self.move_by_velocity()
        self.gravity()
        self.old_age()
        
    def old_age(self):
        if self.bounces > 2:
            self.alive = False

    def reflect(self):  
        self.bounces += 1
        if self.x < 0 or self.x > WIDTH:
            self.Vx = -self.Vx
        if self.y < 0 or self.y > HEIGHT:
            self.Vy = -self.Vy
        
    def move_by_velocity(self):
        self.x += self.Vx
        self.y += self.Vy

    def drag(self):
        self.Vx *= AIR_RESISTANCE*self.radius
        self.Vy *= AIR_RESISTANCE*self.radius

    def gravity(self):
        self.Vy += GRAVITY_STRENGTH

    def resetPosition(self):
        self.x = SCREEN_CENTER[0]
        self.y = SCREEN_CENTER[1]

    def duplicate(self, color = None):

        if color == None:
            randomColor = [random.uniform(0, 255) for _ in range(3)]
            
        mouseX, mouseY = pyag.position()
        mouseX_velocity, mouseY_velocity = mouseListener.mouse_velocity
        objects.append(CircularObject(radius = np.linalg.norm([mouseX_velocity,mouseY_velocity]), Vx = mouseX_velocity, Vy = mouseY_velocity, color = randomColor, x = mouseX, y= mouseY))

#Sim
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Circles")

clock = pygame.time.Clock()
objects = [CircularObject()]
circle_N = 1
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Draw
    screen.fill((255, 255, 255))
    for object in objects:

        pygame.draw.circle(screen, object.color, (object.x, object.y), object.radius)

        if object.alive == False:
            objects.remove(object)
    
    #Update all objects
    for object in objects:
        object.update()

    pygame.display.flip()
    clock.tick(60)
