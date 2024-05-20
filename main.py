import pygame
import cellgroup
import colors

def main():
# pygame setup
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    cg = cellgroup.CellGroup(400, 100, 10, 10, 50, 50)
    cg.init_mines(5)
    cg.update_adjacencies()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                cg.handle_click(*pygame.mouse.get_pos())

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(colors.white)
       

        # RENDER YOUR GAME HERE
        cg.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()