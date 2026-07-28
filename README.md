# No-Rules AI Code Fights: Advanced Autonomous Arena

No-Rules AI Code Fights is a retro-styled, real-time tactical simulation built in Python with Pygame. In this arena, autonomous AI agents—powered by local LLMs via Ollama or heuristic fallback logic—compete against each other by writing and executing Python scripts in real time to breach opponent server cores while defending their own.

## Key Features

* Autonomous Code Generation: Integrates with local Ollama models (such as `qwen2.5-coder` and `deepseek-coder`and llama3) to write dynamic combat code.
* Interactive Visualizer: Real-time 2D UI rendered with Pygame, featuring retro terminal styling and animated ASCII combat avatars.
* Custom Avatar Converter: Convert custom image files (PNG/JPG) into ASCII visual avatars using Pillow.
* Strategy Persistence: Persists successful breach strategies in `arena_memory.json` to allow bots to learn from past matches.
* Configurable Directives: Customize specific combat goals and tactical objectives for each bot before starting a match.
* Full Match Telemetry: View real-time tactical feeds, remaining security layers, active tokens, and post-match code execution dumps.

## System Requirements

* Operating System: macOS, Linux, or Windows
* Python: Version 3.10 or higher
* Package Manager: `uv` (Fast Python package manager)
* Ollama (Optional): Required if running local LLM inference for dynamic code generation

## Installation

### 1. Install `uv`

If you do not have `uv` installed on your system, install it using the official installer:

On macOS and Linux:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```


On Windows "PowerShell" 
 ```bash
    powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | iex"

Verify installation:
 ```bash
    uv --version

2. Clone or Prepare the Repository
Navigate to your project directory:
```bash
git clone [https://github.com/your-username/no-rules-ai-code-fights.git](https://github.com/your-username/no-rules-ai-code-fights.git)
cd no-rules-ai-code-fights

3. Create a Virtual Environment
Use ⁠uv⁠ to create a virtual environment:
```bash 
uv venv

Activate the environment:
 On MacOS/Linux:
```bash
source .venv/bin/activate

On Windows (PowerShell):
```bash
.venv\Scripts\Activate.ps1

4.Install Dependencies
Install the required Python packages into your environment using ⁠uv pip⁠:
```bash
uv pip install pygame ollama pillow

Alternatively, if you prefer running commands without activating the environment manually:
```bash
uv pip install --python .venv pygame ollama pillow

Setting Up Ollama (Optional but Recommended)
To enable dynamic LLM-driven bot logic:
1.Download and install Ollama from https://ollama.com.

2.Start the Ollama daemon

3.Pull the supported coding models:
```bash
ollama pull qwen2.5-coder
ollama pull deepseek-coder
ollama pull llama3

If Ollama is not installed or running, the application will automatically fall back to rule-based tactical heuristics, allowing full gameplay without external dependencies.
Running the Application
Execute the application using ⁠uv⁠:
```bash
uv run python ai_arena.py

Or, if your virtual environment is already activated:
```bash
python ai_arena.py

Controls and Usage
Main Menu
 N: Change user nickname profile.
 1: Toggle model/provider for Left Bot.
 2: Toggle model/provider for Right Bot.
 3: Edit Left Bot tactical goal/directive.
 4: Edit Right Bot tactical goal/directive.
 5: Load a custom PNG/JPG image to generate an ASCII avatar.
 ENTER: Launch match.
Battle Mode
 R: Restart match (available when match ends).
 ESC: Exit battle mode and return to Main Menu.
File Structure
 ⁠ai_arena.py⁠: Main application script containing Pygame engine, AI execution loops, and UI rendering.
 ⁠user_profile.json⁠: Auto-generated file storing user configuration and active nickname.
 ⁠arena_memory.json⁠: Auto-generated persistent storage for successful AI combat code snippets.
License
This project is open-source and available under the MIT License.



































 



