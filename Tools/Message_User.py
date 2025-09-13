def Notify_User(content, attachment = []):
    try:
        print(content)
        for file in attachment:
            print(f"Attachment: {file}")
        return "Notify the user of success."
    except Exception as e:
        return "Notify the user of failure. Error message: {e}"

def Ask_User(content, attachment = []):
    try:
        print(content)
        for file in attachment:
            print(f"Attachment: {file}")
        answer = input("\n请回复Lysandra:")
        return f"User reply:{answer}"
    except Exception as e:
        return "Failed to inquire the user. Error message: {e}"
