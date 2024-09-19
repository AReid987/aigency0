from melo.api import TTS
import logging
from baseHandler import BaseHandler
import librosa
import numpy as np
from rich.console import Console
import torch

logger = logging.getLogger(__name__)

console = Console()


class MeloTTSHandler(BaseHandler):
    def setup(
        self,
        should_listen,
        device="mps",
        language="EN_NEWEST",
        speaker_to_id="EN-Newest",
        gen_kwargs={},  # Unused
        blocksize=512,
    ):
        """
        Sets up the text-to-speech model with specified parameters.
        
        Args:
            should_listen (bool): Flag to indicate if the model should listen for input.
            device (str): The device to run the model on. Default is "mps".
            language (str): The language model to use. Default is "EN_NEWEST".
            speaker_to_id (str): The speaker ID to use. Default is "EN-Newest".
            gen_kwargs (dict): Unused parameter for generation kwargs. Default is an empty dict.
            blocksize (int): The block size for processing. Default is 512.
        
        Returns:
            None: This method doesn't return anything, it sets up instance variables.
        """
        self.should_listen = should_listen
        self.device = device
        self.model = TTS(language=language, device=device)
        self.speaker_id = self.model.hps.data.spk2id[speaker_to_id]
        self.blocksize = blocksize
        self.warmup()

    def warmup(self):
        """
        Warms up the text-to-speech model by performing a sample conversion.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything explicitly.
        """
        logger.info(f"Warming up {self.__class__.__name__}")
        _ = self.model.tts_to_file("text", self.speaker_id, quiet=True)

    def process(self, llm_sentence):
        """Processes a sentence using a text-to-speech model and yields audio chunks.
        
        Args:
            llm_sentence (str): The sentence to be converted to speech.
        
        Returns:
            Generator[np.ndarray]: A generator yielding audio chunks as numpy arrays.
        """
        console.print(f"[green]ASSISTANT: {llm_sentence}")
        if self.device == "mps":
            import time

            start = time.time()
            torch.mps.synchronize()  # Waits for all kernels in all streams on the MPS device to complete.
            torch.mps.empty_cache()  # Frees all memory allocated by the MPS device.
            _ = (
                time.time() - start
            )  # Removing this line makes it fail more often. I'm looking into it.

        audio_chunk = self.model.tts_to_file(llm_sentence, self.speaker_id, quiet=True)
        if len(audio_chunk) == 0:
            self.should_listen.set()
            return
        audio_chunk = librosa.resample(audio_chunk, orig_sr=44100, target_sr=16000)
        audio_chunk = (audio_chunk * 32768).astype(np.int16)
        for i in range(0, len(audio_chunk), self.blocksize):
            yield np.pad(
                audio_chunk[i : i + self.blocksize],
                (0, self.blocksize - len(audio_chunk[i : i + self.blocksize])),
            )

        self.should_listen.set()
