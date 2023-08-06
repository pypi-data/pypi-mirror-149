class DataMessageProcessor:

    def __init__(self, listen_to_stream):
        self.listen_to_stream = listen_to_stream

    def get_listen_to_stream(self):
        return self.listen_to_stream

    def process_message(self, message):
        pass
