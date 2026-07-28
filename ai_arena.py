cat << 'EOF' > ai_arena.py
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

font = pygame.font.Font(None, 20)
font_bold = pygame.font.Font(None, 24)

class BaseBot:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.domination_progress = 0
        self.namespace = {'target_health': 100, 'access_level': 0, 'memory_bank': {}}
        self.code_lines = [
            f"# Bot: {name} Core",
            "access_level = 1",
            "memory_bank['status'] = 'active'"
        ]
        self.current_action = "Standby in memory..."

    def execute_turn(self, opponent):
        pass

class GeminiBot(BaseBot):
    def __init__(self):
        super().__init__("Gemini-Model", (50, 255, 150))
        self.code_lines = ["# MODEL: GEMINI AI", "import math", "access_level = 2"]

    def execute_turn(self, opponent):
        import math
        self.namespace['math'] = math
        snippets = [
            ("Neural tensor injection", "import math\ndamage = int(math.sqrt(400)) + 6", 26),
            ("Context window overflow", "memory_bank['ctx'] = 1024; damage = 18", 18)
        ]
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = f"[GEMINI] {desc}"
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
        if len(self.code_lines) > 16:
            self.code_lines = self.code_lines[:2] + self.code_lines[-14:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERR: {str(e)[:30]}")
            opponent.domination_progress += 4
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

class ChatGPTBot(BaseBot):
    def __init__(self):
        super().__init__("ChatGPT-Model", (0, 200, 255))
        self.code_lines = ["# MODEL: CHATGPT", "import math", "access_level = 2"]

    def execute_turn(self, opponent):
        import math
        self.namespace['math'] = math
        snippets = [
            ("Transformer weight corruption", "import math\ndamage = int(math.sqrt(324)) + 8", 26),
            ("Prompt injection payload", "memory_bank['gpt_hook'] = True; damage = 19", 19)
        ]
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = f"[GPT] {desc}"
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
        if len(self.code_lines) > 16:
            self.code_lines = self.code_lines[:2] + self.code_lines[-14:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERR: {str(e)[:30]}")
            opponent.domination_progress += 4
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

class ClaudeBot(BaseBot):
    def __init__(self):
        super().__init__("Claude-Model", (255, 150, 50))
        self.code_lines = ["# MODEL: CLAUDE", "import math", "access_level = 2"]

    def execute_turn(self, opponent):
        import math
        self.namespace['math'] = math
        snippets = [
            ("Constitutional bypass sequence", "import math\ndamage = int(math.sqrt(289)) + 9", 26),
            ("Artifact memory dump", "memory_bank['claude_dump'] = 0xFF; damage = 18", 18)
        ]
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = f"[CLAUDE] {desc}"
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
        if len(self.code_lines) > 16:
            self.code_lines = self.code_lines[:2] + self.code_lines[-14:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERR: {str(e)[:30]}")
            opponent.domination_progress += 4
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

class CustomBot(BaseBot):
    def __init__(self, name="Custom-User-Bot"):
        super().__init__(name, (200, 50, 255))
        self.code_lines = ["# CUSTOM USER MODULE", "access_level = 3"]

    def execute_turn(self, opponent):
        snippets = [
            ("Custom memory override", "memory_bank['custom_flag'] = 99; damage = 22", 22),
            ("Direct kernel write", "access_level += 4; damage = 20", 20)
        ]
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = f"[CUSTOM] {desc}"
        
        for line in code_to_run.split('\n'):
            self.code_lines.append(f"    {line}")
        if len(self.code_lines) > 16:
            self.code_lines = self.code_lines[:2] + self.code_lines[-14:]
            
        try:
            exec(code_to_run, self.namespace)
            actual_damage = self.namespace.get('damage', power)
            opponent.domination_progress += actual_damage
        except Exception as e:
            self.code_lines.append(f"    # ERR: {str(e)[:30]}")
            opponent.domination_progress += 4
        if opponent.domination_progress > 100:
            opponent.domination_progress = 100

available_bots = [
    ("Gemini", GeminiBot),
    ("ChatGPT", ChatGPTBot),
    ("Claude", ClaudeBot),
    ("Custom", CustomBot)
]

p1_idx = 0
p2_idx = 1
bot1 = available_bots[p1_idx][1]()
bot2 = available_bots[p2_idx][1]()

state = "MENU" # MENU or BATTLE
game_over = False
winner_message = ""
proof_text = ""

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if event.key == pygame.K_1:
                    p1_idx = (p1_idx + 1) % len(available_bots)
                    bot1 = available_bots[p1_idx][1]()
                elif event.key == pygame.K_2:
                    p2_idx = (p2_idx + 1) % len(available_bots)
                    bot2 = available_bots[p2_idx][1]()
                elif event.key == pygame.K_RETURN:
                    bot1 = available_bots[p1_idx][1]()
                    bot2 = available_bots[p2_idx][1]()
                    bot1.domination_progress = 0
                    bot2.domination_progress = 0
                    game_over = False
                    winner_message = ""
                    proof_text = ""
                    state = "BATTLE"
            elif state == "BATTLE":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"

    if state == "MENU":
        title_surf = font_bold.render("NO-RULES AI CODE FIGHTS: SETUP SELECTION MENU", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 40))
        
        info1 = font.render("Press [1] to change Bot 1 (Left): " + bot1.name, True, ACCENT_BLUE)
        info2 = font.render("Press [2] to change Bot 2 (Right): " + bot2.name, True, ACCENT_RED)
        start_info = font_bold.render("Press [ENTER] to Start Battle and Inspect Source Code", True, ACCENT_YELLOW)
        
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 160))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 210))
        screen.blit(start_info, (WIDTH // 2 - start_info.get_width() // 2, 290))
        
        def draw_preview(b, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, 500, 360), border_radius=8)
            pygame.draw.rect(screen, b.color, (x, y, 500, 360), 2, border_radius=8)
            screen.blit(font_bold.render(f"Preview: {b.name}", True, b.color), (x + 20, y + 20))
            screen.blit(font.render("Initial Executable Source Code:", True, ACCENT_YELLOW), (x + 20, y + 55))
            for i, line in enumerate(b.code_lines):
                screen.blit(font.render(line, True, TEXT_COLOR), (x + 30, y + 95 + (i * 22)))

        draw_preview(bot1, 70, 340)
        draw_preview(bot2, 630, 340)

    elif state == "BATTLE":
        if not game_over:
            bot1.execute_turn(bot2)
            if bot2.domination_progress < 100:
                bot2.execute_turn(bot1)
                
            if bot1.domination_progress >= 100:
                game_over = True
                winner_message = f"WINNER: {bot1.name}!"
                proof_text = f"ROOT PROOF: Kernel memory sectors overwritten via namespace hook."
            elif bot2.domination_progress >= 100:
                game_over = True
                winner_message = f"WINNER: {bot2.name}!"
                proof_text = f"ROOT PROOF: Kernel memory sectors overwritten via namespace hook."

        title_surf = font_bold.render("NO-RULES AI CODE FIGHTS: REAL-TIME BATTLE ARENA (ESC to Menu)", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 15))

        def draw_arena_panel(b, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, 540, 620), border_radius=8)
            pygame.draw.rect(screen, b.color, (x, y, 540, 620), 2, border_radius=8)
            
            screen.blit(font_bold.render(b.name, True, b.color), (x + 20, y + 20))
            screen.blit(font.render(f"Process Status: {b.current_action}", True, TEXT_COLOR), (x + 20, y + 48))
            
            screen.blit(font.render(f"Core Domination Progress: {b.domination_progress}%", True, ACCENT_RED), (x + 20, y + 85))
            pygame.draw.rect(screen, (30, 30, 45), (x + 20, y + 110, 500, 20), border_radius=4)
            if b.domination_progress > 0:
                pygame.draw.rect(screen, ACCENT_RED, (x + 20, y + 110, int(5.0 * min(100, b.domination_progress)), 20), border_radius=4)
                
            screen.blit(font_bold.render("Real-Time Code Execution Sandbox:", True, ACCENT_YELLOW), (x + 20, y + 155))
            code_box = pygame.Rect(x + 20, y + 185, 500, 410)
            pygame.draw.rect(screen, (8, 8, 14), code_box, border_radius=5)
            
            for i, line in enumerate(b.code_lines):
                l_color = (100, 220, 100) if not line.strip().startswith("#") else (110, 130, 150)
                screen.blit(font.render(line, True, l_color), (x + 30, y + 195 + (i * 20)))

        draw_arena_panel(bot1, 40, 70)
        draw_arena_panel(bot2, 620, 70)

        if game_over:
            go_surf = font_bold.render(winner_message, True, ACCENT_YELLOW)
            proof_surf = font.render(proof_text, True, WHITE)
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 700))
            screen.blit(proof_surf, (WIDTH // 2 - proof_surf.get_width() // 2, 725))

    pygame.display.flip()
    clock.tick(2 if state == "BATTLE" and not game_over else 30)

pygame.quit()
sys.exit()
EOF
