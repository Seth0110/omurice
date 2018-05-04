import pygameimport timepygame.init()# all colorswhite = (255,255,255)black = (0,0,0)darkOrange = (244,200,66)lightRed = (244,80, 66)red = (244,66,66)green = (66,244,152)darkBlue = (66,78,244)darkGray = (62,78,81)lineColor = (229,251,255)# font for the main screenfont = pygame.font.SysFont(None, 22)mainScreenHeight = 750mainScreenWidth = 1050robotIcon = pygame.image.load('atrobots.png')#main game arenascreen = pygame.display.set_mode((1050,750))pygame.display.set_caption("ATROBOTS")splashScreen1 = pygame.display.set_mode((700,450))clock = pygame.time.Clock()def splashScreen():    #splashScreen1.fill(white)    splashScreen1.blit(robotIcon,(10,10))    time.sleep(5)# Main Game windowdef gameArena():    screen = pygame.display.set_mode((1050, 750))    done = False    while not done:        for event in pygame.event.get():            if event.type == pygame.QUIT:                done = True            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:                is_blue = not is_blue        pressed = pygame.key.get_pressed()        if pressed[pygame.K_UP]: y -= 3        if pressed[pygame.K_DOWN]: y += 3        if pressed[pygame.K_LEFT]: x -= 3        if pressed[pygame.K_RIGHT]: x += 3        screen.fill(darkGray)        #pygame.draw.rect(screen, red, pygame.Rect(200, 500, 60, 60))        #pygame.draw.rect(screen,darkOrange,(550,550,100,50))        drawProgBar1()        drawProgBar2()        drawProgBar3()        drawProgBar4()        statusBar()        pygame.display.flip()        pygame.display.update()        clock.tick(60)# Button Objectdef button(msg, x, y, w, h, ic, ac, action=None):    mouse = pygame.mouse.get_pos()    click = pygame.mouse.get_pressed()    if x + w > mouse[0] > x and y + h > mouse[1] > y:        pygame.draw.rect(screen, ac, (x, y, w, h))        if click[0] == 1 and action != None:            if action == "play":                gameArena()            elif action == "QUIT":                pygame.quit()                quit()    else:        pygame.draw.rect(screen, ic, (x, y, w, h))    smallText = pygame.font.Font(None, 20)    textSurf, textRect = text_objects(msg, smallText)    textRect.center = ((x + (w / 2)), (y + (h / 2)))    screen.blit(textSurf, textRect)# message objectdef message(msg, color,xP,yP):    text = font.render(msg, True, color)    screen.blit(text, [xP, yP])# message Objectdef text_objects(text, font):    textSurface = font.render(text, True, black)    return textSurface, textSurface.get_rect()#for sound#pygame.mixer.music.load('foo.mp3')    #pygame.mixer.music.play(0)def play_next_song():    global _songs    _songs = _songs[1:] + [_songs[0]]  # move current song to the back of the list    pygame.mixer.music.load(_songs[0])    pygame.mixer.music.play()# First Progress bardef drawProgBar1():    pygame.draw.line(screen, lineColor, (850, 750), (850, 0), 6)    message("Robot: ", green, 860, 5)    message("Wins: ", green, 970, 5)    message("A: ", green, 870, 30)    pygame.draw.rect(screen, green, pygame.Rect(890, 35, 120, 8))    message("H: ", green, 870, 60)    pygame.draw.rect(screen, green, pygame.Rect(890, 65, 120, 8))    message("K: ", green, 870, 90)    message("D: ", green, 970, 90)    message("Error: ", green, 870, 120)# Second Progress Bardef drawProgBar2():    pygame.draw.line(screen, lineColor, (850, 150), (1050, 150), 4)    message("Robot: ", darkOrange, 860, 155)    message("Wins: ", darkOrange, 970, 155)    message("A: ", darkOrange, 870, 180)    pygame.draw.rect(screen, darkOrange, pygame.Rect(890, 185, 120, 8))    message("H: ", darkOrange, 870, 210)    pygame.draw.rect(screen, darkOrange, pygame.Rect(890, 215, 120, 8))    message("K: ", darkOrange, 870, 240)    message("D: ", darkOrange, 970, 240)    message("Error: ", darkOrange, 870, 270)#Third Progress Bardef drawProgBar3():    pygame.draw.line(screen, lineColor, (850, 300), (1050, 300), 4)    message("Robot: ", white, 860, 305)    message("Wins: ", white, 970, 305)    message("A: ", white, 870, 330)    pygame.draw.rect(screen, white, pygame.Rect(890, 335, 120, 8))    message("H: ", white, 870, 360)    pygame.draw.rect(screen, white, pygame.Rect(890, 365, 120, 8))    message("K: ", white, 870, 390)    message("D: ", white, 970, 390)    message("Error: ", white, 870, 420)#Fourth Progress Bardef drawProgBar4():    pygame.draw.line(screen, lineColor, (850, 450), (1050, 450), 4)    message("Robot: ", red, 860, 455)    message("Wins: ", red, 970, 455)    message("A: ", red, 870, 480)    pygame.draw.rect(screen, red, pygame.Rect(890, 485, 120, 8))    message("H: ", red, 870, 510)    pygame.draw.rect(screen, red, pygame.Rect(890, 515, 120, 8))    message("K: ", red, 870, 540)    message("D: ", red, 970, 540)    message("Error: ", red, 870, 570)# status footer on the main windowdef statusBar():    pygame.draw.line(screen, lineColor, (850, 600), (1050, 600), 4)    pygame.draw.line(screen, lineColor, (0, 600), (850, 600), 4)    message("Free Memory: ", white, 50, 640)    message("Cycle: ", white, 300, 640)    message("Limit: ", white, 520, 640)    message("Match: ", white, 730, 640)def menuScreen():    menuWindow = pygame.display.set_mode((700, 450))    pygame.display.set_caption("ATROBOTS|MENU")    menu = True    while menu:        for event in pygame.event.get():            if event.type == pygame.QUIT:                pygame.quit()                quit()        menuWindow.fill(darkGray)        pygame.draw.line(menuWindow, lineColor, (0, 52), (700, 52), 4)        #borders        #left        pygame.draw.line(menuWindow, lineColor, (1,0), (1,450), 4)        #right        pygame.draw.line(menuWindow, lineColor, (697,0), (697, 450), 4)        #top        pygame.draw.line(menuWindow, lineColor, (2, 1), (700, 1), 4)        #buttom        pygame.draw.line(menuWindow, lineColor, (0, 447), (700, 447), 4)        #Top text        message("Welcome To ATROBOTS v1.2.0 by Omurice",white,(420/2),(52/2))        #SELECTING ROBOTS        button("R1",25,75,45,35,white,red)        button("R2", 25, 125, 45, 35, white, red)        button("R3", 25, 178, 45, 35, white, red)        button("R4", 450, 75, 45, 35, white, red)        button("R5", 450, 125, 45, 35, white, red)        button("R6", 450, 178, 45, 35, white, red)        #MENU        pygame.draw.line(menuWindow, lineColor, (0, 220), (700, 220), 4)        button("Show Arc", 25, 230, 110, 30, white, darkOrange)        button("Show Source", 160, 230, 110, 30, white, darkOrange)        button("Disable Graphics", 295, 230, 110, 30, white, darkOrange)        button("Quiet Mode", 430, 230, 110, 30, white, darkOrange)        button("Compile Only", 565, 230, 110, 30, white, darkOrange)        button("Show Arc", 25, 285, 110, 30, white, darkOrange)        button("Show Source", 160, 285, 110, 30, white, darkOrange)        button("Disable Graphics", 295, 285, 110, 30, white, darkOrange)        button("Quiet Mode", 430, 285, 110, 30, white, darkOrange)        # play and Quit        button("Play", 25, 370, 300, 30, white, green,action="play")        button("Quit", 375, 370, 300, 30, white, red)       # button("Quiet Mode", 430, 285, 110, 30, white, darkOrange)        pygame.display.flip()        pygame.display.update()        #clock.tick(60)#splashScreen()menuScreen()gameArena()