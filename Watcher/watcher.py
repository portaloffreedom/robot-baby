import time

from watchdog.observers import Observer
from watchdog.tricks import ShellCommandTrick

class Watchdog:

    SLEEP_TIME = 5

    def __init__(self, __cmd_prefix="", __cmd_suffix="", __path='.'):
        """
        Constructor for watchdog mechanism. Given command is executed as
        terminal command based on combination of altered file and given
        command as constructor parameter.

        Args:
            __cmd_prefix: first part of command that is executed. Eg. 'ls -la'
            __cmd_suffix: second part of command that goes after file that
            is monitored. May be omitted with ''.
            __path: path to directory that is being monitored
        """
        self.__cmd = __cmd_prefix + ' ${watch_src_path} ' + __cmd_suffix
        self.__path = __path
        self.__event_handler = ShellCommandTrick(shell_command=self.__cmd,
                                                 patterns='*',
                                                 ignore_patterns='',
                                                 ignore_directories=True,
                                                 wait_for_process=False,
                                                 drop_during_process=False)

        self.__observer = Observer()
        self.__observer.schedule(self.__event_handler, self.__path, recursive=False)

    def run(self):
        """
        Synchronous run
        """
        self.__observer.start()
        try:
            while True:
                time.sleep(self.SLEEP_TIME)
        except KeyboardInterrupt:
            self.__observer.stop()
        self.__observer.join()

    def start(self):
        """
        Asynchronous run
        """
        self.__observer.start()

    def join(self):
        self.__observer.join()

    def stop(self):
        self.__observer.stop()

# Usage example
if __name__ == "__main__":
    wdog = Watchdog(
            './robogen-file-viewer',
            'conf.txt',
            '/tmp')
    wdog.run()
