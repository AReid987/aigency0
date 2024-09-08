<<<<<<< HEAD
from agent import Agent
from python.helpers import files
from python.helpers.print_style import PrintStyle

from agent import Agent
from python.helpers.tool import Tool, Response
from python.helpers import files
from python.helpers.print_style import PrintStyle

class TaskDone(Tool):

    def execute(self,**kwargs):
        self.agent.set_data("timeout", 0)
        return Response(message=self.args["text"], break_loop=True)

    def before_execution(self, **kwargs):
        pass # do not add anything to the history or output
    
    def after_execution(self, response, **kwargs):
=======
from python.helpers.tool import Tool, Response

class TaskDone(Tool):

    async def execute(self,**kwargs):
        self.agent.set_data("timeout", 0)
        return Response(message=self.args["text"], break_loop=True)

    async def before_execution(self, **kwargs):
        self.log = self.agent.context.log.log(type="response", heading=f"{self.agent.agent_name}: Task done:", content=self.args.get("text", ""))
    
    async def after_execution(self, response, **kwargs):
>>>>>>> 83f71b59 (new remote. who dis?)
        pass # do add anything to the history or output