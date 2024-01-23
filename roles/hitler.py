from __future__ import annotations

import copy
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

@event_listener("get_role_metadata")
def on_get_role_metadata(evt, var, kind):
    if kind == "role_categories":
        evt.data["hitler"] = {"Wolfteam"}

@event_listener("send_role")
def on_send_role(evt: Event, var: GameState):
    if not var.setup_completed or var.always_pm_role:
        num_players = len(get_players(var))
        fascists = var.roles["fascist"]
        hitlers = var.roles["hitler"]
        if not hitlers:
            return

        for hitler in hitlers:
            hitler.queue_message(messages["hitler_notify"])
        hitler.send_messages()

        for hitler in hitlers:
            if num_players < 7:
                # Preparing for all possibilities that will never actually happen :)
                other_hitlers = copy.copy(hitlers)
                other_hitlers.remove(hitler)
                if other_hitlers:
                    hitler.send(messages["fascists_list_with_hitler"].format("hitler", other_hitlers, "fascist", fascists))
                else:
                    hitler.send(messages["fascists_list"].format("fascist", fascists))
            else:
                hitler.send(messages["no_fascist_list"])

@event_listener("team_win")
def on_player_win(evt, var, player, main_role, all_roles, winner):
    if winner == "fascists" and main_role == "hitler":
        evt.data["team_win"] = True
