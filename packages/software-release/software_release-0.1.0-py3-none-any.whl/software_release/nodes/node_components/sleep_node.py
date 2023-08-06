from time import sleep
from software_release.nodes.node import Node


@Node.register_as_subclass('sleep')
class ActiveBranchCheckNode(Node):
    
    def __init__(self, sleep_seconds):
        self.sleep_seconds = float(sleep_seconds)


    def handle(self, request):
        sleep(self.sleep_seconds)
        return super().handle(request)
