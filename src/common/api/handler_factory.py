from injector import Injector


def handler_factory(injector: Injector):
    def factory(handler_cls):
        return injector.get(handler_cls)
    return factory
