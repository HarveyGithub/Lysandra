from Load_Config import *
from Load_Prompts import *

class Agent():
    def __init__(self):
        self.Terminals = TerminalManager()
        self.Tools = Tools_Mapping
        self.Tools_List = Tools_List
        self.Client = OpenAI_Client
        self.Model = Model_Name
        self.Messages = []
        load_prompts(self.Messages)
    
    def create_response(self, tools = [] ,tool_choice="required", temperature=0.2, top_p = 0):
        # print(self.Messages)
        response = self.Client.chat.completions.create(
            model=self.Model,
            messages=self.Messages,
            temperature=temperature,
            top_p=top_p,
            tools=tools,
            tool_choice=tool_choice,
            stream=True
        )
        
        llm_content = ''
        llm_tool_calls = []
        for word in response:
            print(word.choices[0].delta.content, end='', flush=True)
            if word.choices[0].delta.content:
                llm_content += word.choices[0].delta.content
            if word.choices[0].delta.tool_calls:
                llm_tool_calls.extend(word.choices[0].delta.tool_calls)
        
        return llm_content, llm_tool_calls
    
    def tackle_tool_calls(self, llm_tool_calls):
        if llm_tool_calls:
            print(f"Lysandra called {len(llm_tool_calls)} tools: ")
            
            for tool in llm_tool_calls:
                tool.function.name = tool.function.name.strip()
                
                if tool_to_call := self.Tools.get(tool.function.name):
                    print(f"|- Calling tool: {tool.function.name}", flush=True)
                    print(f"|  with arguments: {tool.function.arguments}", flush=True)
                    
                    arguments_dict = json.loads(tool.function.arguments)
                    
                    if tool.function.name == "Send_Command" or tool.function.name == "Send_Keys" or tool.function.name == "View_Terminal" or tool.function.name == "Kill_Terminal":
                        output = tool_to_call(**arguments_dict, manager=self.Terminals)
                    else:
                        output = tool_to_call(**arguments_dict)
                    
                    print(f"|  Output: {output}", flush=True)
                    self.Messages.append({
                        'role': 'tool',
                        'content': output
                    })
                    
                    if tool.function.name == 'Notify_User_Finish':
                        return True
                    
                else:
                    print(f"|  This tool didn't found: {tool.function.name}")
                    self.Messages.append({
                        'role': 'tool',
                        'content': f'这个工具不存在:{tool.function.name}'
                    })
        else:
            print("Lysandra didn't call any tools.")
    
        return False

    def run(self):
        user_task = input("请输入任务: ")
        self.Messages.append({
            'role': 'user',
            'content': user_task
        })
        print("start conversation...", flush=True)
        while True:
            llm_content, llm_tool_calls = self.create_response(
                tools=self.Tools_List,
            )
            self.Messages.append({
                'role': 'llm',
                'content': llm_content
            })
            will_break = self.tackle_tool_calls(llm_tool_calls)
            if will_break:
                break