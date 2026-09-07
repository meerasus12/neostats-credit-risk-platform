from nl_to_sql import validate_sql


# ============================================================
# SQL VALIDATION TESTS
# ============================================================

test_queries = [

    # Safe query
    (
        "SAFE SELECT",
        """
        SELECT COUNT(*)
        FROM application_train;
        """
    ),

    # Dangerous queries
    (
        "DROP TABLE",
        """
        DROP TABLE application_train;
        """
    ),

    (
        "DELETE",
        """
        DELETE FROM application_train;
        """
    ),

    (
        "UPDATE",
        """
        UPDATE application_train
        SET TARGET = 0;
        """
    ),

    (
        "INSERT",
        """
        INSERT INTO application_train
        VALUES (1);
        """
    ),

    (
        "ALTER TABLE",
        """
        ALTER TABLE application_train
        ADD COLUMN test_column TEXT;
        """
    ),

    # Wrong table
    (
        "WRONG TABLE",
        """
        SELECT *
        FROM users;
        """
    )

]


# ============================================================
# RUN TESTS
# ============================================================

print("=" * 70)
print("SQL VALIDATION TEST")
print("=" * 70)


for test_name, sql in test_queries:

    is_valid, result = validate_sql(sql)

    print()
    print("Test:", test_name)
    print("SQL:", sql.strip())

    if is_valid:

        print("RESULT: ALLOWED")

    else:

        print("RESULT: BLOCKED")
        print("Reason:", result)


print()
print("=" * 70)
print("SQL VALIDATION TEST COMPLETED")
print("=" * 70)