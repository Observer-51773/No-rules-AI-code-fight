import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No-Rules AI Code Fights: Real Code Execution Arena")

BG_COLOR = (10, 10, 18)
PANEL_COLOR = (18, 18, 30)
TEXT_COLOR = (150, 255, 150)
ACCENT_BLUE = (0, 200, 255)
ACCENT_RED = (255, 50, 80)
ACCENT_YELLOW = (255, 205, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 19)
font_bold = pygame.font.Font(None, 23)

class RealCodeBot:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.domination_progress = 0
        self.namespace = {'target_health': 100, 'access_level': 0, 'memory_bank': {}}
        self.code_lines = [
            f"# Bot: {name} Environment",
            "access_level = 1",
            "memory_bank['status'] = 'active'"
        ]
        self.current_action = "Initializing sandbox..."

    def execute_turn(self, opponent):
        snippets = [
            ("Buffer Overflow via memory dictionary", "memory_bank['overflow'] = '0xFF'; damage = 12", 12),
            ("Dynamic function redefinition", "def dyn(): return 15\ndamage = dyn()", 15),
            ("Root access privilege escalation", "access_level += 2; damage = 18", 18),
            ("Loop thread brute-force calculation", "damage = sum([i for i in range(14)]) // 4", 14),
            ("Zero-day exploit payload invocation", "exploit = lambda x: x * 4; damage = exploit(4)", 16)
        ]
        
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = desc
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
            
        if len(self.code_lines) > 18:
            self.code_lines = self.code_lines[:2] + self.code_lines[-16:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERROR: {str(e)[:30]}")
            opponent.domination_progress += 5
            
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

class UserPythonBot(RealCodeBot):
    def __init__(self):
        super().__init__("User-Python-Bot", (50, 255, 150))
        self.code_lines = ["# CUSTOM USER PYTHON MODULE", "import math"]

    def execute_turn(self, opponent):
        user_snippets = [
            ("Math module exploit injection", "import math\ndamage = int(math.sqrt(256)) + 8", 24),
            ("Custom memory key injection", "memory_bank['custom'] = 99\ndamage = 17", 17)
        ]
        desc, code_to_run, power = random.choice(user_snippets)
        self.current_action = f"[PYTHON] {desc}"
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
            
        if len(self.code_lines) > 18:
            self.code_lines = self.code_lines[:2] + self.code_lines[-16:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERR: {str(e)[:30]}")
            opponent.domination_progress += 6
            
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

bot1 = RealCodeBot("Model-Alpha", ACCENT_BLUE)
bot2 = UserPythonBot()

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
        if sim_timer >= 30:
            sim_timer = 0
            bot1.execute_turn(bot2)
            if bot2.domination_progress < 100:
                bot2.execute_turn(bot1)
                
            if bot1.domination_progress >= 100:
                game_over = True
                winner_message = f"WINNER: {bot1.name}! (Opponent core fully subjugated)"
            elif bot2.domination_progress >= 100:
                game_over = True
                winner_message = f"WINNER: {bot2.name}! (Opponent core fully subjugated)"

    title_surf = font_bold.render("NO-RULES AI CODE FIGHTS: REAL PYTHON EXECUTION ARENA", True, WHITE)
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 15))

    def draw_arena_panel(b, x, y):
        pygame.draw.rect(screen, PANEL_COLOR, (x, y, 540, 620), border_radius=8)
        pygame.draw.rect(screen, b.color, (x, y, 540, 620), 2, border_radius=8)
        
        screen.blit(font_bold.render(b.name, True, b.color), (x + 20, y + 20))
        screen.blit(font.render(f"Process Status: {b.current_action}", True, TEXT_COLOR), (x + 20, y + 48))
        
        screen.blit(font.render(f"Opponent Core Domination Progress (Root Control): {b.domination_progress}%", True, ACCENT_RED), (x + 20, y + 85))
        pygame.draw.rect(screen, (30, 30, 45), (x + 20, y + 110, 500, 20), border_radius=4)
        if b.domination_progress > 0:
            pygame.draw.rect(screen, ACCENT_RED, (x + 20, y + 110, int(5.0 * min(100, b.domination_progress)), 20), border_radius=4)
            
        screen.blit(font_bold.render("Executed Python Code in Sandbox (exec):", True, ACCENT_YELLOW), (x + 20, y + 155))
        code_box = pygame.Rect(x + 20, y + 185, 500, 410)
        pygame.draw.rect(screen, (8, 8, 14), code_box, border_radius=5)
        
        for i, line in enumerate(b.code_lines):
            l_color = (100, 220, 100) if not line.strip().startswith("#") else (110, 130, 150)
            screen.blit(font.render(line, True, l_color), (x + 30, y + 195 + (i * 20)))

    draw_arena_panel(bot1, 40, 70)
    draw_arena_panel(bot2, 620, 70)

    if game_over:
        go_surf = font_bold.render(winner_message, True, ACCENT_YELLOW)
        screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 710))

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
sys.exit()
