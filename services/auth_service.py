from typing import Optional, Dict, Any

class AuthService:
    def __init__(self, login_file: str = "logins.txt"):
        self.login_file = login_file
        self.current_user: Optional[Dict[str, Any]] = None

    def login(self, username: str, password: str) -> bool:
        try:
            with open(self.login_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        continue
                    file_username, file_password, file_role = [p.strip() for p in parts]
                    if username == file_username and password == file_password:
                        self.current_user = {"username": username, "role": file_role}
                        return True
        except FileNotFoundError:
            pass
        return False

    def logout(self):
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        return self.current_user