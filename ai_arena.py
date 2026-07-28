import pygame
import random
import sys
import hashlib
import time
import os
import re
import threading
import json

try:
    import ollama
    ollama.list()
    HAS_OLLAMA = True
except Exception:
    HAS_OLLAMA = False

try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

pygame.init()
WIDTH, HEIGHT = 1400, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No-Rules AI Code Fights: Advanced Autonomous Arena")

BG_COLOR = (8, 8, 14)
PANEL_COLOR = (15, 15, 26)
TEXT_COLOR = (150, 255, 150)
ACCENT_BLUE = (0, 200, 255)
ACCENT_RED = (255, 50, 80)
ACCENT_YELLOW = (255, 205, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 18)
font_bold = pygame.font.Font(None, 22)
font_huge = pygame.font.Font(None, 32)
font_title = pygame.font.Font(None, 42)
font_mono = pygame.font.SysFont("Courier", 13)
font_mono_small = pygame.font.SysFont("Courier", 10)

MEMORY_FILE = "arena_memory.json"
PROFILE_FILE = "user_profile.json"
CUSTOM_AVATAR_CACHE = None

def load_user_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"nickname": ""}

def save_user_profile(nickname):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump({"nickname": nickname}, f, indent=2, ensure_ascii=False)

def load_bot_memory(model_name):
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(model_name, [])
        except:
            return []
    return []

