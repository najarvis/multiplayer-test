import pygame
import sys, time
import base64, pickle
import client, player, ui, camera

def run(host=None):
    pygame.init()

    screen_size = (1600, 900)
    screen = pygame.display.set_mode(screen_size)

    clock = pygame.time.Clock()

    if host is None:
        # We can specify a different host to connect to with sys args.
        # for example: python main.py localhost
        player_client = client.Client()
    else:
        player_client = client.Client(host)

    # The player that we will be sending input for.
    main_player = player.Player()

    # Set up the camera that keeps the player in the center of the screen.
    main_camera = camera.Camera(main_player, screen_size)

    game_ui = ui.UI(main_player)

    last_coord = None

    done = False
    while not done:
        delta = clock.tick(60) # Update approximately 60fps

        # The only data sent to the server (currently) are the true / false
        # values for whether the keys w, a, s, d, or space are pressed.
        keys = pygame.key.get_pressed()
        filtered = [
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d],
            keys[pygame.K_SPACE]]

        # Encode that array and send it off
        b64_msg = base64.b64encode(pickle.dumps(filtered))

        # Get the data back from the server that looks like:
        # [my pos, [all other players positions]]
        curr_time = time.time()
        players = player_client.send_message(b64_msg)
        if players is None and last_coord is not None:
            players = last_coord

        elif players is not None and last_coord is None:
            last_coord = players

        if players is not None:
            # Update the player's position based on what the server said
            delta = time.time() - curr_time
            pygame.display.set_caption("Ping: {:.2f}".format((delta * 500)))
            main_player.update(players[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0, 0, 0))

        # Create a player instance and draw it for all other players
        if players is not None:
            for other_player in players[1]:
                player.Player.create_other(other_player).render(screen, main_camera)

        # Draw the main player
        main_player.render(screen, main_camera)

        game_ui.render(screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
