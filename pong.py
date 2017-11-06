import sys
import pygame

from ball import Ball
from neuralnet import AIPaddle
from neuralnet import NNPaddle


class PongGame:
    window_width = 500
    window_height = 500

    def __init__(self):
        self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
        # self.paddle1 = Paddle(PongGame.window_width - 50, PongGame.window_height / 2)
        self.paddle1 = NNPaddle(PongGame.window_width - 50, PongGame.window_height / 2, self.ball, self)
        self.paddle2 = AIPaddle(50, PongGame.window_height / 2, self.ball, self)
        # self.paddle2 = NNPaddle(50, PongGame.window_height / 2, self.ball, self)
        self.temp_cpu_move_down = True

        self.start_game()

    def start_game(self):
        pygame.init()

        clock = pygame.time.Clock()
        display = pygame.display.set_mode((PongGame.window_width, PongGame.window_height))
        pygame.display.set_caption('Neural Net Pong')

        while True:
            delta = clock.tick(60) / 1000
            display.fill((255, 255, 255))

            # listen for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.handle_input(delta)

            self.handle_collisions()

            # super super advanced AI
            self.paddle1.follow_ball(delta)
            self.paddle2.follow_ball(delta)

            self.ball.move(delta)

            self.handle_offscreen()

            self.draw(display)
            flip = pygame.display.flip()

    def draw(self, display):
        self.paddle1.draw(display)
        self.paddle2.draw(display)
        self.ball.draw(display)

    def handle_input(self, delta):
        # listen for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.paddle1.bounds.y > 0:
            self.paddle1.move_up(delta)
        if keys[pygame.K_DOWN] and self.paddle1.bounds.y + self.paddle1.bounds.height < PongGame.window_height:
            self.paddle1.move_down(delta)

    def handle_collisions(self):
        # collision with human paddle
        if self.ball.intersects_paddle(self.paddle2, self.paddle1):
            self.ball.vel_x = -self.ball.vel_x
            self.ball.vel_x *= 1.1
            self.ball.vel_y *= 1.1
        # collision with ceiling
        elif self.ball.bounds.y <= 0 or self.ball.bounds.y + self.ball.bounds.height >= PongGame.window_height:
            self.ball.vel_y = -self.ball.vel_y

    def handle_offscreen(self):
        if self.ball.bounds.x + self.ball.bounds.width > PongGame.window_width or self.ball.bounds.x <= 0:
            self.ball = Ball(PongGame.window_width / 2, PongGame.window_height / 2)
            self.paddle1.reset(PongGame.window_width - 50, PongGame.window_height / 2, self.ball)
            self.paddle2.reset(50, PongGame.window_height / 2, self.ball)


def main():
    PongGame()


if __name__ == '__main__':
    main()