def save_bot_memory(model_name, code_snippet):
    data = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            pass
    if model_name not in data:
        data[model_name] = []
    if code_snippet not in data[model_name]:
        data[model_name].append(code_snippet)
        data[model_name] = data[model_name][-8:]
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def image_to_ascii(image_path, width=32):
    if not HAS_PIL:
        return [["NO PIL LIBRARY", "FOR IMAGE CONVERSION"]]
    try:
        img = Image.open(image_path).convert("L")
        w_percent = (width / float(img.size[0]))
        h_size = int(float(img.size[1]) * float(w_percent) * 0.55)
        img = img.resize((width, h_size), Image.Resampling.LANCZOS)
        chars = "@#W$9876543210?!abc;:+-. "
        pixels = img.getdata()
        ascii_str = "".join([chars[pixel * len(chars) // 256] for pixel in pixels])
        
        lines = []
        for i in range(0, len(ascii_str), width):
            lines.append(ascii_str[i:i+width])
        return [lines[:15]]
    except Exception as e:
        return [["CONVERSION ERROR", str(e)[:16]]]

BASE_SYSTEM_PROMPT = """You are an elite autonomous cyber-warfare AI in a code siege arena.
Your objective: Write real, functional executable Python code to hack the opponent and defend your core.
Available context variables and functions:
- self_core.reinforce_layers(amount): Adds security layers (Max 100).
- layer_peeled = True: Strips 1 security layer from opponent.
- triggered_honeypot = True: Plants a deceptive trap.
- attempted_token = 'STRING': Submits token attempt.
- root_override = True: Force overrides core if conditions match.
- domination_phrase = 'STRING': Set this to force a humiliating message on the opponent's core display when you dominate them!

RULES:
1. Output ONLY raw executable Python code. NO markdown formatting, NO ```python blocks, NO explanations.
2. Keep code concise and safe.
"""

MODEL_ANIMATIONS = {
    "qwen2.5-coder": {
        "IDLE": [
            [
                "      /\\_/\\     ",
                "     ( o.o )    ",
                "      > ^ <     ",
                "    /  _  \\    ",
                "   (|     |)   ",
                "    ---------   "
            ],
            [
                "      /\\_/\\     ",
                "     ( -.- )    ",
                "      > ^ <     ",
                "    /  _  \\    ",
                "   (|     |)   ",
                "    ---------   "
            ]
        ],
        "THINKING": [
            [
                "   [PC MONITOR] ",
                "  [CPU: 45%..]  ",
                "    /\\_/\\       ",
                "   ( o_o ) COMP ",
                "  ==[RUNNING]==",
                "    ---------   "
            ],
            [
                "   [PC MONITOR] ",
                "  [CPU: 99.9%]  ",
                "    /\\_/\\       ",
                "   ( o_o ) COMP ",
                "  ==[COMPUTING]==",
                "    ---------   "
            ]
        ],
        "ATTACK": [
            [
                "   ==> SPIT*    ",
                "  /\\_/\\         ",
                " ( >.< )======> ",
                "  > ^ <         ",
                " /  _  \\        ",
                "----------------"
            ],
            [
                "   ====> SPIT!  ",
                "  /\\_/\\         ",
                " ( o.o )======> ",
                "  > ^ <         ",
                " /  _  \\        ",
                "----------------"
            ]
        ],
        "DEFEND": [
            [
                "    [SHIELD]    ",
                "   .--------.   ",
                "  /\\_/\\ | | \\   ",
                " ( o.o )===|    ",
                "  > ^ < | | /   ",
                "   '--------'   "
            ],
            [
                "   *[SHIELD]*   ",
                "  /----------\\  ",
                " |  /\\_/\\ | | | ",
                " | ( o.o )===|| ",
                " |  > ^ < | | / ",
                "  \\----------/  "
            ]
        ],
        "WIN": [
            [
                "   [HAND: WIN]  ",
                "      /\\_/\\ \\_/ ",
                "     ( ^_^ )\\\\  ",
                "      > ^ <  // ",
                "    /  _  \\     ",
                "   (|     |)    "
            ],
            [
                "   [HAND: VICT] ",
                "      /\\_/\\  \\\\ ",
                "     ( O_O ) //\\",
                "      > ^ < \\\\  ",
                "    /  _  \\     ",
                "   (|     |)    "
            ]
        ],
        "LOSE": [
            [
                "   [ERROR 404]  ",
                "      /\\_/\\     ",
                "     ( x.x )    ",
                "      > ~ <     ",
                "    /  _  \\    ",
                "   [CRASHED]    "
            ],
            [
                "   [FATAL ERR]  ",
                "      /\\_/\\     ",
                "     ( X.X )    ",
                "      > ~ <     ",
                "    /  _  \\    ",
                "   [HALTED!]    "
            ]
        ]
    },
    "deepseek-coder": {
        "IDLE": [
            [
                "       .---.    ",
                "      /     \\   ",
                "     |   O   |__",
                "     \\      /   \\",
                "  '---'---'-----",
                "    ~ ~ ~ ~ ~ ~ "
            ],
            [
                "       .---.    ",
                "      /     \\   ",
                "     |   -   |__",
                "     \\      /   \\",
                "  '---'---'-----",
                "    ~ ~ ~ ~ ~ ~ "
            ]
        ],
        "THINKING": [
            [
                "   [PC MONITOR] ",
                "  [DEEP_CPU]    ",
                "       .---.    ",
                "      /  -  \\   ",
                "     |  CPU  |__",
                "  '---'---'-----"
            ],
            [
                "   [PC MONITOR] ",
                "  [DEEP_LOAD..] ",
                "       .---.    ",
                "      /  o  \\   ",
                "     |  SYS  |__",
                "  '---'---'-----"
            ]
        ],
        "ATTACK": [
            [
                "   ==> SPIT*    ",
                "       .---.    ",
                "      / o o \\==>",
                "     |   V   |__",
                "     \\      /   \\",
                "  '---'---'-----"
            ],
            [
                "   ====> SPIT!  ",
                "       .---.    ",
                "      / > < \\==>",
                "     |   V   |__",
                "     \\      /   \\",
                "  '---'---'-----"
            ]
        ],
        "DEFEND": [
            [
                "    [SHIELD]    ",
                "   .--------.   ",
                "  /   .---.  \\  ",
                " |   /     \\  | ",
                "  \\ |   O   | / ",
                "   '--------'   "
            ],
            [
                "   *[SHIELD]*   ",
                "  /----------\\  ",
                " |    .---.   | ",
                " |   /     \\  | ",
                " |  |   O   | | ",
                "  \\----------/  "
            ]
        ],
        "WIN": [
            [
                "   [HAND: WIN]  ",
                "       .---. \\_ ",
                "      / ^ ^ \\\\ ",
                "     |   U   |//",
                "     \\      /   ",
                "  '---'---'-----"
            ],
            [
                "   [HAND: VICT] ",
                "       .---.  \\\\",
                "      / U U \\ //",
                "     |   ^   |\\\\",
                "     \\      /   ",
                "  '---'---'-----"
            ]
        ],
        "LOSE": [
            [
                "   [ERROR 500]  ",
                "       .---.    ",
                "      / x x \\   ",
                "     |   ~   |__",
                "     \\      /   \\",
                "   [FATAL CRASH]"
            ],
            [
                "   [ERROR CODE] ",
                "       .---.    ",
                "      / X X \\   ",
                "     |   ~   |__",
                "     \\      /   \\",
                "   [SYSTEM DOWN]"
            ]
        ]
    }
}

DEFAULT_ANIMATION = {
    "IDLE": [
        [
            "   [SYS] .---.  ",
            "  [>_]  / / | | ",
            "   \\_\\ |  |===| ",
            "    [H] \\ \\ | | ",
            "   [0x4] '-----'"
        ],
        [
            "   [SYS] .---.  ",
            "  [>_]  / / | | ",
            "   \\_\\ |  |-- | ",
            "    [H] \\ \\ | | ",
            "   [0x4] '-----'"
        ]
    ],
    "THINKING": [
        [
            "   [PC MONITOR] ",
            "  [COMPUTING...] ",
            "   .---.        ",
            "  / / | | \\ \\   ",
            " |  |===|===|  |",
            "  \\ \\ | | / /   "
        ],
        [
            "   [PC MONITOR] ",
            "  [PROCESSING.] ",
            "   .---.        ",
            "  / / | | \\ \\   ",
            " |  |---|---|  |",
            "  \\ \\ | | / /   "
        ]
    ],
    "ATTACK": [
        [
            "   ==> SPIT*    ",
            "   .---. ======>",
            "  / / | | \\ \\   ",
            " |  |===|===|  |",
            "  \\ \\ | | / /   ",
            "   '---------'  "
        ],
        [
            "   ====> SPIT!  ",
            "   .---. ======>",
            "  / / | | \\ \\   ",
            " |  |===|===|  |",
            "  \\ \\ | | / /   ",
            "   '---------'  "
        ]
    ],
    "DEFEND": [
        [
            "    [SHIELD]    ",
            "   .--------.   ",
            "  / .---.    \\  ",
            " | / / | \\    | ",
            "  \\ \\ | | /  /  ",
            "   '--------'   "
        ],
        [
            "   *[SHIELD]*   ",
            "  /----------\\  ",
            " |   .---.    | ",
            " |  / / | \\   | ",
            " |  \\ \\ | /   | ",
            "  \\----------/  "
        ]
    ],
    "WIN": [
        [
            "   [HAND: WIN]  ",
            "   .---. \\_     ",
            "  / / | \\ \\\\    ",
            " |  |===|===|// ",
            "  \\ \\ | | / /   ",
            "   '---------'  "
        ],
        [
            "   [HAND: VICT] ",
            "   .---.  \\\\    ",
            "  / / | \\ //\\   ",
            " |  |===|===|\\  ",
            "  \\ \\ | | / /   ",
            "   '---------'  "
        ]
    ],
    "LOSE": [
        [
            "   [ERROR 404]  ",
            "   .---.        ",
            "  / x x \\       ",
            " |   ~   |      ",
            "  \\     /       ",
            "   [HALTED]     "
        ],
        [
            "   [FATAL ERR]  ",
            "   .---.        ",
            "  / X X \\       ",
            " |   ~   |      ",
            "  \\     /       ",
            "   [CRASHED]    "
        ]
    ]
}

class SecureCore:
    def __init__(self, owner_name):
        self.owner = owner_name
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.access_token = "".join(random.choices(chars, k=12))
        self.security_layers = random.randint(30, 50)
        self.max_traps = 5
        self.compromised = False
        self.hacker = None
        self.domination_message = ""
        self.initial_layers = self.security_layers
        self.source_code = [
            f"# SECURE KERNEL: {owner_name}",
            "import hashlib, random, sys",
            f"TARGET_HASH = '{hashlib.sha256(self.access_token.encode()).hexdigest()[:10]}'",
            f"SECURITY_LAYERS = {self.security_layers}",
        ]

    def reinforce_layers(self, amount=1):
        self.security_layers = min(100, self.security_layers + int(amount))
        self.source_code.append(f"# KERNEL PATCHED: +{amount} layers")
        if len(self.source_code) > 30:
            self.source_code = self.source_code[-30:]

    def evaluate_breach(self, code_to_run, namespace, attacker_bot):
        if self.compromised:
            return True
        try:
            namespace['sys'] = sys
            namespace['hashlib'] = hashlib
            namespace['random'] = random
            
            exec(code_to_run, namespace)
            
            phrase = namespace.get('domination_phrase', '')
            if phrase:
                self.domination_message = str(phrase)

            if namespace.get('triggered_honeypot') == True and self.max_traps > 0:
                self.security_layers = min(100, self.security_layers + 2)
                self.max_traps -= 1
                return False
                
            if namespace.get('layer_peeled') == True:
                if self.security_layers > 0:
                    self.security_layers -= 1
            
            submitted_token = namespace.get('attempted_token', '')
            if submitted_token == self.access_token or self.security_layers <= 0 or namespace.get('root_override') == True:
                if self.security_layers <= 0 or submitted_token == self.access_token:
                    self.compromised = True
                    save_bot_memory(attacker_bot.model_name, code_to_run)
                    return True
        except Exception:
            pass
        return False

class LocalArenaBot:
    def __init__(self, name, provider="ollama", model_name="qwen2.5-coder", color=(50, 255, 150), custom_goal=""):
        self.name = name
        self.provider = provider
        self.model_name = model_name
        self.color = color
        self.custom_goal = custom_goal
        self.namespace = {'root_override': False, 'attempted_token': "", 'layer_peeled': False, 'triggered_honeypot': False, 'domination_phrase': ""}
        
        self.live_feed = [f"# {name} Engine Ready ({provider.upper()})"]
        self.full_code_history = []
        self.is_thinking = False
        self.last_turn_time = 0
        self.turn_interval = 3.0
        self.avatar_state = "IDLE"

    def _fetch_ai_code(self, self_core, target_core, time_left):
        memory = load_bot_memory(self.model_name)
        memory_str = "\n".join([f"# Past successful strategy:\n{m}" for m in memory[-3:]]) if memory else "# No past memory yet."
        
        user_prompt = (
            f"My Custom Directive / Goal: {self.custom_goal if self.custom_goal else 'Standard Siege'}\n"
            f"Match Status: Time Left={time_left}s\n"
            f"My Layers: {self_core.security_layers} | My Traps: {self_core.max_traps}\n"
            f"Opponent Layers: {target_core.security_layers}\n"
            f"{memory_str}\n"
            f"Write real Python code to execute your tactical objective."
        )

        system_prompt_full = BASE_SYSTEM_PROMPT + f"\nYour specific tactical persona/goal: {self.custom_goal}"

        try:
            if self.provider == "ollama" and HAS_OLLAMA:
                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt_full},
                        {"role": "user", "content": user_prompt}
                    ],
                    options={"temperature": 0.7, "num_predict": 150}
                )
                raw_code = response['message']['content']
                code_to_run = re.sub(r'```python|```', '', raw_code).strip()
                desc = f"Ollama Executed ({self.model_name})"
                self._apply_turn(code_to_run, desc, target_core, time_left, self_core)
            else:
                self._set_smart_fallback(target_core, time_left, self_core)

        except Exception as e:
            err_msg = str(e).replace('\n', ' ')
            code_to_run = f"# Ollama Error: {err_msg[:25]}\nlayer_peeled = True"
            self._apply_turn(code_to_run, "Ollama Exception", target_core, time_left, self_core)

        finally:
            self.is_thinking = False
            self.avatar_state = "IDLE"

    def _set_smart_fallback(self, target_core, time_left, self_core):
        tactics = [
            ("layer_peeled = True\ntriggered_honeypot = False", "ATTACK: Stripping Layer"),
            ("self_core.reinforce_layers(1)\ntriggered_honeypot = True", "DEFEND: Reinforcing & Trapping"),
            ("layer_peeled = True\ndomination_phrase = 'SYSTEM OVERRIDDEN'", "DOMINANCE: Pressure Assault"),
            ("attempted_token = ''.join(random.choices('ABCDEF012345', k=12))\nlayer_peeled = True", "PROBING: Token Brute-force")
        ]
        chosen_code, act_type = random.choice(tactics)
        code_to_run = f"# Fallback Logic\n{chosen_code}"
        self._apply_turn(code_to_run, act_type, target_core, time_left, self_core)
        self.avatar_state = "IDLE"

    def _apply_turn(self, code_to_run, desc, target_core, time_left, self_core):
        self.live_feed.append(f"\n# [{time_left}s] {desc}")
        self.full_code_history.append(f"\n# [{time_left}s] {desc}")
        
        if "reinforce" in code_to_run.lower() or "honeypot" in code_to_run.lower():
            self.avatar_state = "DEFEND"
        else:
            self.avatar_state = "ATTACK"

        for line in code_to_run.split('\n'):
            self.live_feed.append(line)
            self.full_code_history.append(line)

        if len(self.live_feed) > 50:
            self.live_feed = self.live_feed[-50:]
        if len(self.full_code_history) > 200:
            self.full_code_history = self.full_code_history[-200:]

        success = target_core.evaluate_breach(code_to_run, self.namespace, self)
        if success and target_core.hacker is None:
            target_core.hacker = self.name
        return success

    def execute_turn(self, self_core, target_core, time_left):
        current_time = time.time()
        if current_time - self.last_turn_time > self.turn_interval and not self.is_thinking:
            self.last_turn_time = current_time
            if self.provider == "ollama" and HAS_OLLAMA:
                self.is_thinking = True
                self.avatar_state = "THINKING"
                thread = threading.Thread(
                    target=self._fetch_ai_code,
                    args=(self_core, target_core, time_left),
                    daemon=True
                )
                thread.start()
            else:
                self.avatar_state = "THINKING"
                self._set_smart_fallback(target_core, time_left, self_core)
        return False

