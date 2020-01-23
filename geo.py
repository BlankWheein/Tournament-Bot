import pygame
import random, sys, math
pygame.init()
myfont = pygame.font.SysFont("monospace", 30)
WIN_WIDTH, WIN_HEIGHT = 1500, 900
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

while True:
    for corners in range(2, 25):

        radar_len = 3000/corners/2
        x2, y2 = WIN_WIDTH/2+radar_len/2, WIN_HEIGHT/2 -200
        pointangle = 360/corners
        lines = []

        for x in range(1, corners+1):
            x1, y1 = x2, y2
            x2, y2 = x1 + math.cos(math.radians(pointangle*x)) * radar_len, y1 + math.sin(math.radians(pointangle*x)) * radar_len
            lines.append((x1, y1))
            lines.append((x2, y2))

        label = myfont.render(f"Corners: {corners}", 1, (255,255,0))
        screen.blit(label, (100, 100))
        
        pygame.draw.polygon(screen, (255, 255, 255), lines, 1)
        pygame.display.update()
        pygame.time.delay(1000)
        screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
