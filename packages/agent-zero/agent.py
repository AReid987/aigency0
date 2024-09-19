import asyncio
import importlib
import inspect
import json
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import python.helpers.log as Log
from langchain.schema import AIMessage
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from python.helpers import errors, extract_tools, files, rate_limiter
from python.helpers.defer import DeferredTask
from python.helpers.dirty_json import DirtyJson
from python.helpers.print_style import PrintStyle

<< << << < HEAD

== == == =

>>>>>> > 83f71b59(new remote. who dis?)

<< << << < HEAD

== == == =


class AgentContext:

    _contexts: dict[str, 'AgentContext'] = {}
    _counter: int = 0

    def __init__(self, config: 'AgentConfig', id: str | None = None, agent0: 'Agent|None' = None):
        # build context
        self.id = id or str(uuid.uuid4())
        self.config = config
        self.log = Log.Log()
        self.agent0 = agent0 or Agent(0, self.config, self)
        self.paused = False
        self.streaming_agent: Agent | None = None
        self.process: DeferredTask | None = None
        AgentContext._counter += 1
        self.no = AgentContext._counter

        self._contexts[self.id] = self

    @staticmethod
    def get(id: str):
        return AgentContext._contexts.get(id, None)

    @staticmethod
    def first():
        if not AgentContext._contexts: return None
        return list(AgentContext._contexts.values())[0]

    @staticmethod
    def remove(id: str):
        context = AgentContext._contexts.pop(id, None)
        if context and context.process: context.process.kill()
        return context

    def reset(self):
        if self.process: self.process.kill()
        self.log.reset()
        self.agent0 = Agent(0, self.config, self)
        self.streaming_agent = None
        self.paused = False

    def communicate(self, msg: str, broadcast_level: int = 1):
        self.paused = False  # unpause if paused

        if self.process and self.process.is_alive():
            if self.streaming_agent: current_agent = self.streaming_agent
            else:                     current_agent = self.agent0

            # set intervention messages to agent(s):
            intervention_agent = current_agent
            while intervention_agent and broadcast_level != 0:
                intervention_agent.intervention_message = msg
                broadcast_level -= 1
                intervention_agent = intervention_agent.data.get(
                    "superior", None)
        else:
            self.process = DeferredTask(self.agent0.message_loop, msg)

        return self.process


>>>>>> > 83f71b59(new remote. who dis?)


@dataclass
class AgentConfig:
    chat_model: BaseChatModel | BaseLLM
    utility_model: BaseChatModel | BaseLLM
    embeddings_model: Embeddings


<< << << < HEAD
    memory_subdir: str = ""
== == == =
    prompts_subdir: str = ""
    memory_subdir: str = ""
    knowledge_subdir: str = ""
>>>>>> > 83f71b59(new remote. who dis?)
    auto_memory_count: int = 3
    auto_memory_skip: int = 2
    rate_limit_seconds: int = 60
    rate_limit_requests: int = 15
<< << << < HEAD
    rate_limit_input_tokens: int = 1000000
== == == =
    rate_limit_input_tokens: int = 0
>>>>>> > 83f71b59(new remote. who dis?)
    rate_limit_output_tokens: int = 0
    msgs_keep_max: int = 25
    msgs_keep_start: int = 5
    msgs_keep_end: int = 10
    response_timeout_seconds: int = 60
    max_tool_response_length: int = 3000
    code_exec_docker_enabled: bool = True
    code_exec_docker_name: str = "agent-zero-exe"
    code_exec_docker_image: str = "frdel/agent-zero-exe:latest"
    code_exec_docker_ports: dict[str, int] = field(
        default_factory=lambda: {"22/tcp": 50022})
    code_exec_docker_volumes: dict[str, dict[str, str]] = field(
        default_factory=lambda: {files.get_abs_path("work_dir"): {"bind": "/root", "mode": "rw"}})
    code_exec_ssh_enabled: bool = True
    code_exec_ssh_addr: str = "localhost"
    code_exec_ssh_port: int = 50022
    code_exec_ssh_user: str = "root"
    code_exec_ssh_pass: str = "toor"
    additional: Dict[str, Any] = field(default_factory=dict)
<< << << < HEAD


class Agent:

    paused = False
    streaming_agent = None

    def __init__(self, number: int, config: AgentConfig):


== == == =

# intervention exception class - skips rest of message loop iteration


class InterventionException(Exception):
    pass

# killer exception class - not forwarded to LLM, cannot be fixed on its own, ends message loop


class KillerException(Exception):
    pass


class Agent:

    def __init__(self, number: int, config: AgentConfig, context: AgentContext | None = None):


