import threading


class ThreadManager:
    """
    Manages multiple threads used to execute given handler tasks.
    """

    def __init__(self, handlers):
        """Initialize the ThreadManager with a list of handlers.

        Args:
            handlers (list): A list of handler objects to be managed by the ThreadManager.

        Returns:
            None: This method doesn't return anything.
        """        self.handlers = handlers
        self.threads = []

    """Stops all handlers and joins their associated threads.
    
    Args:
        self: The instance of the class containing this method.
    
    Returns:
        None: This method doesn't return anything.
    """

    def start(self):
        """
        Starts the execution of all registered handlers in separate threads.

        Args:
            self: The instance of the class containing this method.

        Returns:
            None: This method doesn't return anything.
        """
        for handler in self.handlers:
            thread = threading.Thread(target=handler.run)
            self.threads.append(thread)
            thread.start()

    def stop(self):
        for handler in self.handlers:
            handler.stop_event.set()
        for thread in self.threads:
            thread.join()
