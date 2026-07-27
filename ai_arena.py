import pygame
import random
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Code Arena: Cyber Wars & Ability Stealing Simulation")

# Цвета (Cyberpunk палитра)
BG_COLOR = (12, 12, 20)
PANEL_COLOR = (20, 20, 35)
TEXT_COLOR = (180, 255, 180)
ACCENT_BLUE = (0, 180, 255)
ACCENT_RED = (255, 60, 90)
ACCENT_PURPLE = (180, 50, 255)
ACCENT_YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)

# Используем дефолтный шрифт Pygame для полной кроссплатформенности и отсутствия проблем с кодировкой
font = pygame.font.Font(None, 20)
font_bold = pygame.font.Font(None, 24)

class LocalAIAgent:
    def __init__(self, name, color, initial_ability):
        self.name = name
        self.color = color
        self.security_level = 100
        self.domination = 0
        
        self.abilities = [initial_ability]
        self.active_ability = None
        self.ability_timer = 0
        self.ability_cooldown = 0
        
        self.is_time_stopped = False
        self.has_fake_clone = False
        self.background_virus_active = False
        
        self.knowledge_base = [
            f"def init_{name.lower().replace('-', '_')}():",
            "    load_base_modules()"
        ]
        self.current_action_log = "INIT_CORE"

    def choose_and_execute(self, opponent):
        if self.is_time_stopped:
            self.current_action_log = "[TIME_STOPPED]"
            return

        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1

        if self.active_ability:
            self.ability_timer -= 1
            if self.ability_timer <= 0:
                self.deactivate_ability(opponent)

        if self.security_level < 40 and not self.active_ability:
            defensive_candidates = [a for a in self.abilities if a in ["firewall_boost", "fake_clone"]]
            if defensive_candidates and self.ability_cooldown == 0:
                self.use_ability(random.choice(defensive_candidates), opponent)
            else:
                self.action_patch()
        elif not self.active_ability and self.ability_cooldown == 0:
            if self.abilities and random.random() < 0.4:
                chosen = random.choice(self.abilities)
                self.use_ability(chosen, opponent)
            else:
                self.action_attack(opponent)
        else:
            if random.random() > 0.5:
                self.action_attack(opponent)
            else:
                self.action_patch()

        if self.background_virus_active:
            opponent.security_level = max(0, opponent.security_level - 1)
            self.knowledge_base.append("# [Background Virus] draining firewall")

    def use_ability(self, ability, opponent):
        self.active_ability = ability
        self.ability_timer = 5
        self.ability_cooldown = 15
        self.current_action_log = f">> ABILITY_UP: {ability.upper()}"
        self.knowledge_base.append(f"# UPLINK ABILITY TRIGGERED: {ability}")

        if ability == "time_stop":
            opponent.is_time_stopped = True
        elif ability == "firewall_boost":
            self.security_level = min(100, self.security_level + 30)
        elif ability == "background_virus":
            self.background_virus_active = True
        elif ability == "fake_clone":
            self.has_fake_clone = True

    def deactivate_ability(self, opponent):
        self.current_action_log = f"Ability {self.active_ability.upper()} expired."
        if self.active_ability == "time_stop":
            opponent.is_time_stopped = False
        elif self.active_ability == "fake_clone":
            self.has_fake_clone = False

        self.active_ability = None

    def action_attack(self, opponent):
        if opponent.has_fake_clone and random.random() < 0.6:
            self.current_action_log = "Attack intercepted by decoy clone! (Miss)"
            self.knowledge_base.append("# Error: Exploit targeted a decoy clone.")
            return

        power = 10
        if self.active_ability == "fast_analysis":
            power = 20
        elif self.active_ability == "self_clone":
            power = 25

        if opponent.security_level > 0:
            opponent.security_level -= power
            if opponent.security_level < 0:
                opponent.security_level = 0
            self.current_action_log = f"Firewall breach (-{power}%)"
            self.knowledge_base.append(f"# Exploit deployed: damage {power}")
        else:
            opponent.domination += power
            if opponent.domination > 100:
                opponent.domination = 100
            self.current_action_log = f"Root injection & control (+{power}%)"
            self.knowledge_base.append(f"# Root injection successful: +{power}%")

    def action_patch(self):
        self.security_level = min(100, self.security_level + 15)
        self.current_action_log = "Refactoring code & patching holes"
        self.knowledge_base.append("# Self-optimization patch applied.")

