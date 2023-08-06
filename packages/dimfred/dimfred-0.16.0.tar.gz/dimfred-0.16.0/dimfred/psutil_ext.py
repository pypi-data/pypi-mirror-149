import psutil


def find(process_name):
    for p in psutil.process_iter():
        try:
            if process_name == p.name():
                return p
        except:
            pass


setattr(psutil, "find", find)
