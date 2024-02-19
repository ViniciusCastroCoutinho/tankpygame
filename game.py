import pygame
from menu import Menu
from maze import Maze
from tank import Tank
from bullet import Bullet


class Game:
    def __init__(self):
        self.game_start = True

    def game_running(self):
        if self.game_start:
            pygame.init()

            RED = (144, 38, 10)
            YELLOW = (216, 169, 64)
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            WIDTH = 1280
            HEIGHT = 720
            HALF_W = WIDTH // 2
            GAME_HEIGHT_START = 70
            GAME_HEIGHT = HEIGHT - GAME_HEIGHT_START
            HALF_GH_LENGHT = GAME_HEIGHT // 2
            HALF_GH_POS = GAME_HEIGHT_START + (GAME_HEIGHT // 2)

            size = (WIDTH, HEIGHT)
            screen = pygame.display.set_mode(size)
            pygame.display.set_caption("COMBAT")

            # game mode
            game_mode = 0

            # menu screen
            menu = Menu(screen)

            # walls
            std_dimension = 24
            w90 = pygame.Rect(0, GAME_HEIGHT_START, std_dimension, GAME_HEIGHT)
            w91 = pygame.Rect(WIDTH - std_dimension, GAME_HEIGHT_START, std_dimension, GAME_HEIGHT)
            w92 = pygame.Rect(0, GAME_HEIGHT_START + 40, WIDTH, std_dimension)  # Top wall
            w93 = pygame.Rect(0, HEIGHT - std_dimension, WIDTH, std_dimension)
            w1 = pygame.Rect(HALF_W - std_dimension + 25, HALF_GH_LENGHT // 2 - 28, std_dimension + 40, 4 * std_dimension + 80)
            w2 = pygame.Rect(HALF_W // 2 + 65, HALF_GH_POS - std_dimension + 10, 4 * std_dimension + 27, std_dimension + 20)
            w3 = pygame.Rect(HALF_W // 4 - 32, 2 * HALF_GH_POS // 3 - 10, 2 * std_dimension + 77, std_dimension + 20)
            w4 = pygame.Rect(w3[0] + w3[2] // 2 + 9, w3[1], w3[2] // 2 - 8, HALF_GH_POS - w3[1])

            # maze
            maze = Maze()
            maze.add_wall(w1)
            maze.add_wall(w2)
            maze.add_wall(w3)
            maze.add_wall(w4)
            maze.mirror_walls_horizontally(GAME_HEIGHT_START, HEIGHT)
            maze.mirror_walls_vertically(WIDTH)
            maze.add_wall(w90)
            maze.add_wall(w91)
            maze.add_wall(w92)
            maze.add_wall(w93)

            # music & sounds
            pygame.mixer.music.load(
                'assets/sounds/[FREE] Kingdom Hearts - Dearly Beloved 8-Bit (No copyright music) #kingdomhearts'
                ' #8bit #remix #chill.mp3')
            pygame.mixer.music.play(90, 0.0, 1000)
            walk = pygame.mixer.Sound('assets/sounds/walk_sfx.wav')
            magic_summon = pygame.mixer.Sound('assets/sounds/bullet_summon.wav')
            magic_bounce = pygame.mixer.Sound('assets/sounds/bullet_bounce.wav')
            player_take_damage = pygame.mixer.Sound('assets/sounds/mage_damage.wav')

            # players
            players = []
            p_size_x = 52.2
            p_size_y = 59.5
            p1 = Tank(p_size_x, p_size_y, std_dimension, HALF_GH_POS, "assets/sprites/black_mage(1).png", 0)
            p2 = Tank(p_size_x, p_size_y, WIDTH - std_dimension - p_size_x,
                      HALF_GH_POS, "assets/sprites/red_mage(1).png", 1)
            players.append(p1)
            players.append(p2)

            # joysticks
            # joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

            # bullets
            bullets = []

            # Clock
            clock = pygame.time.Clock()

            while self.game_start:
                current_time = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()
                # player movement
                for player in players:
                    if keys[player.up]:
                        player.action = 8
                        player.move_up()
                        walk.play()
                        if maze.collision(player.hit_box) != -1:
                            player.move_down()
                        player.crosshair(17, -40)
                        if keys[player.right]:
                            player.action = 9
                            player.crosshair(70, -20)
                            player.move_right()
                            if maze.collision(player.hit_box) != -1:
                                player.move_left()
                        elif keys[player.left]:
                            player.action = 15
                            player.crosshair(-38, -20)
                            player.move_left()
                        if maze.collision(player.hit_box) != -1:
                            player.move_right()
                    elif keys[player.down]:
                        player.action = 12
                        player.crosshair(17, 80)
                        walk.play()
                        player.move_down()
                        if maze.collision(player.hit_box) != -1:
                            player.move_up()
                        if keys[player.right]:
                            player.action = 11
                            player.crosshair(70, 70)
                            player.move_right()
                            if maze.collision(player.hit_box) != -1:
                                player.move_left()
                        elif keys[player.left]:
                            player.action = 13
                            player.crosshair(-38, 70)
                            player.move_left()
                            if maze.collision(player.hit_box) != -1:
                                player.move_right()
                    elif keys[player.right]:
                        player.action = 10
                        player.crosshair(70, 40)
                        walk.play()
                        player.move_right()
                        if maze.collision(player.hit_box) != -1:
                            player.move_left()
                    elif keys[player.left]:
                        player.action = 14
                        player.crosshair(-38, 40)
                        walk.play()
                        player.move_left()
                        if maze.collision(player.hit_box) != -1:
                            player.move_right()
                    else:
                        stop = player.stop_animation(player.action)
                        player.action = stop

                # quit
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_start = False

                    # menu screen
                    if menu.status() is True:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == pygame.mouse.get_pressed(3)[0]:
                                if menu.in_gm0():
                                    game_mode = 0
                                    menu.turn_off()
                                    pygame.mixer.music.pause()
                                    pygame.mixer.music.load('assets/sounds/RPG_MUSIC.mp3')
                                    pygame.mixer.music.play(-1, 1, 0)

                                elif menu.in_gm1():
                                    game_mode = 1
                                    menu.turn_off()
                                    pygame.mixer.music.pause()
                                    pygame.mixer.music.load('assets/sounds/RPG_MUSIC.mp3')
                                    pygame.mixer.music.play(-1, 1, 0)

                                elif menu.in_credits():
                                    menu.credits_screen = True

                                elif menu.in_quit():
                                    self.game_start = False

                                elif menu.in_back():
                                    menu.credits_screen = False
                    # player shooting
                    for player in players:
                        if event.type == pygame.KEYDOWN:
                            if event.key == player.shoot:
                                if player.has_bullet is False:
                                    bullets.append(Bullet(player, 40, 40, "assets/sprites/fireball_spritesheet(1).png"))
                                    player.bullet_cooldown = current_time
                                    magic_summon.play()
                                    player.has_bullet = True

                # updating bullets
                temp_bullets = list(bullets)
                for bullet in bullets:
                    if bullet.is_over() or bullet.is_out_of_bounds(screen) or bullet.is_in_wall(maze):
                        temp_bullets.remove(bullet)
                        bullet.shooter.has_bullet = False
                    else:
                        bullet.move_x()
                        if maze.collision(bullet.hit_box) != -1:
                            if game_mode == 0:
                                wall = maze.walls[maze.collision(bullet.hit_box)]
                                bullet.update_mvt_x(wall)
                                magic_bounce.play()
                            elif game_mode == 1:
                                temp_bullets.remove(bullet)
                                bullet.shooter.has_bullet = False
                                magic_bounce.play()

                        bullet.move_y()
                        if maze.collision(bullet.hit_box) != -1:
                            if game_mode == 0:
                                wall = maze.walls[maze.collision(bullet.hit_box)]
                                bullet.update_mvt_y(wall)
                            elif game_mode == 1:
                                temp_bullets.remove(bullet)
                                bullet.shooter.has_bullet = False

                        # checking collision with enemies
                        temp_players = list(players)
                        for player in players:
                            if player != bullet.shooter and player.bullet_collision(bullet):
                                temp_bullets.remove(bullet)
                                temp_players.remove(player)
                                player_take_damage.play()
                                bullet.shooter.has_bullet = False
                        players = temp_players
                bullets = temp_bullets

                # drawing
                if menu.status() is True:
                    if not menu.credits_screen:
                        menu.menu_background(screen)
                        menu.initial_menu(screen, 3, WHITE)
                    else:
                        menu.menu_background(screen)
                        menu.credits_menu(screen, 3, WHITE)
                else:
                    # maze part 1
                    maze.draw_map(screen, 0)
                    #maze.draw(screen, YELLOW)

                    # update animation walking
                    for player in players:
                        if current_time - player.last_update >= player.animation_cooldown:
                            player.frame += 1
                            player.last_update = current_time
                            if player.frame >= len(player.animation_list[player.action]):
                                player.frame = 0

                        # show frame
                        # pygame.draw.rect(screen, BLACK, player.hit_box)  # hit_box
                        screen.blit(player.animation_list[player.action][player.frame],
                                    (player.positionx, player.positiony))
                        pygame.draw.rect(screen, RED, (player.positionx + player.crosshair_x,
                                                       player.positiony + player.crosshair_y, 20, 20))

                    # update bullet
                    for bullet in bullets:
                        if current_time - bullet.last_update >= bullet.animation_cooldown:
                            bullet.frame += 1
                            bullet.last_update = current_time
                            if bullet.frame >= len(bullet.animation_list[bullet.action]):
                                bullet.frame = 0
                        # show frame
                        # pygame.draw.rect(screen, (0, 0, 0), bullet.hit_box)  # hit_box
                        screen.blit(bullet.animation_list[bullet.action][bullet.frame],
                                    (bullet.x, bullet.y))

                    # draw maze part2
                    maze.draw_obstacle(screen, 0)
                # update screen
                pygame.display.flip()
                clock.tick(60)
        else:
            pygame.quit()
