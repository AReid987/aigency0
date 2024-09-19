import concurrent.futures
import os

from agent import Agent
from python.helpers import duckduckgo_search, files, perplexity_search
from python.helpers.errors import handle_error
from python.helpers.print_style import PrintStyle
from python.helpers.tool import Response, Tool

from . import memory_tool, online_knowledge_tool

<< << << < HEAD


class Knowledge(Tool):
    def execute(self, question="", **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Schedule the two functions to be run in parallel

            # perplexity search, if API provided
== == == =


class Knowledge(Tool):
    async def execute(self, question="", **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Schedule the two functions to be run in parallel

            # perplexity search, if API key provided
>>>>>> > 83f71b59(new remote. who dis?)
            if os.getenv("API_KEY_PERPLEXITY"):
                perplexity = executor.submit(
                    perplexity_search.perplexity_search, question)
            else:
                PrintStyle.hint(
                    "No API key provided for Perplexity. Skipping Perplexity search.")
<< << << < HEAD
== == == =
                self.agent.context.log.log(
                    type="hint", content="No API key provided for Perplexity. Skipping Perplexity search.")
>>>>>> > 83f71b59(new remote. who dis?)
                perplexity = None

            # duckduckgo search
            duckduckgo = executor.submit(duckduckgo_search.search, question)

            # memory search
            future_memory = executor.submit(memory_tool.search, self.agent, question)

            # Wait for both functions to complete
<<<<<<< HEAD
            perplexity_result = (perplexity.result() if perplexity else "") or ""
            duckduckgo_result = duckduckgo.result()
            memory_result = future_memory.result()

        msg = files.read_file("prompts/tool.knowledge.response.md", 
                              online_sources = perplexity_result + "\n\n" + str(duckduckgo_result),
=======
            try:
                perplexity_result = (perplexity.result() if perplexity else "") or ""
            except Exception as e:
                handle_error(e)
                perplexity_result = "Perplexity search failed: " + str(e)

            try:
                duckduckgo_result = duckduckgo.result()
            except Exception as e:
                handle_error(e)
                duckduckgo_result = "DuckDuckGo search failed: " + str(e)

            try:
                memory_result = future_memory.result()
            except Exception as e:
                handle_error(e)
                memory_result = "Memory search failed: " + str(e)

        msg = self.agent.read_prompt("tool.knowledge.response.md", 
                              online_sources = ((perplexity_result + "\n\n") if perplexity else "") + str(duckduckgo_result),
>>>>>>> 83f71b59 (new remote. who dis?)
                              memory = memory_result )

        if self.agent.handle_intervention(msg): pass # wait for intervention and handle it, if paused

<<<<<<< HEAD
        return Response(message=msg, break_loop=False)
=======
        return Response(message=msg, break_loop=False)
>>>>>>> 83f71b59 (new remote. who dis?)
