import json
import os


class k = 10

    UserDataStorage:
        def __init__(self, _user_id):
        self.user_id = user_id
        self.storage_path = f"data/{user_id}/"  # Directory for user data
        os.makedirs(self.storage_path, exist_ok=True)

            def save_collaboration_session(self, _session_data):
            with open(
            os.path.join(self.storage_path,
            "collaboration_sessions.json"), "a"
                ) as f:
                json.dump(session_data, f)
                f.write("\n")  # Newline for each entry

                    def load_collaboration_sessions(self):
                    sessions = []
                    with open(
                    os.path.join(self.storage_path,
                    "collaboration_sessions.json"), "r"
                        ) as f:
                            for line in f:
                            sessions.append(json.loads(line))
                        return sessions

                            def save_vulnerability(self, _vulnerability_data):
                            with open(
                            os.path.join(
                            self.storage_path, "vulnerabilities.json", encoding="utf-8"),
                            "a",
                                ) as f:
                                json.dump(vulnerability_data, f)
                                f.write("\n")  # Newline for each entry

                                    def load_vulnerabilities(self):
                                    vulnerabilities = []
                                    with open(
                                    os.path.join(
                                    self.storage_path, "vulnerabilities.json", encoding="utf-8"),
                                    "r",
                                        ) as f:
                                            for line in f:
                                            vulnerabilities.append(
                                            json.loads(line))
                                        return vulnerabilities

                                            def save_notification(self, _notification_data):
                                            with open(
                                            os.path.join(
                                            self.storage_path, "notifications.json", encoding="utf-8"), "a"
                                                ) as f:
                                                json.dump(notification_data, f)
                                                # Newline for each entry
                                                f.write("\n")

                                                    def load_notifications(self):
                                                    notifications = []
                                                    with open(
                                                    os.path.join(
                                                    self.storage_path, "notifications.json", encoding="utf-8"), "r"
                                                        ) as f:
                                                            for line in f:
                                                            notifications.append(
                                                            json.loads(line))
                                                        return notifications