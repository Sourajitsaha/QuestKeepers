import pygame
import sys
#import ssp

def climbing(xp):
    # Initialize Pygame
    pygame.init()

    # Create window
    WIDTH, HEIGHT = 680, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Climbing")

    # Clock
    clock = pygame.time.Clock()

    # Load cloud image
    cloud_img = pygame.image.load("cloud.png").convert_alpha()
    cloud_img = pygame.transform.scale(cloud_img, (120, 80))

    # Cloud positions
    clouds = [
        [50, -100],
        [100, -300],
        [200, -500]
    ]

    # Cloud speed
    cloud_speed = 30  # pixels per second

    # Load images
    character1 = pygame.image.load("frame_001-removebg-preview.png").convert_alpha()
    character2 = pygame.image.load("frame_002-removebg-preview.png").convert_alpha()
    character3 = pygame.image.load("frame_004-removebg-preview.png").convert_alpha()

    # Resize images
    character1 = pygame.transform.scale(character1, (200, 200))
    character2 = pygame.transform.scale(character2, (200, 200))
    character3 = pygame.transform.scale(character3, (200, 200))

    frames = [character1, character2, character3]

    # Character position
    x = 247
    y = HEIGHT // 2

    # Speed in pixels per second
    speed = 50
    steps_left = xp
    step_size = 5
    step_timer = 0
    step_interval = 0.4
    running = True
    reached_peak=False
    while running:

        # Time since last frame (seconds)
        dt = clock.tick(60) / 1000
        step_timer += dt
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move character upward


        # Reset when reaching top
        if y <= 50:
            reached_peak=True
            print("Reset")
            #y = HEIGHT // 2

        # Background
        screen.fill((109, 172, 228))

        # Move and draw clouds


        # Mountain
        pygame.draw.rect(screen, (92, 41, 13), (340, 0, 340, 700))

        if steps_left>0 and not reached_peak:
              if step_timer >= step_interval:
                    step_timer = 0

                    y -= step_size
                    steps_left -= 1



              if reached_peak:
                  text_font = pygame.font.SysFont("arial", 50, bold=True)
                  text_surface = text_font.render(
                      "You reached the peak!",
                      True,
                      (255, 255, 255)
                  )
                  screen.blit(text_surface, (100, 350))
                  pygame.display.flip()  # Show the message
                  pygame.time.wait(3000)  # Wait 3 seconds
                  running = False

              # Make clouds fall down
              for cloud in clouds:
                  text_font = pygame.font.SysFont('freesanbold.ttf', 25, bold=True)
                  text_surface = text_font.render(f"Your QP left: {steps_left}", True, (0, 0, 0))
                  screen.blit(text_surface, (20, 50))
                  cloud[1] += cloud_speed * dt

                  # Reset cloud to top when it leaves screen
                  if cloud[1] > HEIGHT:
                      cloud[1] = -100

                  screen.blit(cloud_img, (cloud[0], cloud[1]))
        else:
                if steps_left==0:

                    text_font = pygame.font.SysFont("arial", 30, bold=True)
                    text_surface = text_font.render(
                        "You have used all of your QuestPoints!",
                        True,
                        (255, 255, 255)
                    )
                    screen.blit(text_surface, (100, 350))
                    pygame.display.flip()  # Show the message
                    pygame.time.wait(3000)  # Wait 3 seconds
                    running = False
                text_font=pygame.font.SysFont('freesanbold.ttf',25,bold=True)
                text_surface=text_font.render("Insufficient QuestPoints to climb",True, (0,0,0))
                screen.blit(text_surface, (20, 50))

        # Animation (change frame every 300 ms)
        frame = (pygame.time.get_ticks() // 400) % len(frames)

        # Draw character
        screen.blit(frames[frame], (x, y))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    xp = int(sys.argv[1])
    climbing(xp)