>>>>>> > 83f71b59(new remote. who dis?)

        # agent config
        self.config = config

<< << << < HEAD
== == == =
        # agent context
        self.context = context or AgentContext(config)

>>>>>> > 83f71b59(new remote. who dis?)
        # non-config vars
        self.number = number
        self.agent_name = f"Agent {self.number}"

<< << << < HEAD
        self.system_prompt = files.read_file(
            "./prompts/agent.system.md", agent_name=self.agent_name)
        self.tools_prompt = files.read_file("./prompts/agent.tools.md")

        self.history = []
        self.last_message = ""
        self.intervention_message = ""
        self.intervention_status = False
        self.rate_limiter = rate_limiter.RateLimiter(max_calls=self.config.rate_limit_requests, max_input_tokens=self.config.rate_limit_input_tokens,
                                                     max_output_tokens=self.config.rate_limit_output_tokens, window_seconds=self.config.rate_limit_seconds)
        self.data = {}  # free data object all the tools can use

        os.chdir(files.get_abs_path("./work_dir"))  # change CWD to work_dir


    def message_loop(self, msg: str):
        try:
            printer = PrintStyle(italic=True, font_color="#b3ffd9", padding=False)    
            user_message = files.read_file("./prompts/fw.user_message.md", message=msg)
            self.append_message(user_message, human=True) # Append the user's input to the history                        
            memories = self.fetch_memories(True)
                
            while True: # let the agent iterate on his thoughts until he stops by using a tool
                Agent.streaming_agent = self #mark self as current streamer
                agent_response = ""
                self.intervention_status = False # reset interventon status

                try:

                    system = self.system_prompt + "\n\n" + self.tools_prompt
                    memories = self.fetch_memories()
=======
        self.history = []
        self.last_message = ""
        self.intervention_message = ""
        self.rate_limiter = rate_limiter.RateLimiter(self.context.log,max_calls=self.config.rate_limit_requests,max_input_tokens=self.config.rate_limit_input_tokens,max_output_tokens=self.config.rate_limit_output_tokens,window_seconds=self.config.rate_limit_seconds)
        self.data = {} # free data object all the tools can use

    async def message_loop(self, msg: str):
        try:
            printer = PrintStyle(italic=True, font_color="#b3ffd9", padding=False)    
            user_message = self.read_prompt("fw.user_message.md", message=msg)
            await self.append_message(user_message, human=True) # Append the user's input to the history                        
            memories = await self.fetch_memories(True)
                
            while True: # let the agent iterate on his thoughts until he stops by using a tool
                self.context.streaming_agent = self #mark self as current streamer
                agent_response = ""

                try:

                    system = self.read_prompt("agent.system.md", agent_name=self.agent_name) + "\n\n" + self.read_prompt("agent.tools.md")
                    memories = await self.fetch_memories()
>>>>>>> 83f71b59 (new remote. who dis?)
                    if memories: system+= "\n\n"+memories

                    prompt = ChatPromptTemplate.from_messages([
                        SystemMessage(content=system),
                        MessagesPlaceholder(variable_name="messages") ])
                    
                    inputs = {"messages": self.history}
                    chain = prompt | self.config.chat_model

                    formatted_inputs = prompt.format(messages=self.history)
                    tokens = int(len(formatted_inputs)/4)     
                    self.rate_limiter.limit_call_and_input(tokens)
                    
                    # output that the agent is starting
<<<<<<< HEAD
                    PrintStyle(bold=True, font_color="green", padding=True, background_color="white").print(f"{self.agent_name}: Starting a message:")
                                            
                    for chunk in chain.stream(inputs):
                        if self.handle_intervention(agent_response): break # wait for intervention and handle it, if paused
=======
                    PrintStyle(bold=True, font_color="green", padding=True, background_color="white").print(f"{self.agent_name}: Generating:")
                    log = self.context.log.log(type="agent", heading=f"{self.agent_name}: Generating:")
                              
                    async for chunk in chain.astream(inputs):
                        await self.handle_intervention(agent_response) # wait for intervention and handle it, if paused
>>>>>>> 83f71b59 (new remote. who dis?)

                        if isinstance(chunk, str): content = chunk
                        elif hasattr(chunk, "content"): content = str(chunk.content)
                        else: content = str(chunk)
                        
                        if content:
