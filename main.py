import pygame
import client
import base64
import pickle
import player

def run():
    pygame.init()

    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()
    done = False

    player_client = client.Client()
    main_player = player.Player((20, 20))

    while not done:
        delta = clock.tick(1000/30)

        keys = pygame.key.get_pressed()
        filtered = [
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d]]

        b64_msg = base64.b64encode(pickle.dumps(filtered))
        position = player_client.send_message(b64_msg)
        
        main_player.update(position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        surface.fill((0, 0, 0))
        main_player.render(surface)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run()
