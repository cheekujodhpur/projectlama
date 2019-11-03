class Players:
    def __init__(self, n_players):
        self.n = n_players

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __str__(self):
        return f"I am the {self.n}Players class"
