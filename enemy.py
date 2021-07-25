from entity import *


class Enemy(Entity):

    def __init__(self, app, pos, number):
        super().__init__(app, pos)
        self.number = number
        self.personality = None
        self.target = None
        self.speed = None
        self.set_personality()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.check_move():
                self.move()
        self.set_grid_pos()

    def draw(self):
        self.draw_character()

    def set_personality(self):
        if self.number == 0:
            self.color = OIKAKE
            self.personality = "hunter"
            self.speed = 2
        if self.number == 1:
            self.color = MACHIBUSE
            self.personality = "ambusher"
            self.speed = 1
        if self.number == 2:
            self.color = KIMAGURE
            self.personality = "wayward"
            self.speed = 1
        if self.number == 3:
            self.color = OTOBOKE
            self.personality = "fool"
            self.speed = 1

    def move(self):
        if self.personality == "hunter":
            self.direction = self.path_dir(self.target)
        if self.personality == "ambusher":
            self.direction = self.path_dir(self.target)
        if self.personality == "wayward":
            self.direction = self.Wayward()
        if self.personality == "fool":
            self.direction = self.path_dir(self.target)

    def path_dir(self, target):
        next_cell = self.find_next_cell(target)
        x_dir = next_cell[0] - self.grid_pos[0]
        y_dir = next_cell[1] - self.grid_pos[1]
        return vec(x_dir, y_dir)

    def find_next_cell(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target.x), int(target.y)])
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(COLS)] for x in range(ROWS)]
        for cell in self.app.walls:
            if cell.x < COLS and cell.y < ROWS:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0],
                                         neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append(
                                        {"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def set_target(self):
        if self.personality == "hunter" or self.personality == "ambusher":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos.x > COLS // 2 and self.app.player.grid_pos.y > ROWS // 2:
                return vec(1, 1)
            if self.app.player.grid_pos.x > COLS // 2 and self.app.player.grid_pos.y < ROWS // 2:
                return vec(1, ROWS - 2)
            if self.app.player.grid_pos.x < COLS // 2 and self.app.player.grid_pos.y > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)

    def Hunter(self):
        pass

    def Ambusher(self):
        pass

    def Wayward(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def Fool(self):
        pass
