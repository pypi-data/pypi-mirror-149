SFY = "sfy"

# TODO: probably create another `rich_messages.py` and apply all formatting there
PROMPT_LOGIN_SUCCESSFUL = f"""[green bold]Login Successful![/]"""
PROMPT_LOGOUT_SUCCESSFUL = f"""[green bold]Logged Out![/]"""
PROMPT_POST_LOGIN = (
    f"""[cyan]You can now initiate a new service using [bold]{SFY} init[/][/]"""
)
PROMPT_ALREADY_LOGGED_OUT = f"""[yellow]You are already logged out[/]"""
