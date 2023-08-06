

class HandlerChain:

    @classmethod
    def from_handlers(cls, handlers):
        hc = HandlerChain()
        hc._handlers = handlers
        handler = handlers[0]
        for i in range(1, len(handlers)):
            next_handler = handlers[i]
            handler.set_next(next_handler)
            handler = handlers[i]
        return hc

    def handle(self, request):
        return self._handlers[0].handle(request)
