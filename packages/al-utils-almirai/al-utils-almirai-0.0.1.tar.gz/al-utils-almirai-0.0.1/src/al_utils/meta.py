def merge_meta(cls1: type, cls2: type):
    class MergeMeta(type(cls1), type(cls2)):
        pass

    class Merge(cls1, cls2, metaclass=MergeMeta):
        pass
    return Merge
