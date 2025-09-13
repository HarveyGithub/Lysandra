from flask import Flask, render_template, request, jsonify
from Agent.Agent import Agent
import threading
import time
import json

app = Flask(__name__)

# 全局变量存储agent实例和消息历史
agent_instance = None
messages = []

# 定义一个函数来将对象转换为可JSON序列化的格式
def serialize_tool_calls(tool_calls):
    if not tool_calls:
        return []
    
    serialized = []
    for tool_call in tool_calls:
        serialized.append({
            "index": getattr(tool_call, "index", None),
            "id": getattr(tool_call, "id", None),
            "type": getattr(tool_call, "type", None),
            "function": {
                "name": getattr(tool_call.function, "name", None),
                "arguments": getattr(tool_call.function, "arguments", None)
            } if hasattr(tool_call, "function") else None
        })
    return serialized

class WebAgent(Agent):
    def __init__(self):
        super().__init__()
        self.web_messages = []
        
    def create_response(self, tools=[], tool_choice="auto", temperature=0.2, top_p=0.7):
        # 重写create_response方法以捕获输出
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
            if word.choices[0].delta.content:
                llm_content += word.choices[0].delta.content
            if word.choices[0].delta.tool_calls:
                llm_tool_calls.extend(word.choices[0].delta.tool_calls)
        
        return llm_content, llm_tool_calls

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_agent', methods=['POST'])
def start_agent():
    global agent_instance, messages
    if agent_instance is None:
        agent_instance = WebAgent()
        messages = []
        return jsonify({"status": "success", "message": "Agent started successfully"})
    else:
        return jsonify({"status": "error", "message": "Agent is already running"})

@app.route('/send_message', methods=['POST'])
def send_message():
    global agent_instance, messages
    if agent_instance is None:
        return jsonify({"status": "error", "message": "Agent not started"})
    
    try:
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({"status": "error", "message": "No message provided"})
        
        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_input})
        agent_instance.Messages.append({"role": "user", "content": user_input})
        
        # 模拟Agent.run的任务循环处理
        llm_content = ""
        while True:
            # 获取AI响应
            content, tool_calls = agent_instance.create_response(
                tools=agent_instance.Tools_List,
            )
            
            llm_content += content
            
            # 序列化tool_calls以确保它们可以被JSON序列化
            serialized_tool_calls = serialize_tool_calls(tool_calls)
            
            # 添加AI响应到历史
            messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": serialized_tool_calls
            })
            
            # 处理工具调用
            if tool_calls:
                will_break = agent_instance.tackle_tool_calls(tool_calls)
                if will_break:
                    agent_instance = None  # 重置agent实例
                    break
            else:
                # 没有更多工具调用，结束循环
                break
        
        return jsonify({
            "status": "success",
            "user_message": user_input,
            "ai_response": llm_content,
            "messages": messages
        })
    except Exception as e:
        # 记录错误日志
        print(f"Error in send_message: {str(e)}")
        return jsonify({"status": "error", "message": f"Internal server error: {str(e)}"}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    # 创建消息副本并序列化tool_calls
    messages_copy = []
    for msg in messages:
        msg_copy = msg.copy()
        if "tool_calls" in msg_copy:
            msg_copy["tool_calls"] = serialize_tool_calls(msg_copy["tool_calls"])
        messages_copy.append(msg_copy)
    
    return jsonify({"messages": messages_copy})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)