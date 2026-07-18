import pygame
import sys

# Initialize Pygame
pygame.init()

# Create window
WIDTH, HEIGHT = 680, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Climbing Game")

# Clock to control FPS
clock = pygame.time.Clock()

# Load images
character1 = pygame.image.load("frame_001-removebg-preview.png").convert_alpha()
character2 = pygame.image.load("frame_002-removebg-preview.png").convert_alpha()
character3 = pygame.image.load("frame_004-removebg-preview.png").convert_alpha()

# Resize images (change size if needed)
character1 = pygame.transform.scale(character1, (200, 200))
character2 = pygame.transform.scale(character2, (200, 200))
character3 = pygame.transform.scale(character3, (200, 200))
# Store frames in a list
frames = [character1, character2,character3]

# Character position
x = 247
y = 350

speed=0.007


running = True

while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    y -= speed
    if y <= 50:
        # Move player upward
        print("reset")
        y = HEIGHT // 2


    # Background
    screen.fill((135, 206, 235))

    # Mountain / wall
    pygame.draw.rect(screen, (92,41,13), (340,0,340,700))

    # Change frame every 200 milliseconds
    frame = (pygame.time.get_ticks() // 900) % len(frames)

    # Draw character
    screen.blit(frames[frame], (x, y))

    # Update display
    pygame.display.update()

    # Limit to 60 FPS
    clock.tick(60)

pygame.quit()
sys.exit()