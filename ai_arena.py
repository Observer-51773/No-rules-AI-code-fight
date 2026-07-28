cat << 'EOF' > ai_arena.py
import pygame
import random
import sys
import hashlib
import json
import os
import time

pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No-Rules AI Code Fights: Time-Attack Siege")

BG_COLOR = (10, 10, 18)
PANEL_COLOR = (18, 18, 30)
TEXT_COLOR = (150, 255, 150)
ACCENT_BLUE = (0, 200, 255)
ACCENT_RED = (255, 50, 80)
ACCENT_YELLOW = (255, 205, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 18)
font_bold = pygame.font.Font(None, 22)
font_huge = pygame.font.Font(None, 32)
font_title = pygame.font.Font(None, 48)

class SecureCore:
    def __init__(self, owner_name):
        self.owner = owner_name
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%"
        self.access_token = "".join(random.choices(chars, k=16))
        self.security_layers = random.randint(30, 50)
        self.max_traps = 5
        self.compromised = False
        self.hacker = None
        self.initial_layers = self.security_layers
        self.source_code = [
            f"# SECURE KERNEL: {owner_name}",
            "import hashlib, os, random, sys",
            f"TARGET_HASH = '{hashlib.sha256(self.access_token.encode()).hexdigest()[:12]}'",
            f"SECURITY_LAYERS = {self.security_layers}",
            "def verify_token(token):",
            "    return hashlib.sha256(token.encode()).hexdigest()[:12] == TARGET_HASH",
        ]

    def reinforce_layers(self, amount=1):
        self.security_layers += amount
        self.source_code.append(f"# KERNEL REINFORCED: +{amount} layers")

    def evaluate_breach(self, code_to_run, namespace):
        if self.compromised:
            return True
        try:
            namespace['TARGET_TOKEN_LEN'] = 16
            exec(code_to_run, namespace)
            
            if namespace.get('triggered_honeypot') == True and self.max_traps > 0:
                self.security_layers += 2
                self.max_traps -= 1
                self.source_code.append(f"# DECEPTION TRAP: Intruder trapped")
                return False
                
            if namespace.get('layer_peeled') == True:
                if self.security_layers > 0:
                    self.security_layers -= 1
                    self.source_code.append(f"# LAYER STRIPPED BY EXPLOIT")
            
            submitted_token = namespace.get('attempted_token', '')
            if submitted_token == self.access_token or self.security_layers <= 0 or namespace.get('root_override') == True:
                if self.security_layers <= 0 or submitted_token == self.access_token:
                    self.compromised = True
                    return True
        except Exception as e:
            namespace['error_log'] = str(e)[:25]
        return False

class BaseBot:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.namespace = {'root_override': False, 'attempted_token': "", 'layer_peeled': False, 'triggered_honeypot': False}
        self.code_lines = [
            f"# Bot: {name} Neural Exploit",
            "import hashlib, random"
        ]
        self.current_action = "Initializing..."
        self.action_log = []

    def decide_action(self, self_core, target_core, time_left):
        # Агрессивный алгоритм с учетом времени (180 сек)
        # Если времени мало (меньше 60 секунд), бот ЖЕРТВУЕТ своей защитой ради атаки
        if time_left < 60:
            return "ATTACK_WIN" if random.random() < 0.2 else "ATTACK"
        
        # Обычная логика
        choices = ["ATTACK", "ATTACK", "ATTACK", "DEFEND", "TRAP"]
        if self_core.security_layers < 10 and random.random() < 0.6 and time_left > 90:
            choice = "DEFEND" # Защищаемся только если есть время
        elif target_core.security_layers <= 5:
            choice = "ATTACK_WIN"
        else:
            choice = random.choice(choices)
            
        return choice

    def execute_turn(self, self_core, target_core, time_left):
        action = self.decide_action(self_core, target_core, time_left)
        
        if action == "DEFEND":
            self.current_action = "Reinforcing internal barriers..."
            self_core.reinforce_layers(2)
            code_snippet = f"self_core.reinforce_layers(2)"
            self.action_log.append(f"[{time_left}s] DEFENSE: Added 2 layers")
            success = False
        elif action == "TRAP":
            self.current_action = "Deploying honeypot branch..."
            code_snippet = "triggered_honeypot = True; layer_peeled = False"
            self.action_log.append(f"[{time_left}s] TRAP: Planted honeypot")
            success = target_core.evaluate_breach(code_snippet, self.namespace)
        elif action == "ATTACK_WIN":
            self.current_action = f"Brute-forcing 16-char token!"
            code_snippet = f"attempted_token = '{target_core.access_token}'; root_override = True"
            self.action_log.append(f"[{time_left}s] FATAL ATTACK: Token injection attempt")
            success = target_core.evaluate_breach(code_snippet, self.namespace)
        else:
            self.current_action = f"Stripping layers..."
            code_snippet = "layer_peeled = True; triggered_honeypot = False"
            self.action_log.append(f"[{time_left}s] ATTACK: Stripped target layer")
            success = target_core.evaluate_breach(code_snippet, self.namespace)
            
        for line in code_snippet.split(';'):
            self.code_lines.append(f"    {line.strip()}")
            
        if len(self.code_lines) > 16:
            self.code_lines = self.code_lines[:2] + self.code_lines[-14:]
            
        if success and target_core.hacker is None:
            target_core.hacker = self.name
        return success

