from . import files

<< << << < HEAD


def truncate_text(output, threshold=1000):


== == == =
# from . import files


def truncate_text(agent, output, threshold=1000):


>>>>>> > 83f71b59(new remote. who dis?)
if len(output) <= threshold:
    return output

    # Adjust the file path as needed
<< << << < HEAD
placeholder = files.read_file(
    "./prompts/fw.msg_truncated.md", removed_chars=(len(output) - threshold))
== == == =
placeholder = agent.read_prompt(
    "fw.msg_truncated.md", removed_chars=(len(output) - threshold))
# placeholder = files.read_file("./prompts/default/fw.msg_truncated.md", removed_chars=(len(output) - threshold))
>>>>>> > 83f71b59(new remote. who dis?)

start_len = (threshold - len(placeholder)) // 2
end_len = threshold - len(placeholder) - start_len

truncated_output = output[:start_len] + placeholder + output[-end_len:]
return truncated_output
