import pygame

def run():
    pygame.init()

    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()
    done = False

    while not done:
        delta = clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run()