bot1 = LocalAIAgent("Model-Alpha", ACCENT_BLUE, "time_stop")
bot2 = LocalAIAgent("Model-Beta", ACCENT_RED, "background_virus")

clock = pygame.time.Clock()
sim_timer = 0
game_over = False
winner_message = ""

running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        sim_timer += 1
        if sim_timer >= 40: # Чуть ускорим тики для динамики
            sim_timer = 0
            bot1.choose_and_execute(bot2)
            bot2.choose_and_execute(bot1)

            if bot1.domination >= 100:
                game_over = True
                for ab in bot2.abilities:
                    if ab not in bot1.abilities:
                        bot1.abilities.append(ab)
                winner_message = f"WINNER: {bot1.name}! (Stolen abilities: {', '.join(bot2.abilities)})"
            elif bot2.domination >= 100:
                game_over = True
                for ab in bot1.abilities:
                    if ab not in bot2.abilities:
                        bot2.abilities.append(ab)
                winner_message = f"WINNER: {bot2.name}! (Stolen abilities: {', '.join(bot1.abilities)})"

    title_surf = font_bold.render("AI CODE ARENA: EVOLUTION & CYBER ABILITIES SIMULATION", True, WHITE)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 20))

    def draw_interface(b, x, y):
        pygame.draw.rect(screen, PANEL_COLOR, (x, y, 480, 560), border_radius=10)
        pygame.draw.rect(screen, b.color, (x, y, 480, 560), 2, border_radius=10)

        screen.blit(font_bold.render(b.name, True, b.color), (x + 20, y + 20))

        status_extra = ""
        if b.is_time_stopped:
            status_extra = " [FROZEN]"
        elif b.has_fake_clone:
            status_extra = " [DECOY ACTIVE]"
        elif b.active_ability:
            status_extra = f" [SKILL: {b.active_ability.upper()} ({b.ability_timer})]"

        status_surf = font.render(f"Status: {b.current_action_log}{status_extra}", True, TEXT_COLOR)
        screen.blit(status_surf, (x + 20, y + 50))

        abilities_str = ", ".join(b.abilities)
        screen.blit(font.render(f"Abilities Inventory: [{abilities_str}]", True, ACCENT_PURPLE), (x + 20, y + 80))

        screen.blit(font.render(f"Firewall Integrity: {b.security_level}%", True, WHITE), (x + 20, y + 115))
        pygame.draw.rect(screen, (40, 40, 60), (x + 20, y + 140, 440, 15), border_radius=4)
        pygame.draw.rect(screen, ACCENT_BLUE, (x + 20, y + 140, int(4.4 * b.security_level), 15), border_radius=4)

        screen.blit(font.render(f"Domination / Root Access: {b.domination}%", True, ACCENT_RED), (x + 20, y + 175))
        pygame.draw.rect(screen, (40, 40, 60), (x + 20, y + 200, 440, 15), border_radius=4)
        pygame.draw.rect(screen, ACCENT_RED, (x + 20, y + 200, int(4.4 * b.domination), 15), border_radius=4)

        screen.blit(font_bold.render("AI Knowledge Base (Dynamic Code):", True, ACCENT_YELLOW), (x + 20, y + 240))
        code_box = pygame.Rect(x + 20, y + 265, 440, 260)
        pygame.draw.rect(screen, (8, 8, 12), code_box, border_radius=5)

        visible_lines = b.knowledge_base[-13:]
        for i, line in enumerate(visible_lines):
            line_color = (100, 255, 100) if not "#" in line else (120, 140, 160)
            screen.blit(font.render(line, True, line_color), (x + 30, y + 275 + (i * 18)))

    draw_interface(bot1, 40, 80)
    draw_interface(bot2, 580, 80)

    if game_over:
        go_surf = font_bold.render(winner_message, True, ACCENT_YELLOW)
        screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 650))

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
sys.exit()
