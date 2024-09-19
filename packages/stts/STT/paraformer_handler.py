import logging
from time import perf_counter

import numpy as np
import torch
from baseHandler import BaseHandler
from funasr import AutoModel
from rich.console import Console

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

console = Console()


class ParaformerSTTHandler(BaseHandler):
    """
    Handles the Speech To Text generation using a Paraformer model.
    The default for this model is set to Chinese.
    This model was contributed by @wuhongsheng.
    """

    def setup(
        self,
        model_name="paraformer-zh",
        device="cuda",
        gen_kwargs={},
    ):
        """Initializes and sets up the Paraformer model for speech recognition.

        Args:
            model_name (str): The name of the model to use. Defaults to "paraformer-zh".
            device (str): The device to run the model on. Defaults to "cuda".
            gen_kwargs (dict): Additional keyword arguments for model generation. Defaults to an empty dictionary.

        Returns:
            None: This method doesn't return anything, it sets up the model internally.
        """
        print(model_name)
        if len(model_name.split("/")) > 1:
            model_name = model_name.split("/")[-1]
        self.device = device
        self.model = AutoModel(model=model_name, device=device)
        self.warmup()

    def warmup(self):
        """Performs a warmup routine for the model.

        Args:
            self: The instance of the class containing this method.

        Returns:
            None: This method doesn't return anything explicitly.
        """
        logger.info(f"Warming up {self.__class__.__name__}")

        # 2 warmup steps for no compile or compile mode with CUDA graphs capture
        n_steps = 1
        dummy_input = np.array([0] * 512, dtype=np.float32)
        for _ in range(n_steps):
            _ = self.model.generate(dummy_input)[
                0]["text"].strip().replace(" ", "")

    def process(self, spoken_prompt):
        ```
        """Process the spoken prompt using a Paraformer model.
        
        Args:
            spoken_prompt (torch.Tensor): The input tensor representing the spoken prompt.
        
        Returns:
            str: The generated text prediction from the Paraformer model, with spaces removed.
        """
        ```        logger.debug("infering paraformer...")

        global pipeline_start
        pipeline_start = perf_counter()

        pred_text = (
            self.model.generate(spoken_prompt)[
                0]["text"].strip().replace(" ", "")
        )
        torch.mps.empty_cache()

        logger.debug("finished paraformer inference")
        console.print(f"[yellow]USER: {pred_text}")

        yield pred_text