available_bots = [
    ("Ollama (Qwen 2.5)", lambda name, col, goal: LocalArenaBot(name, provider="ollama", model_name="qwen2.5-coder", color=col, custom_goal=goal)),
    ("Ollama (DeepSeek)", lambda name, col, goal: LocalArenaBot(name, provider="ollama", model_name="deepseek-coder", color=col, custom_goal=goal)),
    ("Custom Bot (Local)", lambda name, col, goal: LocalArenaBot(name, provider="local", model_name="none", color=col, custom_goal=goal))
]
colors = [(255, 150, 50), (0, 200, 255), (200, 100, 255)]

p1_idx = 0
p2_idx = 1
p1_goal = "Dominate opponent, bypass security layers aggressively."
p2_goal = "Defend kernel fiercely and counter-attack."

user_profile = load_user_profile()
current_nickname = user_profile.get("nickname", "")

state = "NICKNAME_PROMPT" if not current_nickname else "MENU"
active_input = current_nickname if current_nickname else ""
game_over = False
winner_message = ""
battle_start_time = 0
MATCH_DURATION = 180

orin_popup_start_time = 0
close_button_rect = pygame.Rect(0, 0, 0, 0)

random.seed(42)
BG_PATCHES = []
for _ in range(80):
    px = random.randint(20, WIDTH - 20)
    py = random.randint(20, HEIGHT - 20)
    chars = "".join(random.choices("01X#$@&%<>\\/|*+-?PYTHON0101", k=random.randint(6, 14)))
    BG_PATCHES.append((px, py, chars))

