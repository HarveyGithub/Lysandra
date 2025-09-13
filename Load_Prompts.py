def load_prompts(Message):
    assprompt=''
    try:
        with open('./Prompts/asssistant_prompts.md','r') as f:
            assprompt=f.read()
    except FileNotFoundError:
        print("错误: Assistant prompts file not found")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    rmdprompt=''
    try:
        with open('./Prompts/remind_promts.md','r') as f:
            assprompt=f.read()
    except FileNotFoundError:
        print("错误: Remind prompts file not found")
    except Exception as e:
        print(f"错误: {str(e)}")

    Message.append({'role':'system','content':assprompt})
    Message.append({'role':'system','content':rmdprompt})
