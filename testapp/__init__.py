import routes
import webob
import webob.dec
import webob.exc

route_map = routes.Mapper()
controller = 'number'
route_map.connect('1', '/1', controller=controller, action='one',
                  conditions={'method':['GET']})
route_map.connect('2', '/2', controller=controller, action='two',
                  conditions={'method':['GET']})


class Number(object):
    def one(self, request):
        return webob.Response(body='One!')

    def two(self, request):
        return webob.Response(body='Two!')


class TestApp(object):
    def __init__(self):
        super(TestApp, self).__init__()

    @webob.dec.wsgify
    def __call__(self, request):
        match = route_map.match(environ=request.environ,
                                url=request.path_info)
        if match:
            controller_name = match['controller']
            action_name = match['action']
            if controller_name == 'number':
                controller = Number()
                return getattr(controller, action_name)(request)

        return webob.exc.HTTPNotFound()


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
