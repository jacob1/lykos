from __future__ import annotations

import re
import random
import itertools
import math
from collections import defaultdict

from src import channels, users
from src.functions import get_players, get_all_players, get_main_role, get_reveal_role, get_target
from src.decorators import command
from src.containers import UserList, UserSet, UserDict, DefaultUserDict
from src.messages import messages
from src.status import try_misdirection, try_exchange
from src.events import Event, event_listener
from src.gamestate import GameState
from src.users import User

@event_listener("send_role")
def on_send_role(evt: Event, var: GameState):
    if not var.setup_completed or var.always_pm_role:
        liberals = var.roles["liberal"]
        if liberals:
            for liberal in liberals:
                liberal.queue_message(messages["liberal_notify"])
            liberal.send_messages()

@event_listener("get_role_metadata")
def on_get_role_metadata(evt, var, kind):
    if kind == "role_categories":
        evt.data["liberal"] = {"Village"}

@event_listener("team_win")
def on_player_win(evt, var, player, main_role, all_roles, winner):
    if winner == "liberals" and main_role == "liberal":
        evt.data["team_win"] = True