<<<<<<< HEAD
                            printer.stream(content) # output the agent response stream                
                            agent_response += content # concatenate stream into the response

                    self.rate_limiter.set_output_tokens(int(len(agent_response)/4))
                    
                    if not self.handle_intervention(agent_response):
                        if self.last_message == agent_response: #if assistant_response is the same as last message in history, let him know
                            self.append_message(agent_response) # Append the assistant's response to the history
                            warning_msg = files.read_file("./prompts/fw.msg_repeat.md")
                            self.append_message(warning_msg, human=True) # Append warning message to the history
                            PrintStyle(font_color="orange", padding=True).print(warning_msg)

                        else: #otherwise proceed with tool
                            self.append_message(agent_response) # Append the assistant's response to the history
                            tools_result = self.process_tools(agent_response) # process tools requested in agent message
                            if tools_result: return tools_result #break the execution if the task is done

                # Forward errors to the LLM, maybe he can fix them
                except Exception as e:
                    error_message = errors.format_error(e)
                    msg_response = files.read_file("./prompts/fw.error.md", error=error_message) # error message template
                    self.append_message(msg_response, human=True)
                    PrintStyle(font_color="red", padding=True).print(msg_response)
                    
        finally:
            Agent.streaming_agent = None # unset current streamer
=======
                            printer.stream(content) # output the agent response stream
                            agent_response += content # concatenate stream into the response
                            self.log_from_stream(agent_response, log)

                    self.rate_limiter.set_output_tokens(int(len(agent_response)/4)) # rough estimation
                    
                    await self.handle_intervention(agent_response)

                    if self.last_message == agent_response: #if assistant_response is the same as last message in history, let him know
                        await self.append_message(agent_response) # Append the assistant's response to the history
                        warning_msg = self.read_prompt("fw.msg_repeat.md")
                        await self.append_message(warning_msg, human=True) # Append warning message to the history
                        PrintStyle(font_color="orange", padding=True).print(warning_msg)
                        self.context.log.log(type="warning", content=warning_msg)

                    else: #otherwise proceed with tool
                        await self.append_message(agent_response) # Append the assistant's response to the history
                        tools_result = await self.process_tools(agent_response) # process tools requested in agent message
                        if tools_result: #final response of message loop available
                            return tools_result #break the execution if the task is done

                except InterventionException as e:
                    pass # intervention message has been handled in handle_intervention(), proceed with conversation loop
                except asyncio.CancelledError as e:
                    PrintStyle(font_color="white", background_color="red", padding=True).print(f"Context {self.context.id} terminated during message loop")
                    raise e # process cancelled from outside, kill the loop
                except KillerException as e:
                    error_message = errors.format_error(e)
                    self.context.log.log(type="error", content=error_message)
                    raise e # kill the loop
                except Exception as e: # Forward other errors to the LLM, maybe it can fix them
                    error_message = errors.format_error(e)
                    msg_response = self.read_prompt("fw.error.md", error=error_message) # error message template
                    await self.append_message(msg_response, human=True)
                    PrintStyle(font_color="red", padding=True).print(msg_response)
                    self.context.log.log(type="error", content=msg_response)
                    
        finally:
            self.context.streaming_agent = None # unset current streamer

    def read_prompt(self, file:str, **kwargs):
        content = ""
        if self.config.prompts_subdir:
            try:
                content = files.read_file(files.get_abs_path(f"./prompts/{self.config.prompts_subdir}/{file}"), **kwargs)
            except Exception as e:
                pass
        if not content:
            content = files.read_file(files.get_abs_path(f"./prompts/default/{file}"), **kwargs)
        return content
>>>>>>> 83f71b59 (new remote. who dis?)

    def get_data(self, field:str):
        return self.data.get(field, None)

    def set_data(self, field:str, value):
        self.data[field] = value

<<<<<<< HEAD
    def append_message(self, msg: str, human: bool = False):
=======
    async def append_message(self, msg: str, human: bool = False):
>>>>>>> 83f71b59 (new remote. who dis?)
        message_type = "human" if human else "ai"
        if self.history and self.history[-1].type == message_type:
            self.history[-1].content += "\n\n" + msg
        else:
            new_message = HumanMessage(content=msg) if human else AIMessage(content=msg)
            self.history.append(new_message)
<<<<<<< HEAD
            self.cleanup_history(self.config.msgs_keep_max, self.config.msgs_keep_start, self.config.msgs_keep_end)
=======
            await self.cleanup_history(self.config.msgs_keep_max, self.config.msgs_keep_start, self.config.msgs_keep_end)
>>>>>>> 83f71b59 (new remote. who dis?)
        if message_type=="ai":
            self.last_message = msg

    def concat_messages(self,messages):
        return "\n".join([f"{msg.type}: {msg.content}" for msg in messages])

