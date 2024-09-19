import logging

import numpy as np
import torch
from baseHandler import BaseHandler
from rich.console import Console
from utils.utils import int2float
from VAD.vad_iterator import VADIterator

logger = logging.getLogger(__name__)

console = Console()


class VADHandler(BaseHandler):
    """
    Handles voice activity detection. When voice activity is detected, audio will be accumulated until the end of speech is detected and then passed
    to the following part.
    """

    def setup(
        self,
        should_listen,
        thresh=0.3,
        sample_rate=16000,
        min_silence_ms=1000,
        min_speech_ms=500,
        max_speech_ms=float("inf"),
        speech_pad_ms=30,
    ):
        """Sets up the Voice Activity Detection (VAD) system.

        Args:
            should_listen (bool): Flag to determine if the system should listen.
            thresh (float): Threshold for VAD detection. Default is 0.3.
            sample_rate (int): Audio sample rate in Hz. Default is 16000.
            min_silence_ms (int): Minimum duration of silence in milliseconds. Default is 1000.
            min_speech_ms (int): Minimum duration of speech in milliseconds. Default is 500.
            max_speech_ms (float): Maximum duration of speech in milliseconds. Default is infinity.
            speech_pad_ms (int): Padding duration for speech in milliseconds. Default is 30.

        Returns:
            None: This method doesn't return anything, it initializes the VAD system.
        """
        self.should_listen = should_listen
        self.sample_rate = sample_rate
        self.min_silence_ms = min_silence_ms
        self.min_speech_ms = min_speech_ms
        self.max_speech_ms = max_speech_ms
        self.model, _ = torch.hub.load("snakers4/silero-vad", "silero_vad")
        self.iterator = VADIterator(
            self.model,
            threshold=thresh,
            sampling_rate=sample_rate,
            min_silence_duration_ms=min_silence_ms,
            speech_pad_ms=speech_pad_ms,
        )

    def process(self, audio_chunk):
        """Process an audio chunk for voice activity detection.

        Args:
            audio_chunk (bytes): The input audio chunk to be processed.

        Returns:
            numpy.ndarray or None: If valid speech is detected, returns the processed audio array.
            Otherwise, returns None.
        """
        audio_int16 = np.frombuffer(audio_chunk, dtype=np.int16)
        audio_float32 = int2float(audio_int16)
        vad_output = self.iterator(torch.from_numpy(audio_float32))
        if vad_output is not None and len(vad_output) != 0:
            logger.debug("VAD: end of speech detected")
            array = torch.cat(vad_output).cpu().numpy()
            duration_ms = len(array) / self.sample_rate * 1000
            if duration_ms < self.min_speech_ms or duration_ms > self.max_speech_ms:
                logger.debug(
                    f"audio input of duration: {len(array) / self.sample_rate}s, skipping"
                )
            else:
                self.should_listen.clear()
                logger.debug("Stop listening")
                yield array
