# =========================
# Class: BaseStorage (Superclass)
# แสดง: Encapsulation, Superclass
# =========================

import json
from datetime import datetime

# จำลอง localStorage ด้วย dictionary
local_storage = {}


class BaseStorage:

    # Constructor
    def __init__(self, prefix="app"):
        self.__storage_prefix = prefix
        self.__is_initialized = True

    # Getter (Encapsulation)
    @property
    def prefix(self):
        return self.__storage_prefix

    @property
    def initialized(self):
        return self.__is_initialized

    # =========================
    # Protected-style methods
    # =========================

    def _save_to_storage(self, key, value):
        local_storage[f"{self.__storage_prefix}_{key}"] = json.dumps(value)

    def _load_from_storage(self, key):
        data = local_storage.get(f"{self.__storage_prefix}_{key}")
        return json.loads(data) if data else None

    def _remove_from_storage(self, key):
        local_storage.pop(f"{self.__storage_prefix}_{key}", None)

    # =========================
    # Polymorphism
    # =========================

    def get_status(self):
        return f"BaseStorage (prefix: {self.__storage_prefix}) initialized: {self.__is_initialized}"

    def clear(self):
        print("BaseStorage.clear() called — subclass should override this.")


# =========================
# Class: AuthManager
# แสดง: Inheritance, Polymorphism
# =========================

class AuthManager(BaseStorage):

    def __init__(self):
        super().__init__("auth")
        self.__user_key = "user"
        self.__session_key = "session"

    # Getter
    @property
    def user_key(self):
        return self.__user_key

    @property
    def session_key(self):
        return self.__session_key

    # =========================
    # Override get_status
    # =========================

    def get_status(self):
        logged_in = self.is_logged_in()
        user = self.get_user()

        username = user["username"] if user else "none"

        return f"AuthManager | logged in: {logged_in} | user: {username}"

    # =========================
    # Override clear
    # =========================

    def clear(self):
        self._remove_from_storage(self.__user_key)
        self._remove_from_storage(self.__session_key)

    # =========================
    # Register
    # =========================

    def register(self, full_name, email, username, password):

        if not all([full_name, email, username, password]):
            print("กรุณากรอกข้อมูลให้ครบ")
            return False

        user = RegisteredUser(full_name, email, username, password)

        self._save_to_storage(self.__user_key, user.to_json())

        print("สมัครสมาชิกสำเร็จ")
        return True

    # =========================
    # Login
    # =========================

    def login(self, username, password):

        user_data = self.get_user()

        if (
            user_data and
            username == user_data["username"] and
            password == user_data["password"]
        ):

            self._save_to_storage(
                self.__session_key,
                {
                    "loggedIn": True,
                    "loginTime": datetime.now().isoformat()
                }
            )

            print("Login สำเร็จ")
            return True

        print("Username หรือ Password ไม่ถูกต้อง")
        return False

    # =========================
    # Logout
    # =========================

    def logout(self):
        self._remove_from_storage(self.__session_key)
        print("Logout สำเร็จ")

    # =========================
    # ตรวจสอบ Login
    # =========================

    def is_logged_in(self):

        session = self._load_from_storage(self.__session_key)

        return session is not None and session.get("loggedIn") is True

    # =========================
    # ดึงข้อมูลผู้ใช้
    # =========================

    def get_user(self):
        return self._load_from_storage(self.__user_key)


# =========================
# Class: BaseUser
# =========================

class BaseUser:

    def __init__(self, full_name, email):

        self.full_name = full_name
        self.__email = email
        self.__register_date = datetime.now().strftime("%d/%m/%Y")

    # Getters
    @property
    def email(self):
        return self.__email

    @property
    def register_date(self):
        return self.__register_date

    # Polymorphism
    def get_role(self):
        return "base"

    def get_summary(self):
        return f"User: {self.full_name} | Role: {self.get_role()}"


# =========================
# Class: RegisteredUser
# =========================

class RegisteredUser(BaseUser):

    def __init__(self, full_name, email, username, password):

        super().__init__(full_name, email)

        self.username = username
        self.__password = password

    # Getter
    @property
    def password(self):
        return self.__password

    # Override get_role
    def get_role(self):
        return "registered"

    # Override get_summary
    def get_summary(self):

        return (
            f"RegisteredUser: {self.full_name} "
            f"(@{self.username}) | สมัครเมื่อ: {self.register_date}"
        )

    # =========================
    # to_json
    # =========================

    def to_json(self):

        return {
            "fullName": self.full_name,
            "email": self.email,
            "username": self.username,
            "password": self.__password,
            "registerDate": self.register_date,
            "role": self.get_role(),
        }


# =========================
# Instance
# =========================

auth_manager = AuthManager()

# =========================
# ทดลองใช้งาน
# =========================

auth_manager.register(
    "สมชาย ใจดี",
    "somchai@gmail.com",
    "somchai",
    "1234"
)

print(auth_manager.get_status())

auth_manager.login("somchai", "1234")

print(auth_manager.get_status())

print("ข้อมูลผู้ใช้:")
print(auth_manager.get_user())

auth_manager.logout()

print(auth_manager.get_status())