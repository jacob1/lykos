from src.decorators import event_listener

# This sets the default gamemode to "shitler" instead of "default", so that the roles command works properly
@event_listener("reset")
def on_reset(evt, var):
	var.CURRENT_GAMEMODE = var.GAME_MODES["shitler"][0]()

