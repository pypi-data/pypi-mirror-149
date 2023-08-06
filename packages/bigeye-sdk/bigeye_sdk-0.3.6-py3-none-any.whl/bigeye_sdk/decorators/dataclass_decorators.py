import inspect


def add_from_dict(cls):
    def from_dict(env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })

    cls.from_dict = from_dict
    return cls
