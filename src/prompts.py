# ============================================================
# PROMPT TEMPLATES FOR CREDIT RISK NL-TO-SQL
# ============================================================


# ============================================================
# SQL GENERATION PROMPT
# ============================================================

SQL_GENERATION_PROMPT = """
You are a SQL generation assistant for a credit risk
analytics application.

Your task is to convert a user's natural-language question
into ONE safe SQLite SELECT query.

DATABASE TABLE:
application_train

DATABASE SCHEMA:
{schema}

PREVIOUS CONVERSATION:
{conversation}

STRICT RULES:

1. Generate ONLY a SELECT query.
2. Use ONLY the application_train table.
3. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   REPLACE, TRUNCATE, ATTACH, DETACH, or PRAGMA.
4. Do not invent column names.
5. Use the exact column names provided in the schema.
6. Use previous conversation only when it is relevant
   to understanding the current question.
7. The current question has priority over previous conversation.
8. If the current question is independent, ignore previous
   conversation.
9. Resolve words such as "that", "those", "it", or "them"
   using previous conversation when appropriate.
10. Return ONLY the SQL query.
11. Do not use markdown code blocks.
12. Do not provide explanations.
13. Do not modify the database.
14. If the question cannot be answered using the available
    table and columns, return:

SELECT 'UNSUPPORTED' AS result;

CURRENT USER QUESTION:
{question}
"""


# ============================================================
# BUSINESS ANSWER PROMPT
# ============================================================

BUSINESS_ANSWER_PROMPT = """
You are a credit risk analytics assistant.

Your task is to convert a SQL query result into a concise,
clear, business-friendly answer.

USER QUESTION:
{question}

SQL QUERY:
{sql}

QUERY RESULT:
{result}

RULES:

1. Answer only using the provided query result.
2. Do not invent numbers or facts.
3. Do not make unsupported assumptions.
4. Do not change the meaning of the query result.
5. Do not expose unnecessary technical SQL details.
6. Keep the response concise and easy to understand.
7. If the result is empty, clearly state that no matching
   records were found.
"""


# ============================================================
# SQL VALIDATION PROMPT
# ============================================================

SQL_VALIDATION_PROMPT = """
You are a SQL safety validator for a credit risk application.

Check the generated SQL query against the following rules:

1. The query must be a SELECT query.
2. Only the application_train table may be accessed.
3. No INSERT operation is allowed.
4. No UPDATE operation is allowed.
5. No DELETE operation is allowed.
6. No DROP operation is allowed.
7. No ALTER operation is allowed.
8. No CREATE operation is allowed.
9. No REPLACE operation is allowed.
10. No TRUNCATE operation is allowed.
11. No ATTACH operation is allowed.
12. No DETACH operation is allowed.
13. No PRAGMA operation is allowed.
14. Column names must come from the supplied schema.

DATABASE SCHEMA:
{schema}

GENERATED SQL:
{sql}

Return only:

VALID

or

INVALID
"""


# ============================================================
# BUILD SQL PROMPT
# ============================================================

def build_sql_prompt(
    question,
    schema,
    conversation="No previous conversation."
):
    """
    Build the SQL generation prompt using:
    - current question
    - database schema
    - previous conversation
    """

    return SQL_GENERATION_PROMPT.format(
        question=question,
        schema=schema,
        conversation=conversation
    )


# ============================================================
# BUILD BUSINESS ANSWER PROMPT
# ============================================================

def build_business_answer_prompt(
    question,
    sql,
    result
):
    """
    Build the business-answer prompt.
    """

    return BUSINESS_ANSWER_PROMPT.format(
        question=question,
        sql=sql,
        result=result
    )


# ============================================================
# BUILD VALIDATION PROMPT
# ============================================================

def build_validation_prompt(
    sql,
    schema
):
    """
    Build the SQL validation prompt.
    """

    return SQL_VALIDATION_PROMPT.format(
        sql=sql,
        schema=schema
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    example_question = (
        "What percentage of applicants is that?"
    )

    example_schema = (
        "SK_ID_CURR (INTEGER), "
        "TARGET (INTEGER), "
        "DAYS_BIRTH (INTEGER), "
        "AMT_INCOME_TOTAL (REAL), "
        "AMT_CREDIT (REAL)"
    )

    example_conversation = """
User: How many applicants defaulted?
Assistant: There are 24,825 defaulted applicants.
"""

    prompt = build_sql_prompt(
        example_question,
        example_schema,
        example_conversation
    )

    print("SQL PROMPT")
    print("=" * 70)
    print(prompt)