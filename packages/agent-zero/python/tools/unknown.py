from python.helpers.tool import Tool, Response
<<<<<<< HEAD
from python.helpers import files

class Unknown(Tool):
    def execute(self, **kwargs):
        return Response(
                message=files.read_file("prompts/fw.tool_not_found.md",
                                        tool_name=self.name,
                                        tools_prompt=files.read_file("prompts/agent.tools.md")), 
=======

class Unknown(Tool):
    async def execute(self, **kwargs):
        return Response(
                message=self.agent.read_prompt("fw.tool_not_found.md",
                                        tool_name=self.name,
                                        tools_prompt=self.agent.read_prompt("agent.tools.md")), 
>>>>>>> 83f71b59 (new remote. who dis?)
                break_loop=False)

