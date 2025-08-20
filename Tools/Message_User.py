def Notify_User(content, attachment = []):
    try:
        print(content)
        for file in attachment:
            print(f"Attachment: {file}")
        return "通知用户成功。"
    except Exception as e:
        return "通知用户失败，错误信息：{e}"

def Notify_User_Finish(content, attachment = []):
    try:
        print(content)
        for file in attachment:
            print(f"Attachment: {file}")
        return "通知用户任务完成成功。"
    except Exception as e:
        return "通知用户任务完成失败，错误信息：{e}"

def Ask_User(content, attachment = []):
    try:
        print(content)
        for file in attachment:
            print(f"Attachment: {file}")
        answer = input("\n请回复Lysandra:")
        return answer
    except Exception as e:
        return "询问用户失败，错误信息：{e}"