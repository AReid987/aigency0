from time import perf_counter
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
)
import torch

from baseHandler import BaseHandler
from rich.console import Console
import logging

logger = logging.getLogger(__name__)
console = Console()


class WhisperSTTHandler(BaseHandler):
    """
    Handles the Speech To Text generation using a Whisper model.
    """

    def setup(
        self,
        model_name="distil-whisper/distil-large-v3",
        device="cuda",
        torch_dtype="float16",
        compile_mode=None,
        gen_kwargs={},
    ):
        """
        Sets up the speech-to-text model and processor for transcription.
        
        Args:
            model_name (str): The name of the pre-trained model to use. Defaults to "distil-whisper/distil-large-v3".
            device (str): The device to run the model on. Defaults to "cuda".
            torch_dtype (str): The PyTorch data type to use for the model. Defaults to "float16".
            compile_mode (str or None): The compilation mode for the model. If None, no compilation is performed. Defaults to None.
            gen_kwargs (dict): Additional keyword arguments for model generation. Defaults to an empty dictionary.
        
        Returns:
            None
        """
        self.device = device
        self.torch_dtype = getattr(torch, torch_dtype)
        self.compile_mode = compile_mode
        self.gen_kwargs = gen_kwargs

        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name,
            torch_dtype=self.torch_dtype,
        ).to(device)

        # compile
        if self.compile_mode:
            self.model.generation_config.cache_implementation = "static"
            self.model.forward = torch.compile(
                self.model.forward, mode=self.compile_mode, fullgraph=True
            )
        self.warmup()

    def prepare_model_inputs(self, spoken_prompt):
        """Prepares input features for the model from a spoken prompt.
        
        Args:
            spoken_prompt (numpy.ndarray): The audio signal of the spoken prompt.
        
        Returns:
            torch.Tensor: The processed input features ready for model inference.
        """
        input_features = self.processor(
            spoken_prompt, sampling_rate=16000, return_tensors="pt"
        ).input_features
        input_features = input_features.to(self.device, dtype=self.torch_dtype)

        return input_features

    def warmup(self):
        """
        Performs a warmup of the model by running inference on dummy input data.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, but it logs the warmup process and timing information.
        """
        logger.info(f"Warming up {self.__class__.__name__}")

        # 2 warmup steps for no compile or compile mode with CUDA graphs capture
        n_steps = 1 if self.compile_mode == "default" else 2
        dummy_input = torch.randn(
            (1, self.model.config.num_mel_bins, 3000),
            dtype=self.torch_dtype,
            device=self.device,
        )
        if self.compile_mode not in (None, "default"):
            # generating more tokens than previously will trigger CUDA graphs capture
            # one should warmup with a number of generated tokens above max tokens targeted for subsequent generation
            # hence, having min_new_tokens < max_new_tokens in the future doesn't make sense
            warmup_gen_kwargs = {
                "min_new_tokens": self.gen_kwargs[
                    "max_new_tokens"
                ],  # Yes, assign max_new_tokens to min_new_tokens
                "max_new_tokens": self.gen_kwargs["max_new_tokens"],
                **self.gen_kwargs,
            }
        else:
            warmup_gen_kwargs = self.gen_kwargs

        if self.device == "cuda":
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)
            torch.cuda.synchronize()
            start_event.record()

        for _ in range(n_steps):
            _ = self.model.generate(dummy_input, **warmup_gen_kwargs)

        if self.device == "cuda":
            end_event.record()
            torch.cuda.synchronize()

            logger.info(
                f"{self.__class__.__name__}:  warmed up! time: {start_event.elapsed_time(end_event) * 1e-3:.3f} s"
            )

    def process(self, spoken_prompt):
        """Processes spoken input and generates transcribed text.
        
        Args:
            spoken_prompt (numpy.ndarray): The audio input as a numpy array.
        
        Returns:
            str: The transcribed text from the spoken input.
        """
        logger.debug("infering whisper...")

        global pipeline_start
        pipeline_start = perf_counter()

        input_features = self.prepare_model_inputs(spoken_prompt)
        pred_ids = self.model.generate(input_features, **self.gen_kwargs)
        pred_text = self.processor.batch_decode(
            pred_ids, skip_special_tokens=True, decode_with_timestamps=False
        )[0]

        logger.debug("finished whisper inference")
        console.print(f"[yellow]USER: {pred_text}")

        yield pred_text
