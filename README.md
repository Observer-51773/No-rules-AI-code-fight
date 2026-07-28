Cyberpunk tactical AI coding simulation built with Pygame, where bots execute real executable Python code inside isolated sandboxes.

## Features
* Real Sandbox Execution: Bots run actual Python code snippets inside an isolated namespace, modifying local variables and memory banks.
* Dynamic Evolution: The system handles syntax errors on the fly and logs them directly to the bot's terminal.
* Custom Bot Support: Easily plug in your own custom logic modules and attack algorithms.

## Quick Start Guide

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
