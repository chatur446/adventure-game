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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Press Start 2P', cursive;
            background: #111;
            color: #0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .game-container {
            width: 90%;
            max-width: 800px;
            background: #000;
            border: 2px solid #0f0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px #0f0;
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        .stats {
            margin-bottom: 20px;
            font-size: 18px;
            color: #0ff;
            text-shadow: 0 0 5px #0ff;
        }
        .story {
            font-size: 20px;
            margin-bottom: 30px;
            line-height: 1.6;
            min-height: 100px; /* Reserve space for text */
        }
        .choices-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        button {
            font-family: 'Press Start 2P', cursive;
            background: transparent;
            border: 2px solid #f0f;
            color: #f0f;
            padding: 12px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-shadow: 0 0 5px #f0f;
        }
        button:hover {
            background: #f0f;
            color: #000;
            box-shadow: 0 0 15px #f0f;
        }
        .msg {
            margin-top: 20px;
            font-size: 24px;
            color: #ff0;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🕹 Adventure RPG</h1>
        <div class="stats">❤️ HP: {{ hp }} | ⭐ Score: {{ score }}</div>
        <div class="story" id="story-text"></div>
        
        {% if choices %}
            <div class="choices-container">
                {% for choice in choices %}
                <form method="post" style="display: inline;">
                    <input type="hidden" name="choice" value="{{ choice }}">
                    <button type="submit">{{ choice|capitalize }}</button>
                </form>
                {% endfor %}
            </div>
        {% else %}
            <div class="msg">The End 🎬</div>
            <form method="post" action="/reset">
                <button type="submit">Play Again</button>
            </form>
        {% endif %}
    </div>

    <script>
        const storyTextElement = document.getElementById('story-text');
        const fullText = `{{ text|safe }}`; // Get text from Flask, ensure it's safe
        let i = 0;

        function typeWriter() {
            if (i < fullText.length) {
                storyTextElement.innerHTML += fullText.charAt(i);
                i++;
                setTimeout(typeWriter, 50); // Adjust speed here (milliseconds)
            }
        }

        // Start the effect when the page loads
        window.onload = typeWriter;
    </script>
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
