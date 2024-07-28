class SetupQueries:
    DEFAULT_STATUSES = """
    INSERT INTO status (name)
    VALUES
    ("New"),
    ("Cleaning"),
    ("Cleaned"),
    ("Rejected")
    """

    DEFAULT_SEVERITIES = """
    INSERT INTO severity (name)
    VALUES
    ("Low"),
    ("Medium"),
    ("High")
    """

    DEFAULT_TRASH_TYPES = """
    INSERT INTO trash_type (name)
    VALUES
    ("Litter"),
    ("Debris"),
    ("Poop"),
    ("Other")
    """

    DEFAULT_USER_TYPES = """
    INSERT INTO user_type (name)
    VALUES
    ("Civilian"),
    ("Cleaner"),
    ("Admin")
    """


ALL_SETUP_QUERIES = [
    SetupQueries.DEFAULT_STATUSES,
    SetupQueries.DEFAULT_TRASH_TYPES,
    SetupQueries.DEFAULT_USER_TYPES,
    SetupQueries.DEFAULT_SEVERITIES,
]
