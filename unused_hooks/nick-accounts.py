import inspect
from src.decorators import HOOKS

# Wrap around existing hooks, replacing the "account" parameter with the nick before calling them
class fakehook:
    def __init__(self, orig_func):
        self.orig_func = orig_func
        self.hookid = 0

        sig = inspect.signature(orig_func.func)

        i = 0
        self.nick_pos = None
        self.rawnick_pos = None
        self.account_pos = None
        # Search for nick and account parameters
        for parameter in sig.parameters.values():
            if parameter.name == "nick":
                self.nick_pos = i
            elif parameter.name == "rawnick":
                self.rawnick_pos = i
            elif parameter.name == "account":
                self.account_pos = i
            i = i + 1
        if not self.account_pos or (not self.nick_pos and not self.rawnick_pos):
            raise Exception("Hook must have account, and either nick or rawnick parameters")

    def caller(self, *args, **kwargs):
        _ignore_locals_ = True

        new_args = list(args)
        if self.nick_pos:
            fake_account = new_args[self.nick_pos]
        elif self.rawnick_pos:
            fake_account = new_args[self.rawnick_pos]
        else:
            raise Exception("No account, this shouldn't happen")

        # rawnick parameter and sometimes nick parameter has the full host, ensure we only use the nick
        fake_account = fake_account.split("!")[0]
        if "account" in kwargs:
            kwargs["account"] = fake_account
        else:
            new_args[self.account_pos] = fake_account

        return self.orig_func.caller(*new_args, **kwargs)

# On nick change, we need to log the user into their new "account"
class nickhook:
    def __init__(self):
        self.hookid = 0

    def caller(self, cli, old_rawnick, nick):
        _ignore_locals_ = True

        for fn in HOOKS.get("account", []):
            fn.caller(cli, nick + "!" + old_rawnick.split("!")[1], nick)


replace_events = ["whospcrpl", "whoisaccount", "on_loggedin", "account", "join"]
for event in replace_events:
    for i in range(len(HOOKS[event])):
        HOOKS[event][i] = fakehook(HOOKS[event][i])

HOOKS["nick"].append(nickhook())
