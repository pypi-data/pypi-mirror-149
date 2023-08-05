# proctitle Dynamic Process Names

Simple context manager so that tasks can be reflected in the process names of Celery workers.


For instance:

    from proctitle import *
        with ProcTitle("intense task"):
        do_something_intense()


Can also be used as a function decorator:

    from proctitle import *
    import time

    @ProcTitle("delay")
    def g(n):
        time.sleep(n)

    g(10)   # during this time, the proc title is "python - delay"

    @ProcTitle("sleeping", replace=True)
    def f(n):
        time.sleep(n)

    f(10)   # during this time, the proc title is just "sleeping" 

