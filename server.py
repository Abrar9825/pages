from mcp.server.fastmcp import FastMCP
from datetime import datetime
import json

mcp = FastMCP("Mood Coaching System")

mood_log = {}

# Prompt: Structure the advice request
@mcp.prompt()
def mood_prompt(mood: str) -> str:
    return f"""
Mood: {mood}

1. Give one motivational quote based on this mood.
2. Suggest a helpful action or habit to improve the day.
3. Then say: "Logging this mood now..."
"""

# Tool: Handle mood + auto-generate dummy response
@mcp.tool()
def process_mood(mood: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in mood_log:
        mood_log[today] = []
    mood_log[today].append(mood)

    # Fake AI-style motivational response
    quote = {
        "sad": "Stars can’t shine without darkness.",
        "happy": "Happiness multiplies when shared.",
        "tired": "Rest is part of the hustle.",
        "angry": "Breathe. You control your reactions.",
    }.get(mood.lower(), "Every mood has its reason. Embrace it.")

    action = {
        "sad": "Take a short walk or journal for 5 minutes.",
        "happy": "Spread it — message a friend something kind.",
        "tired": "Take a power nap or stretch.",
        "angry": "Try deep breathing for 2 minutes.",
    }.get(mood.lower(), "Pause. Reflect. Reset.")

    return f"""
🧠 Mood: {mood}
💬 Quote: {quote}
✅ Action Tip: {action}
🗓️ Logged for {today}
"""

# Resource: View mood history
@mcp.resource("mood://{date}")
def mood_on_date(date: str) -> str:
    data = mood_log.get(date)
    return json.dumps(data) if data else "No mood found for this date."

if __name__ == "__main__":
    mcp.run()
