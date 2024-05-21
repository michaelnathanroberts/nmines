import pygame
from game import Game
import colors

def main():
# pygame setup
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 1280))
    clock = pygame.time.Clock()
    running = True
    game = Game()

    while game.running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                game.handle_click()
            elif event.type == pygame.KEYUP:
                game.handle_key(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(colors.white)
       

        # RENDER YOUR GAME HERE
        game.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()