#Oribtal around Sun: earth, mars, venus, mercury (4 closest planets)

import pygame
import math
pygame.init()                                                      #intializes pygame

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))                  #main window we are going to draw on
pygame.display.set_caption("Planet Simulation")         

#Colorss
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
FONT = pygame.font.SysFont("comicsans", 16)

#Kilograms 
SUNMASS = 1.98892 * 10**30
EARTHMASS = 5.9742 * 10**24
MARSMASS = 6.39 * 10**23
VENUSMASS = 4.8685 * 10**24
MERCURYMASS = 3.10 * 10**23

#------------------------------  PLANETS -----------------------------

class Planet:
    AU = 149.6e6 * 1000                                             #Astronomical Units, 1 [Kilometers(149.6e6) to Meters(1000)] (average distance between Earth and the Sun)
    G = 6.67428e-11                                                 #Gravitial constant = force of attraction between objects
    SCALE = 200 / AU                                                # 1 AU = 100 pixels: The speed scale of planets orbitiing. Its hard to mimic planets speed on program so we scale it down by pixels.
    TIMESTEP = 3600 * 24                                            # 1 Day: Simulating the days 

    def __init__(self, x, y, radius, color, mass):
        self.x = x                                                  
        self.y = y
        self.radius = radius                                        
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
       

        self.x_vel = 0                                             
        self.y_vel = 0

    
    def draw(self, WINDOW):                                             #draws on to the screen (0,0 is top left hand, 0,800 top right hand, 800,800 bottom right hand)
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
         updated_points = []
         for point in self.orbit:
            x_draw, y_draw = point 
            x_draw = x_draw * self.SCALE + WIDTH / 2
            y_draw = y_draw * self.SCALE + HEIGHT / 2
            updated_points.append((x_draw, y_draw))

         pygame.draw.lines(WINDOW, self.color, False, updated_points, 2)
         
        pygame.draw.circle(WINDOW, self.color, (x, y), self.radius)    #window, color, position, size
       
                
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            WINDOW.blit(distance_text, (x - distance_text.get_width()/2 , y - distance_text.get_height()/2))


#------------------------------  PHYSICS -----------------------------
    def attraction(self, other):                                        
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)         #calculated distance two objects

        if other.sun:                                                   #want to know if the other planet is the sun 
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2         #straight line force of attraction
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y                                         #these are actauly values not to scale


    def update_position(self, planets):
        total_fx = total_fy = 0                                         #getting the total force exerted 
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP              
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



#------------------------------  MAIN LOOP -----------------------------

def main():                                                        #pygame event loop: infinite loop that runs while the simu is running (keep events running if not it will open then close)
   
    run = True
    clock = pygame.time.Clock()                                    #sets framerate


    #planets
    sun = Planet(0, 0, 30, YELLOW, SUNMASS)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, EARTHMASS)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, MARSMASS)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, MERCURYMASS)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, VENUSMASS)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]


    #window loop
    while run:
        clock.tick(60)     
        WINDOW.fill((0, 0, 0))                                       
        #WINDOW.fill(WHITE)
        #pygame.display.update()                                   #everyloop it updates the display

        for event in pygame.event.get():                           #gets every event that is running in pygame(key press, mouse movement, etc.)
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()

main()