<<<<<<< HEAD
    def send_adhoc_message(self, system: str, msg: str, output_label:str):
=======
    async def send_adhoc_message(self, system: str, msg: str, output_label:str):
>>>>>>> 83f71b59 (new remote. who dis?)
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system),
            HumanMessage(content=msg)])

        chain = prompt | self.config.utility_model
        response = ""
        printer = None
<<<<<<< HEAD

        if output_label:
            PrintStyle(bold=True, font_color="orange", padding=True, background_color="white").print(f"{self.agent_name}: {output_label}:")
            printer = PrintStyle(italic=True, font_color="orange", padding=False)                
=======
        logger = None

        if output_label:
            PrintStyle(bold=True, font_color="orange", padding=True, background_color="white").print(f"{self.agent_name}: {output_label}:")
            printer = PrintStyle(italic=True, font_color="orange", padding=False)
            logger = self.context.log.log(type="adhoc", heading=f"{self.agent_name}: {output_label}:")       
>>>>>>> 83f71b59 (new remote. who dis?)

        formatted_inputs = prompt.format()
        tokens = int(len(formatted_inputs)/4)     
        self.rate_limiter.limit_call_and_input(tokens)
    
<<<<<<< HEAD
        for chunk in chain.stream({}):
=======
        async for chunk in chain.astream({}):
>>>>>>> 83f71b59 (new remote. who dis?)
            if self.handle_intervention(): break # wait for intervention and handle it, if paused

            if isinstance(chunk, str): content = chunk
            elif hasattr(chunk, "content"): content = str(chunk.content)
            else: content = str(chunk)

            if printer: printer.stream(content)
            response+=content
<<<<<<< HEAD
=======
            if logger: logger.update(content=response)
>>>>>>> 83f71b59 (new remote. who dis?)

        self.rate_limiter.set_output_tokens(int(len(response)/4))

        return response
            
    def get_last_message(self):
        if self.history:
            return self.history[-1]

<<<<<<< HEAD
    def replace_middle_messages(self,middle_messages):
        cleanup_prompt = files.read_file("./prompts/fw.msg_cleanup.md")
        summary = self.send_adhoc_message(system=cleanup_prompt,msg=self.concat_messages(middle_messages), output_label="Mid messages cleanup summary")
        new_human_message = HumanMessage(content=summary)
        return [new_human_message]

    def cleanup_history(self, max:int, keep_start:int, keep_end:int):
=======
    async def replace_middle_messages(self,middle_messages):
        cleanup_prompt = self.read_prompt("fw.msg_cleanup.md")
        summary = await self.send_adhoc_message(system=cleanup_prompt,msg=self.concat_messages(middle_messages), output_label="Mid messages cleanup summary")
        new_human_message = HumanMessage(content=summary)
        return [new_human_message]

    async def cleanup_history(self, max:int, keep_start:int, keep_end:int):
>>>>>>> 83f71b59 (new remote. who dis?)
        if len(self.history) <= max:
            return self.history

        first_x = self.history[:keep_start]
        last_y = self.history[-keep_end:]

        # Identify the middle part
        middle_part = self.history[keep_start:-keep_end]

        # Ensure the first message in the middle is "human", if not, move one message back
        if middle_part and middle_part[0].type != "human":
            if len(first_x) > 0:
                middle_part.insert(0, first_x.pop())

        # Ensure the middle part has an odd number of messages
        if len(middle_part) % 2 == 0:
            middle_part = middle_part[:-1]

        # Replace the middle part using the replacement function
<<<<<<< HEAD
        new_middle_part = self.replace_middle_messages(middle_part)
=======
        new_middle_part = await self.replace_middle_messages(middle_part)
>>>>>>> 83f71b59 (new remote. who dis?)

        self.history = first_x + new_middle_part + last_y

        return self.history

<<<<<<< HEAD
    def handle_intervention(self, progress:str="") -> bool:
        while self.paused: time.sleep(0.1) # wait if paused
        if self.intervention_message and not self.intervention_status: # if there is an intervention message, but not yet processed
            if progress.strip(): self.append_message(progress) # append the response generated so far
            user_msg = files.read_file("./prompts/fw.intervention.md", user_message=self.intervention_message) # format the user intervention template
            self.append_message(user_msg,human=True) # append the intervention message
            self.intervention_message = "" # reset the intervention message
            self.intervention_status = True
        return self.intervention_status # return intervention status

    def process_tools(self, msg: str):
