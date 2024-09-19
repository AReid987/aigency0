import socket
from rich.console import Console
import logging

logger = logging.getLogger(__name__)

console = Console()


class SocketSender:
    """
    Handles sending generated audio packets to the clients.
    """

    def __init__(self, stop_event, queue_in, host="0.0.0.0", port=12346):
        """Initialize a new instance of the class.
        
        Args:
            stop_event (threading.Event): An event to signal when to stop the process.
            queue_in (queue.Queue): A queue for incoming data.
            host (str, optional): The host address to bind to. Defaults to "0.0.0.0".
            port (int, optional): The port number to listen on. Defaults to 12346.
        
        Returns:
            None: This method initializes the object and doesn't return anything.
        """
        self.stop_event = stop_event
        self.queue_in = queue_in
        self.host = host
        self.port = port

    def run(self):
        """Runs the sender process to transmit audio chunks over a socket connection.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logger.info("Sender waiting to be connected...")
        self.conn, _ = self.socket.accept()
        logger.info("sender connected")

        while not self.stop_event.is_set():
            audio_chunk = self.queue_in.get()
            self.conn.sendall(audio_chunk)
            if isinstance(audio_chunk, bytes) and audio_chunk == b"END":
                break
        self.conn.close()
        logger.info("Sender closed")
