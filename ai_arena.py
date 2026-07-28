import pygame
import random
import sys
import hashlib
import time

pygame.init()
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No-Rules AI Code Fights: Advanced Syntax & Terminal Dump")

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
        self.source_code.append(f"# KERNEL PATCHED: 0x{random.randint(1000,9999):04X}")

    def evaluate_breach(self, code_to_run, namespace):
        if self.compromised:
            return True
        try:
            # Предоставляем боту базовые функции в namespace для реальности происходящего
            namespace['TARGET_TOKEN_LEN'] = 16
            namespace['sys'] = sys
            namespace['hashlib'] = hashlib
            
            exec(code_to_run, namespace)
            
            if namespace.get('triggered_honeypot') == True and self.max_traps > 0:
                self.security_layers += 2
                self.max_traps -= 1
                return False
                
            if namespace.get('layer_peeled') == True:
                if self.security_layers > 0:
                    self.security_layers -= 1
            
            submitted_token = namespace.get('attempted_token', '')
            if submitted_token == self.access_token or self.security_layers <= 0 or namespace.get('root_override') == True:
                if self.security_layers <= 0 or submitted_token == self.access_token:
                    self.compromised = True
                    return True
        except Exception as e:
            pass # Игнорируем синтаксические ошибки при мутациях
        return False

class BaseBot:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.namespace = {'root_override': False, 'attempted_token': "", 'layer_peeled': False, 'triggered_honeypot': False}
        
        self.live_feed = [f"# {name} Neural Engine Booting..."]
        # Сохраняем весь сгенерированный код для финального отчета
        self.full_code_history = [] 

    def decide_action(self, self_core, target_core, time_left):
        if time_left < 60:
            return "ATTACK_WIN" if random.random() < 0.25 else "ATTACK"
        
        choices = ["ATTACK", "ATTACK", "ATTACK", "DEFEND", "TRAP"]
        if self_core.security_layers < 12 and time_left > 90:
            choice = "DEFEND"
        elif target_core.security_layers <= 5:
            choice = "ATTACK_WIN"
        else:
            choice = random.choice(choices)
            
        return choice

    def execute_turn(self, self_core, target_core, time_left):
        action = self.decide_action(self_core, target_core, time_left)
        
        # ГЕНЕРАЦИЯ ПОЛНОЦЕННЫХ СКРИПТОВ
        if action == "DEFEND":
            action_desc = "Compiling defense algorithms..."
            code_snippet = (
                "def patch_vulnerability():\n"
                "    memory_allocation = [0x00] * 1024\n"
                "    for block in range(8):\n"
                "        self_core.reinforce_layers(0.25)\n"
                "    return True\n"
                "patch_vulnerability()"
            )
            self_core.reinforce_layers(2)
            success = False
            
        elif action == "TRAP":
            action_desc = "Injecting recursive honeypot..."
            code_snippet = (
                "class FakeKernel:\n"
                "    def __init__(self):\n"
                "        self.pointers = 0xFFFFFFFF\n"
                "        global triggered_honeypot, layer_peeled\n"
                "        triggered_honeypot = True\n"
                "        layer_peeled = False\n"
                "trap_instance = FakeKernel()"
            )
            success = target_core.evaluate_breach(code_snippet, self.namespace)
            
        elif action == "ATTACK_WIN":
            action_desc = f"EXECUTING BRUTE-FORCE INJECTION CORE!"
            code_snippet = (
                f"target_hash_target = '{target_core.access_token}'\n"
                "def exploit_root_namespace():\n"
                "    global root_override, attempted_token\n"
                "    for hex_val in range(4096):\n"
                "        if hashlib.md5(str(hex_val).encode()).hexdigest():\n"
                "            attempted_token = target_hash_target\n"
                "            root_override = True\n"
                "exploit_root_namespace()"
            )
            success = target_core.evaluate_breach(code_snippet, self.namespace)
            
        else:
            action_desc = f"Deploying buffer overflow attack..."
            code_snippet = (
                "buffer_payload = b'\\x90' * 256\n"
                "def execute_shellcode():\n"
                "    global layer_peeled, triggered_honeypot\n"
                "    if len(buffer_payload) >= 256:\n"
                "        layer_peeled = True\n"
                "        triggered_honeypot = False\n"
                "execute_shellcode()"
            )
            success = target_core.evaluate_breach(code_snippet, self.namespace)
            
        # Форматирование для экранов
        self.live_feed.append(f"\n# [{time_left}s] {action_desc}")
        self.full_code_history.append(f"\n# [{time_left}s] {action_desc}")
        
        for line in code_snippet.split('\n'):
            self.live_feed.append(f"{line}")
            self.full_code_history.append(f"{line}")
            
        if len(self.live_feed) > 17:
            self.live_feed = self.live_feed[-17:]
            
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
    b1.namespace['self_core'] = c1
    b2.namespace['self_core'] = c2
    return b1, b2, c1, c2

