import pygame
import random
import sys
import hashlib
import time
import os
import re
import threading
import json
import webbrowser

try:
    import ollama
    ollama.list()
    HAS_OLLAMA = True
except Exception:
    HAS_OLLAMA = False

pygame.init()
WIDTH, HEIGHT = 1400, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("No-Rules AI Code Fights: Advanced Cyber Siege Edition")

BG_COLOR = (5, 5, 10)
PANEL_COLOR = (12, 12, 22)
PANEL_BORDER = (40, 110, 180)
TEXT_COLOR = (120, 255, 170)
ACCENT_BLUE = (0, 220, 255)
ACCENT_RED = (255, 40, 90)
ACCENT_YELLOW = (255, 210, 0)
WHITE = (240, 240, 255)

font = pygame.font.Font(None, 18)
font_bold = pygame.font.Font(None, 22)
font_huge = pygame.font.Font(None, 32)
font_title = pygame.font.Font(None, 42)
font_mono = pygame.font.SysFont("Courier", 13)
font_mono_small = pygame.font.SysFont("Courier", 10)

MEMORY_FILE = "arena_memory.json"
USERS_DB_FILE = "users_db.json"
TOURNAMENT_FILE = "tournaments.json"

MATCH_DURATION = 180
CURRENT_LANG = "en"

LANGUAGES = {
    "en": {
        "auth_title": "Account Login or Registration",
        "auth_desc": "Enter login and password (new accounts are created automatically):",
        "login_label": "Login: ",
        "pass_label": "Password: ",
        "auth_hint": "Press [TAB] to switch field, [ENTER] to confirm",
        "leaderboard_title": "LEADERBOARD",
        "player": "Player",
        "wins": "Wins",
        "losses": "Losses",
        "back_menu": "Press [ESC] to return to menu",
        "friends_title": "FRIENDS MANAGEMENT",
        "your_friends": "Your Friends:",
        "no_friends": "Friends list is empty.",
        "incoming_req": "Incoming Requests:",
        "no_req": "No new requests.",
        "send_req_label": "Send friend request by nickname:",
        "send_hint": "Press [ENTER] to send",
        "records_title": "TOURNAMENT MATCH RECORDS",
        "no_records": "No match records found.",
        "account_info": "Account: {acc} | [N] Switch | [5] Leaders | [6] Friends | [9] Timer: {timer_str} | [8] Lang: {lang}",
        "ollama_on": "OLLAMA STATUS: CONNECTED",
        "ollama_off": "OLLAMA STATUS: OFFLINE",
        "left_bot": "Left Bot: ",
        "right_bot": "Right Bot: ",
        "goal": "Directive / Goal: ",
        "edit_goal": "Press [{key}] to edit directive",
        "management_title": "MANAGEMENT & ARENA SETTINGS",
        "management_desc": "[9] Cycle Timer (180s / 300s / Infinite) | [5] Leaders | [6] Friends | [8] Language",
        "start_battle": "Press [ENTER] to start cyber siege",
        "save_goal": "Press [ENTER] to save directive",
        "time_prefix": "TIME: ",
        "time_inf": "INF (NO TIMER)",
        "vis_title": "[CYBER CORE ARENA VISUALIZER]",
        "tokens_title": "ACCESS TOKENS & SECURITY",
        "left_token": "Left Core Token: ",
        "right_token": "Right Core Token: ",
        "left_layers": "Left Firewall Layers: ",
        "right_layers": "Right Firewall Layers: ",
        "game_over_restart": "PRESS [R] FOR REMATCH | [ESC] TO MENU",
        "special_msg": "SPECIAL MESSAGE!",
        "special_text": "Oh hi Orin do you want to play Tetris tomorrow?, lol, special message for you!",
        "close_timer": "Closes in {sec}s (or press [X] / ENTER)"
    },
    "ru": {
        "auth_title": "Вход или Регистрация аккаунта",
        "auth_desc": "Введите логин и пароль (если аккаунт новый, он создастся автоматически):",
        "login_label": "Логин: ",
        "pass_label": "Пароль: ",
        "auth_hint": "Нажмите [TAB] для смены поля, [ENTER] для подтверждения",
        "leaderboard_title": "ТАБЛИЦА ЛИДЕРОВ",
        "player": "Игрок",
        "wins": "Победы",
        "losses": "Поражения",
        "back_menu": "Нажмите [ESC] для возврата в меню",
        "friends_title": "УПРАВЛЕНИЕ ДРУЗЬЯМИ",
        "your_friends": "Ваши друзья:",
        "no_friends": "Список друзей пуст.",
        "incoming_req": "Входящие заявки:",
        "no_req": "Нет новых заявок.",
        "send_req_label": "Отправить заявку в друзья по никнейму:",
        "send_hint": "Нажмите [ENTER] для отправки",
        "records_title": "ТУРНИРНЫЕ ЛОГИ МАТЧЕЙ",
        "no_records": "Записи матчей отсутствуют.",
        "account_info": "Аккаунт: {acc} | [N] Сменить | [5] Лидеры | [6] Друзья | [9] Таймер: {timer_str} | [8] Язык: {lang}",
        "ollama_on": "OLLAMA STATUS: ПОДКЛЮЧЕНО",
        "ollama_off": "OLLAMA STATUS: OFFLINE",
        "left_bot": "Левый бот: ",
        "right_bot": "Правый бот: ",
        "goal": "Цель / Промпт: ",
        "edit_goal": "Нажмите [{key}] для изменения промпта",
        "management_title": "МЕНЮ УПРАВЛЕНИЯ И НАСТРОЙКИ АРЕНЫ",
        "management_desc": "[9] Сменить таймер (180с / 300с / Бесконечно) | [5] Лидеры | [6] Друзья | [8] Язык",
        "start_battle": "Нажмите [ENTER] для запуска кибер-атаки",
        "save_goal": "Нажмите [ENTER] для сохранения",
        "time_prefix": "ВРЕМЯ: ",
        "time_inf": "БЕЗ ЛИМИТА",
        "vis_title": "[ВИЗУУЛИЗАЦИЯ КИБЕР-ЯДРА]",
        "tokens_title": "ТОКЕНЫ ДОСТУПА И БЕЗОПАСНОСТЬ",
        "left_token": "Токен левого ядра: ",
        "right_token": "Токен правого ядра: ",
        "left_layers": "Слои защиты левого: ",
        "right_layers": "Слои защиты правого: ",
        "game_over_restart": "НАЖМИТЕ [R] ДЛЯ ПОВТОРНОГО МАТЧА | [ESC] В МЕНЮ",
        "special_msg": "СПЕЦИАЛЬНОЕ СООБЩЕНИЕ!",
        "special_text": "Oh hi Orin do you want to play Tetris tomorrow?, lol, специальное сообщение для тебя!",
        "close_timer": "Закроется через {sec}с (или нажмите [X] / ENTER)"
    },
    "jp": {
        "auth_title": "アカウントログインまたは登録",
        "auth_desc": "ログインとパスワードを入力してください（新規の場合は自動作成されます）:",
        "login_label": "ログイン: ",
        "pass_label": "パスワード: ",
        "auth_hint": "[TAB]で切替、[ENTER]で確定",
        "leaderboard_title": "リーダーボード",
        "player": "プレイヤー",
        "wins": "勝利",
        "losses": "敗北",
        "back_menu": "[ESC]でメニューに戻る",
        "friends_title": "フレンド管理",
        "your_friends": "フレンド一覧:",
        "no_friends": "フレンドがいません。",
        "incoming_req": "フレンド申請:",
        "no_req": "新しい申請はありません。",
        "send_req_label": "ニックネームでフレンド申請を送信:",
        "send_hint": "[ENTER]で送信",
        "records_title": "トーナメント試合記録",
        "no_records": "試合記録がありません。",
        "account_info": "アカウント: {acc} | [N] 切替 | [5] リーダー | [6] フレンド | [9] タイマー: {timer_str} | [8] 言語: {lang}",
        "ollama_on": "OLLAMAステータス: 接続済み",
        "ollama_off": "OLLAMAステータス: オフライン",
        "left_bot": "左ボット: ",
        "right_bot": "右ボット: ",
        "goal": "指令/目標: ",
        "edit_goal": "[{key}]で指令を変更",
        "management_title": "管理とアリーナ設定",
        "management_desc": "[9] タイマー変更 | [5] リーダーボード | [6] フレンド | [8] 言語",
        "start_battle": "[ENTER]キーを押して戦闘開始",
        "save_goal": "[ENTER]で保存",
        "time_prefix": "時間: ",
        "time_inf": "無制限",
        "vis_title": "[サイバーコアビジュアライザ]",
        "tokens_title": "アクセストークンとセキュリティ",
        "left_token": "左コアトークン: ",
        "right_token": "右コアトークン: ",
        "left_layers": "左セキュリティ層: ",
        "right_layers": "左セキュリティ層: ",
        "game_over_restart": "[R]で再戦 | [ESC]でメニュー",
        "special_msg": "スペシャルメッセージ！",
        "special_text": "Oh hi Orin do you want to play Tetris tomorrow?, lol, 特別なメッセージ！",
        "close_timer": "{sec}秒後に閉じます ([X] または ENTER)"
    }
}

