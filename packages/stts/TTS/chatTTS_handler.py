import logging

import ChatTTS
import librosa
import numpy as np
import torch
from baseHandler import BaseHandler
from rich.console import Console

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

console = Console()


class ChatTTSHandler(BaseHandler):
    def setup(
        self,
        should_listen,
        device="cuda",
        gen_kwargs={},  # Unused
        stream=True,
        chunk_size=512,
    ):
        """
        Sets up the ChatTTS model and initializes necessary parameters for text-to-speech conversion.

        Args:
            should_listen (bool): Determines if the model should listen for input.
            device (str): The device to run the model on. Defaults to "cuda".
            gen_kwargs (dict): Unused parameter for generation kwargs. Defaults to an empty dictionary.
            stream (bool): Whether to stream the audio output. Defaults to True.
            chunk_size (int): The size of audio chunks for processing. Defaults to 512.

        Returns:
            None: This method doesn't return anything, it initializes instance variables.
        """
        self.should_listen = should_listen
        self.device = device
        self.model = ChatTTS.Chat()
        self.model.load(compile=False)  # Doesn't work for me with True
        self.chunk_size = chunk_size
        self.stream = stream
        rnd_spk_emb = self.model.sample_random_speaker()
        self.params_infer_code = ChatTTS.Chat.InferCodeParams(
            spk_emb=rnd_spk_emb,
        )
        self.warmup()

    def warmup(self):
        """Warms up the model by performing an initial inference.

        This method prepares the model for subsequent operations by running a test inference
        on a sample input. It logs the warm-up process using the logger.

        Args:
            self: The instance of the class containing this method.

        Returns:
            None: This method doesn't return anything.
        """
        logger.info(f"Warming up {self.__class__.__name__}")
        _ = self.model.infer("text")

    def process(self, llm_sentence):
        """Processes a sentence using a language model and generates audio output.

        Args:
            llm_sentence str: The input sentence to be processed by the language model.

        Returns:
            generator: A generator that yields audio chunks as numpy arrays.

        """        console.print(f"[green]ASSISTANT: {llm_sentence}")
        if self.device == "mps":
            import time

            start = time.time()
            # Waits for all kernels in all streams on the MPS device to complete.
            torch.mps.synchronize()
            # Frees all memory allocated by the MPS device.
            torch.mps.empty_cache()
            _ = (
                time.time() - start
            )  # Removing this line makes it fail more often. I'm looking into it.

        wavs_gen = self.model.infer(
            llm_sentence, params_infer_code=self.params_infer_code, stream=self.stream
        )

        if self.stream:
            wavs = [np.array([])]
            for gen in wavs_gen:
                if gen[0] is None or len(gen[0]) == 0:
                    self.should_listen.set()
                    return
                audio_chunk = librosa.resample(
                    gen[0], orig_sr=24000, target_sr=16000)
                audio_chunk = (audio_chunk * 32768).astype(np.int16)[0]
                while len(audio_chunk) > self.chunk_size:
                    # 返回前 chunk_size 字节的数据
                    yield audio_chunk[: self.chunk_size]
                    audio_chunk = audio_chunk[self.chunk_size:]  # 移除已返回的数据
                yield np.pad(audio_chunk, (0, self.chunk_size - len(audio_chunk)))
        else:
            wavs = wavs_gen
            if len(wavs[0]) == 0:
                self.should_listen.set()
                return
            audio_chunk = librosa.resample(
                wavs[0], orig_sr=24000, target_sr=16000)
            audio_chunk = (audio_chunk * 32768).astype(np.int16)
            for i in range(0, len(audio_chunk), self.chunk_size):
                yield np.pad(
                    audio_chunk[i: i + self.chunk_size],
                    (0, self.chunk_size -
                     len(audio_chunk[i: i + self.chunk_size])),
                )
        self.should_listen.set()
