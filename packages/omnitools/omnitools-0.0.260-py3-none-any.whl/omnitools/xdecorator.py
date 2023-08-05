def overloaded(*router):
    def dec(_func):
        def wrapper(*args, **kwargs):
            self = None
            args = list(args)
            if args:
                qualname = args[0].__qualname__ if hasattr(args[0], "__qualname__") else args[0].__class__.__qualname__
                if qualname == _func.__qualname__.split(".")[0]:
                    self = args.pop(0)
            func = None
            sig = []
            for route in router:
                condition = route[1]
                exist = False
                found = [False]
                __func = None
                try:
                    t = kwargs[condition.kwargs_k]
                    exist = True
                    if callable(condition.condition) and condition.condition(t):
                        __func = route[0]
                        found[0] = True
                except:
                    pass
                if not found[0]:
                    try:
                        t = args[condition.args_i]
                        exist = True
                        if callable(condition.condition) and condition.condition(t):
                            __func = route[0]
                            found[0] = True
                    except:
                        pass
                sig = args+list(kwargs.values())
                if condition.types:
                    found.append(False)
                    if len(sig) == len(condition.types):
                        match_type = all(isinstance(_, __) for _, __ in zip(sig, condition.types))
                        if match_type:
                            __func = route[0]
                            found[1] = True
                # print(__func,found,args,kwargs,len(sig),len(condition.types),callable(condition.condition) and condition.condition(args[condition.args_i]))
                if len(found) == 1 and found[0]:
                    func = __func
                    break
                elif len(found) == 2 and all(found):
                    func = __func
                    break
                elif len(found) == 2 and found[1] and exist:
                    func = __func
                    break
            args.insert(0, self)
            # print(args, kwargs)
            if not func:
                raise LookupError("cannot find appropriate handler for method {} with signature {}".format(
                    _func.__qualname__,
                    [type(_).__name__ for _ in sig]
                ))
            return func(*args, **kwargs)
        return wrapper
    return dec


class overload_condition:
    def __init__(self, *types, args_i=-1, kwargs_k=None, condition=None):
        self.types = types or []
        self.args_i = args_i
        self.kwargs_k = kwargs_k
        self.condition = condition


