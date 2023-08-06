from .core import eigenvector_following, conjugate_gradient, l_bfgs, force_minimization


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def add(self, key, builder):
        self._builders[key] = builder

    def __call__(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


class SmartObjectFactory(ObjectFactory):

    def __call__(self, key, *args, **kwargs):
        # Filter kwargs by key and remove key from argument
        # We follow the convention that arguments passed to a function will be prefixed by key followed by an underscore
        filter_kwargs = {}
        for arg in kwargs:
            if arg.startswith(key):
                strip_arg = arg[len(key) + 1:]
                filter_kwargs[strip_arg] = kwargs[arg]

        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(*args, **filter_kwargs)


optimize = SmartObjectFactory()
optimize.add('ef', eigenvector_following)
optimize.add('cg', conjugate_gradient)
optimize.add('lbfgs', l_bfgs)
optimize.add('wmin', force_minimization)
