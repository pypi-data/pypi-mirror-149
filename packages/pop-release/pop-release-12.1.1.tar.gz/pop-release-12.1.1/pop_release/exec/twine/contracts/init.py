def pre(hub, ctx):
    func_ctx = ctx.get_arguments().get("ctx")
    if func_ctx and not func_ctx.acct:
        # If no acct was set then collect them from the environment
        func_ctx.acct = hub.acct.twine.settings.default()
