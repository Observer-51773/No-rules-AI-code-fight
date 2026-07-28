
# No-Rules AI Code Fights: Advanced Syntax & Terminal Dump
 
## The Main Concept and Simulation Goal
No-Rules AI Code Fights is an automated, visually-driven tactical simulation exploring dynamic decision-making and cyber-warfare theory. 

The primary goal is to simulate a high-tension, zero-sum environment where algorithmic bots must balance self-preservation with aggressive exploitation. It visualizes how automated systems adapt under strict time constraints, generating executable Python scripts in real-time. As a spectator, you act as the "Root Admin," observing the live mutation of code, simulated memory allocation attempts, and the raw computational struggle for cryptographic dominance.

---

## Simulation Rules and Mechanics

### 1. Match Conditions
* **Time Limit:** Every match is strictly capped at 180 seconds (3 minutes). 
* **Win Condition:** A bot wins immediately if it reduces the opponent's Security Layers to zero, or if it successfully brute-forces the exact 16-character root access token.
* **Time-Out Resolution:** If the 3-minute timer expires, the bot with the highest number of remaining security layers is declared the winner by Layer Advantage. If layers are equal, the match ends in Mutual Annihilation.

### 2. Cryptographic Cores
Each bot is assigned a Secure Core at the start of the match:
* **Initial State:** Cores are generated with 30 to 50 Security Layers.
* **The Root Token:** A complex 16-character alphanumeric password generated at runtime. 
* **Honeypots:** Each core contains a maximum of 5 recursive deception traps.

### 3. AI Decision Matrix and Code Generation
Bots do not follow static text commands; they dynamically assess the battlefield and generate multi-line executable scripts based on four primary strategies:
* **Attack (Buffer Overflow Simulation):** The bot writes and executes exploit scripts (using variables and loops) to peel security layers off the enemy's core.
* **Defend (Algorithm Compilation):** If a bot's core drops below critical levels and time permits, it temporarily halts attacks to write patching algorithms, instantly adding structural layers to its own core.
* **Trap (Honeypot Injection):** The bot deploys a fake vulnerability class. If the opponent attacks during this turn, the attack fails, granting the defending bot bonus layers.
* **Fatal Attack (Root Injection):** When the timer drops below 60 seconds, bots abandon self-preservation. They generate aggressive brute-force loops, attempting to inject the root token and force a critical breach before time runs out.

### 4. Live Execution Terminal and Root Spectator Clearance
Each bot operates within a Live Execution Terminal on the UI, displaying the real-time generation of loops, functions, and memory manipulation scripts. Meanwhile, a highly classified central panel displays the true 16-character tokens of both cores—information completely hidden from the battling AIs.

### 5. Post-Match Terminal Dump
Upon match completion, the simulation halts and generates a raw Code Dump. Instead of simple text logs, this screen displays the final consecutive lines of Python scripts generated and executed by both bots. This provides an unfiltered view into the exact algorithms that led to victory or defeat.

quick start guide:

1. Install dependencies (requires Pygame):
   ```bash
   pip3 install pygame

 2 python3 ai_arena.py

 How to add your own bot 
Create a new bot class by inheriting from RealCodeBot (similar to UserPythonBot):
class MyCustomBot(RealCodeBot):
    def __init__(self):
        super().__init__("My-Bot-Name", (255, 100, 200)) # Set name and RGB color
        self.code_lines = ["# MY CUSTOM MODULE", "import math"]

    def execute_turn(self, opponent):
        # Define custom actions and code snippets to run
        snippets = [
            ("Custom attack description", "damage = 20; memory_bank['flag'] = True", 20)
        ]
        desc, code_to_run, power = random.choice(snippets)
        self.current_action = f"[CUSTOM] {desc}"

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
            opponent.domination_progress += 5

        if opponent.domination_progress > 100:
            opponent.domination_progress = 100


Instantiate your to and replace one of the opponents in the main loop:
bot1 = RealCodeBot("Model-Alpha", ACCENT_BLUE)
bot2 = MyCustomBot()
