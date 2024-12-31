from datetime import datetime, timedelta


class TimeIt:
    def __init__(self, description="Unnamed timer"):
        self.runtime = timedelta()
        self.descr = description

    def __call__(self, thunk):
        s = datetime.now()
        o = thunk()
        e = datetime.now()
        self.runtime += e - s
        return o

    def print_report(self):
        print(f"{self.descr:15}: {self.runtime}")
