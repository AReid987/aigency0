from agent import Agent
from python.helpers import files
from python.helpers.print_style import PrintStyle
from python.helpers.tool import Response, Tool

<< << << < HEAD


class Delegation(Tool):

    def execute(self, message="", reset="", **kwargs):
        # create subordinate agent using the data object on this agent and set superior agent to his data object
        if self.agent.get_data("subordinate") is None or str(reset).lower().strip() == "true":
            subordinate = Agent(self.agent.number+1, self.agent.config)
            subordinate.set_data("superior", self.agent)
            self.agent.set_data("subordinate", subordinate)
        # run subordinate agent message loop
        return Response(message=self.agent.get_data("subordinate").message_loop(message), break_loop=False)


== == == =


class Delegation(Tool):

    async def execute(self, message="", reset="", **kwargs):
        # create subordinate agent using the data object on this agent and set superior agent to his data object
        if self.agent.get_data("subordinate") is None or str(reset).lower().strip() == "true":
            subordinate = Agent(self.agent.number+1,
                                self.agent.config, self.agent.context)
            subordinate.set_data("superior", self.agent)
            self.agent.set_data("subordinate", subordinate)
        # run subordinate agent message loop
        return Response(message=await self.agent.get_data("subordinate").message_loop(message), break_loop=False)


>>>>>> > 83f71b59(new remote. who dis?)
