import random
from src.events import Event, event_listener
from src.gamestate import GameState
from src.messages import messages

GIF_CHANCE = .03

@event_listener("transition_day_resolve")
def on_transition_day_resolve(evt: Event, var: GameState, dead, killers):
    if random.random() < GIF_CHANCE:
        evt.data["message"]["gif"].append(messages["gifs"])
