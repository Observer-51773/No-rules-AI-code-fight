
# No-Rules AI Code Fights: Local Ollama Arena

## Project Goal
To create an autonomous cyber-warfare simulation arena where local AI models write and execute real-time Python code to breach opponent secure kernels, manage layered defenses, and compete in a tactical code siege.

## Key Updates & Features
* **Local Ollama Integration**: Fully offline execution powered by local models (`qwen2.5-coder`, `deepseek-coder`, `llama3`) alongside a built-in custom local fallback agent.
* **Real Code Execution Sandbox**: AI-generated code snippets are safely evaluated within an isolated namespace using Python's `exec`, directly translating script logic into game mechanics (layer peeling, honeypot traps, and token brute-forcing).
* **Pygame Visual Interface**: Real-time terminal feeds displaying active execution lines, core integrity metrics, security layers, and a comprehensive code history dump upon match conclusion.
* **Zero Cloud Dependencies**: Complete independence from external APIs, ensuring no rate limits, latency, or internet connectivity requirements.

## Installation & Setup

1. **Prerequisites**: Ensure Python 3, Pygame, and Ollama are installed on your system.
2. **Create and Activate Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

