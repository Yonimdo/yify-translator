# Create your views here.
from functools import wraps

from dauditlog.models import Log, Audit


def auditit(tag_name):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(log, *args, **kwargs):
            au = Audit()
            au.request = kwargs if kwargs else args
            au.func_name = func.__name__
            au.note = tag_name
            if log:
                au.log = log
                args = (log, *args)
            try:
                result = func(*args, **kwargs)
                au.response = result
                au.passed = True
            except Exception as e:
                au.error_message = e
                result = au
            au.save()
            return result

        return func_wrapper

    return tags_decorator


def logit(tag_name):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(request, *args, **kwargs):
            lg = Log()
            lg.request = request.build_absolute_uri()
            lg.note = tag_name
            lg.request_body = {"body": request.body, "POST": request.POST}
            if request.user and request.user.is_authenticated:
                lg.user = request.user
            lg.save()
            kwargs['log'] = lg
            result = func(request, *args, **kwargs)
            try:
                assert result.status_code == 200
                # try this ^^
                lg.response = result.content
                lg.passed = True
            except Exception as e:
                # N
                lg.error_message = e
            lg.save()
            return result

        return func_wrapper

    return tags_decorator
