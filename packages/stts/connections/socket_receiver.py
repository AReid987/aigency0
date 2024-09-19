import logging
import socket

from rich.console import Console

logger = logging.getLogger(__name__)

console = Console()


class SocketReceiver:
    """
    Handles reception of the audio packets from the client.
    """

    def __init__(
        self,
        stop_event,
        queue_out,
        should_listen,
        host="0.0.0.0",
        port=12345,
        chunk_size=1024,
    ):
        """Initialize a new instance of the class.

        Args:
            stop_event (Event): An event to signal when to stop the process.
            queue_out (Queue): A queue for output communication.
            should_listen (bool): A flag indicating whether the instance should listen for incoming connections.
            host (str, optional): The host address to bind to. Defaults to "0.0.0.0".
            port (int, optional): The port number to listen on. Defaults to 12345.
            chunk_size (int, optional): The size of data chunks to process. Defaults to 1024.

        Returns:
            None: This method initializes the object and doesn't return anything.
        """
        self.stop_event = stop_event
        self.queue_out = queue_out
        self.should_listen = should_listen
        self.chunk_size = chunk_size
        self.host = host
        self.port = port

    def receive_full_chunk(self, conn, chunk_size):
        """Receives a full chunk of data from a connection.

        Args:
            conn (socket.socket): The connection socket to receive data from.
            chunk_size (int): The expected size of the chunk to receive.

        Returns:
            bytes or None: The received data as bytes if successful, or None if the connection closed before receiving the full chunk.
        """
        data = b""
        """
        Runs the receiver component to listen for incoming audio data.
        
        This method sets up a socket connection, listens for incoming connections, and continuously receives audio chunks until stopped. The received audio chunks are then placed in an output queue.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, but it modifies the instance state and puts data into the output queue.
        """
        while len(data) < chunk_size:
            packet = conn.recv(chunk_size - len(data))
            if not packet:
                # connection closed
                return None
            data += packet
        return data

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logger.info("Receiver waiting to be connected...")
        self.conn, _ = self.socket.accept()
        logger.info("receiver connected")

        self.should_listen.set()
        while not self.stop_event.is_set():
            audio_chunk = self.receive_full_chunk(self.conn, self.chunk_size)
            if audio_chunk is None:
                # connection closed
                self.queue_out.put(b"END")
                break
            if self.should_listen.is_set():
                self.queue_out.put(audio_chunk)
        self.conn.close()
        logger.info("Receiver closed")
