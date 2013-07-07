import subprocess


class SubProcessManager(object):
    __PROCESS = None

    @staticmethod
    def get_process():
        return SubProcessManager.__PROCESS

    @staticmethod
    def remove_process():
        SubProcessManager.__PROCESS = None

    @staticmethod
    def set_process(args):
        if SubProcessManager.__PROCESS is None:
            p = subprocess.Popen(args)
            SubProcessManager.__PROCESS = p

    @staticmethod
    def poll_process():
        if SubProcessManager.__PROCESS is None:
            return None
        else:
            return SubProcessManager.__PROCESS.poll()
