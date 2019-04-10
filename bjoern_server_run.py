from app import app
import bjoern, os
import signal

# import sys
# import os
# import inspect
#
# class ReloadApplicationMiddleware(object):
#     def __init__(self, import_func):
#         self.import_func = import_func
#         self.app = import_func()
#         self.files = self.get_module_mtimes()
#
#     def get_module_mtimes(self):
#         files = {}
#         for module in sys.modules.values():
#             try:
#                 file = inspect.getsourcefile(module)
#                 files[file] = os.stat(file).st_mtime
#             except TypeError:
#                 continue
#         return files
#
#     def shall_reload(self):
#         for file, mtime in self.get_module_mtimes().items():
#             if not file in self.files or self.files[file] < mtime:
#                 self.files = self.get_module_mtimes()
#                 return True
#         return False
#
#     def __call__(self, *args, **kwargs):
#         if self.shall_reload():
#             print('Reloading...')
#             self.app = self.import_func()
#         return self.app(*args, **kwargs)
#
# def import_app():
#    sys.modules.pop('app', None)
#    import app
#    return app.app

NUM_WORKERS = 3
worker_pids = []

bjoern.listen(app, "localhost", 5000)
for _ in range(NUM_WORKERS):
    pid = os.fork()
    if pid > 0:
        worker_pids.append(pid)
    elif pid == 0:
        try:
            bjoern.run()
        except KeyboardInterrupt:
            pass
        exit()

try:
    for _ in range(NUM_WORKERS):
        os.wait()
except KeyboardInterrupt:
    for pid in worker_pids:
        os.kill(pid, signal.SIGINT)

# bjoern.run(app, '0.0.0.0', 5000)
