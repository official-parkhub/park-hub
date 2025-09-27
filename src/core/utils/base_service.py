from app.core.utils.request_context import RequestContext, RequestContextUser


class BaseService(RequestContextUser):
    def __init__(self, rc: RequestContext):
        super().__init__(rc)
