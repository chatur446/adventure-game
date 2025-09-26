🕹 Adventure RPG Game (Python + Flask)
📌 Project Overview

This project is a console-style text adventure game built with Python (Flask framework) that runs in the browser.
The player explores a branching storyline inside a dark cave, facing challenges like fighting dragons 🐉, discovering treasures 💎, and making survival choices.

The game uses a "choose your own adventure" style where the player types commands (fight, run, open, etc.) and the story unfolds based on those decisions.

✨ Features

- Built with Flask (lightweight Python web framework).

- Playable directly in the browser (no extra software needed).

- Branching story paths with multiple endings.

- Health (HP) system → player starts with 100 HP, can lose or gain HP.

- Score system → earn points for defeating enemies and finding treasure.

- Replay option → restart and try different choices.

- Clean retro console-style UI (green text on black background).

⚔️ Gameplay Example

1. Start:

   You wake up in a dark cave. A dragon blocks the exit! 🐉
   Choices: fight, run


2. If player chooses fight:

   You draw your sword and fight! ⚔️ The dragon breathes fire...
   Choices: attack, defend


3. If player chooses attack:
   🎉 You slay the dragon, lose 20 HP, but gain 100 Score!

4. If player chooses open chest:
  💰 You find treasure and win the game!

🛠️ Tech Stack

- Python 3

- Flask (web framework)

- HTML/CSS (inline, for styling)

🚀 How to Run Locally

1. Clone the repo:
'''bash
   git clone https://github.com/YOUR-USERNAME/adventure-game.git
   cd adventure-game'''

2. (Optional) Create a virtual environment:

   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate   # Mac/Linux


3. Install dependencies:

   pip install flask


4. Run the game:

   python app.py


5. Open your browser at:
   👉 http://127.0.0.1:5000

🔮 Future Improvements

- Add random events (enemy ambush, traps, bonus HP).

- More story paths and endings.

- Inventory system (collect weapons or items).

- Deploy online (Render/Heroku) so anyone can play via URL.
