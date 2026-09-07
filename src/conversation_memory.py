# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []

# Maximum number of previous interactions to remember
MAX_HISTORY = 10


# ============================================================
# ADD MESSAGE
# ============================================================

def add_to_memory(question, answer):
    """
    Store a question and its answer in conversation memory.
    """

    conversation_history.append({
        "question": question,
        "answer": answer
    })

    # Keep only the most recent interactions
    if len(conversation_history) > MAX_HISTORY:

        conversation_history.pop(0)


# ============================================================
# GET MEMORY
# ============================================================

def get_memory():
    """
    Return the stored conversation history.
    """

    return conversation_history


# ============================================================
# FORMAT MEMORY FOR LLM
# ============================================================

def get_memory_text():
    """
    Convert conversation history into text that can be
    included in an LLM prompt.
    """

    if not conversation_history:

        return "No previous conversation."


    memory_lines = []

    for item in conversation_history:

        memory_lines.append(
            f"User: {item['question']}"
        )

        memory_lines.append(
            f"Assistant: {item['answer']}"
        )


    return "\n".join(memory_lines)


# ============================================================
# CLEAR MEMORY
# ============================================================

def clear_memory():
    """
    Clear the conversation history.
    """

    conversation_history.clear()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CONVERSATION MEMORY TEST")
    print("=" * 60)


    add_to_memory(
        "How many applicants defaulted?",
        "There are 24,825 defaulted applicants."
    )


    add_to_memory(
        "How many applicants are there?",
        "There are 307,511 applicants."
    )


    print()
    print("Stored conversation:")
    print()


    print(get_memory_text())


    print()
    print("=" * 60)
    print("MEMORY TEST COMPLETED")
    print("=" * 60)