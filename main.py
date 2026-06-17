import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QTextEdit, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt


# =========================
# System Layer
# =========================
class SystemctlService:

    @staticmethod
    def run(cmd):
        """安全执行 systemctl"""
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    @staticmethod
    def stop(service):
        return SystemctlService.run(["systemctl", "stop", service])

    @staticmethod
    def start(service):
        return SystemctlService.run(["systemctl", "start", service])

    @staticmethod
    def restart(service):
        return SystemctlService.run(["systemctl", "restart", service])

    @staticmethod
    def status(service):
        return SystemctlService.run(["systemctl", "is-active", service])


# =========================
# UI Component
# =========================
class ServiceCard(QFrame):

    def __init__(self, service_name, logger):
        super().__init__()

        self.service_name = service_name
        self.logger = logger

        self.setFrameShape(QFrame.Box)

        self.label = QLabel(f"{service_name}")
        self.status_label = QLabel("UNKNOWN")

        self.btn_start = QPushButton("Start")
        self.btn_stop = QPushButton("Stop")
        self.btn_restart = QPushButton("Restart")

        self.btn_start.clicked.connect(self.start_service)
        self.btn_stop.clicked.connect(self.stop_service)
        self.btn_restart.clicked.connect(self.restart_service)

        layout = QVBoxLayout()

        top = QHBoxLayout()
        top.addWidget(self.label)
        top.addWidget(self.status_label)

        btns = QHBoxLayout()
        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_stop)
        btns.addWidget(self.btn_restart)

        layout.addLayout(top)
        layout.addLayout(btns)

        self.setLayout(layout)

        self.refresh_status()

    def log(self, msg):
        self.logger.append(msg)

    def set_status(self, running):
        if running:
            self.status_label.setText("🟢 running")
        else:
            self.status_label.setText("🔴 stopped")

    def refresh_status(self):
        ok, out = SystemctlService.status(self.service_name)
        self.set_status("active" in out)
        self.log(f"[status] {self.service_name}: {out.strip()}")

    def start_service(self):
        ok, out = SystemctlService.start(self.service_name)
        self.log(f"[start] {self.service_name}: {out}")
        self.refresh_status()

    def stop_service(self):
        ok, out = SystemctlService.stop(self.service_name)
        self.log(f"[stop] {self.service_name}: {out}")
        self.refresh_status()

    def restart_service(self):
        ok, out = SystemctlService.restart(self.service_name)
        self.log(f"[restart] {self.service_name}: {out}")
        self.refresh_status()


# =========================
# Main Window
# =========================
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Systemd Control Panel")
        self.resize(700, 500)

        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # 服务列表（可以扩展）
        self.services = [
            "hdnginx"
        ]

        for s in self.services:
            card = ServiceCard(s, self.log)
            layout.addWidget(card)

        layout.addWidget(QLabel("Logs:"))
        layout.addWidget(self.log)

        self.setLayout(layout)


# =========================
# Entry
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())