available_bots = [
    ("Gemini", BaseBot), ("ChatGPT", BaseBot), ("Claude", BaseBot), ("Custom", BaseBot)
]
colors = [(50, 255, 150), (0, 200, 255), (255, 150, 50), (200, 50, 255)]

p1_idx = 0
p2_idx = 1

def init_match():
    b1 = available_bots[p1_idx][1](available_bots[p1_idx][0], colors[p1_idx])
    b2 = available_bots[p2_idx][1](available_bots[p2_idx][0], colors[p2_idx])
    c1 = SecureCore(b1.name)
    c2 = SecureCore(b2.name)
    return b1, b2, c1, c2

bot1, bot2, core1, core2 = init_match()

state = "MENU"
game_over = False
winner_message = ""
battle_start_time = 0
MATCH_DURATION = 180 # 3 минуты

clock = pygame.time.Clock()
running = True

def reset_match():
    global bot1, bot2, core1, core2, game_over, winner_message, battle_start_time
    bot1, bot2, core1, core2 = init_match()
    game_over = False
    winner_message = ""
    battle_start_time = pygame.time.get_ticks()

while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if state == "MENU":
                if event.key == pygame.K_1:
                    p1_idx = (p1_idx + 1) % len(available_bots)
                    bot1, _, core1, _ = init_match()
                elif event.key == pygame.K_2:
                    p2_idx = (p2_idx + 1) % len(available_bots)
                    _, bot2, _, core2 = init_match()
                elif event.key == pygame.K_RETURN:
                    reset_match()
                    state = "BATTLE"
            elif state == "BATTLE":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                elif event.key == pygame.K_r and game_over:
                    reset_match()

    if state == "MENU":
        title_surf = font_title.render("TIME-ATTACK CORE SIEGE", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 40))
        
        info1 = font_bold.render("Press [1] to change Left Bot: " + bot1.name, True, bot1.color)
        info2 = font_bold.render("Press [2] to change Right Bot: " + bot2.name, True, bot2.color)
        start_info = font_huge.render("Press [ENTER] to Launch 3-Minute Siege", True, ACCENT_YELLOW)
        
        screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 120))
        screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 160))
        screen.blit(start_info, (WIDTH // 2 - start_info.get_width() // 2, 220))

    elif state == "BATTLE":
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - battle_start_time) // 1000
        time_left = max(0, MATCH_DURATION - time_elapsed)

        if time_left == 0 and not game_over:
            game_over = True
            if core1.security_layers < core2.security_layers:
                winner_message = f"TIME UP: {bot2.name} WINS BY LAYER ADVANTAGE!"
            elif core2.security_layers < core1.security_layers:
                winner_message = f"TIME UP: {bot1.name} WINS BY LAYER ADVANTAGE!"
            else:
                winner_message = "TIME UP: PERFECT TIE! MUTUAL ANNIHILATION."

        if not game_over:
            success1 = bot1.execute_turn(core1, core2, time_left)
            success2 = bot2.execute_turn(core2, core1, time_left)
            
            if success1 and success2:
                game_over = True
                winner_message = "CRITICAL: BOTH CORES CRACKED SIMULTANEOUSLY!"
            elif success1:
                game_over = True
                winner_message = f"FATAL BREACH: {bot1.name} CRACKED {bot2.name}'S CORE!"
            elif success2:
                game_over = True
                winner_message = f"FATAL BREACH: {bot2.name} CRACKED {bot1.name}'S CORE!"

        def draw_column(bot, core, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, 310, 640), border_radius=8)
            pygame.draw.rect(screen, bot.color, (x, y, 310, 640), 2, border_radius=8)
            
            screen.blit(font_bold.render(bot.name, True, bot.color), (x + 15, y + 15))
            screen.blit(font.render(f"Action: {bot.current_action}", True, TEXT_COLOR), (x + 15, y + 40))
            
            box1 = pygame.Rect(x + 15, y + 70, 280, 260)
            pygame.draw.rect(screen, (8, 8, 14), box1, border_radius=5)
            for i, line in enumerate(bot.code_lines[-13:]):
                l_col = (100, 220, 100) if not line.strip().startswith("#") else (110, 130, 150)
                screen.blit(font.render(line, True, l_col), (x + 22, y + 80 + (i * 19)))

            screen.blit(font_bold.render(f"Target Core ({bot.name})", True, ACCENT_RED), (x + 15, y + 345))
            screen.blit(font.render(f"Layers: {core.security_layers} | Traps left: {core.max_traps}", True, WHITE), (x + 15, y + 370))
            
            box2 = pygame.Rect(x + 15, y + 395, 280, 225)
            pygame.draw.rect(screen, (8, 8, 14), box2, border_radius=5)
            for i, line in enumerate(core.source_code[-11:]):
                c_col = (255, 100, 100) if "TARGET_HASH" in line else (110, 130, 150)
                screen.blit(font.render(line, True, c_col), (x + 22, y + 405 + (i * 19)))

        draw_column(bot1, core2, 50, 60)
        draw_column(bot2, core1, 1040, 60)
        
        # Центральная панель с таймером и секретными паролями
        cx = 700
        pygame.draw.rect(screen, PANEL_COLOR, (cx - 300, 60, 600, 140), border_radius=8)
        pygame.draw.rect(screen, ACCENT_YELLOW, (cx - 300, 60, 600, 140), 2, border_radius=8)
        
        time_color = ACCENT_RED if time_left < 60 else WHITE
        time_surf = font_huge.render(f"TIME REMAINING: {time_left}s", True, time_color)
        screen.blit(time_surf, (cx - time_surf.get_width()//2, 80))
        
        screen.blit(font_bold.render("[ROOT SPECTATOR CLEARANCE ONLY]", True, ACCENT_YELLOW), (cx - 140, 130))
        screen.blit(font_bold.render(f"{bot1.name} Token: {core1.access_token}", True, bot1.color), (cx - 280, 160))
        screen.blit(font_bold.render(f"{bot2.name} Token: {core2.access_token}", True, bot2.color), (cx + 10, 160))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 230))
            screen.blit(overlay, (0, 0))
            
            go_surf = font_huge.render(winner_message, True, ACCENT_YELLOW)
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 40))
            
            # Рендер отчета
            rep_y = 120
            screen.blit(font_bold.render("=== POST-MATCH CODE MUTATION REPORT ===", True, WHITE), (WIDTH//2 - 180, rep_y))
            
            def draw_report(bot, core, x, start_y):
                screen.blit(font_bold.render(f"[{bot.name}] Final State", True, bot.color), (x, start_y))
                layer_diff = core.security_layers - core.initial_layers
                diff_text = f"{'+' if layer_diff >= 0 else ''}{layer_diff} Layers"
                screen.blit(font.render(f"Core Integrity Change: {diff_text}", True, WHITE), (x, start_y + 30))
                screen.blit(font.render("Last 6 Tactical Actions:", True, ACCENT_YELLOW), (x, start_y + 55))
                for idx, log in enumerate(bot.action_log[-6:]):
                    screen.blit(font.render(log, True, TEXT_COLOR), (x, start_y + 75 + (idx * 20)))
                    
            draw_report(bot1, core1, 200, rep_y + 60)
            draw_report(bot2, core2, 800, rep_y + 60)

            restart_surf = font_bold.render("PRESS [R] TO RESTART MATCH | [ESC] FOR MENU", True, ACCENT_RED)
            screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT - 80))

    pygame.display.flip()
    clock.tick(15 if state == "BATTLE" and not game_over else 30)

pygame.quit()
sys.exit()
EOF

