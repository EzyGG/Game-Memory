import ezyapi.mysql_connection as connect
from ezyapi.UUID import UUID


class UserError(Exception):
    pass


class UserNotFoundException(UserError):
    def __init__(self, username=None, password=None):
        if username is not None and password is not None:
            super().__init__(f"User '{username}' with password : '{password}' cannot be found.")
        elif username is not None:
            super().__init__(f"User '{username}' cannot be found.")
        elif password is not None:
            super().__init__(f"User with password : '{password}' cannot be found.")
        else:
            super().__init__("User cannot be found.")


class UserAlreadyExistsException(UserError):
    def __init__(self):
            super().__init__("User already exists.")


class User:

    def __init__(self, connection_id: str | UUID, password: str = ""):
        self.uuid: UUID = None
        self.password: str = None
        self.reconnect(connection_id, password)

    @staticmethod
    def create_user(username: str, completename: str | None, mail: str | None, password: str):
        if not username or password is None:
            raise UserError("Username or Password not allowed...")
        username, completename = str(username), str(completename) if completename else None
        mail, password = str(mail) if mail else None, str(password)
        u = User(username, password)
        if u.exists():
            raise UserAlreadyExistsException()
        connect.execute(f"""INSERT INTO users(uuid, username, completename, mail, password)
                        VALUES ("{UUID(username)}", "{username}", {('"' + completename + '"') if completename else 'null'},
                        {('"' + mail + '"') if mail else 'null'}, "{password if password else ''}");""")
        connect.commit()
        u = User(username, password)
        if not u.connected():
            raise UserError("Cannot connect the user.")
        return User(username, password)

    def exists(self) -> bool:
        connect.execute(f"""SELECT * FROM users WHERE uuid="{str(self.uuid).lower()}"
                            OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}\"""")
        return bool(len(connect.fetch()))

    def connected(self) -> bool:
        connect.execute(f"""SELECT * FROM users WHERE (uuid="{str(self.uuid).lower()}"
                            OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}")
                            AND password="{self.password}\"""")
        return bool(len(connect.fetch()))

    def reconnect(self, connection_id: str | UUID, password: str = ""):
        self.uuid, self.password = str(connection_id), str(password)
        if self.connected():
            connect.execute(f"""SELECT uuid FROM users WHERE (uuid="{str(self.uuid).lower()}"
                                OR username="{str(self.uuid).lower()}" OR mail="{str(self.uuid).lower()}")
                                AND password="{self.password}\"""")
            self.uuid = UUID.parseUUID(connect.fetch(1)[0])

    def get_uuid(self) -> UUID:
        return self.uuid

    def get_username(self) -> str:
        connect.execute(f"""SELECT username FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def get_completename(self) -> str:
        connect.execute(f"""SELECT completename FROM users WHERE uuid="{self.uuid}\"""")
        f = connect.fetch(1)[0]
        return self.get_username() if f is None else f

    def set_completename(self, completename: str):
        connect.execute(f"""UPDATE users SET completename = "{completename}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_mail(self) -> str:
        connect.execute(f"""SELECT mail FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_mail(self, mail: str):
        connect.execute(f"""UPDATE users SET mail = "{mail}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_password(self) -> str:
        connect.execute(f"""SELECT password FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_password(self, password: str):
        connect.execute(f"""UPDATE users SET password = "{password}" WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_creation(self):
        connect.execute(f"""SELECT creation FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def is_admin(self) -> bool:
        connect.execute(f"""SELECT admin FROM users WHERE uuid="{self.uuid}\"""")
        return bool(connect.fetch(1)[0])

    def is_frozen(self) -> bool:
        connect.execute(f"""SELECT frozen FROM users WHERE uuid="{self.uuid}\"""")
        return bool(connect.fetch(1)[0])

    def set_frozen(self, frozen: bool):
        connect.execute(f"""UPDATE users SET frozen = {1 if bool(frozen) else 0} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_lvl(self) -> int:
        connect.execute(f"""SELECT lvl FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def get_exp(self) -> int:
        connect.execute(f"""SELECT exp FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def get_gp(self) -> int:
        connect.execute(f"""SELECT gp FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def get_theme(self) -> int:
        connect.execute(f"""SELECT theme FROM users WHERE uuid="{self.uuid}\"""")
        return connect.fetch(1)[0]

    def set_theme(self, theme: int):
        connect.execute(f"""UPDATE users SET theme = {theme} WHERE uuid="{self.uuid}\"""")
        connect.commit()

    def get_played_games(self) -> int:
        connect.execute(f"""SELECT * FROM sets WHERE player="{self.uuid}\"""")
        return len(connect.fetch())

    def get_total_wins(self) -> int:
        connect.execute(f"""SELECT * FROM sets WHERE player="{self.uuid}\" AND won=1""")
        return len(connect.fetch())
