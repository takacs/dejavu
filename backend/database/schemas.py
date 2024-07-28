class Schemas:
    TRASH = """
        CREATE TABLE "trash"
        (
        "id" INTEGER,
        "created_user_id" TEXT NOT NULL,
        "created_at" DATETIME NOT NULL,
        "cleaned_user_id" TEXT,
        "cleaned_at" DATETIME,
        "location_x" REAL NOT NULL,
        "location_y" REAL NOT NULL,
        "trash_type_id" INTEGER NOT NULL,
        "status_id" INTEGER NOT NULL,
        "severity_id" INTEGER NOT NULL,
        "image_url" TEXT NOT NULL,
        "description" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("trash_type_id") REFERENCES trash_type(id),
        FOREIGN KEY("status_id") REFERENCES status(id),
        FOREIGN KEY("severity_id") REFERENCES severity(id)
        FOREIGN KEY("created_user_id") REFERENCES user(id)
        FOREIGN KEY("cleaned_user_id") REFERENCES user(id)

        )
        """

    TRASH_TYPE = """
        CREATE TABLE "trash_type"
        (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    USER = """
        CREATE TABLE "user"
        (
        "id" INTEGER,
        "username" TEXT NOT NULL,
        "password" TEXT NOT NULL,
        "email" TEXT NOT NULL,
        "user_type_id" ID NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("user_type_id") REFERENCES user_type(id)
        )
        """

    USER_TYPE = """
        CREATE TABLE "user_type"
        (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    STATUS = """
        CREATE TABLE "status"
        (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    SEVERITY = """
        CREATE TABLE "severity"
        (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    ENFORCE_FK = """
        PRAGMA foreign_keys = ON
        """


ALL_TABLE_SCHEMAS = [
    Schemas.USER_TYPE,
    Schemas.TRASH_TYPE,
    Schemas.STATUS,
    Schemas.SEVERITY,
    Schemas.USER,
    Schemas.TRASH,
    Schemas.ENFORCE_FK,
]
