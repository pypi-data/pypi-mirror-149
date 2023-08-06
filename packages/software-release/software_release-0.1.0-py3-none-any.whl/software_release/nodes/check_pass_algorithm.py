import attr

from .algorithm import Strategy, Context


@attr.s
class PassCheckContext(Context):

    positional_arguments = attr.ib()
    keyword_Arguments = attr.ib()

    def do(self):
        return self._strategy.do_algorithm(
            *self.positional_arguments,
            **self.keyword_Arguments
        )



@attr.s
class PassCheckAlgorithm(Strategy):
    checker = attr.ib()

    def do_algorithm(self, *args, **kwargs):
        return self.checker(*args, **kwargs)



