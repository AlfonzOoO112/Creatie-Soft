import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
GRAY = (169, 169, 169)
YELLOW = (255, 223, 0)

font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

def draw_text(text, color, x, y, font):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, text_rect)

def main_menu():
    buttons = [pygame.image.load('Assets/1.png'),
               pygame.image.load('Assets/2.png'),
               pygame.image.load('Assets/exit.png')]
    running = True
    while running:
        screen.fill((1, 50, 32))

        draw_text("Main Menu", BLACK, WIDTH // 2 , HEIGHT // 4 - 100, font)

        button_width, button_height = 400, 150
        button1 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 180, button_width, button_height)
        button2 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 30, button_width, button_height)
        button3 = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 120, button_width, button_height)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover_button1 = button1.collidepoint(mouse_x, mouse_y)
        hover_button2 = button2.collidepoint(mouse_x, mouse_y)
        hover_button3 = button3.collidepoint(mouse_x, mouse_y)


        button_color = BLUE
        hover_color = YELLOW

        buttons[0] = pygame.transform.scale(buttons[0], (button_width, button_height))
        screen.blit(buttons[0], (WIDTH // 2 - button_width // 2, HEIGHT // 2 - 180))
        buttons[1] = pygame.transform.scale(buttons[1], (button_width, button_height))
        screen.blit(buttons[1], (WIDTH // 2 - button_width // 2, HEIGHT // 2 - 30))
        buttons[2] = pygame.transform.scale(buttons[2], (button_width, button_height))
        screen.blit(buttons[2], (WIDTH // 2 - button_width // 2, HEIGHT // 2 + 120))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    choose_bulb_game()
                    running = False
                elif button2.collidepoint(event.pos):
                    sorting_trash_game()
                    running = False
                elif button3.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def choose_bulb_game():
    wattages = [random.randint(5, 100) for _ in range(5)]
    correct_choice = min(wattages)

    bulb_positions = [
        [150, 300],
        [300, 300],
        [450, 300],
        [600, 300],
        [750, 300],
    ]

    bulb_image = pygame.image.load('Assets/bulb.png')
    bulb_image = pygame.transform.scale(bulb_image, (400, 350))
    bulb_width, bulb_height = bulb_image.get_size()

    socket_position = (WIDTH // 2, 500)
    socket_radius = 60

    dragging = False
    dragged_bulb_index = None

    def check_in_socket(bulb_position):
        bx, by = bulb_position
        sx, sy = socket_position
        distance = ((bx - sx) ** 2 + (by - sy) ** 2) ** 0.5
        return distance <= socket_radius

    running = True
    result = None
    while running:
        screen.fill(WHITE)

        socket_color = GRAY
        if dragging and dragged_bulb_index is not None:
            if check_in_socket(bulb_positions[dragged_bulb_index]):
                socket_color = GREEN

        pygame.draw.circle(screen, socket_color, socket_position, socket_radius)
        draw_text("Socket", BLACK, socket_position[0], socket_position[1] - 80, font)

        for i, (x, y) in enumerate(bulb_positions):
            if dragging and i == dragged_bulb_index:
                screen.blit(bulb_image, (x - bulb_width // 2, y - bulb_height // 2))  
            else:
                screen.blit(bulb_image, (x - bulb_width // 2, y - bulb_height // 2))
            draw_text(str(wattages[i]) + " W", BLACK, x, y + 60, button_font)

        if result == "win":
            draw_text("Ai castigat!", GREEN, WIDTH // 2, 100, font)
        elif result == "lose":
            draw_text("Ai pierdut!", RED, WIDTH // 2, 100, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (x, y) in enumerate(bulb_positions):
                    if (x - 50 <= event.pos[0] <= x + 50) and (y - 50 <= event.pos[1] <= y + 50):
                        dragging = True
                        dragged_bulb_index = i
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    if check_in_socket(bulb_positions[dragged_bulb_index]):
                        if wattages[dragged_bulb_index] == correct_choice:
                            result = "win"
                        else:
                            result = "lose"
                    dragging = False
                    dragged_bulb_index = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_bulb_index is not None:
                    bulb_positions[dragged_bulb_index][0] = event.pos[0]
                    bulb_positions[dragged_bulb_index][1] = event.pos[1]

        pygame.display.flip()

    main_menu()

def sorting_trash_game():
    images = [pygame.image.load('Assets/sticla.png'),
              pygame.image.load('Assets/metal.png'),
              pygame.image.load('Assets/hartie.png'),
              pygame.image.load('Assets/mar.png'),
              pygame.image.load('Assets/plastic.png'),
              pygame.image.load('Assets/metal_2.png'),
              pygame.image.load('Assets/hartie_2.png'),
              pygame.image.load('Assets/menajer.png')]

    trash_type = []
    trash = []

    bins_type = []
    bins = []
    bins_pos = []

    for i in range(4):
        x = 100
        y = 100
        t = 1
        if i == 0:
            x = 50
            y = 50
            t = 1
        elif i == 1:
            x = 650
            y = 50
            t = 2
        elif i == 2:
            x = 650
            y = 450
            t = 3
        elif i == 3:
            x = 50
            y = 450
            t = 4

        bin = pygame.Rect(x, y, 90, 90)
        bins.append(bin)
        bins_pos.append((x, y))
        bins_type.append(t)

    for i in range(6):
        x = random.randint(150, 650)
        y = random.randint(150, 450)
        w = 40
        h = 70
        t = random.randint(0, 3)

        obj = pygame.Rect(x, y, w, h)
        trash.append(obj)
        trash_type.append(t)

    activate_box = None

    def check_in_bin(trash_pos, bin_pos):
        bx, by = trash_pos
        sx, sy = bin_pos
        distance = ((bx - sx) ** 2 + (by - sy) ** 2) ** 0.5
        return distance <= 90

    points = 0
    last = 0
    run = True
    while run:
        screen.fill(BLUE)

        for obj in range(len(trash)):
            image = None
            if trash_type[obj] == 0:
                image = images[0]
            elif trash_type[obj] == 1:
                image = images[1]
            elif trash_type[obj] == 2:
                image = images[2]
            elif trash_type[obj] == 3:
                image = images[3]
            screen.blit(image, (trash[obj].x-15, trash[obj].y))

        for obj in range(len(bins)):
            image = None
            if bins_type[obj] == 1:
                image = images[4]
            elif bins_type[obj] == 2:
                image = images[5]
            elif bins_type[obj] == 3:
                image = images[6]
            elif bins_type[obj] == 4:
                image = images[7]
            image = pygame.transform.scale(image, (120, 120))
            screen.blit(image, (bins[obj].x - 15, bins[obj].y))

        now = pygame.time.get_ticks()
        if now - last > 1000:
            x = random.randint(150, 650)
            y = random.randint(150, 450)
            w = 40
            h = 70
            t = random.randint(0, 3)

            obj = pygame.Rect(x, y, w, h)
            trash.append(obj)
            trash_type.append(t)
            last = now

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for obj in range(len(trash)):
                        if trash[obj].collidepoint(event.pos):
                            activate_box = obj

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if activate_box is not None:
                        if check_in_bin((trash[activate_box].x, trash[activate_box].y), (bins_pos[trash_type[activate_box]])):
                            points += 1
                            trash.pop(activate_box)
                            trash_type.pop(activate_box)
                        activate_box = None

            if event.type == pygame.MOUSEMOTION:
                if activate_box is not None:
                    trash[activate_box].move_ip(event.rel)

            if now >= 30000:
                run = False

            if event.type == pygame.QUIT:
                run = False

        draw_text(f"Puncte: {points}", WHITE, WIDTH // 2, 30, font)
        draw_text(f"Timp: {int(now/1000)}", WHITE, WIDTH // 2, 70, font)



        pygame.display.flip()

    main_menu()

main_menu()
