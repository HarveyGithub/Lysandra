import Test.A
import time
from Test.A import tm
tm.send_command("1", "echo \"U@u7412369\" | sudo -S echo \"Try to get root\"")
time.sleep(2)
tm.send_command("1", "clear")
time.sleep(1)
print(tm.get_output("1"), end='\n\n')
# tm.send_command(tm, "1", "echo \"U@u7412369\" | sudo -S sudo echo \"Try to get root\"")
tm.close_terminal("1")