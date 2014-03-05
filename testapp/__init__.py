import webob
import webob.dec

class TestApp(object):
    def __init__(self):
        super(TestApp, self).__init__()

    @webob.dec.wsgify
    def __call__(self, request):
        return webob.Response(body='Hello my friend!')


class TestFilter(object):
    def __init__(self, app):
        super(TestFilter, self).__init__()
        self.app = app

    @webob.dec.wsgify
    def __call__(self, request):
        if request.path_info.endswith('silent'):
            return webob.Response(body='Shhhhhh')
        else:
            return self.app(request)


def app_factory(global_config, **local_conf):
    return TestApp()


def filter_factory(global_config, **local_conf):
    return lambda app: TestFilter(app)


testapp = TestApp()
