from threading import Thread
from time import perf_counter
from baseHandler import BaseHandler
import numpy as np
import torch
from transformers import (
    AutoTokenizer,
)
from parler_tts import ParlerTTSForConditionalGeneration, ParlerTTSStreamer
import librosa
import logging
from rich.console import Console
from utils.utils import next_power_of_2
from transformers.utils.import_utils import (
    is_flash_attn_2_available,
)

torch._inductor.config.fx_graph_cache = True
# mind about this parameter ! should be >= 2 * number of padded prompt sizes for TTS
torch._dynamo.config.cache_size_limit = 15

logger = logging.getLogger(__name__)

console = Console()


if not is_flash_attn_2_available() and torch.cuda.is_available():
    logger.warn(
        """Parler TTS works best with flash attention 2, but is not installed
        Given that CUDA is available in this system, you can install flash attention 2 with `uv pip install flash-attn --no-build-isolation`"""
    )


class ParlerTTSHandler(BaseHandler):
    def setup(
        self,
        should_listen,
        model_name="ylacombe/parler-tts-mini-jenny-30H",
        device="cuda",
        torch_dtype="float16",
        compile_mode=None,
        gen_kwargs={},
        max_prompt_pad_length=8,
        description=(
            "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. "
            "She speaks very fast."
        ),
        play_steps_s=1,
        blocksize=512,
    ):
        """
        Sets up the text-to-speech model with specified parameters and configurations.
        
        Args:
            should_listen (bool): Flag to determine if the model should listen for input.
            model_name (str): Name of the pre-trained model to use. Defaults to "ylacombe/parler-tts-mini-jenny-30H".
            device (str): Device to run the model on. Defaults to "cuda".
            torch_dtype (str): PyTorch data type to use. Defaults to "float16".
            compile_mode (str or None): Compilation mode for the model. Defaults to None.
            gen_kwargs (dict): Additional keyword arguments for generation. Defaults to an empty dictionary.
            max_prompt_pad_length (int): Maximum padding length for prompts. Defaults to 8.
            description (str): Description of the speaker's voice characteristics. Defaults to a specific description.
            play_steps_s (float): Number of seconds to play for each step. Defaults to 1.
            blocksize (int): Size of the audio block to process. Defaults to 512.
        
        Returns:
            None: This method initializes the object's attributes and sets up the model.
        """
        self.should_listen = should_listen
        self.device = device
        self.torch_dtype = getattr(torch, torch_dtype)
        self.gen_kwargs = gen_kwargs
        self.compile_mode = compile_mode
        self.max_prompt_pad_length = max_prompt_pad_length
        self.description = description

        self.description_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.prompt_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = ParlerTTSForConditionalGeneration.from_pretrained(
            model_name, torch_dtype=self.torch_dtype
        ).to(device)

        framerate = self.model.audio_encoder.config.frame_rate
        self.play_steps = int(framerate * play_steps_s)
        self.blocksize = blocksize

        if self.compile_mode not in (None, "default"):
            logger.warning(
                "Torch compilation modes that captures CUDA graphs are not yet compatible with the STT part. Reverting to 'default'"
            )
            self.compile_mode = "default"

        if self.compile_mode:
            self.model.generation_config.cache_implementation = "static"
            self.model.forward = torch.compile(
                self.model.forward, mode=self.compile_mode, fullgraph=True
            )

        self.warmup()

    def prepare_model_inputs(
        self,
        prompt,
        max_length_prompt=50,
        pad=False,
    ):
        """Prepares model inputs for generating responses based on a given prompt and description.
        
        Args:
            prompt (str): The input prompt to be tokenized and prepared for the model.
            max_length_prompt (int, optional): The maximum length for padding the prompt. Defaults to 50.
            pad (bool, optional): Whether to pad the prompt to max_length_prompt. Defaults to False.
        
        Returns:
            dict: A dictionary containing the prepared inputs for the model, including:
                - input_ids: Tensor of tokenized description input IDs.
                - attention_mask: Tensor of attention mask for the description.
                - prompt_input_ids: Tensor of tokenized prompt input IDs.
                - prompt_attention_mask: Tensor of attention mask for the prompt.
                - Additional generation kwargs from self.gen_kwargs.
        """
        pad_args_prompt = (
            {"padding": "max_length", "max_length": max_length_prompt} if pad else {}
        )

        tokenized_description = self.description_tokenizer(
            self.description, return_tensors="pt"
        )
        input_ids = tokenized_description.input_ids.to(self.device)
        attention_mask = tokenized_description.attention_mask.to(self.device)

        tokenized_prompt = self.prompt_tokenizer(
            prompt, return_tensors="pt", **pad_args_prompt
        )
        prompt_input_ids = tokenized_prompt.input_ids.to(self.device)
        prompt_attention_mask = tokenized_prompt.attention_mask.to(self.device)

        gen_kwargs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "prompt_input_ids": prompt_input_ids,
            "prompt_attention_mask": prompt_attention_mask,
            **self.gen_kwargs,
        }

        return gen_kwargs

    def warmup(self):
        """Warms up the model for improved performance during inference.
        
        This method performs a series of steps to prepare the model for efficient execution,
        especially important for CUDA-based operations. It conducts warm-up runs with varying
        input lengths based on the compilation mode and device type.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return a value but performs warm-up operations.
        """
        logger.info(f"Warming up {self.__class__.__name__}")

        if self.device == "cuda":
            start_event = torch.cuda.Event(enable_timing=True)
            end_event = torch.cuda.Event(enable_timing=True)

        # 2 warmup steps for no compile or compile mode with CUDA graphs capture
        n_steps = 1 if self.compile_mode == "default" else 2

        if self.device == "cuda":
            torch.cuda.synchronize()
            start_event.record()
        if self.compile_mode:
            pad_lengths = [2**i for i in range(2, self.max_prompt_pad_length)]
            for pad_length in pad_lengths[::-1]:
                model_kwargs = self.prepare_model_inputs(
                    "dummy prompt", max_length_prompt=pad_length, pad=True
                )
                for _ in range(n_steps):
                    _ = self.model.generate(**model_kwargs)
                logger.info(f"Warmed up length {pad_length} tokens!")
        else:
            model_kwargs = self.prepare_model_inputs("dummy prompt")
            for _ in range(n_steps):
                _ = self.model.generate(**model_kwargs)

        if self.device == "cuda":
            end_event.record()
            torch.cuda.synchronize()
            logger.info(
                f"{self.__class__.__name__}:  warmed up! time: {start_event.elapsed_time(end_event) * 1e-3:.3f} s"
            )

    def process(self, llm_sentence):
        """Processes a given sentence using a language model and generates audio output.
        
        Args:
            llm_sentence (str): The input sentence to be processed by the language model.
        
        Returns:
            generator: A generator that yields audio chunks as numpy arrays.
        """
        console.print(f"[green]ASSISTANT: {llm_sentence}")
        nb_tokens = len(self.prompt_tokenizer(llm_sentence).input_ids)

        pad_args = {}
        if self.compile_mode:
            # pad to closest upper power of two
            pad_length = next_power_of_2(nb_tokens)
            logger.debug(f"padding to {pad_length}")
            pad_args["pad"] = True
            pad_args["max_length_prompt"] = pad_length

        tts_gen_kwargs = self.prepare_model_inputs(
            llm_sentence,
            **pad_args,
        )

        streamer = ParlerTTSStreamer(
            self.model, device=self.device, play_steps=self.play_steps
        )
        tts_gen_kwargs = {"streamer": streamer, **tts_gen_kwargs}
        torch.manual_seed(0)
        thread = Thread(target=self.model.generate, kwargs=tts_gen_kwargs)
        thread.start()

        for i, audio_chunk in enumerate(streamer):
            global pipeline_start
            if i == 0 and "pipeline_start" in globals():
                logger.info(
                    f"Time to first audio: {perf_counter() - pipeline_start:.3f}"
                )
            audio_chunk = librosa.resample(audio_chunk, orig_sr=44100, target_sr=16000)
            audio_chunk = (audio_chunk * 32768).astype(np.int16)
            for i in range(0, len(audio_chunk), self.blocksize):
                yield np.pad(
                    audio_chunk[i : i + self.blocksize],
                    (0, self.blocksize - len(audio_chunk[i : i + self.blocksize])),
                )

        self.should_listen.set()
