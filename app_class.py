from settings import *
from player import *
from enemy import *
pygame.init()


class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()  # a clock for controling the frames per second
        self.running = True
        self.state = 'Start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT// ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.make_enemies()
        self.player = Player(self, self.p_pos)

    def run(self):
        while self.running:
            if self.state == 'Start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'Playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'Game Over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

### HELPING FUNCTIONS  ###

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(
            self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    elif char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    elif char == 'P':
                        self.p_pos = vec(xidx, yidx)
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append(vec(xidx, yidx))
                    elif char == 'B':
                        pygame.draw.rect(self.background, BLACK, (
                            xidx*self.cell_width, yidx*self.cell_height, self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, pos, idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GRAY,
                             (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GRAY, (0, x *
                             self.cell_height), (WIDTH, x*self.cell_height))
        for coin in self.coins:
            pygame.draw.rect(self.background, GOLD, (coin.x*self.cell_width,
                             coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0 
        self.reset_pos()
        self.coins = [] 
        with open('walls.txt', 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = 'Playing'
        
    def reset_pos(self):
        self.player.grid_pos = self.player.starting_pos
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0 
        for enemy in self.enemies:
            enemy.grid_pos = enemy.starting_pos
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
            
### START FUNCTIONS ###

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'Playing'

    def start_update(self):
        pass
    
    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, ORANGE, START_FONT, True)
        self.draw_text('1 PLAYER ONLY', self.screen, [
                       WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, BLUE1, START_FONT, True)
        self.draw_text('HIGH SCORE', self.screen, [
                       5, 0], START_TEXT_SIZE, WHITE, START_FONT)
        pygame.display.update()

### PLAYING FUNCTIONS ###

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)

        self.screen.blit(
            self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text('HIGH SCORE: 0', self.screen, [
                       5, 0], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, [
                       WIDTH//2+50, 0], START_TEXT_SIZE, WHITE, START_FONT)
        self.draw_text('LIFES: ', self.screen, [
                       5, HEIGHT - 25], START_TEXT_SIZE, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "Game Over"
        else:
            self.reset_pos()
            
    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, GOLD,
                               (int(coin.x*self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y*self.cell_height)+self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)

### GAME OVER FUNCTIONS

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
                
    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, "arial", centered=True)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  36, (190, 190, 190), "arial", centered=True)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()
