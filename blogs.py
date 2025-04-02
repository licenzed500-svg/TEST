import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QWidget, QComboBox, QLineEdit, QDialog, QFormLayout
)


class TokenDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Управление токенами")
        self.setGeometry(150, 150, 300, 400)

        layout = QFormLayout()

        self.telegraphTokenField = QLineEdit()
        self.writeAsTokenField = QLineEdit()
        self.mediumTokenField = QLineEdit()

        self.getTelegraphTokenButton = QPushButton("Получить токен Telegraph")
        self.getTelegraphTokenButton.clicked.connect(self.getTelegraphToken)

        self.getWriteAsTokenButton = QPushButton("Получить токен Write.as")
        self.getWriteAsTokenButton.clicked.connect(self.getWriteAsTokenDialog)

        self.getMediumTokenButton = QPushButton("Получить токен Medium")
        self.getMediumTokenButton.clicked.connect(self.showMediumTokenInstructions)

        self.saveButton = QPushButton("Сохранить токены")
        self.saveButton.clicked.connect(self.saveTokens)

        layout.addRow("Telegraph токен:", self.telegraphTokenField)
        layout.addRow(self.getTelegraphTokenButton)
        layout.addRow("Write.as токен:", self.writeAsTokenField)
        layout.addRow(self.getWriteAsTokenButton)
        layout.addRow("Medium токен:", self.mediumTokenField)
        layout.addRow(self.getMediumTokenButton)
        layout.addRow(self.saveButton)

        self.setLayout(layout)
        self.loadTokens()

    def getTelegraphToken(self):
        short_name = "TestShortName"  # Можно заменить на ввод от пользователя
        author_name = "TestAuthorName"  # Можно заменить на ввод от пользователя
        url = "https://api.telegra.ph/createAccount"
        payload = {"short_name": short_name, "author_name": author_name}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            telegraph_token = result.get("result", {}).get("access_token", "")
            self.telegraphTokenField.setText(telegraph_token)
        else:
            self.telegraphTokenField.setText("Ошибка получения токена")

    def getWriteAsTokenDialog(self):
        credentialsDialog = WriteAsCredentialsDialog(self)
        credentialsDialog.exec()

    def showMediumTokenInstructions(self):
        dialog = MediumTokenInstructionsDialog(self)
        dialog.exec()

    def saveTokens(self):
        telegraph_token = self.telegraphTokenField.text()
        write_as_token = self.writeAsTokenField.text()
        medium_token = self.mediumTokenField.text()

        with open("telegraph_token.txt", "w") as telegraph_file:
            telegraph_file.write(telegraph_token)

        with open("writeas_token.txt", "w") as write_as_file:
            write_as_file.write(write_as_token)

        with open("medium_token.txt", "w") as medium_file:
            medium_file.write(medium_token)

        self.parent().telegraphToken = telegraph_token
        self.parent().writeAsToken = write_as_token
        self.parent().mediumToken = medium_token
        self.parent().tokenLabel.setText(f"Telegraph токен: {telegraph_token}")
        self.parent().writeAsTokenLabel.setText(f"Write.as токен: {write_as_token}")
        self.parent().mediumTokenLabel.setText(f"Medium токен: {medium_token}")
        self.close()

    def loadTokens(self):
        try:
            with open("telegraph_token.txt", "r") as telegraph_file:
                self.telegraphTokenField.setText(telegraph_file.read().strip())
        except FileNotFoundError:
            pass

        try:
            with open("writeas_token.txt", "r") as write_as_file:
                self.writeAsTokenField.setText(write_as_file.read().strip())
        except FileNotFoundError:
            pass

        try:
            with open("medium_token.txt", "r") as medium_file:
                self.mediumTokenField.setText(medium_file.read().strip())
        except FileNotFoundError:
            pass
class MediumTokenInstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Получение токена Medium")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()
        instructions = QLabel(
            "Для получения токена Medium:\n"
            "1. Перейдите на Medium в раздел Developer Settings.\n"
            "2. Создайте интеграцию и получите токен доступа.\n"
            "3. Вставьте ваш токен в поле 'Medium токен' и сохраните его."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        self.closeButton = QPushButton("Закрыть")
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)


class WriteAsCredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите учетные данные Write.as")
        self.setGeometry(200, 200, 300, 200)

        layout = QFormLayout()
        self.usernameField = QLineEdit()
        self.passwordField = QLineEdit()
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
        self.getTokenButton = QPushButton("Получить токен")
        self.getTokenButton.clicked.connect(self.getWriteAsToken)

        layout.addRow("Имя пользователя:", self.usernameField)
        layout.addRow("Пароль:", self.passwordField)
        layout.addRow(self.getTokenButton)

        self.setLayout(layout)

    def getWriteAsToken(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
        url = "https://write.as/api/auth/login"
        payload = {"alias": username, "pass": password}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            write_as_token = result.get("data", {}).get("access_token", "")
            self.parent().writeAsTokenField.setText(write_as_token)
            self.close()
        else:
            self.parent().writeAsTokenField.setText("Ошибка получения токена")
            self.close()


class BlogUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.telegraphToken = ""
        self.writeAsToken = ""
        self.mediumToken = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Загрузчик постов")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Введите текст для публикации...")
        self.textEdit.setMinimumHeight(300)
        layout.addWidget(self.textEdit)

        self.platformSelect = QComboBox()
        self.platformSelect.addItems(["Telegraph", "Write.as", "Medium"])
        layout.addWidget(self.platformSelect)

        self.sendButton = QPushButton("Опубликовать")
        self.sendButton.clicked.connect(self.publishPost)
        layout.addWidget(self.sendButton)

        self.tokenButton = QPushButton("Управление токенами")
        self.tokenButton.clicked.connect(self.showTokenDialog)
        layout.addWidget(self.tokenButton)

        self.tokenLabel = QLabel("Telegraph токен не установлен")
        layout.addWidget(self.tokenLabel)

        self.writeAsTokenLabel = QLabel("Write.as токен не установлен")
        layout.addWidget(self.writeAsTokenLabel)

        self.mediumTokenLabel = QLabel("Medium токен не установлен")
        layout.addWidget(self.mediumTokenLabel)

        self.linkLabel = QLabel("Ссылка на опубликованный пост появится здесь")
        layout.addWidget(self.linkLabel)

        self.linkField = QLineEdit()
        self.linkField.setReadOnly(True)
        layout.addWidget(self.linkField)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.loadTokens()

    def showTokenDialog(self):
        dialog = TokenDialog(self)
        dialog.exec()

    def loadTokens(self):
        try:
            with open("telegraph_token.txt", "r") as telegraph_file:
                self.telegraphToken = telegraph_file.read().strip()
                self.tokenLabel.setText(f"Telegraph токен: {self.telegraphToken}")
        except FileNotFoundError:
            pass

        try:
            with open("writeas_token.txt", "r") as write_as_file:
                self.writeAsToken = write_as_file.read().strip()
                self.writeAsTokenLabel.setText(f"Write.as токен: {self.writeAsToken}")
        except FileNotFoundError:
            pass

        try:
            with open("medium_token.txt", "r") as medium_file:
                self.mediumToken = medium_file.read().strip()
                self.mediumTokenLabel.setText(f"Medium токен: {self.mediumToken}")
        except FileNotFoundError:
            pass

    def publishPost(self):
        platform = self.platformSelect.currentText()
        content = self.textEdit.toPlainText()
        if not content.strip():
            self.linkLabel.setText("Ошибка: текст не может быть пустым")
            return

        if platform == "Telegraph":
            self.postToTelegraph(content)
        elif platform == "Write.as":
            self.postToWriteAs(content)
        elif platform == "Medium":
            self.postToMedium(content)

    def postToTelegraph(self, content):
        if not self.telegraphToken:
            self.linkLabel.setText("Ошибка: Telegraph токен не установлен")
            return

        url = "https://api.telegra.ph/createPage"
        headers = {"Content-Type": "application/json"}
        payload = {
            "access_token": self.telegraphToken,
            "title": "BlogUploader",
            "content": [{"tag": "p", "children": [content]}],
            "author_name": "BlogUploader"
        }
        response = requests.post(url, json=payload, headers=headers)
        self.handleResponse(response, "Telegraph")

    def postToWriteAs(self, content):
        if not self.writeAsToken:
            self.linkLabel.setText("Ошибка: Write.as токен не установлен")
            return

        url = "https://write.as/api/posts"
        headers = {"Authorization": f"Token {self.writeAsToken}", "Content-Type": "application/json"}
        payload = {"body": content}
        response = requests.post(url, json=payload, headers=headers)

        # Обработка ответа от Write.as
        if response.status_code in [200, 201]:
            result = response.json()
            self.linkField.setText(result.get("data", {}).get("url", ""))
            self.linkLabel.setText("Пост успешно опубликован на Write.as")
        else:
            self.linkLabel.setText("Ошибка публикации на Write.as")

        def postToMedium(self, content):
            if not self.mediumToken:
                self.linkLabel.setText("Ошибка: Medium токен не установлен")
                return

            url = "https://api.medium.com/v1/users/me/posts"
            headers = {"Authorization": f"Bearer {self.mediumToken}", "Content-Type": "application/json"}
            payload = {
                "title": "BlogUploader Post",
                "contentFormat": "markdown",
                "content": content,
                "publishStatus": "public"
            }
            response = requests.post(url, json=payload, headers=headers)

            # Обработка ответа от Medium
            if response.status_code in [200, 201]:
                result = response.json()
                self.linkField.setText(result.get("url", ""))
                self.linkLabel.setText("Пост успешно опубликован на Medium")
            else:
                self.linkLabel.setText("Ошибка публикации на Medium")

        def handleResponse(self, response, platform):
            if response.status_code in [200, 201]:
                result = response.json()
                self.linkField.setText(result.get("result", {}).get("url", result.get("data", {}).get("url", "")))
                self.linkLabel.setText(f"Пост опубликован на {platform}")
            else:
                self.linkLabel.setText(f"Ошибка публикации на {platform}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = BlogUploader()
    mainWin.show()
    sys.exit(app.exec())
