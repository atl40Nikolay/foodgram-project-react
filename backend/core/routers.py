from rest_framework.routers import SimpleRouter


class StandartRouter(SimpleRouter):
    def __init__(self, trailing_slash='/?'):
        super(StandartRouter, self).__init__()
        self.trailing_slash = trailing_slash
