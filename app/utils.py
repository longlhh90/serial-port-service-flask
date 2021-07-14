class Collections:
    @staticmethod
    def drop_none(dictionary):
        return {k: v for k, v in dictionary.items() if v is not None}

    @staticmethod
    def drop_falsy(dictionary):
        return {k: v for k, v in dictionary.items() if v}
