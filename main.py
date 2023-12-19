import pygame
import sys
import matplotlib.pyplot as plt

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
WALL_X = 50
COLLISION_SOUND = pygame.mixer.Sound('src/collision_sound.mp3')

MASS = 1
POWER = int(input("Введите степень десятки при массе большого блока: "))

V_0 = -0.0001
CYCLE_COUNT = 1000

BACKGROUND_COLOR = (0, 0, 0)
GROUND_COLOR = (255, 255, 255)
FONT_COLOR = (255, 255, 255)
BIG_BLOCK_COLOR = (66, 186, 246)
SMALL_BLOCK_COLOR = (192, 192, 192)

BIG_BLOCK_X = 400
BIG_BLOCK_Y = 300
BIG_BLOCK_LEN = 100
SMALL_BLOCK_X = 150
SMALL_BLOCK_Y = 350
SMALL_BLOCK_LEN = 50

COUNT_FONT = pygame.font.Font(pygame.font.get_default_font(), 18)


class Block:

    def __init__(self, x, y, mass, velocity, length) -> None:
        self.x = x
        self.y = y
        self.mass = mass
        self.prev_velocity = velocity
        self.velocity = velocity
        self.length = length

    def update_x(self) -> None:
        self.x += self.velocity

    def wall_collision(self) -> bool:
        if self.x <= WALL_X:
            self.prev_velocity = self.velocity
            self.velocity = -self.velocity
            return True
        return False


def blocks_collision(first_block: Block, second_block: Block) -> bool:
    if first_block.x > second_block.x:
        first_block, second_block = second_block, first_block
    if first_block.x + first_block.length < second_block.x:
        return False
    update_velocities(first_block, second_block)
    return True


def update_velocities(first_block: Block, second_block: Block) -> None:
    first_block.prev_velocity = first_block.velocity
    second_block.prev_velocity = second_block.velocity
    v = first_block.velocity
    u = second_block.velocity
    m1 = first_block.mass
    m2 = second_block.mass
    first_block.velocity = (2 * m2 / (m1 + m2)) * u + (m1 - m2) / (m1 + m2) * v
    second_block.velocity = (2 * m1 / (m1 + m2)) * v + (m2 - m1) / (m1 + m2) * u


def update_screen(screen: pygame.Surface, big_block: Block, small_block: Block, count: int) -> None:
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, (0, 400, 1000, 100))
    pygame.draw.rect(screen, GROUND_COLOR, (0, 0, 50, 1000))

    pygame.draw.rect(screen, BIG_BLOCK_COLOR, (big_block.x, big_block.y, big_block.length, big_block.length))
    pygame.draw.rect(screen, SMALL_BLOCK_COLOR, (small_block.x, small_block.y, small_block.length, small_block.length))

    text = COUNT_FONT.render("Количество столкновений: " + str(count), 1, FONT_COLOR)
    screen.blit(text, (100, 50))

    pygame.display.update()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    small_block = Block(SMALL_BLOCK_X, SMALL_BLOCK_Y, MASS, 0, SMALL_BLOCK_LEN)
    big_block = Block(BIG_BLOCK_X, BIG_BLOCK_Y, (10 ** POWER) * MASS, V_0, BIG_BLOCK_LEN)

    count = 0
    time = 0

    times = []
    x_small_block = []
    x_big_block = []
    v_small_block = []
    v_big_block = []
    a_small_block = []
    a_big_block = []

    update_screen(screen, big_block, small_block, count)

    while True:

        x_big_block.append(big_block.x)
        x_small_block.append(small_block.x)
        v_big_block.append(big_block.velocity)
        v_small_block.append(small_block.velocity)
        a_big_block.append(big_block.velocity - big_block.prev_velocity)
        a_small_block.append(small_block.velocity - small_block.prev_velocity)

        times.append(time)
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        if big_block.x > SCREEN_WIDTH:
            pygame.quit()
            break

        for i in range(CYCLE_COUNT):

            if blocks_collision(small_block, big_block):
                count += 1
                COLLISION_SOUND.play()

            if small_block.wall_collision():
                count += 1
                COLLISION_SOUND.play()

            big_block.update_x()
            small_block.update_x()

        update_screen(screen, big_block, small_block, count)

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

    axs[0, 0].plot(times, x_big_block)
    axs[0, 0].set_ylabel("x большого блока")
    axs[0, 0].set_title("Изменения координаты x")

    axs[1, 0].plot(times, x_small_block)
    axs[1, 0].set_ylabel("x маленького блока")
    axs[1, 0].set_xlabel("Количество пересчетов")

    axs[0, 1].plot(times, v_big_block)
    axs[0, 1].set_ylabel("v большого блока")
    axs[0, 1].set_title("Изменения скорости v")

    axs[1, 1].plot(times, v_small_block)
    axs[1, 1].set_ylabel("v маленького блока")
    axs[1, 1].set_xlabel("Количество пересчетов")

    axs[0, 2].plot(times, a_big_block)
    axs[0, 2].set_ylabel("a большого блока")
    axs[0, 2].set_title("Изменения ускорения a")

    axs[1, 2].plot(times, a_small_block)
    axs[1, 2].set_ylabel("a маленького блока")
    axs[1, 2].set_xlabel("Количество пересчетов")

    fig.tight_layout()
    plt.show()

    sys.exit()


if __name__ == '__main__':
    main()
