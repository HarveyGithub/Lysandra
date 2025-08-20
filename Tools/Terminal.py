import time
from Agent.Terminal import TerminalManager

def Send_Command(command, terminal_id, dir, manager: TerminalManager):
    if terminal_id not in manager.terminals:
        manager.create_terminal(terminal_id)
        manager.send_command(terminal_id, "conda init && conda activate Manus_Sandbox")
        time.sleep(2)
        manager.send_command(terminal_id, "echo \"U@u7412369\" | sudo -S echo \"Try to get root\"")
        time.sleep(2)
        manager.send_command(terminal_id, "clear")
        time.sleep(1)
    manager.send_command(terminal_id, "cd " + dir)
    manager.send_command(terminal_id, command)
    time.sleep(2)
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def View_Terminal(terminal_id, manager: TerminalManager):
    if terminal_id not in manager.terminals:
        return ValueError(f"终端 {terminal_id} 不存在")
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def Send_Keys(keys, terminal_id, manager: TerminalManager, end_newline=False):
    if terminal_id not in manager.terminals:
        manager.create_terminal(terminal_id)
    manager.send_keys(terminal_id + "\n" if end_newline else "", keys)
    time.sleep(2)
    output = manager.get_output(terminal_id)
    return "终端输出:\n" + output

def Kill_Terminal(terminal_id, manager: TerminalManager):
    manager.close_terminal(terminal_id)
    return f"终端 {terminal_id} 已关闭"