import pygame
from sys import exit
from block import Block
import numpy as np

BUTTON_COLOR = (190, 240, 255)
BUTTON_BORDER_COLOR = (45, 170, 210)


class Direction(enumerate):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


initial_board = np.array(
    [
        [1, 4, 0, 4, 0, 0, 4, 0],
        [0, 4, 0, 4, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 0, 4, 0],
        [0, 0, 4, 0, 4, 0, 4, 0],
        [4, 0, 0, 0, 4, 0, 4, 0],
        [0, 4, 4, 0, 4, 0, 4, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 9],
    ]
)


class Game:
    def __init__(self, window, win_width, win_height) -> None:
        self.window = window
        self.win_width = win_width
        self.win_height = win_height
        self.board = initial_board.copy()
        self.block_group = pygame.sprite.Group()
        self.player_state = (0, 0)
        self.alive = True
        self.q_table = np.zeros((4, 8, 8))  # 8x8 table for each action

        self.q_table[0, 0, :] = -np.inf
        self.q_table[1, 7, :] = -np.inf
        self.q_table[2, :, 0] = -np.inf
        self.q_table[3, :, 7] = -np.inf

        self.background = pygame.image.load("./graphics/background.png").convert()
        self.control_background = pygame.image.load(
            "./graphics/control_background.png"
        ).convert()

        self.buttons_rect = []
        self.iteration = 0
        self.iteration_rect = None

    def actions(self):
        if self.player_state[0] == 0:
            if self.player_state[1] == 0:
                return [Direction.DOWN, Direction.RIGHT]
            elif self.player_state[1] == 7:
                return [Direction.DOWN, Direction.LEFT]
            else:
                return [Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        elif self.player_state[0] == 7:
            if self.player_state[1] == 0:
                return [Direction.UP, Direction.RIGHT]
            elif self.player_state[1] == 7:
                return [Direction.UP, Direction.LEFT]
            else:
                return [Direction.UP, Direction.LEFT, Direction.RIGHT]
        elif self.player_state[1] == 0:
            return [Direction.UP, Direction.DOWN, Direction.RIGHT]
        elif self.player_state[1] == 7:
            return [Direction.UP, Direction.DOWN, Direction.LEFT]
        else:
            return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    def transition_model(self, action):
        if action == Direction.UP:
            self.board[self.player_state[0]][self.player_state[1]] = 0
            self.board[self.player_state[0] - 1][self.player_state[1]] = 1
            self.player_state = (self.player_state[0] - 1, self.player_state[1])

        elif action == Direction.DOWN:
            self.board[self.player_state[0]][self.player_state[1]] = 0
            self.board[self.player_state[0] + 1][self.player_state[1]] = 1
            self.player_state = (self.player_state[0] + 1, self.player_state[1])
        elif action == Direction.LEFT:
            self.board[self.player_state[0]][self.player_state[1]] = 0
            self.board[self.player_state[0]][self.player_state[1] - 1] = 1
            self.player_state = (self.player_state[0], self.player_state[1] - 1)
        elif action == Direction.RIGHT:
            self.board[self.player_state[0]][self.player_state[1]] = 0
            self.board[self.player_state[0]][self.player_state[1] + 1] = 1
            self.player_state = (self.player_state[0], self.player_state[1] + 1)
        else:
            raise Exception("Invalid action")

        if self.player_state == (7, 7):
            self.alive = False
            return 100

        if initial_board[self.player_state[0]][self.player_state[1]] == 4:
            self.alive = False
            return -100

        else:
            return -1

    def eps_greedy(self, eps):
        if np.random.uniform(0, 1) < eps:
            return np.random.choice(self.actions())
        else:
            q_line = self.q_table[:, self.player_state[0], self.player_state[1]]
            # print(q_line)
            # print(np.flatnonzero(q_line == q_line.max()))
            return np.random.choice(np.flatnonzero(q_line == q_line.max()))

    def set_q_value(self, state, action, value):
        self.q_table[action, state[0], state[1]] = value

    def restart(self):
        self.player_state = (0, 0)
        self.board = initial_board.copy()
        self.alive = True
        self.draw_board()

    def iterate_episode(self):
        while self.alive:
            # print("NEW ITERATION")
            action = self.eps_greedy(0.1)
            old_state = self.player_state
            # print("STATE: ", self.player_state, "ACTION: ", action)

            reward = self.transition_model(action)
            # print("REWARD: ", reward)

            self.set_q_value(
                old_state,
                action,
                reward
                + 0.9
                * self.q_table[:, self.player_state[0], self.player_state[1]].max(),
            )

            # print(self.q_table[:, old_state[0], old_state[1]])

            #### update gui
            self.block_group.empty()
            self.draw_board()
            pygame.display.update()
            # pygame.time.delay(5000)

    def learn(self, n_episodes):
        for i in range(n_episodes):
            self.iteration += 1
            self.restart()
            # pygame.time.delay(3000)
            self.iterate_episode()

    def stop(self):
        self.alive = False

    def draw_board(self):
        self.window.blit(self.background, (0, 0))
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.block_group.add(Block(j * 96, i * 96, self.board[i][j]))

        self.block_group.draw(self.window)

    def draw_control_section(self):
        # control_background = pygame.Surface([200, self.win_height])
        # control_background.fill((255, 255, 255))
        self.window.blit(self.control_background, (8 * 96, 0))

        # button to start learning
        button_width = 140
        button_height = 40
        border = 2

        learn_button_surf = pygame.Surface([button_width, button_height])
        learn_button_surf.fill(BUTTON_COLOR)
        learn_button_rect = learn_button_surf.get_rect(topleft=((8 * 96 + 30, 100)))
        learn_button_border = pygame.Surface(
            [button_width + border * 2, button_height + border * 2]
        )
        learn_button_border.fill(BUTTON_BORDER_COLOR)

        font = pygame.font.SysFont("Arial", 25)
        learn_text_surf = font.render("LEARN 25", True, (0, 0, 0))
        learn_text_rect = learn_text_surf.get_rect(center=learn_button_rect.center)
        self.window.blit(learn_button_border, (8 * 96 + 30 - border, 100 - border))
        self.window.blit(learn_button_surf, learn_button_rect)
        self.window.blit(learn_text_surf, learn_text_rect)

        # learn button 100
        learn_button100_surf = pygame.Surface([button_width, button_height])
        learn_button100_surf.fill(BUTTON_COLOR)
        learn_button100_rect = learn_button100_surf.get_rect(
            topleft=((8 * 96 + 30, 250))
        )
        learn_button100_border = pygame.Surface(
            [button_width + border * 2, button_height + border * 2]
        )
        learn_button100_border.fill(BUTTON_BORDER_COLOR)

        learn_text100_surf = font.render("LEARN 100", True, (0, 0, 0))
        learn_text100_rect = learn_text100_surf.get_rect(
            center=learn_button100_rect.center
        )
        self.window.blit(learn_button100_border, (8 * 96 + 30 - border, 250 - border))
        self.window.blit(learn_button100_surf, learn_button100_rect)
        self.window.blit(learn_text100_surf, learn_text100_rect)

        # button to draw result
        result_button_surf = pygame.Surface([button_width, button_height])
        result_button_surf.fill(BUTTON_COLOR)
        result_button_rect = result_button_surf.get_rect(topleft=((8 * 96 + 30, 400)))
        result_button_border = pygame.Surface(
            [button_width + border * 2, button_height + border * 2]
        )
        result_button_border.fill(BUTTON_BORDER_COLOR)
        result_text_surf = font.render("POLICY", True, (0, 0, 0))
        result_text_rect = result_text_surf.get_rect(center=result_button_rect.center)
        self.window.blit(result_button_border, (8 * 96 + 30 - border, 400 - border))
        self.window.blit(result_button_surf, result_button_rect)
        self.window.blit(result_text_surf, result_text_rect)

        self.buttons_rect = [
            learn_button_rect,
            learn_button100_rect,
            result_button_rect,
        ]

        iteration_text_surf = font.render(
            "Iteration: " + str(self.iteration), True, (0, 0, 0)
        )
        iteration_text_rect = iteration_text_surf.get_rect(topleft=(8 * 96 + 30, 550))
        self.window.blit(iteration_text_surf, iteration_text_rect)

    def draw_result(self):
        self.window.blit(self.background, (0, 0))
        self.block_group.empty()
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                # draw arrows
                if initial_board[i][j] != 4 and initial_board[i][j] != 9:
                    q_line = self.q_table[:, i, j]
                    best_action = np.random.choice(
                        np.flatnonzero(q_line == q_line.max())
                    )
                    if best_action == 0:
                        self.block_group.add(Block(j * 96, i * 96, "u"))
                    elif best_action == 1:
                        self.block_group.add(Block(j * 96, i * 96, "d"))
                    elif best_action == 2:
                        self.block_group.add(Block(j * 96, i * 96, "l"))
                    elif best_action == 3:
                        self.block_group.add(Block(j * 96, i * 96, "r"))
                    else:
                        raise Exception("Invalid action")
                else:
                    self.block_group.add(Block(j * 96, i * 96, 4))
        self.block_group.draw(self.window)

    def check_input(self):
        mouse_input = pygame.mouse.get_pressed()
        if mouse_input[0]:
            if self.buttons_rect[0].collidepoint(pygame.mouse.get_pos()):
                self.learn(25)
            if self.buttons_rect[1].collidepoint(pygame.mouse.get_pos()):
                self.learn(100)
            if self.buttons_rect[2].collidepoint(pygame.mouse.get_pos()):
                self.draw_result()

    def update_iteration_gui(self):
        font = pygame.font.SysFont("Arial", 25)
        iteration_text_surf = font.render(
            "Iteration: " + str(self.iteration), True, (0, 0, 0)
        )
        iteration_text_rect = iteration_text_surf.get_rect(center=(8 * 96 + 70, 550))
        self.window.blit(iteration_text_surf, iteration_text_rect)
