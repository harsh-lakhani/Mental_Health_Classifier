import threading
from pyspark import InheritableThread as Thread

class FlaskThread(Thread):
    def __init__(self, target, args=()):
        super().__init__( target=target, args=args)
        self.target = target
        self.args = args
        self.stop_event = threading.Event()
        self.daemon = True
        self.start()

    def run(self):
        self.target(*self.args)
    def stop(self):        
        self.stop_event.set()
     
    def stop_and_join(self):
        self.stop()
        if self.is_alive():
            self.join()