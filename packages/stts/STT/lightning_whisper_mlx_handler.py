import logging
from time import perf_counter
from baseHandler import BaseHandler
from lightning_whisper_mlx import LightningWhisperMLX
import numpy as np
from rich.console import Console
import torch

logger = logging.getLogger(__name__)

console = Console()


class LightningWhisperSTTHandler(BaseHandler):
    """
    Handles the Speech To Text generation using a Whisper model.
    """

    def setup(
        self,
        model_name="distil-large-v3",
        device="cuda",
        torch_dtype="float16",
        compile_mode=None,
        gen_kwargs={},
    ):
        if len(model_name.split("/")) > 1:
            model_name = model_name.split("/")[-1]
        self.device = device
        self.model = LightningWhisperMLX(model=model_name, batch_size=6, quant=None)
        self.warmup()

    def warmup(self):
        """
        Performs a warmup routine for the transcription model.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything explicitly.
        """        logger.info(f"Warming up {self.__class__.__name__}")

        # 2 warmup steps for no compile or compile mode with CUDA graphs capture
        n_steps = 1
        dummy_input = np.array([0] * 512)

        for _ in range(n_steps):
            _ = self.model.transcribe(dummy_input)["text"].strip()

    def process(self, spoken_prompt):
        """Processes spoken input and transcribes it to text using a whisper model.
        
        Args:
            spoken_prompt (str): The audio input to be transcribed.
        
        Returns:
            str: The transcribed text from the spoken input.
        """
        logger.debug("infering whisper...")

        global pipeline_start
        pipeline_start = perf_counter()

        pred_text = self.model.transcribe(spoken_prompt)["text"].strip()
        torch.mps.empty_cache()

        logger.debug("finished whisper inference")
        console.print(f"[yellow]USER: {pred_text}")

        yield pred_text
