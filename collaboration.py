class Collaboration:
    def __init__(self):
        self.shared_reports = []

    def share_report(self, report):
        self.shared_reports.append(report)
        return "Report shared successfully."

    def get_shared_reports(self):
        return self.shared_reports