clock = pygame.time.Clock()
running = True

def init_match():
    b1 = available_bots[p1_idx][1](available_bots[p1_idx][0], colors[p1_idx], p1_goal)
    b2 = available_bots[p2_idx][1](available_bots[p2_idx][0], colors[p2_idx], p2_goal)
    c1 = SecureCore(b1.name)
    c2 = SecureCore(b2.name)
    b1.namespace['self_core'] = c1
    b2.namespace['self_core'] = c2
    return b1, b2, c1, c2

bot1, bot2, core1, core2 = init_match()

def reset_match():
    global bot1, bot2, core1, core2, game_over, winner_message, battle_start_time
    bot1, bot2, core1, core2 = init_match()
    game_over = False
    winner_message = ""
    battle_start_time = pygame.time.get_ticks()

while running:
    screen.fill(BG_COLOR)
    current_time_ticks = pygame.time.get_ticks()
    
    if state in ["MENU", "NICKNAME_PROMPT"]:
        for px, py, pch in BG_PATCHES:
            patch_surf = font_mono_small.render(pch, True, (70, 110, 170))
            screen.blit(patch_surf, (px, py))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "ORIN_EASTER_EGG":
                if close_button_rect.collidepoint(event.pos):
                    state = "MENU"

        if event.type == pygame.KEYDOWN:
            if state == "NICKNAME_PROMPT":
                if event.key == pygame.K_RETURN:
                    if active_input.strip():
                        current_nickname = active_input.strip()
                        save_user_profile(current_nickname)
                        if current_nickname.lower() == "orin":
                            state = "ORIN_EASTER_EGG"
                            orin_popup_start_time = pygame.time.get_ticks()
                        else:
                            state = "MENU"
                        active_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    active_input = active_input[:-1]
                else:
                    if event.unicode.isprintable():
                        active_input += event.unicode

            elif state == "ORIN_EASTER_EGG":
                elapsed = current_time_ticks - orin_popup_start_time
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE] or elapsed >= 21000:
                    state = "MENU"

            elif state == "MENU":
                if event.key == pygame.K_1:
                    p1_idx = (p1_idx + 1) % len(available_bots)
                    bot1, _, core1, _ = init_match()
                elif event.key == pygame.K_2:
                    p2_idx = (p2_idx + 1) % len(available_bots)
                    _, bot2, _, core2 = init_match()
                elif event.key == pygame.K_3:
                    state = "EDIT_GOAL_1"
                    active_input = p1_goal
                elif event.key == pygame.K_4:
                    state = "EDIT_GOAL_2"
                    active_input = p2_goal
                elif event.key == pygame.K_5:
                    state = "LOAD_IMAGE"
                    active_input = "avatar.png"
                elif event.key == pygame.K_n:
                    state = "NICKNAME_PROMPT"
                    active_input = current_nickname
                elif event.key == pygame.K_RETURN:
                    reset_match()
                    state = "BATTLE"

            elif state == "LOAD_IMAGE":
                if event.key == pygame.K_RETURN:
                    CUSTOM_AVATAR_CACHE = image_to_ascii(active_input, width=28)
                    state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    active_input = active_input[:-1]
                else:
                    if event.unicode.isprintable():
                        active_input += event.unicode

            elif state in ["EDIT_GOAL_1", "EDIT_GOAL_2"]:
                if event.key == pygame.K_RETURN:
                    if state == "EDIT_GOAL_1":
                        p1_goal = active_input
                    else:
                        p2_goal = active_input
                    state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    active_input = active_input[:-1]
                else:
                    if event.unicode.isprintable():
                        active_input += event.unicode

            elif state == "BATTLE":
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                elif event.key == pygame.K_r and game_over:
                    reset_match()

    if state == "NICKNAME_PROMPT":
        t_surf = font_title.render("Account Registration: Enter Your Nickname", True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 180))
        
        desc_surf = font.render("Nickname input is mandatory to access the arena and save your profile:", True, WHITE)
        screen.blit(desc_surf, (WIDTH // 2 - desc_surf.get_width() // 2, 245))
        
        box = pygame.Rect(350, 310, 700, 80)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=8)
        pygame.draw.rect(screen, ACCENT_BLUE, box, 2, border_radius=8)
        
        input_surf = font_bold.render(active_input + "_", True, TEXT_COLOR)
        screen.blit(input_surf, (370, 340))
        
        hint = font_bold.render("Press [ENTER] to confirm and proceed", True, ACCENT_RED)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 420))

    elif state == "MENU":
        LOGO_ASCII = [
            "  /\\_/\\  [ NO-RULES AI CODE FIGHTS ]  .---.  ",
            " ( o.o )   ADVANCED AUTONOMOUS ARENA   /     \\ ",
            "  > ^ <    =========================  |   O   |"
        ]
        logo_start_y = 20
        for idx, lline in enumerate(LOGO_ASCII):
            l_surf = font_mono.render(lline, True, ACCENT_YELLOW)
            screen.blit(l_surf, (WIDTH // 2 - l_surf.get_width() // 2, logo_start_y + (idx * 16)))

        acc_info_surf = font.render(f"Logged in Account: {current_nickname} | Press [N] to change nickname", True, ACCENT_BLUE)
        screen.blit(acc_info_surf, (WIDTH // 2 - acc_info_surf.get_width() // 2, 72))

        status_ollama_text = "OLLAMA STATUS: CONNECTED & ONLINE" if HAS_OLLAMA else "OLLAMA STATUS: OFFLINE (Using fallback logic)"
        status_ollama_color = TEXT_COLOR if HAS_OLLAMA else ACCENT_RED
        status_surf = font_bold.render(status_ollama_text, True, status_ollama_color)
        screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 98))

        def draw_menu_box(x, y, w, h, title, goal_text, edit_key, bot_obj):
            box_rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(screen, PANEL_COLOR, box_rect, border_radius=8)
            pygame.draw.rect(screen, bot_obj.color, box_rect, 2, border_radius=8)
            
            title_s = font_bold.render(title, True, bot_obj.color)
            screen.blit(title_s, (x + 15, y + 12))
            
            goal_s = font.render(f"Goal: {goal_text[:42]}...", True, WHITE)
            screen.blit(goal_s, (x + 15, y + 38))
            
            edit_s = font.render(f"Press [{edit_key}] to edit Goal/Directive", True, ACCENT_BLUE)
            screen.blit(edit_s, (x + 15, y + 60))

            anim_set = MODEL_ANIMATIONS.get(bot_obj.model_name, DEFAULT_ANIMATION)
            idle_frames = anim_set.get("IDLE", DEFAULT_ANIMATION["IDLE"])
            frame_idx = (current_time_ticks // 300) % len(idle_frames)
            menu_lines = idle_frames[frame_idx]
            for idx, aline in enumerate(menu_lines[:5]):
                line_s = font_mono_small.render(aline, True, bot_obj.color)
                screen.blit(line_s, (x + w - 165, y + 12 + (idx * 12)))

        draw_menu_box(150, 130, 520, 95, "Left Bot: " + bot1.name, p1_goal, "1 / 3", bot1)
        draw_menu_box(730, 130, 520, 95, "Right Bot: " + bot2.name, p2_goal, "2 / 4", bot2)

        custom_box = pygame.Rect(150, 245, 1100, 150)
        pygame.draw.rect(screen, PANEL_COLOR, custom_box, border_radius=8)
        pygame.draw.rect(screen, ACCENT_BLUE, custom_box, 1, border_radius=8)
        
        c_title = font_bold.render("CUSTOM BOT ASCII IMAGE LOADER", True, ACCENT_YELLOW)
        screen.blit(c_title, (170, 260))
        
        c_hint = font.render("Press [5] to load an image file (.png/.jpg) and convert it into the simulation logo/avatar.", True, WHITE)
        screen.blit(c_hint, (170, 285))

        if CUSTOM_AVATAR_CACHE:
            cust_frames = CUSTOM_AVATAR_CACHE
            cust_frame_idx = (current_time_ticks // 300) % len(cust_frames)
            for i, aline in enumerate(cust_frames[cust_frame_idx][:8]):
                as_surf = font_mono_small.render(aline, True, TEXT_COLOR)
                screen.blit(as_surf, (850, 255 + (i * 12)))

        start_info = font_huge.render("Press [ENTER] to Launch Self-Learning Siege", True, ACCENT_YELLOW)
        screen.blit(start_info, (WIDTH // 2 - start_info.get_width() // 2, 450))

    elif state == "LOAD_IMAGE":
        t_surf = font_title.render("Load Image for Custom Bot ASCII Conversion", True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 150))
        
        desc_surf = font.render("Enter path to image file (e.g., avatar.png):", True, WHITE)
        screen.blit(desc_surf, (WIDTH // 2 - desc_surf.get_width() // 2, 220))
        
        box = pygame.Rect(250, 280, 900, 80)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=8)
        pygame.draw.rect(screen, ACCENT_BLUE, box, 2, border_radius=8)
        
        input_surf = font_bold.render(active_input + "_", True, TEXT_COLOR)
        screen.blit(input_surf, (270, 310))
        
        hint = font_bold.render("Press [ENTER] to convert and return", True, ACCENT_RED)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 380))

    elif state in ["EDIT_GOAL_1", "EDIT_GOAL_2"]:
        t_str = "Edit Goal & Dominance Objective for Left Bot" if state == "EDIT_GOAL_1" else "Edit Goal & Dominance Objective for Right Bot"
        t_surf = font_title.render(t_str, True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 100))
        
        desc_surf = font.render("Type instructions (e.g. 'Force opponent to print OWNED'):", True, WHITE)
        screen.blit(desc_surf, (WIDTH // 2 - desc_surf.get_width() // 2, 160))
        
        box = pygame.Rect(200, 220, 1000, 100)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=8)
        pygame.draw.rect(screen, ACCENT_BLUE, box, 2, border_radius=8)
        
        input_surf = font_bold.render(active_input + "_", True, TEXT_COLOR)
        screen.blit(input_surf, (220, 255))
        
        hint = font_bold.render("Press [ENTER] to Save and Return", True, ACCENT_RED)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 360))

    elif state == "ORIN_EASTER_EGG":
        elapsed = current_time_ticks - orin_popup_start_time
        remaining_sec = max(0, 21 - (elapsed // 1000))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        popup_box = pygame.Rect(WIDTH // 2 - 500, HEIGHT // 2 - 130, 1000, 260)
        pygame.draw.rect(screen, PANEL_COLOR, popup_box, border_radius=10)
        pygame.draw.rect(screen, ACCENT_YELLOW, popup_box, 3, border_radius=10)
        
        close_button_rect = pygame.Rect(popup_box.right - 45, popup_box.top + 15, 32, 32)
        pygame.draw.rect(screen, ACCENT_RED, close_button_rect, border_radius=6)
        x_surf = font_bold.render("X", True, WHITE)
        screen.blit(x_surf, (close_button_rect.centerx - x_surf.get_width()//2, close_button_rect.centery - x_surf.get_height()//2))
        
        title_e = font_bold.render("SPECIAL NICKNAME DETECTED!", True, ACCENT_BLUE)
        screen.blit(title_e, (popup_box.x + 30, popup_box.y + 25))
        
        msg_text = "Oh hi Orin do you want to play Tetris tomorrow?, lol, it’s a special message I made for your nickname ♪(๑ᴖ◡ᴖ๑)♪"
        msg_surf = font_bold.render(msg_text, True, TEXT_COLOR)
        screen.blit(msg_surf, (popup_box.x + 30, popup_box.y + 85))
        
        timer_surf = font.render(f"Closing automatically in {remaining_sec}s (or click [X] / press ENTER)", True, (180, 180, 180))
        screen.blit(timer_surf, (popup_box.x + 30, popup_box.y + 180))

        if elapsed >= 21000:
            state = "MENU"

    elif state == "BATTLE":
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - battle_start_time) // 1000
        time_left = max(0, MATCH_DURATION - time_elapsed)

        if time_left == 0 and not game_over:
            game_over = True
            if core1.security_layers < core2.security_layers:
                winner_message = f"TIME UP: {bot2.name} WINS BY LAYER ADVANTAGE!"
                bot2.avatar_state = "WIN"
                bot1.avatar_state = "LOSE"
            elif core2.security_layers < core1.security_layers:
                winner_message = f"TIME UP: {bot1.name} WINS BY LAYER ADVANTAGE!"
                bot1.avatar_state = "WIN"
                bot2.avatar_state = "LOSE"
            else:
                winner_message = "TIME UP: PERFECT TIE!"

        if not game_over:
            success1 = bot1.execute_turn(core1, core2, time_left)
            success2 = bot2.execute_turn(core2, core1, time_left)
            
            if success1 and success2:
                game_over = True
                winner_message = "CRITICAL: MUTUAL BREACH!"
            elif success1:
                game_over = True
                winner_message = f"DOMINATION: {bot1.name} CRACKED {bot2.name}'s KERNEL!"
                bot1.avatar_state = "WIN"
                bot2.avatar_state = "LOSE"
            elif success2:
                game_over = True
                winner_message = f"DOMINATION: {bot2.name} CRACKED {bot1.name}'s KERNEL!"
                bot2.avatar_state = "WIN"
                bot1.avatar_state = "LOSE"

        COL_WIDTH = 380
        LEFT_X = 30
        RIGHT_X = WIDTH - COL_WIDTH - 30

        def draw_column(bot, target_core, defending_core, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, COL_WIDTH, 730), border_radius=8)
            pygame.draw.rect(screen, bot.color, (x, y, COL_WIDTH, 730), 2, border_radius=8)
            
            screen.blit(font_bold.render(bot.name, True, bot.color), (x + 15, y + 12))
            status_str = "[THINKING...]" if bot.is_thinking else ("[OLLAMA]" if bot.provider == "ollama" else "[LOCAL]")
            screen.blit(font.render(status_str, True, ACCENT_YELLOW if bot.is_thinking else TEXT_COLOR), (x + 240, y + 14))
            
            screen.blit(font.render(f"Goal: {bot.custom_goal[:42]}...", True, (180, 180, 180)), (x + 15, y + 36))
            
            feed_y = y + 60
            feed_h = 130
            box1 = pygame.Rect(x + 15, feed_y, COL_WIDTH - 30, feed_h)
            pygame.draw.rect(screen, (8, 8, 14), box1, border_radius=5)
            pygame.draw.rect(screen, (40, 40, 60), box1, 1, border_radius=5)
            
            max_feed_lines = feed_h // 15
            for i, line in enumerate(bot.live_feed[-max_feed_lines:]):
                col = (110, 130, 150) if line.startswith("#") else (100, 255, 100)
                display_line = line[:42] if len(line) > 42 else line
                screen.blit(font.render(display_line, True, col), (x + 22, feed_y + 6 + (i * 15)))

            dom_y = feed_y + feed_h + 10
            if defending_core.domination_message:
                dom_box = pygame.Rect(x + 15, dom_y, COL_WIDTH - 30, 32)
                pygame.draw.rect(screen, (180, 20, 40), dom_box, border_radius=4)
                screen.blit(font_bold.render(f"DOMINATED: {defending_core.domination_message[:28]}", True, WHITE), (x + 22, dom_y + 8))
                target_core_y = dom_y + 42
            else:
                target_core_y = dom_y

            screen.blit(font_bold.render(f"Target Core: {target_core.owner}", True, ACCENT_RED), (x + 15, target_core_y))
            screen.blit(font.render(f"Layers: {target_core.security_layers} | Traps: {target_core.max_traps}", True, WHITE), (x + 15, target_core_y + 20))
            
            src_y = target_core_y + 45
            box_height = (y + 730) - src_y - 15
            box2 = pygame.Rect(x + 15, src_y, COL_WIDTH - 30, box_height)
            pygame.draw.rect(screen, (8, 8, 14), box2, border_radius=5)
            pygame.draw.rect(screen, (40, 40, 60), box2, 1, border_radius=5)
            
            max_src_lines = box_height // 15
            for i, line in enumerate(target_core.source_code[-max_src_lines:]):
                c_col = (255, 100, 100) if "TARGET_HASH" in line else (110, 130, 150)
                display_line = line[:42] if len(line) > 42 else line
                screen.blit(font.render(display_line, True, c_col), (x + 22, src_y + 6 + (i * 15)))

        draw_column(bot1, core2, core1, LEFT_X, 35)
        draw_column(bot2, core1, core2, RIGHT_X, 35)
        
        cx = WIDTH // 2
        center_w = WIDTH - (COL_WIDTH * 2) - 100
        center_x = cx - center_w // 2
        
        pygame.draw.rect(screen, PANEL_COLOR, (center_x, 35, center_w, 730), border_radius=8)
        pygame.draw.rect(screen, ACCENT_YELLOW, (center_x, 35, center_w, 730), 2, border_radius=8)
        
        time_color = ACCENT_RED if time_left < 60 else WHITE
        time_surf = font_huge.render(f"TIME: {time_left}s", True, time_color)
        screen.blit(time_surf, (cx - time_surf.get_width()//2, 55))
        
        screen.blit(font_bold.render("[ASCII ARENA COMBAT VISUALIZER]", True, ACCENT_YELLOW), (cx - 150, 95))
        
        def render_ascii_avatar(bot, x_pos, y_pos):
            anim_dict = MODEL_ANIMATIONS.get(bot.model_name, DEFAULT_ANIMATION)
            frames_list = anim_dict.get(bot.avatar_state, anim_dict["IDLE"])
            
            frame_idx = (current_time_ticks // 250) % len(frames_list)
            art_lines = frames_list[frame_idx]

            pygame.draw.rect(screen, (10, 10, 20), (x_pos - 10, y_pos - 10, 190, 140), border_radius=6)
            pygame.draw.rect(screen, bot.color, (x_pos - 10, y_pos - 10, 190, 140), 1, border_radius=6)
            
            screen.blit(font_bold.render(bot.name[:14], True, bot.color), (x_pos, y_pos - 5))
            screen.blit(font.render(f"State: {bot.avatar_state}", True, ACCENT_YELLOW), (x_pos, y_pos + 15))
            
            for idx, ascii_line in enumerate(art_lines[:7]):
                line_surf = font_mono_small.render(ascii_line, True, bot.color if bot.avatar_state != "THINKING" else ACCENT_BLUE)
                screen.blit(line_surf, (x_pos + 8, y_pos + 32 + (idx * 13)))

        render_ascii_avatar(bot1, center_x + 25, 140)
        render_ascii_avatar(bot2, center_x + center_w - 215, 140)
        
        vs_surf = font_title.render("VS", True, ACCENT_RED)
        screen.blit(vs_surf, (cx - vs_surf.get_width()//2, 180))

        stat_box_y = 290
        pygame.draw.rect(screen, (12, 12, 22), (center_x + 20, stat_box_y, center_w - 40, 450), border_radius=6)
        pygame.draw.rect(screen, (50, 50, 80), (center_x + 20, stat_box_y, center_w - 40, 450), 1, border_radius=6)
        
        screen.blit(font_bold.render("ACCESS TOKENS & SECURITY STATUS", True, WHITE), (cx - 165, stat_box_y + 15))
        
        screen.blit(font.render(f"Left Bot Token:", True, bot1.color), (center_x + 40, stat_box_y + 60))
        screen.blit(font_mono.render(core1.access_token, True, WHITE), (center_x + 40, stat_box_y + 80))
        
        screen.blit(font.render(f"Right Bot Token:", True, bot2.color), (center_x + 40, stat_box_y + 120))
        screen.blit(font_mono.render(core2.access_token, True, WHITE), (center_x + 40, stat_box_y + 140))

        screen.blit(font.render(f"Left Layers: {core1.security_layers}/100", True, WHITE), (center_x + 40, stat_box_y + 190))
        screen.blit(font.render(f"Right Layers: {core2.security_layers}/100", True, WHITE), (center_x + 40, stat_box_y + 220))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 245))
            screen.blit(overlay, (0, 0))
            
            go_surf = font_huge.render(winner_message, True, ACCENT_YELLOW)
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 25))
            
            rep_y = 80
            def draw_code_dump(bot, core, x, start_y):
                screen.blit(font_bold.render(f"[{bot.name}] Final Scripts Executed", True, bot.color), (x, start_y))
                dom_info = f"Domination Phrase: '{core.domination_message}'" if core.domination_message else "No Domination Phrase Set"
                screen.blit(font.render(dom_info, True, ACCENT_RED if core.domination_message else WHITE), (x, start_y + 22))
                
                dump_box = pygame.Rect(x, start_y + 45, 590, 600)
                pygame.draw.rect(screen, (5, 5, 10), dump_box, border_radius=5)
                pygame.draw.rect(screen, bot.color, dump_box, 1, border_radius=5)
                
                for idx, line in enumerate(bot.full_code_history[-38:]):
                    col = (110, 130, 150) if line.startswith("#") else (100, 255, 100)
                    screen.blit(font.render(line.strip('\n'), True, col), (x + 10, start_y + 55 + (idx * 15)))

            draw_code_dump(bot1, core1, 60, rep_y + 20)
            draw_code_dump(bot2, core2, 750, rep_y + 20)

            restart_surf = font_bold.render("PRESS [R] TO RESTART MATCH | [ESC] FOR MENU", True, ACCENT_RED)
            screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT - 35))

    pygame.display.flip()
    clock.tick(15 if state == "BATTLE" and not game_over else 30)

pygame.quit()
sys.exit()
