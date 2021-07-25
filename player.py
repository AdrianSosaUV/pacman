from entity import *


class Player(Entity):

    def __init__(self, app, pos):
        super().__init__(app, pos, PLAYER_COLOUR)
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.verify_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        self.set_grid_pos()
        if self.on_coin():
            self.eat_coin()

    def draw(self):
        self.draw_character()
        self.draw_lifes()

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 100

    def draw_lifes(self):
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, CHERRY,
                               (80 + 20 * x, HEIGHT - 10), self.radius)

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
