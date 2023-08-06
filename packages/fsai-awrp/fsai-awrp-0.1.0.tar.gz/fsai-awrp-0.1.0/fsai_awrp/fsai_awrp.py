import os, time
from threading import Thread


class ArgoWorkflowsReportProgress:
    def __init__(self) -> None:
        # Set the default variables
        self.current_progress = 0
        self.total_progress = 100
        self.save_interval = 2

    def set_current_progress(self, current_progress):
        if self.current_progress <= self.total_progress:
            self.current_progress = current_progress

    def set_total_progress(self, total_progress):
        if self.total_progress <= 1:
            self.total_progress = total_progress

    def set_save_interval(self, save_interval):
        self.save_interval = save_interval

    def get_progress_file_path(self):
        return os.environ.get("ARGO_PROGRESS_FILE", "/tmp/progress.txt")

    def save_file(self):
        while True:
            with open(self.get_progress_file_path(), "w") as f:
                f.write("%s/%s" % (self.current_progress, self.total_progress))
                f.close
            print(self.current_progress, self.total_progress)
            time.sleep(self.save_interval)

    def start_reporting(self):

        # Make the storage directory
        os.makedirs(os.path.dirname(self.get_progress_file_path()), exist_ok=True)

        # Start the file save thread
        t = Thread(target=self.save_file)
        t.start()
