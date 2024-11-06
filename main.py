import pygame
import sys
import random

#i love naming my varibles stupid stuff but this was for a grade so i had to actaully name them in a way my teacher could read

# pygame stuff
pygame.init()

# const
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# loading images
def load_image(path, max_width=None, max_height=None):
    image = pygame.image.load(path)
    if max_width or max_height:
        original_width, original_height = image.get_size()
        aspect_ratio = original_width / original_height
        if max_width and max_height:
            if original_width > original_height:
                new_width = max_width
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
        elif max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        elif max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        image = pygame.transform.scale(image, (new_width, new_height))
    return image

# actually loading the images
sans_image = load_image('images/sans.png', max_width=150)
heart_image = load_image('images/heart.png', max_width=50)
bone_image = load_image('images/bones.png', max_width=50)

# display settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale Battle Simulation")
clock = pygame.time.Clock()

def draw_border():
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100), 5)

# Difficulty selector function
def difficulty_selector():
    global BONE_SPAWN_RATE
    font = pygame.font.Font(None, 50)
    difficulty_options = ["Easy", "Medium", "Hard"]
    selected_index = 0

    while True:
        screen.fill((0, 0, 0))
        draw_border()

        # render title
        title_text = font.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # render difficulty options
        for i, option in enumerate(difficulty_options):
            if i == selected_index:
                option_text = font.render(option, True, WHITE)
                screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))
                pygame.draw.rect(screen, WHITE, (WIDTH // 2 - option_text.get_width() // 2 - 10, 200 + i * 50 - 10, option_text.get_width() + 20, option_text.get_height() + 20), 2)
            else:
                option_text = font.render(option, True, (100, 100, 100))
                screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 200 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(difficulty_options)
                if event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(difficulty_options)
                if event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        BONE_SPAWN_RATE = 50  # easy
                    elif selected_index == 1:
                        BONE_SPAWN_RATE = 30  # medium
                    elif selected_index == 3:
                        BONE_SPAWN_RATE = 20  # hard
                    return

        pygame.display.flip()
        clock.tick(FPS)

# bones
BONE_SPAWN_RATE = 40  # i have it set at medium for normal
bones = []

# the game itself
def main_game():
    global player_pos, current_time, high_score, bones
    player_pos = [WIDTH // 2, HEIGHT // 2]
    current_time = 0
    high_score = 0
    bones = []

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_border()

        # sans the funny skeleton, idk if im gonna make him do anything
        sans_rect = sans_image.get_rect(center=(WIDTH // 2, 100))
        screen.blit(sans_image, sans_rect.topleft)

        # update player 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_pos[1] > 50:  # up
            player_pos[1] -= 5
        if keys[pygame.K_s] and player_pos[1] < HEIGHT - 50 - heart_image.get_height():  # down
            player_pos[1] += 5
        if keys[pygame.K_a] and player_pos[0] > 50:  # left
            player_pos[0] -= 5
        if keys[pygame.K_d] and player_pos[0] < WIDTH - 50 - heart_image.get_width():  # right
            player_pos[0] += 5

        # drawing the player
        screen.blit(heart_image, (player_pos[0], player_pos[1]))

        # spawns the bones
        if random.randint(1, BONE_SPAWN_RATE) == 1:  # Use the defined BONE_SPAWN_RATE
            bone_data = spawn_bone()
            bones.append({"position": list(bone_data[0]), "direction": bone_data[1], "angle": 0})

        # drawing and moving the bones
        for bone in bones[:]:
            if bone["direction"] == "LEFT":
                bone["position"][0] += 3  # right
            elif bone["direction"] == "RIGHT":
                bone["position"][0] -= 3  # left
            elif bone["direction"] == "TOP":
                bone["position"][1] += 3  # down
            elif bone["direction"] == "BOTTOM":
                bone["position"][1] -= 3  # up

            bone["angle"] += 5  
            if bone["angle"] >= 360:
                bone["angle"] = 0  

            rotated_bone = pygame.transform.rotate(bone_image, bone["angle"])
            rotated_rect = rotated_bone.get_rect(center=(bone["position"][0] + rotated_bone.get_width() // 2, bone["position"][1] + rotated_bone.get_height() // 2))
            screen.blit(rotated_bone, rotated_rect.topleft)

            player_rect = pygame.Rect(player_pos[0], player_pos[1], heart_image.get_width(), heart_image.get_height())
            if check_collision(player_rect, rotated_rect):
                current_time = 0  # reset current time on collision
                bones.remove(bone)  # get rid of the bone after colliding

            # get rid of off-screen bones
            if (bone["position"][0] < 0 or bone["position"][0] > WIDTH or 
                bone["position"][1] < 0 or bone["position"][1] > HEIGHT):
                bones.remove(bone)

        # update time
        current_time += 1 / FPS

        # Update high score
        if current_time > high_score:
            high_score = current_time

        # draw the timer things
        font = pygame.font.Font(None, 50)
        current_time_text = font.render(f'Current Score: {int(current_time)}', True, WHITE)
        high_score_text = font.render(f'High Score: {int(high_score)}', True, WHITE)
        screen.blit(current_time_text, (50, 20))
        screen.blit(high_score_text, (WIDTH - int(high_score_text.get_width() + 50), 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(FPS)

def spawn_bone():
    side = random.choice(['LEFT', 'RIGHT', 'TOP', 'BOTTOM'])
    if side == 'LEFT':
        return [0, random.randint(50, HEIGHT - 50)], side  # x, y, and direction
    elif side == 'RIGHT':
        return [WIDTH, random.randint(50, HEIGHT - 50)], side
    elif side == 'TOP':
        return [random.randint(50, WIDTH - 100), 0], side
    elif side == 'BOTTOM':
        return [random.randint(50, WIDTH - 100), HEIGHT], side

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Start the game
difficulty_selector()
main_game()
pygame.quit()