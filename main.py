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

    player_client = client.Client()

    # Create a player instance and change it's color to red to differenciate
    main_player = player.Player()
    main_player.img.fill((255, 0, 0))

    done = False
    while not done:
        delta = clock.tick(1000/30) # Update 30x per second (approximately 30fps)

        # The only data sent to the server (currently) are the true / false
        # values for whether the keys w, a, s, or d are pressed.
        keys = pygame.key.get_pressed()
        filtered = [
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d]]

        # Encode that array and send it off
        b64_msg = base64.b64encode(pickle.dumps(filtered))

        # Get the data back from the server that looks like:
        # [my pos, [all other players positions]]
        players = player_client.send_message(b64_msg)

        # Update the player's position based on what the server said
        main_player.update(players[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0, 0, 0))

        # Create a player instance and draw it for all other players
        for other_player in players[1]:
            player.Player(other_player).render(screen)

        # Draw the main player
        main_player.render(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run()
