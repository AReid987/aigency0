import threading
import sounddevice as sd
import numpy as np

import time
import logging

logger = logging.getLogger(__name__)


class LocalAudioStreamer:
    def __init__(
        self,
        input_queue,
        output_queue,
        list_play_chunk_size=512,
    ):
        """Initialize the object with input and output queues and chunk size for list play.
        
        Args:
            input_queue (Queue): The queue for receiving input data.
            output_queue (Queue): The queue for sending output data.
            list_play_chunk_size (int, optional): The chunk size for list play operations. Defaults to 512.
        
        Returns:
            """Callback function for audio stream processing.
            
            Args:
                indata (numpy.ndarray): Input audio data.
                outdata (numpy.ndarray): Output audio data buffer to be filled.
                frames (int): Number of frames in the buffer.
                time (CData): Stream time information.
                status (CallbackFlags): Status flags indicating stream state.
            
            Returns:
                None: This function modifies outdata in-place and doesn't return anything.
            """            None: This method initializes the object and doesn't return anything.
        """
        self.list_play_chunk_size = list_play_chunk_size

        self.stop_event = threading.Event()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        """Runs the audio stream processing loop.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything explicitly.
        """
        def callback(indata, outdata, frames, time, status):
            if self.output_queue.empty():
                self.input_queue.put(indata.copy())
                outdata[:] = 0 * outdata
            else:
                outdata[:] = self.output_queue.get()[:, np.newaxis]

        logger.debug("Available devices:")
        logger.debug(sd.query_devices())
        with sd.Stream(
            samplerate=16000,
            dtype="int16",
            channels=1,
            callback=callback,
            blocksize=self.list_play_chunk_size,
        ):
            logger.info("Starting local audio stream")
            while not self.stop_event.is_set():
                time.sleep(0.001)
            print("Stopping recording")