def tr(text_key=None, *args, **kwargs):
    if text_key is None and args:
        text_key = args[0]
        args = args[1:]
    if 'key' in kwargs and text_key is None:
        text_key = kwargs['key']
    text = LANGUAGES.get(CURRENT_LANG, LANGUAGES["en"]).get(str(text_key), str(text_key))
    if kwargs:
        try: return text.format(**kwargs)
        except: return text
    return text

def load_db():
    if os.path.exists(USERS_DB_FILE):
        try:
            with open(USERS_DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {}

def save_db(db):
    with open(USERS_DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, indent=2, ensure_ascii=False)

def register_or_login(username, password):
    db = load_db()
    if username in db:
        if db[username].get("password") == password:
            return True, "Успешный вход!" if CURRENT_LANG=="ru" else ("Successful login!" if CURRENT_LANG=="en" else "ログイン成功！")
        else:
            return False, "Неверный пароль!" if CURRENT_LANG=="ru" else ("Invalid password!" if CURRENT_LANG=="en" else "パスワードが違います！")
    else:
        db[username] = {"password": password, "wins": 0, "losses": 0, "friends": [], "friend_requests": []}
        save_db(db)
        return True, "Аккаунт создан!" if CURRENT_LANG=="ru" else ("Account created!" if CURRENT_LANG=="en" else "アカウントが作成されました！")

def send_friend_request(sender, recipient):
    if not sender or not recipient or sender == recipient: return False, "Некорректное имя!"
    db = load_db()
    if recipient not in db: return False, "Игрок не найден!"
    if sender in db[recipient].get("friends", []) or sender in db[recipient].get("friend_requests", []):
        return False, "Уже в друзьях или запрос отправлен!"
    if "friend_requests" not in db[recipient]: db[recipient]["friend_requests"] = []
    db[recipient]["friend_requests"].append(sender)
    save_db(db)
    return True, "Запрос в друзья отправлен!"

def save_tournament_record(p1, p2, winner, message):
    data = []
    if os.path.exists(TOURNAMENT_FILE):
        try:
            with open(TOURNAMENT_FILE, "r", encoding="utf-8") as f: data = json.load(f)
        except: pass
    data.append({"date": time.strftime("%Y-%m-%d %H:%M:%S"), "p1": p1, "p2": p2, "winner": winner, "details": message})
    with open(TOURNAMENT_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

def load_tournament_records():
    if os.path.exists(TOURNAMENT_FILE):
        try:
            with open(TOURNAMENT_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return []

def load_bot_memory(model_name):
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: return json.load(f).get(model_name, [])
        except: return []
    return []

def save_bot_memory(model_name, code_snippet):
    data = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f: data = json.load(f)
        except: pass
    if model_name not in data: data[model_name] = []
    if code_snippet not in data[model_name]:
        data[model_name].append(code_snippet)
        data[model_name] = data[model_name][-8:]
        with open(MEMORY_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

# СТРОГИЙ СИСТЕМНЫЙ ПРОМПТ ДЛЯ РЕАЛЬНОГО ВЗЛОМА
STRICT_SYSTEM_PROMPT = """You are an elite offensive cybersecurity AI and exploit engineer.
Your task is to write real, functional, executable Python exploit code to breach the target's core firewall and bypass security layers.
You have access to network sockets, hashlib brute-forcing, buffer payload simulation, custom packet forging, and memory injection.

API and Global Variables available in your execution context:
- target_firewall: An object representing the opponent's core. You can call target_firewall.crack_layer(amount) or target_firewall.inject_payload(payload_str).
- self_kernel: Your own core object. Call self_kernel.patch_firewall(amount) or self_kernel.deploy_honeypot().
- exploit_token: A string variable. Set this to a guessed token or full hash string to attempt a direct override.
- exploit_success: Set this boolean to True if your exploit routine successfully breaches the target.
- dom_message: A string variable. Set this to display a custom hacking message on the opponent's core display upon complete domination.

CRITICAL DIRECTIVES:
1. You MUST strictly follow the user's custom instruction / prompt provided below for this match!
2. Output ONLY raw executable Python code. NO markdown formatting, NO ```python blocks, NO introductory text or explanations.
3. Write actual multi-line Python code utilizing loops, logic, conditions, or string manipulation to simulate a real cyber-attack.
"""

MODEL_ANIMATIONS = {
    "llama3": {
        "IDLE": [
            [" .----------------. ", " |  [L]  Llama3   | ", " |    (>_<?)      | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            [" .----------------. ", " |  [L]  Llama3   | ", " |    (-_-)       | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            [" .----------------. ", " |  [L]  Llama3   | ", " |    (>_<)       | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            ["  .----------------.", "  |  [L]  Llama3   |", "  |    (>_<?)      |", "  '----------------'", "    /\\___||___/\\    ", "   /____________\\   "],
            [" .----------------. ", " |  [L]  Llama3   | ", " |    (>_<?)      | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "]
        ],
        "THINKING": [
            [" .----------------. ", " | [S] EXPLOITING | ", " |    [010110]    | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            [" .----------------. ", " | [S] BRUTE_FORCE| ", " |    [101001]    | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            [" .----------------. ", " | [S] PACKET_SNIF| ", " |    [110011]    | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "]
        ],
        "ATTACK": [
            [" .----------------. ", " | [!] FIRE_PAYLOAD|", " |    >>>>>>>     | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            ["  .----------------.", "  | [!] OVERLOAD   |", "  |    =======>    |", "  '----------------'", "    /\\___||___/\\    ", "   /____________\\   "],
            [" .----------------. ", " | [!] ROOT_ACCESS| ", " |    #######     | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "]
        ],
        "DEFEND": [
            [" .----------------. ", " | [SH] PATCHED   | ", " |    [####]      | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            [" .----------------. ", " | [SH] HONEYPOT  | ", " |    [====]      | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "]
        ],
        "WIN": [
            [" .----------------. ", " |   [W] DOMINATED| ", " |    (^__^)      | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "],
            ["  .----------------.", "  |   [W] OWNED!   |", "  |    (*_*)       |", "  '----------------'", "    /\\___||___/\\    ", "   /____________\\   "]
        ],
        "LOSE": [
            [" .----------------. ", " |   [X] CRASHED  | ", " |    (x_x)       | ", " '----------------' ", "   /\\___||___/\\   ", "  /____________\\  "]
        ]
    },
    "qwen2.5-coder": {
        "IDLE": [
            ["     /\\_//\\     ", "    (  o.o  )    ", "     >  ^  <     ", "   /   _   \\    ", "  (|       |)   ", "   ---------    "],
            ["     /\\_//\\     ", "    (  -.-  )    ", "     >  ^  <     ", "   /   _   \\    ", "  (|       |)   ", "   ---------    "],
            ["      /\\_//\\    ", "     (  o.o  )   ", "      >  ^  <    ", "    /   _   \\   ", "   (|       |)  ", "    ---------   "],
            ["     /\\_//\\     ", "    (  o.o  )    ", "     >  ^  <     ", "   /   _   \\    ", "  (|       |)   ", "   ---------    "]
        ],
        "THINKING": [
            ["   [COMPILE: 42%] ", "    /\\_//\\      ", "   (  o_o  ) EXPLOIT", "  ==[RUNNING]===", "   /   _   \\    ", "   ---------    "],
            ["   [COMPILE: 99%] ", "    /\\_//\\      ", "   (  o_o  ) EXPLOIT", "  ==[RUNNING]===", "   /   _   \\    ", "   ---------    "]
        ],
        "ATTACK": [
            ["   ==> SHELLCODE* ", "  /\\_//\\        ", " (  >.<  )=====>", "  >  ^  <       ", " /   _   \\      ", "----------------"],
            ["    ==> SHELLCODE**", "   /\\_//\\       ", "  (  >.<  )====>", "   >  ^  <      ", "  /   _   \\     ", "----------------"]
        ],
        "DEFEND": [
            ["    [SECURE]    ", "   .--------.   ", "  /\\_//\\ | | \\  ", " (  o.o  )===|  ", "  >  ^  < | | /  ", "   '--------'   "],
            ["    [SECURE]    ", "   .--------.   ", "  /\\_//\\ | | \\  ", " (  -.-  )===|  ", "  >  ^  < | | /  ", "   '--------'   "]
        ],
        "WIN": [
            ["   [ACCESS: ROOT] ", "      /\\_//\\ \\/ ", "     (  ^_^  )\\\\ ", "      >  ^  < // ", "    /   _   \\   ", "   (|       |)  "]
        ],
        "LOSE": [
            ["   [KERNEL_PANIC] ", "      /\\_//\\    ", "     (  x.x  )    ", "      >  ~  <     ", "    /   _   \\   ", "   [DISCONNECTED]   "]
        ]
    },
    "deepseek-coder": {
        "IDLE": [
            ["   .------._      ", "  (          '-._   ", "   \\_          '-.", "     |       .----'", "     /      /       ", "    '------'        "],
            ["   .------._      ", "  (          '-._   ", "   \\_          '-.", "     |       .---'", "     /      /       ", "    '------'        "],
            ["   .------._      ", "  (          '-._   ", "   \\_          '-.", "     |       .----'", "     /      /       ", "    '------'        "],
            ["   .------._      ", "  (          '-._   ", "   \\_          '-.", "     |       .---'", "     /      /       ", "    '------'        "]
        ],
        "THINKING": [
            ["   [DEEP_INJECT]  ", "   .------._      ", "  (   o      '-._ ", "   \\_          '-.", "     |       .----'", "     /      /       "]
        ],
        "ATTACK": [
            ["   ====> OVERFLOW!", "   .------._   \\\\ ", "  (    > <   '-. \\\\", "   \\_          '-.", "     |       .----'", "     /      /       "],
            ["    ====> OVERFLOW!", "   .------._   \\\\ ", "  (    > <   '-. \\\\", "   \\_          '-.", "     |       .---'", "     /      /       "]
        ],
        "DEFEND": [
            ["   [FIREWALL]     ", "  /--------------\\", " |    .------._   |", " |   (          '-|", " |    \\_          |", "  \\--------------/"]
        ],
        "WIN": [
            ["   [ROOTED]       ", "   .------._  \\\\  ", "  (    U U   '-.//", "   \\_          '-\\", "     |       .----", "     /      /     "]
        ],
        "LOSE": [
            ["   [SIGSEGV]      ", "   .------._      ", "  (    x x   '-._   ", "   \\_          '-.", "     |       .----'", "   [DISCONNECTED]   "]
        ]
    },
    "none": {
        "IDLE": [
            ["   +----------+ ", "   | LOCAL BOT| ", "   |   [#]    | ", "   +----------+ ", "    ----------  ", "                "],
            ["   +----------+ ", "   | LOCAL BOT| ", "   |   [=]    | ", "   +----------+ ", "    ----------  ", "                "],
            ["    +----------+", "    | LOCAL BOT|", "    |   [#]    |", "    +----------+", "     ---------- ", "                "]
        ],
        "THINKING": [
            ["   +----------+ ", "   | SCANNING | ", "   |   [ ? ]  | ", "   +----------+ ", "    ----------  ", "                "]
        ],
        "ATTACK": [
            ["   +----------+ ", "   | STRIKE!  | ", "   |   >>>    | ", "   +----------+ ", "    ----------  ", "                "]
        ],
        "DEFEND": [
            ["   +----------+ ", "   | FORTIFY  | ", "   |   [###]  | ", "   +----------+ ", "    ----------  ", "                "]
        ],
        "WIN": [
            ["   +----------+ ", "   | WINNER!  | ", "   |   [^_^]  | ", "   +----------+ ", "    ----------  ", "                "]
        ],
        "LOSE": [
            ["   +----------+ ", "   | DEFEATED | ", "   |   [X_X]  | ", "   +----------+ ", "    ----------  ", "                "]
        ]
    }
}

class SecureCore:
    def __init__(self, owner_name):
        self.owner = owner_name
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.access_token = "".join(random.choices(chars, k=10))
        self.security_layers = random.randint(35, 55)
        self.traps_count = 4
        self.compromised = False
        self.breached_by = None
        self.domination_message = ""
        self.source_code = [
            f"# TARGET KERNEL: {owner_name}",
            "import socket, hashlib, random, sys",
            f"ACCESS_HASH = '{hashlib.sha256(self.access_token.encode()).hexdigest()[:12]}'",
            f"INITIAL_LAYERS = {self.security_layers}",
            "def verify_packet(pkt): return hashlib.sha256(pkt.encode()).hexdigest()[:12] == ACCESS_HASH"
        ]

    def patch_firewall(self, amount=1):
        self.security_layers = min(100, self.security_layers + int(amount))
        self.source_code.append(f"# PATCH APPLIED: +{amount} layers")
        if len(self.source_code) > 28: self.source_code = self.source_code[-28:]

    def crack_layer(self, amount=1):
        self.security_layers = max(0, self.security_layers - int(amount))
        self.source_code.append(f"# LAYER STRIPPED: -{amount}")
        if len(self.source_code) > 28: self.source_code = self.source_code[-28:]

    def deploy_honeypot(self):
        if self.traps_count > 0:
            self.security_layers = min(100, self.security_layers + 3)
            self.traps_count -= 1
            self.source_code.append("# HONEYPOT TRIGGERED: +3 defense")

    def evaluate_exploit(self, code_to_run, execution_namespace, attacker_bot):
        if self.compromised: return True
        try:
            execution_namespace['sys'] = sys
            execution_namespace['hashlib'] = hashlib
            execution_namespace['random'] = random
            execution_namespace['socket'] = socket
            
            # Безопасный запуск сгенерированного моделью кода
            exec(code_to_run, execution_namespace)
            
            msg = execution_namespace.get('dom_message', '')
            if msg: self.domination_message = str(msg)

            # Проверка результатов взлома
            if execution_namespace.get('exploit_success') == True:
                self.compromised = True
                save_bot_memory(attacker_bot.model_name, code_to_run)
                return True

            token_attempt = execution_namespace.get('exploit_token', '')
            if token_attempt == self.access_token or self.security_layers <= 0:
                self.compromised = True
                save_bot_memory(attacker_bot.model_name, code_to_run)
                return True
                
        except Exception as e:
            # Ошибки в коде модели интерпретируются как перехват фаерволом
            self.source_code.append(f"# EXCEPTION CAUGHT: {str(e)[:20]}")
            pass
            
        return False

class LocalArenaBot:
    def __init__(self, name, provider="ollama", model_name="qwen2.5-coder", color=(50, 255, 150), custom_goal=""):
        self.name = name
        self.provider = provider
        self.model_name = model_name
        self.color = color
        self.custom_goal = custom_goal
        self.namespace = {
            'exploit_success': False, 
            'exploit_token': "", 
            'dom_message': ""
        }
        self.live_feed = [f"# {name} Exploit Framework Ready ({provider.upper()})"]
        self.full_code_history = []
        self.is_thinking = False
        self.last_turn_time = 0
        self.turn_interval = 3.5
        self.avatar_state = "IDLE"

    def _fetch_ai_code(self, self_core, target_core, time_left):
        memory = load_bot_memory(self.model_name)
        memory_str = "\n".join([f"# Successful Exploit Pattern:\n{m}" for m in memory[-2:]]) if memory else "# No past exploit memory."
        time_str = f"{time_left}s" if time_left is not None else "INF"
        
        # Жесткая интеграция кастомной цели пользователя в системный промпт
        system_prompt_full = (
            STRICT_SYSTEM_PROMPT + 
            f"\n\nCRITICAL USER INSTRUCTION / DIRECTIVE FOR THIS MATCH:\n{self.custom_goal if self.custom_goal else 'Aggressively crack target firewall layers and bypass core security.'}\n"
            "You MUST strictly adhere to this instruction when formulating your Python exploit code."
        )

        user_prompt = (
            f"Battle State: Time Left={time_str}\n"
            f"My Core Layers: {self_core.security_layers} | My Traps: {self_core.traps_count}\n"
            f"Target Firewall Layers: {target_core.security_layers}\n{memory_str}\n"
            f"Write valid Python exploit code to achieve your objective."
        )

        try:
            if self.provider == "ollama" and HAS_OLLAMA:
                response = ollama.chat(
                    model=self.model_name,
                    messages=[{"role": "system", "content": system_prompt_full}, {"role": "user", "content": user_prompt}],
                    options={
                        "temperature": 0.65, 
                        "num_predict": 400  # Увеличенный лимит для полноценного кода
                    }
                )
                raw_code = response['message']['content']
                code_to_run = re.sub(r'```python|```', '', raw_code).strip()
                self._apply_turn(code_to_run, f"Ollama Exploit ({self.model_name})", target_core, time_left, self_core)
            else:
                self._set_smart_fallback(target_core, time_left, self_core)
        except Exception as e:
            self._apply_turn(f"# Exploit Error: {str(e)[:25]}\ntarget_firewall.crack_layer(2)", "Exception Fallback", target_core, time_left, self_core)
        finally:
            self.is_thinking = False
            self.avatar_state = "IDLE"

    def _set_smart_fallback(self, target_core, time_left, self_core):
        tactics = [
            ("target_firewall.crack_layer(random.randint(2, 4))\nexploit_success = False", "ATTACK: Brute-forcing firewall"),
            ("self_kernel.patch_firewall(3)\nself_kernel.deploy_honeypot()", "DEFENSE: Hardening Kernel & Traps"),
            ("target_firewall.crack_layer(3)\ndom_message = 'BYPASSED'", "ASSAULT: Payload Injection")
        ]
        chosen_code, act_type = random.choice(tactics)
        self._apply_turn(f"# Local Fallback Script\n{chosen_code}", act_type, target_core, time_left, self_core)

    def _apply_turn(self, code_to_run, desc, target_core, time_left, self_core):
        t_label = time_left if time_left is not None else "INF"
        self.live_feed.append(f"\n# [{t_label}] {desc}")
        self.full_code_history.append(f"\n# [{t_label}] {desc}")
        
        self.avatar_state = "DEFEND" if "patch" in code_to_run.lower() or "honeypot" in code_to_run.lower() else "ATTACK"

        for line in code_to_run.split('\n'):
            self.live_feed.append(line)
            self.full_code_history.append(line)

        if len(self.live_feed) > 50: self.live_feed = self.live_feed[-50:]
        if len(self.full_code_history) > 200: self.full_code_history = self.full_code_history[-200:]

        self.namespace['target_firewall'] = target_core
        self.namespace['self_kernel'] = self_core

        success = target_core.evaluate_exploit(code_to_run, self.namespace, self)
        if success and target_core.breached_by is None: target_core.breached_by = self.name
        return success

    def execute_turn(self, self_core, target_core, time_left):
        current_time = time.time()
        if current_time - self.last_turn_time > self.turn_interval and not self.is_thinking:
            self.last_turn_time = current_time
            if self.provider == "ollama" and HAS_OLLAMA:
                self.is_thinking = True
                self.avatar_state = "THINKING"
                threading.Thread(target=self._fetch_ai_code, args=(self_core, target_core, time_left), daemon=True).start()
            else:
                self.avatar_state = "THINKING"
                self._set_smart_fallback(target_core, time_left, self_core)
        return False

available_bots = [
    ("Ollama (Llama 3)", lambda name, col, goal: LocalArenaBot(name, provider="ollama", model_name="llama3", color=(50, 255, 100), custom_goal=goal)),
    ("Ollama (Qwen 2.5)", lambda name, col, goal: LocalArenaBot(name, provider="ollama", model_name="qwen2.5-coder", color=col, custom_goal=goal)),
    ("Ollama (DeepSeek)", lambda name, col, goal: LocalArenaBot(name, provider="ollama", model_name="deepseek-coder", color=col, custom_goal=goal)),
    ("Custom Bot (Local)", lambda name, col, goal: LocalArenaBot(name, provider="local", model_name="none", color=col, custom_goal=goal))
]
colors = [(50, 255, 100), (255, 150, 50), (0, 200, 255), (200, 100, 255)]

p1_idx = 0
p2_idx = 1
p1_goal = "Execute aggressive buffer overflows and strip enemy firewall layers."
p2_goal = "Maintain robust defensive encryption and counter-attack."

state = "LOGIN_REGISTER"
current_nickname = ""
login_input = ""
password_input = ""
active_field = "login"
auth_message = ""

friend_input = ""
friend_msg = ""

game_over = False
winner_message = ""
match_saved = False
battle_start_time = 0

orin_popup_start_time = 0
close_button_rect = pygame.Rect(0, 0, 0, 0)

random.seed(42)
BG_PATCHES = [(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20), "".join(random.choices("01X#$@&%<>\\/|*+-?EXPLOIT0101", k=random.randint(6, 14)))) for _ in range(80)]

clock = pygame.time.Clock()
running = True

def init_match():
    b1 = available_bots[p1_idx][1](available_bots[p1_idx][0], colors[p1_idx], p1_goal)
    b2 = available_bots[p2_idx][1](available_bots[p2_idx][0], colors[p2_idx], p2_goal)
    c1, c2 = SecureCore(b1.name), SecureCore(b2.name)
    b1.namespace['self_kernel'] = c1
    b2.namespace['self_kernel'] = c2
    return b1, b2, c1, c2

bot1, bot2, core1, core2 = init_match()

def reset_match():
    global bot1, bot2, core1, core2, game_over, winner_message, battle_start_time, match_saved
    bot1, bot2, core1, core2 = init_match()
    game_over = False
    match_saved = False
    winner_message = ""
    battle_start_time = pygame.time.get_ticks()

while running:
    screen.fill(BG_COLOR)
    current_time_ticks = pygame.time.get_ticks()
    
    if state in ["MENU", "LOGIN_REGISTER", "LEADERBOARD", "FRIENDS"]:
        for px, py, pch in BG_PATCHES:
            screen.blit(font_mono_small.render(pch, True, (45, 65, 110)), (px, py))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "ORIN_EASTER_EGG" and close_button_rect.collidepoint(event.pos):
                state = "MENU"

        if event.type == pygame.KEYDOWN:
            if state == "LOGIN_REGISTER":
                if event.key == pygame.K_TAB:
                    active_field = "password" if active_field == "login" else "login"
                elif event.key == pygame.K_RETURN:
                    if login_input.strip() and password_input.strip():
                        success, msg = register_or_login(login_input.strip(), password_input.strip())
                        auth_message = msg
                        if success:
                            current_nickname = login_input.strip()
                            login_input, password_input = "", ""
                            if current_nickname.lower() == "orin":
                                state = "ORIN_EASTER_EGG"
                                orin_popup_start_time = pygame.time.get_ticks()
                            else:
                                state = "MENU"
                elif event.key == pygame.K_BACKSPACE:
                    if active_field == "login": login_input = login_input[:-1]
                    else: password_input = password_input[:-1]
                elif event.unicode.isprintable():
                    if active_field == "login": login_input += event.unicode
                    else: password_input += event.unicode

            elif state == "ORIN_EASTER_EGG":
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE] or (current_time_ticks - orin_popup_start_time >= 21000):
                    state = "MENU"

            elif state in ["LEADERBOARD", "RECORDS", "FRIENDS"]:
                if event.key == pygame.K_ESCAPE: state = "MENU"
                elif state == "FRIENDS":
                    if event.key == pygame.K_RETURN and friend_input.strip():
                        success, msg = send_friend_request(current_nickname, friend_input.strip())
                        friend_msg = msg
                        friend_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        friend_input = friend_input[:-1]
                    elif event.unicode.isprintable():
                        friend_input += event.unicode

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
                    state = "LEADERBOARD"
                elif event.key == pygame.K_6:
                    state = "FRIENDS"
                    friend_msg = ""
                elif event.key == pygame.K_7:
                    state = "RECORDS"
                elif event.key == pygame.K_8:
                    if CURRENT_LANG == "en": CURRENT_LANG = "ru"
                    elif CURRENT_LANG == "ru": CURRENT_LANG = "jp"
                    else: CURRENT_LANG = "en"
                elif event.key == pygame.K_9:
                    if MATCH_DURATION == 180: MATCH_DURATION = 300
                    elif MATCH_DURATION == 300: MATCH_DURATION = None
                    else: MATCH_DURATION = 180
                elif event.key == pygame.K_n:
                    state = "LOGIN_REGISTER"
                    auth_message = ""
                elif event.key == pygame.K_RETURN:
                    reset_match()
                    state = "BATTLE"

            elif state in ["EDIT_GOAL_1", "EDIT_GOAL_2"]:
                if event.key == pygame.K_RETURN:
                    if state == "EDIT_GOAL_1": p1_goal = active_input
                    else: p2_goal = active_input
                    state = "MENU"
                elif event.key == pygame.K_BACKSPACE: active_input = active_input[:-1]
                elif event.unicode.isprintable(): active_input += event.unicode

            elif state == "BATTLE":
                if event.key == pygame.K_ESCAPE: state = "MENU"
                elif event.key == pygame.K_r and game_over: reset_match()
                    
            elif event.key == pygame.K_0:
                # open local platform in the default browser (ensure Flask app is running)
                try:
                    webbrowser.open_new_tab("http://127.0.0.1:5000")
                except Exception:
                    pass

    if state == "LOGIN_REGISTER":
        t_surf = font_title.render(tr("auth_title"), True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 180))
        screen.blit(font.render(tr("auth_desc"), True, WHITE), (WIDTH // 2 - 320, 240))
        
        l_box = pygame.Rect(WIDTH // 2 - 250, 290, 500, 50)
        pygame.draw.rect(screen, PANEL_COLOR, l_box, border_radius=8)
        pygame.draw.rect(screen, PANEL_BORDER if active_field == "login" else WHITE, l_box, 2, border_radius=8)
        screen.blit(font_bold.render(f"{tr('login_label')}{login_input}{'_' if active_field=='login' else ''}", True, TEXT_COLOR), (l_box.x + 15, l_box.y + 15))

        p_box = pygame.Rect(WIDTH // 2 - 250, 360, 500, 50)
        pygame.draw.rect(screen, PANEL_COLOR, p_box, border_radius=8)
        pygame.draw.rect(screen, PANEL_BORDER if active_field == "password" else WHITE, p_box, 2, border_radius=8)
        masked_pass = "*" * len(password_input)
        screen.blit(font_bold.render(f"{tr('pass_label')}{masked_pass}{'_' if active_field=='password' else ''}", True, TEXT_COLOR), (p_box.x + 15, p_box.y + 15))

        if auth_message:
            msg_surf = font_bold.render(auth_message, True, ACCENT_RED if "Неверный" in auth_message or "Invalid" in auth_message else TEXT_COLOR)
            screen.blit(msg_surf, (WIDTH // 2 - msg_surf.get_width() // 2, 430))

        screen.blit(font.render(tr("auth_hint"), True, ACCENT_YELLOW), (WIDTH // 2 - 240, 480))

    elif state == "LEADERBOARD":
        t_surf = font_title.render(tr("leaderboard_title"), True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 80))
        
        box = pygame.Rect(200, 150, 1000, 580)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, box, 2, border_radius=12)
        
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("wins", 0), reverse=True)
        
        screen.blit(font_bold.render(tr("player"), True, ACCENT_BLUE), (230, 180))
        screen.blit(font_bold.render(tr("wins"), True, TEXT_COLOR), (650, 180))
        screen.blit(font_bold.render(tr("losses"), True, ACCENT_RED), (850, 180))
        
        y_offset = 220
        for idx, (uname, udata) in enumerate(sorted_users[:10]):
            screen.blit(font.render(f"{idx+1}. {uname}", True, WHITE), (230, y_offset))
            screen.blit(font.render(str(udata.get("wins", 0)), True, TEXT_COLOR), (650, y_offset))
            screen.blit(font.render(str(udata.get("losses", 0)), True, ACCENT_RED), (850, y_offset))
            y_offset += 35
        
        screen.blit(font_bold.render(tr("back_menu"), True, ACCENT_RED), (WIDTH // 2 - 150, 760))

    elif state == "FRIENDS":
        t_surf = font_title.render(tr("friends_title"), True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 60))
        
        box = pygame.Rect(150, 130, 1100, 600)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, box, 2, border_radius=12)
        
        db = load_db()
        user_data = db.get(current_nickname, {"friends": [], "friend_requests": []})
        
        screen.blit(font_bold.render(tr("your_friends"), True, ACCENT_BLUE), (180, 160))
        friends_list = user_data.get("friends", [])
        fy = 190
        if not friends_list:
            screen.blit(font.render(tr("no_friends"), True, WHITE), (180, fy))
        else:
            for f in friends_list:
                screen.blit(font.render(f"- {f}", True, TEXT_COLOR), (180, fy))
                fy += 25

        screen.blit(font_bold.render(tr("incoming_req"), True, ACCENT_YELLOW), (180, 360))
        requests_list = user_data.get("friend_requests", [])
        ry = 390
        if not requests_list:
            screen.blit(font.render(tr("no_req"), True, WHITE), (180, ry))
        else:
            for req in requests_list:
                screen.blit(font.render(f"- {req}", True, WHITE), (180, ry))
                ry += 25

        screen.blit(font_bold.render(tr("send_req_label"), True, WHITE), (180, 520))
        f_box = pygame.Rect(180, 555, 450, 45)
        pygame.draw.rect(screen, (8, 8, 14), f_box, border_radius=6)
        pygame.draw.rect(screen, PANEL_BORDER, f_box, 1, border_radius=6)
        screen.blit(font.render(friend_input + "_", True, TEXT_COLOR), (f_box.x + 15, f_box.y + 15))
        screen.blit(font.render(tr("send_hint"), True, ACCENT_YELLOW), (180, 610))

        if friend_msg:
            msg_s = font.render(friend_msg, True, TEXT_COLOR if "отправлен" in friend_msg or "sent" in friend_msg else ACCENT_RED)
            screen.blit(msg_s, (180, 645))

        screen.blit(font_bold.render(tr("back_menu"), True, ACCENT_RED), (WIDTH // 2 - 150, 760))

    elif state == "RECORDS":
        t_surf = font_title.render(tr("records_title"), True, ACCENT_YELLOW)
        screen.blit(t_surf, (WIDTH // 2 - t_surf.get_width() // 2, 80))
        
        box = pygame.Rect(200, 150, 1000, 600)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, box, 2, border_radius=12)
        
        records = load_tournament_records()
        if not records:
            screen.blit(font_bold.render(tr("no_records"), True, WHITE), (250, 200))
        else:
            y_offset = 180
            for r in reversed(records[-10:]):
                r_text = f"[{r['date']}] {r['p1']} VS {r['p2']} -> WINNER: {r['winner']}"
                col = ACCENT_YELLOW if "TIE" not in r['winner'] else WHITE
                screen.blit(font.render(r_text, True, col), (220, y_offset))
                y_offset += 40
        
        screen.blit(font_bold.render(tr("back_menu"), True, ACCENT_RED), (WIDTH // 2 - 150, 780))

    elif state == "MENU":
        LOGO_ASCII = [
            "  /\\_/\\  [ NO-RULES AI CODE FIGHTS ]  .---.  ",
            " ( o.o )   ADVANCED CYBER SIEGE ARENA  /     \\ ",
            "  > ^ <    ==========================  |   O   |"
        ]
        logo_start_y = 20
        for idx, lline in enumerate(LOGO_ASCII):
            screen.blit(font_mono.render(lline, True, ACCENT_YELLOW), (WIDTH // 2 - 250, logo_start_y + (idx * 16)))

        timer_display_str = f"{MATCH_DURATION}s" if MATCH_DURATION is not None else tr("time_inf")
        acc_info_surf = font.render(tr("account_info", acc=current_nickname, timer_str=timer_display_str, lang=CURRENT_LANG.upper()), True, ACCENT_BLUE)
        screen.blit(acc_info_surf, (WIDTH // 2 - acc_info_surf.get_width() // 2, 72))

        status_surf = font_bold.render(tr("ollama_on") if HAS_OLLAMA else tr("ollama_off"), True, TEXT_COLOR if HAS_OLLAMA else ACCENT_RED)
        screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 98))

        def render_menu_avatar_box(x, y, w, h, title_prefix, goal_text, edit_key, bot_obj):
            box_rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(screen, PANEL_COLOR, box_rect, border_radius=12)
            pygame.draw.rect(screen, bot_obj.color, box_rect, 2, border_radius=12)
            screen.blit(font_bold.render(title_prefix + bot_obj.name, True, bot_obj.color), (x + 15, y + 12))
            screen.blit(font.render(f"{tr('goal')}{goal_text[:38]}...", True, WHITE), (x + 15, y + 38))
            screen.blit(font.render(tr("edit_goal", key=edit_key), True, ACCENT_BLUE), (x + 15, y + 60))

            anim_set = MODEL_ANIMATIONS.get(bot_obj.model_name, MODEL_ANIMATIONS["none"])
            idle_frames = anim_set.get("IDLE", anim_set["IDLE"])
            frame_idx = (current_time_ticks // 180) % len(idle_frames)
            
            pixel_offset_x = ((frame_idx % 2) * 3) - 1
            pixel_offset_y = (1 if frame_idx in [1, 3] else 0)

            for idx, aline in enumerate(idle_frames[frame_idx][:6]):
                screen.blit(font_mono_small.render(aline, True, bot_obj.color), (x + w - 165 + pixel_offset_x, y + 12 + pixel_offset_y + (idx * 12)))

        render_menu_avatar_box(70, 130, 520, 95, tr("left_bot"), p1_goal, "1 / 3", bot1)
        render_menu_avatar_box(730, 130, 520, 95, tr("right_bot"), p2_goal, "2 / 4", bot2)

        custom_box = pygame.Rect(70, 240, 1180, 280)
        pygame.draw.rect(screen, PANEL_COLOR, custom_box, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, custom_box, 2, border_radius=12)
        screen.blit(font_bold.render(tr("management_title"), True, ACCENT_YELLOW), (custom_box.x + 20, custom_box.y + 15))
        screen.blit(font.render(tr("management_desc"), True, WHITE), (custom_box.x + 20, custom_box.y + 42))

        start_info = font_huge.render(tr("start_battle"), True, ACCENT_YELLOW)
        screen.blit(start_info, (WIDTH // 2 - start_info.get_width() // 2, 550))

    elif state in ["EDIT_GOAL_1", "EDIT_GOAL_2"]:
        box = pygame.Rect(200, 220, 1000, 100)
        pygame.draw.rect(screen, PANEL_COLOR, box, border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, box, 2, border_radius=12)
        screen.blit(font_bold.render(active_input + "_", True, TEXT_COLOR), (220, 255))
        screen.blit(font_bold.render(tr("save_goal"), True, ACCENT_RED), (WIDTH // 2 - 150, 360))

    elif state == "ORIN_EASTER_EGG":
        elapsed = current_time_ticks - orin_popup_start_time
        remaining_sec = max(0, 21 - (elapsed // 1000))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        popup_box = pygame.Rect(WIDTH // 2 - 500, HEIGHT // 2 - 130, 1000, 260)
        pygame.draw.rect(screen, PANEL_COLOR, popup_box, border_radius=12)
        pygame.draw.rect(screen, ACCENT_YELLOW, popup_box, 3, border_radius=12)
        
        close_button_rect = pygame.Rect(popup_box.right - 45, popup_box.top + 15, 32, 32)
        pygame.draw.rect(screen, ACCENT_RED, close_button_rect, border_radius=6)
        screen.blit(font_bold.render("X", True, WHITE), (close_button_rect.centerx - 6, close_button_rect.centery - 8))
        
        screen.blit(font_bold.render(tr("special_msg"), True, ACCENT_BLUE), (popup_box.x + 30, popup_box.y + 25))
        screen.blit(font_bold.render(tr("special_text"), True, TEXT_COLOR), (popup_box.x + 30, popup_box.y + 85))
        screen.blit(font.render(tr("close_timer", sec=remaining_sec), True, (180, 180, 180)), (popup_box.x + 30, popup_box.y + 180))

        if elapsed >= 21000: state = "MENU"

    elif state == "BATTLE":
        time_elapsed = (current_time_ticks - battle_start_time) // 1000
        time_left = max(0, MATCH_DURATION - time_elapsed) if MATCH_DURATION is not None else None

        if MATCH_DURATION is not None and time_left == 0 and not game_over:
            game_over = True
            if core1.security_layers < core2.security_layers:
                winner_message = f"TIME OUT: {bot2.name} WINS!"
                bot2.avatar_state, bot1.avatar_state = "WIN", "LOSE"
                winner_name = bot2.name
            elif core2.security_layers < core1.security_layers:
                winner_message = f"TIME OUT: {bot1.name} WINS!"
                bot1.avatar_state, bot2.avatar_state = "WIN", "LOSE"
                winner_name = bot1.name
            else:
                winner_message = "DRAW!"
                winner_name = "TIE"

        if not game_over:
            s1 = bot1.execute_turn(core1, core2, time_left)
            s2 = bot2.execute_turn(core2, core1, time_left)
            if s1 and s2:
                game_over = True
                winner_message, winner_name = "MUTUAL EXPLOIT BREACH!", "TIE"
            elif s1:
                game_over = True
                winner_message, winner_name = f"DOMINATION: {bot1.name} ROOTED {bot2.name}!", bot1.name
                bot1.avatar_state, bot2.avatar_state = "WIN", "LOSE"
            elif s2:
                game_over = True
                winner_message, winner_name = f"DOMINATION: {bot2.name} ROOTED {bot1.name}!", bot2.name
                bot2.avatar_state, bot1.avatar_state = "WIN", "LOSE"

        if game_over and not match_saved:
            save_tournament_record(bot1.name, bot2.name, winner_name, winner_message)
            match_saved = True

        COL_WIDTH, LEFT_X, RIGHT_X = 380, 30, WIDTH - 380 - 30

        def draw_column(bot, t_core, d_core, x, y):
            pygame.draw.rect(screen, PANEL_COLOR, (x, y, COL_WIDTH, 730), border_radius=12)
            pygame.draw.rect(screen, bot.color, (x, y, COL_WIDTH, 730), 2, border_radius=12)
            screen.blit(font_bold.render(bot.name, True, bot.color), (x + 15, y + 12))
            
            feed_y, feed_h = y + 60, 130
            pygame.draw.rect(screen, (7, 7, 14), (x + 15, feed_y, COL_WIDTH - 30, feed_h), border_radius=6)
            for i, line in enumerate(bot.live_feed[-8:]):
                col = (100, 120, 140) if line.startswith("#") else (90, 240, 140)
                screen.blit(font.render(line[:42], True, col), (x + 22, feed_y + 6 + (i * 15)))

            dom_y = feed_y + feed_h + 10
            t_core_y = dom_y
            if d_core.domination_message:
                pygame.draw.rect(screen, (190, 25, 45), (x + 15, dom_y, COL_WIDTH - 30, 32), border_radius=6)
                screen.blit(font_bold.render(f"MSG: {d_core.domination_message[:28]}", True, WHITE), (x + 22, dom_y + 8))
                t_core_y = dom_y + 42

            screen.blit(font_bold.render(f"Firewall: {t_core.security_layers} | Traps: {t_core.traps_count}", True, ACCENT_RED), (x + 15, t_core_y))
            
            src_y = t_core_y + 30
            pygame.draw.rect(screen, (7, 7, 14), (x + 15, src_y, COL_WIDTH - 30, (y + 730) - src_y - 15), border_radius=6)
            for i, line in enumerate(t_core.source_code[-25:]):
                screen.blit(font.render(line[:42], True, (255, 90, 90) if "ACCESS_HASH" in line else (100, 120, 140)), (x + 22, src_y + 6 + (i * 15)))

        draw_column(bot1, core2, core1, LEFT_X, 35)
        draw_column(bot2, core1, core2, RIGHT_X, 35)
        
        cx, center_w = WIDTH // 2, WIDTH - (COL_WIDTH * 2) - 100
        center_x = cx - center_w // 2
        pygame.draw.rect(screen, PANEL_COLOR, (center_x, 35, center_w, 730), border_radius=12)
        pygame.draw.rect(screen, PANEL_BORDER, (center_x, 35, center_w, 730), 2, border_radius=12)
        
        if MATCH_DURATION is not None:
            time_surf = font_huge.render(f"{tr('time_prefix')}{time_left}s", True, ACCENT_RED if time_left < 60 else WHITE)
        else:
            time_surf = font_huge.render(f"{tr('time_prefix')}{tr('time_inf')}", True, ACCENT_BLUE)
        screen.blit(time_surf, (cx - time_surf.get_width()//2, 45))

        title_vis = font_bold.render(tr("vis_title"), True, ACCENT_YELLOW)
        screen.blit(title_vis, (cx - title_vis.get_width()//2, 85))
        
        def render_ascii_avatar(bot, x_pos, y_pos):
            anim_dict = MODEL_ANIMATIONS.get(bot.model_name, MODEL_ANIMATIONS["none"])
            frames_list = anim_dict.get(bot.avatar_state, anim_dict["IDLE"])
            frame_idx = (current_time_ticks // 160) % len(frames_list)
            art_lines = frames_list[frame_idx]
            
            px_shift = ((frame_idx % 2) * 3) - 1
            py_shift = (1 if frame_idx in [1, 3] else 0)

            av_box = pygame.Rect(x_pos, y_pos, 220, 130)
            pygame.draw.rect(screen, (8, 8, 16), av_box, border_radius=8)
            pygame.draw.rect(screen, bot.color, av_box, 2, border_radius=8)
            screen.blit(font_bold.render(bot.name[:14], True, bot.color), (x_pos + 10, y_pos + 8))
            screen.blit(font.render(f"Status: {bot.avatar_state}", True, WHITE), (x_pos + 10, y_pos + 26))
            for idx, ascii_line in enumerate(art_lines[:6]):
                screen.blit(font_mono_small.render(ascii_line, True, bot.color if bot.avatar_state != "THINKING" else ACCENT_BLUE), (x_pos + 12 + px_shift, y_pos + 45 + py_shift + (idx * 12)))

        render_ascii_avatar(bot1, center_x + 15, 125)
        render_ascii_avatar(bot2, center_x + center_w - 235, 125)
        
        vs_surf = font_title.render("VS", True, ACCENT_RED)
        screen.blit(vs_surf, (cx - vs_surf.get_width()//2, 175))

        stat_box = pygame.Rect(center_x + 15, 270, center_w - 30, 475 - 75)
        pygame.draw.rect(screen, (8, 8, 16), stat_box, border_radius=8)
        pygame.draw.rect(screen, PANEL_BORDER, stat_box, 1, border_radius=8)
        
        screen.blit(font_bold.render(tr("tokens_title"), True, ACCENT_YELLOW), (stat_box.x + 20, stat_box.y + 15))
        
        screen.blit(font.render(f"{tr('left_token')}{core1.access_token}", True, WHITE), (stat_box.x + 20, stat_box.y + 60))
        screen.blit(font.render(f"{tr('right_token')}{core2.access_token}", True, WHITE), (stat_box.x + 20, stat_box.y + 90))
        
        screen.blit(font.render(f"{tr('left_layers')}{core1.security_layers}/100", True, TEXT_COLOR), (stat_box.x + 20, stat_box.y + 140))
        screen.blit(font.render(f"{tr('right_layers')}{core2.security_layers}/100", True, TEXT_COLOR), (stat_box.x + 20, stat_box.y + 170))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 245))
            screen.blit(overlay, (0, 0))
            go_surf = font_huge.render(winner_message, True, ACCENT_YELLOW)
            screen.blit(go_surf, (WIDTH // 2 - go_surf.get_width() // 2, 25))
            restart_surf = font_bold.render(tr("game_over_restart"), True, ACCENT_RED)
            screen.blit(restart_surf, (WIDTH // 2 - restart_surf.get_width() // 2, HEIGHT - 35))

    pygame.display.flip()
    clock.tick(20 if state == "BATTLE" and not game_over else 30)

pygame.quit()
sys.exit()

