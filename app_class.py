from settings import *
from player import *

pygame.init()


class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()  # a clock for controling the frames per second
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT//30
        self.player = Player(self, PLAYER_START_POS)
        self.walls = []
        self.coins = []
        self.load()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
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

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GRAY,
                             (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GRAY, (0, x *
                             self.cell_height), (WIDTH, x*self.cell_height))
        for coin in self.coins:
            pygame.draw.rect(self.background, YELLOW, (coin.x*self.cell_width,
                             coin.y*self.cell_height, self.cell_width, self.cell_height))

### START FUNCTIONS ###

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

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
        self.player.draw()
        pygame.display.update()


    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, 
                               (int(coin.x*self.cell_width) +self.cell_width  // 2 + TOP_BOTTOM_BUFFER // 2,
                                int(coin.y*self.cell_height)+self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 5)
