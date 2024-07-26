class Schemas:
    TRASH = """
        CREATE TABLE "trash"
        (
        "id" INTEGER,
        "created_by" TEXT NOT NULL,
        "created_at" DATETIME NOT NULL,
        "cleaned_by" TEXT,
        "cleaned_at" DATETIME,
        "location_x" REAL,
        "location_x" REAL,
        "trash_type_id" INTEGER,
        "status_id" INTEGER,
        "severity_id" INTEGER,
        "image_url" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("trash_type_id") REFERENCES trash_type(id),
        FOREIGN KEY("status_id") REFERENCES status(id),
        FOREIGN KEY("severity_id") REFERENCES severity(id)
        )
        """

    TRASH_TYPE = """
        CREATE TABLE "trash_type"
        (
        "id" INTEGER,
        "type_name" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    USER = """
        CREATE TABLE "user"
        (
        "id" INTEGER,
        "username" TEXT,
        "password" TEXT,
        "email" TEXT,
        "user_type_id" ID,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("user_type_id") REFERENCES user_type(id)
        )
        """

    USER_TYPE = """
        CREATE TABLE "user_type"
        (
        "id" INTEGER,
        "name" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    STATUS = """
        CREATE TABLE "status"
        (
        "id" INTEGER,
        "name" TEXT,
        "description" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """

    SEVERITY = """
        CREATE TABLE "severity"
        (
        "id" INTEGER,
        "name" TEXT,
        "description" TEXT,
        PRIMARY KEY("id" AUTOINCREMENT)
        )
        """
