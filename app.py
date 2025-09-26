from flask import Flask, request, session, render_template_string

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Story scenes with optional health/score effects
story = {
    "start": {
        "text": "You wake up in a dark cave. A dragon blocks the exit! 🐉 What do you do?",
        "choices": {"fight": "fight_dragon", "run": "run_away"}
    },
    "fight_dragon": {
        "text": "You draw your sword and fight! ⚔️ The dragon breathes fire... Do you 'attack' or 'defend'?",
        "choices": {"attack": "victory", "defend": "burned"}
    },
    "run_away": {
        "text": "You sprint deeper into the cave and find a treasure chest! 💎 Do you 'open' it or 'ignore' it?",
        "choices": {"open": "treasure", "ignore": "lost"}
    },
    "victory": {
        "text": "🎉 You slay the dragon and escape the cave a hero!",
        "choices": {},
        "hp_change": -20,
        "score_change": 100
    },
    "burned": {
        "text": "🔥 The dragon’s fire engulfs you. You lose 40 HP!",
        "choices": {"recover": "escape"},
        "hp_change": -40
    },
    "escape": {
        "text": "Wounded, you crawl through a hidden passage and find daylight. You survived!",
        "choices": {},
        "score_change": 50
    },
    "treasure": {
        "text": "💰 Inside the chest, you find gold and jewels! You win!",
        "choices": {},
        "score_change": 150
    },
    "lost": {
        "text": "😨 You wander endlessly and never find a way out. Game Over!",
        "choices": {},
        "hp_change": -100
    }
}

# HTML Template
page_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Adventure RPG</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; text-align: center; padding: 20px; }
        .story { font-size: 20px; margin: 20px; }
        input, button { padding: 8px; font-size: 16px; margin: 5px; }
        .msg { margin: 20px; font-size: 18px; color: #ff0; }
        .stats { margin: 10px; font-size: 18px; color: #0ff; }
    </style>
</head>
<body>
    <h1>🕹 Adventure RPG</h1>
    <div class="stats">❤️ HP: {{ hp }} | ⭐ Score: {{ score }}</div>
    <div class="story">{{ text }}</div>
    {% if choices %}
        <form method="post">
            <input type="text" name="choice" placeholder="Type your choice..." required>
            <button type="submit">Submit</button>
        </form>
        <div class="msg">Choices: {{ choices|join(", ") }}</div>
    {% else %}
        <div class="msg">The End 🎬</div>
        <form method="post" action="/reset">
            <button type="submit">Play Again</button>
        </form>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def game():
    if "scene" not in session:
        session["scene"] = "start"
        session["hp"] = 100
        session["score"] = 0

    scene = story[session["scene"]]
    text = scene["text"]
    choices = list(scene["choices"].keys())

    # Apply scene effects (HP & Score updates)
    if "hp_change" in scene:
        session["hp"] += scene["hp_change"]
    if "score_change" in scene:
        session["score"] += scene["score_change"]

    # Check for game over
    if session["hp"] <= 0:
        text = "💀 You have no HP left. Game Over!"
        choices = []

    if request.method == "POST" and "choice" in request.form:
        choice = request.form["choice"].lower()
        if choice in scene["choices"]:
            session["scene"] = scene["choices"][choice]
            return game()

    return render_template_string(page_template, text=text, choices=choices,
                                  hp=session["hp"], score=session["score"])

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return game()

if __name__ == "__main__":
    app.run(debug=True)