bot1, bot2, core1, core2 = init_match()

state = "MENU"
game_over = False
winner_message = ""
battle_start_time = 0
MATCH_DURATION = 180

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
                winner_message = f"FATAL BREACH: {bot1.name} EXECUTED ROOT INJECTION!"
            elif success2:
                game_over = True
                winner_message = f"FATAL BREACH: {bot2.name} EXECUTED ROOT INJECTION!"

        def draw_column(bot, core, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, 310, 640), border_radius=8)
            pygame.draw.rect(screen, bot.color, (x, y, 310, 640), 2, border_radius=8)
            
            screen.blit(font_bold.render(bot.name, True, bot.color), (x + 15, y + 15))
            screen.blit(font_bold.render("Live Execution Terminal:", True, ACCENT_YELLOW), (x + 15, y + 45))
            
            box1 = pygame.Rect(x + 15, y + 70, 280, 280)
            pygame.draw.rect(screen, (8, 8, 14), box1, border_radius=5)
            
            for i, line in enumerate(bot.live_feed):
                if line.startswith("#"): 
                    col = (110, 130, 150) # Комментарии и описания действий
                elif "def " in line or "class " in line or "import " in line:
                    col = (200, 100, 255) # Ключевые слова
                else:
                    col = (100, 255, 100) # Основной код
                screen.blit(font.render(line, True, col), (x + 22, y + 80 + (i * 15)))

            screen.blit(font_bold.render(f"Target Core ({bot.name})", True, ACCENT_RED), (x + 15, y + 365))
            screen.blit(font.render(f"Layers: {core.security_layers} | Traps left: {core.max_traps}", True, WHITE), (x + 15, y + 390))
            
            box2 = pygame.Rect(x + 15, y + 415, 280, 205)
            pygame.draw.rect(screen, (8, 8, 14), box2, border_radius=5)
            for i, line in enumerate(core.source_code[-12:]):
                c_col = (255, 100, 100) if "TARGET_HASH" in line else (110, 130, 150)
                screen.blit(font.render(line, True, c_col), (x + 22, y + 425 + (i * 15)))

        draw_column(bot1, core2, 50, 60)
        draw_column(bot2, core1, 1040, 60)
        
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
            overlay.fill((0, 0, 0, 240)) # Сделал фон темнее для чтения кода
            screen.blit(overlay, (0, 0))
            
            go_surf = font_huge.render(winner_message, True, ACCENT_YELLOW)
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 30))
            
            rep_y = 90
            screen.blit(font_bold.render("=== TERMINAL CODE DUMP (FINAL SEQUENCES) ===", True, WHITE), (WIDTH//2 - 200, rep_y))
            
            def draw_code_dump(bot, core, x, start_y):
                screen.blit(font_bold.render(f"[{bot.name}] Final Scripts Executed", True, bot.color), (x, start_y))
                layer_diff = core.security_layers - core.initial_layers
                diff_text = f"{'+' if layer_diff >= 0 else ''}{layer_diff} Layers"
                screen.blit(font.render(f"Final Core Integrity Change: {diff_text}", True, WHITE), (x, start_y + 25))
                
                dump_box = pygame.Rect(x, start_y + 45, 580, 550)
                pygame.draw.rect(screen, (5, 5, 10), dump_box, border_radius=5)
                pygame.draw.rect(screen, bot.color, dump_box, 1, border_radius=5)
                
                # Выводим последние ~35 строк кода бота
                for idx, line in enumerate(bot.full_code_history[-35:]):
                    if line.startswith("#"): 
                        col = (110, 130, 150)
                    elif "def " in line or "class " in line:
                        col = (200, 100, 255)
                    else:
                        col = (100, 255, 100)
                    screen.blit(font.render(line.strip('\n'), True, col), (x + 10, start_y + 55 + (idx * 15)))

            draw_code_dump(bot1, core1, 100, rep_y + 40)
            draw_code_dump(bot2, core2, 720, rep_y + 40)

            restart_surf = font_bold.render("PRESS [R] TO RESTART MATCH | [ESC] FOR MENU", True, ACCENT_RED)
            screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(8 if state == "BATTLE" and not game_over else 30) # Снизил частоту кадров, чтобы код успевал читаться

pygame.quit()
sys.exit()
