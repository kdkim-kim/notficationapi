# client_gui.py

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QMessageBox
import requests


class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

        self.access_token = None

        self.setWindowTitle("Login Form")

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.on_login_button_click)

        self.search_button = QPushButton("Search User Info")
        self.search_button.clicked.connect(self.on_search_button_click)
        self.search_button.setEnabled(False)

        self.user_info_text = QTextEdit()
        self.user_info_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.user_info_text)

        self.setLayout(layout)

    def on_login_button_click(self):
        username = self.username_input.text()
        password = self.password_input.text()

        url = "http://127.0.0.1:8000/token"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.search_button.setEnabled(True)
            QMessageBox.information(self, "Login Successful", "Successfully logged in!")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Login Failed", f"Failed to login: {str(e)}")
            return

    def on_search_button_click(self):
        if self.access_token:
            url = "http://127.0.0.1:8000/users/me/"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                user_info = response.json()
                self.display_user_info(user_info)
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to retrieve user info: {str(e)}")
                return
        else:
            QMessageBox.warning(self, "Not Logged In", "Please log in first.")

    def display_user_info(self, user_info):
        self.user_info_text.clear()
        self.user_info_text.append(f"Username: {user_info['username']}")
        self.user_info_text.append(f"Email: {user_info.get('email', 'N/A')}")
        self.user_info_text.append(f"Full Name: {user_info.get('full_name', 'N/A')}")
        self.user_info_text.append(f"Disabled: {user_info.get('disabled', 'N/A')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_app = LoginApp()
    login_app.show()

    sys.exit(app.exec())
