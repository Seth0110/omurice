#2 moving Triangles: 1 moves with keys, 1 bounces off screen 

import pygame

pygame.init()#initialize pygame
size = width, height = 400 , 300#screen size may be changed
screen = pygame.display.set_mode((size))#create screen
logo = pygame.image.load("T-ROBOTS.bmp") #need to have file and proper path to file for this to work
icon = pygame.display.set_icon(logo)#puts icon in corner
pygame.display.set_caption('AT-Robots')#names window

#colors used
black = (0, 0, 0)
blue = (0, 128, 255)
pink = (191, 63, 63)

#coordinates for blue triangle (moved with arrow keys)
a = 100
b = 100
c = 150
d = 100#could possibly be the same as b 
e = 125
f = 50

#triangle points for pink triangle (moved automatically - bounces)
h = 200
i = 200
j = 250
k = 200
l = 225
m = 150
x = 225#mid point of triangle
y = 175#mid point of triangle

xR = 1#triangle moving right
yD = 1#triangle moving down
wallTouch = 0#wall not touched yet

done = False#window not closed
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    screen.fill(black)#screen is black except for shapes
    
    pygame.draw.polygon(screen, blue, [[a, b], [c, d], [e, f]], 2)#blue triangle moves with keys    
    press = pygame.key.get_pressed()#moves blue triangle using keyboard
    if press[pygame.K_UP]: b -= 3; d -= 3; f -= 3
    if press[pygame.K_DOWN]: b += 3; d += 3; f += 3
    if press[pygame.K_RIGHT]: a += 3; c += 3; e += 3
    if press[pygame.K_LEFT]: a -= 3; c -= 3; e -= 3
    
    #pygame.draw.rect(screen, pink, [x, y, 60, 60], 2)#rectangle test shape
    pygame.draw.polygon(screen, pink, [[h, i], [j, k], [l, m]], 2)#pink triangle bounces off screen
    if x < 25: wallTouch = 0#wall not touched or left wall touched last
    if y > height - 25: wallTouch = 1#bottom wall touched last
    if x > width - 25: wallTouch = 2#right wall touched last
    if y < 25: wallTouch = 3#top wall touched last
    if wallTouch == 0 and yD == 1:#touched left moving down
        x += 3
        h += 3
        j += 3
        l += 3
        y += 3
        i += 3
        k += 3
        m += 3
        xR = 1
        yD = 1
    if wallTouch == 1 and xR == 1:#touched bottom moving right
        x += 3
        h += 3
        j += 3
        l += 3
        y -= 3
        i -= 3
        k -= 3
        m -= 3
        xR = 1
        yD = 0
    if wallTouch == 2 and yD == 0:#touched right moving up
        x -= 3
        h -= 3
        j -= 3
        l -= 3
        y -= 3
        i -= 3
        k -= 3
        m -= 3
        xR = 0
        yD = 0
    if wallTouch == 3 and xR == 0:#touched top moving left
        x -= 3
        h -= 3
        j -= 3
        l -= 3
        y += 3
        i += 3
        k += 3
        m += 3
        xR = 0
        yD = 1
    if wallTouch == 3 and xR == 1:#touched top moving right
        x += 3
        h += 3
        j += 3
        l += 3
        y += 3
        i += 3
        k += 3
        m += 3
        xR = 1
        yD = 1
    if wallTouch == 2 and yD == 1:#touched right moving down
        x -= 3 
        h -= 3
        j -= 3
        l -= 3
        y += 3
        i += 3
        k += 3
        m += 3
        xR = 0
        yD = 1
    if wallTouch == 1 and xR == 0:#touched bottom moving left
        x -= 3
        h -= 3
        j -= 3
        l -= 3
        y -= 3
        i -= 3
        k -= 3
        m -= 3
        xR = 0
        yD = 0
    if wallTouch == 0 and yD == 0:#touched left moving up
        x += 3
        h += 3
        j += 3
        l += 3
        y -= 3
        i -= 3
        k -= 3
        m -= 3
        xR = 1
        yD = 0
    
    pygame.display.flip()#necessary for movement
    clock.tick(30)#slows down movement to reasonable speed
    
pygame.quit()#prevents error on closing program
