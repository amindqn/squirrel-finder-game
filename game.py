# game.py

import pygame
import sys
import random
import assets
from sprites import Player, Obstacle
from settings import *
from utils import load_font


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Squirrel Finder")
        self.clock = pygame.time.Clock()
        self.font = load_font(pygame.font.match_font("arial"), 24)
        self.running = True
        self.game_over = False
        self.game_won = False
        self.game_started = False
        self.level = 1
        self.score = 0
        self.difficulty = None

        # Load assets after initializing Pygame display
        assets.load_assets()

    def new_game(self):
        base_settings = BASE_DIFFICULTY_SETTINGS[self.difficulty]
        # Adjust difficulty based on level
        self.player_speed = max(2, base_settings["player_speed"] - self.level // 5)
        self.obstacle_speed = base_settings["obstacle_speed"] + (self.level - 1) * 0.5
        self.spawn_rate = max(500, base_settings["spawn_rate"] - (self.level - 1) * 100)
        self.rock_spawn_chance = min(
            30, (self.level - 1) * 5
        )  # Percentage chance to spawn a rock

        self.all_sprites = pygame.sprite.Group()
        self.strawberries = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.player = Player(self.player_speed)
        self.all_sprites.add(self.player)
        self.squirrel = None
        self.start_ticks = pygame.time.get_ticks()
        self.next_strawberry_time = self.start_ticks + self.spawn_rate
        self.squirrel_spawn_time = self.start_ticks + 3000

    def run(self):
        while self.running:
            if not self.game_started:
                self.show_start_screen()
            else:
                self.new_game()
                self.play_level()
                if self.game_over:
                    self.show_game_over_screen()
                elif self.game_won:
                    self.show_level_complete_screen()

    def show_start_screen(self):
        selected_option = 0
        options = ["Easy", "Medium", "Hard"]
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        self.difficulty = options[selected_option]
                        self.game_started = True
                        selecting = False

            # Drawing the selection screen
            self.screen.blit(assets.background_img, (0, 0))
            title_font = load_font(pygame.font.match_font("arial"), 48)
            title_text = title_font.render("Squirrel Finder", True, WHITE)
            self.screen.blit(
                title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100)
            )

            for idx, text in enumerate(options):
                color = (255, 215, 0) if idx == selected_option else WHITE
                option_font = load_font(pygame.font.match_font("arial"), 36)
                option_text = option_font.render(text, True, color)
                option_rect = option_text.get_rect()
                option_rect.center = (SCREEN_WIDTH // 2, 250 + idx * 80)
                self.screen.blit(option_text, option_rect)

            instruction_text = self.font.render(
                "Use UP/DOWN arrows to select difficulty, ENTER to start", True, WHITE
            )
            instruction_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            )
            self.screen.blit(instruction_text, instruction_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def play_level(self):
        self.game_over = False
        self.game_won = False
        self.all_sprites.empty()
        self.strawberries.empty()
        self.rocks.empty()
        self.player = Player(self.player_speed)
        self.all_sprites.add(self.player)
        self.squirrel = None
        self.start_ticks = pygame.time.get_ticks()
        self.next_strawberry_time = self.start_ticks + self.spawn_rate
        self.next_rock_time = (
            self.start_ticks + self.spawn_rate * 2
        )  # Rocks spawn less frequently
        self.squirrel_spawn_time = self.start_ticks + 3000

        while not self.game_over and not self.game_won:
            dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def update(self):
        # Spawning strawberries
        current_ticks = pygame.time.get_ticks()
        if current_ticks >= self.next_strawberry_time:
            strawberry = Obstacle(assets.strawberry_img, self.obstacle_speed)
            while strawberry.rect.colliderect(self.player.rect):
                strawberry.rect.x = random.randint(
                    0, SCREEN_WIDTH - strawberry.rect.width
                )
                strawberry.rect.y = random.randint(
                    0, SCREEN_HEIGHT - strawberry.rect.height
                )
            self.all_sprites.add(strawberry)
            self.strawberries.add(strawberry)
            self.next_strawberry_time += self.spawn_rate

        # Spawning rocks
        if current_ticks >= self.next_rock_time:
            if random.randint(1, 100) <= self.rock_spawn_chance:
                rock = Obstacle(assets.rock_img, self.obstacle_speed)
                while rock.rect.colliderect(self.player.rect):
                    rock.rect.x = random.randint(0, SCREEN_WIDTH - rock.rect.width)
                    rock.rect.y = random.randint(0, SCREEN_HEIGHT - rock.rect.height)
                self.all_sprites.add(rock)
                self.rocks.add(rock)
            self.next_rock_time += self.spawn_rate * 2  # Adjust the rock spawn timing

        # Spawn squirrel after delay
        if current_ticks >= self.squirrel_spawn_time and self.squirrel is None:
            self.squirrel = Obstacle(assets.squirrel_img, self.obstacle_speed)
            while self.squirrel.rect.colliderect(self.player.rect):
                self.squirrel.rect.x = random.randint(
                    0, SCREEN_WIDTH - self.squirrel.rect.width
                )
                self.squirrel.rect.y = random.randint(
                    0, SCREEN_HEIGHT - self.squirrel.rect.height
                )
            self.all_sprites.add(self.squirrel)

        # Update sprites
        keys_pressed = pygame.key.get_pressed()
        self.player.update(keys_pressed)
        self.strawberries.update()
        if self.squirrel:
            self.squirrel.update()
        self.rocks.update()

        # Check collisions
        if pygame.sprite.spritecollideany(self.player, self.strawberries):
            self.game_over = True
        if self.squirrel and pygame.sprite.collide_rect(self.player, self.squirrel):
            self.game_won = True
            self.score += 100 * self.level
        if pygame.sprite.spritecollideany(self.player, self.rocks):
            self.player.slow_down()

    def draw(self):
        self.screen.blit(assets.background_img, (0, 0))

        # Draw UI elements
        name_text = self.font.render("AminDqn", True, WHITE)
        self.screen.blit(name_text, (10, 10))
        current_ticks = pygame.time.get_ticks()
        timer_text = self.font.render(
            f"Time: {(current_ticks - self.start_ticks)//1000}", True, WHITE
        )
        self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 40))
        difficulty_text = self.font.render(
            f"Difficulty: {self.difficulty}", True, WHITE
        )
        self.screen.blit(difficulty_text, (10, 40))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_game_over_screen(self):
        message = f"You were caught by a Strawberry! Score: {self.score}. Press ENTER to restart."
        self.level = 1
        self.score = 0
        self.wait_for_key(message)

    def show_level_complete_screen(self):
        message = f"You found the Squirrel! Level up to Level {self.level + 1}. Press ENTER to continue."
        self.level += 1
        self.wait_for_key(message)

    def wait_for_key(self, message):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_won = False
                        waiting = False
                        if self.game_over:
                            self.game_started = False
                            self.game_over = False
    
            # Display the message
            self.screen.blit(assets.background_img, (0, 0))
            text_surface = self.font.render(message, True, WHITE)
            text_rect = text_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
