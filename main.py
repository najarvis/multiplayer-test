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
    main_player.color = (255, 0, 0)

    while not done:
        delta = clock.tick(1000/30)

        keys = pygame.key.get_pressed()
        filtered = [
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d]]

        b64_msg = base64.b64encode(pickle.dumps(filtered))
        players = player_client.send_message(b64_msg)

        main_player.update(players[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0, 0, 0))

        for other_player in players[1]:
            player.Player(other_player).render(screen)

        main_player.render(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run()
