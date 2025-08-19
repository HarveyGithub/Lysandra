from Agent.Terminal import TerminalManager

tm = TerminalManager()

tm.create_terminal("1")
tm.send_command(tm, "1", "echo \"123456\" | sudo -S sudo echo \"Try to get root\"")