=======
    async def handle_intervention(self, progress:str=""):
        while self.context.paused: await asyncio.sleep(0.1) # wait if paused
        if self.intervention_message: # if there is an intervention message, but not yet processed
            msg = self.intervention_message
            self.intervention_message = "" # reset the intervention message
            if progress.strip(): await self.append_message(progress) # append the response generated so far
            user_msg = self.read_prompt("fw.intervention.md", user_message=self.intervention_message) # format the user intervention template
            await self.append_message(user_msg,human=True) # append the intervention message
            raise InterventionException(msg)

    async def process_tools(self, msg: str):
>>>>>>> 83f71b59 (new remote. who dis?)
        # search for tool usage requests in agent message
        tool_request = extract_tools.json_parse_dirty(msg)

        if tool_request is not None:
            tool_name = tool_request.get("tool_name", "")
            tool_args = tool_request.get("tool_args", {})
<<<<<<< HEAD

            tool = self.get_tool(
                        tool_name,
                        tool_args,
                        msg)
                
            if self.handle_intervention(): return # wait if paused and handle intervention message if needed
            tool.before_execution(**tool_args)
            if self.handle_intervention(): return # wait if paused and handle intervention message if needed
            response = tool.execute(**tool_args)
            if self.handle_intervention(): return # wait if paused and handle intervention message if needed
            tool.after_execution(response)
            if self.handle_intervention(): return # wait if paused and handle intervention message if needed
            if response.break_loop: return response.message
        else:
            msg = files.read_file("prompts/fw.msg_misformat.md")
            self.append_message(msg, human=True)
            PrintStyle(font_color="red", padding=True).print(msg)
=======
            tool = self.get_tool(tool_name, tool_args, msg)
                
            await self.handle_intervention() # wait if paused and handle intervention message if needed
            await tool.before_execution(**tool_args)
            await self.handle_intervention() # wait if paused and handle intervention message if needed
            response = await tool.execute(**tool_args)
            await self.handle_intervention() # wait if paused and handle intervention message if needed
            await tool.after_execution(response)
            await self.handle_intervention() # wait if paused and handle intervention message if needed
            if response.break_loop: return response.message
        else:
            msg = self.read_prompt("fw.msg_misformat.md")
            await self.append_message(msg, human=True)
            PrintStyle(font_color="red", padding=True).print(msg)
            self.context.log.log(type="error", content=f"{self.agent_name}: Message misformat:")
>>>>>>> 83f71b59 (new remote. who dis?)


    def get_tool(self, name: str, args: dict, message: str, **kwargs):
        from python.helpers.tool import Tool
        from python.tools.unknown import Unknown
        
        tool_class = Unknown
        if files.exists("python/tools",f"{name}.py"): 
            module = importlib.import_module("python.tools." + name)  # Import the module
            class_list = inspect.getmembers(module, inspect.isclass)  # Get all functions in the module

            for cls in class_list:
                if cls[1] is not Tool and issubclass(cls[1], Tool):
                    tool_class = cls[1]
                    break

        return tool_class(agent=self, name=name, args=args, message=message, **kwargs)

<<<<<<< HEAD
    def fetch_memories(self,reset_skip=False):
=======
    async def fetch_memories(self,reset_skip=False):
>>>>>>> 83f71b59 (new remote. who dis?)
        if self.config.auto_memory_count<=0: return ""
        if reset_skip: self.memory_skip_counter = 0

        if self.memory_skip_counter > 0:
            self.memory_skip_counter-=1
            return ""
        else:
            self.memory_skip_counter = self.config.auto_memory_skip
            from python.tools import memory_tool
            messages = self.concat_messages(self.history)
            memories = memory_tool.search(self,messages)
            input = {
                "conversation_history" : messages,
                "raw_memories": memories
            }
<<<<<<< HEAD
            cleanup_prompt = files.read_file("./prompts/msg.memory_cleanup.md").replace("{", "{{")       
            clean_memories = self.send_adhoc_message(cleanup_prompt,json.dumps(input), output_label="Memory injection")
            return clean_memories

=======
            cleanup_prompt = self.read_prompt("msg.memory_cleanup.md").replace("{", "{{")       
            clean_memories = await self.send_adhoc_message(cleanup_prompt,json.dumps(input), output_label="Memory injection")
            return clean_memories

    def log_from_stream(self, stream: str, logItem: Log.LogItem):
        try:
            if len(stream) < 25: return # no reason to try
            response = DirtyJson.parse_string(stream)
            if isinstance(response, dict): logItem.update(content=stream, kvps=response) #log if result is a dictionary already
        except Exception as e:
            pass

>>>>>>> 83f71b59 (new remote. who dis?)
    def call_extension(self, name: str, **kwargs) -> Any:
        pass