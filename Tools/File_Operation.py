import os
def Read_File(file_path, start_line=0, end_line=0):
    try:
        content = ""
        with open(file_path, "r") as f:
            idx = 0
            for line in f.readlines():
                idx+=1
                if idx >= start_line:
                    content += line
                if idx >= end_line and end_line != 0:
                    break
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

def Write_File(file_path, content, append=False, front_newline=False, end_newline=False):
    try:
        with open(file_path, "a" if append else "w", encoding="utf-8") as f:
            if front_newline:
                f.write("\n")
            f.write(content)
            if end_newline:
                f.write("\n")
        return "Successfully written to file."
    except Exception as e:
        return f"Error: {str(e)}"
