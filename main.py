import pygame
from sys import exit
from game import Game


def main():
    pygame.init()

    board_width, board_height = 8, 8
    block_size = 96
    window_width = board_width * block_size
    window_height = board_height * block_size
    control_section_width = 200

    window = pygame.display.set_mode(
        (window_width + control_section_width, window_height)
    )
    pygame.display.set_caption("Path Finder")
    clock = pygame.time.Clock()
    game = Game(window, window_width, window_height)

    while True:
        for event in pygame.event.get():  # check all input event
            if event.type == pygame.QUIT:
                print(game.q_table)
                pygame.quit()
                exit()  # from sys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.learn(20)
                if event.key == pygame.K_RETURN:
                    game.draw_result()

        game.draw_board()

        # control_background = pygame.Surface([200, window_height])
        # control_background.fill((255, 255, 255))
        # window.blit(control_background, (700, 0))

        game.draw_control_section()
        game.check_input()
        pygame.display.update()
        clock.tick(120)


if __name__ == "__main__":
    main()
