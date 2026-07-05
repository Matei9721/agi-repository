ANSWER_STYLE = "Use a brief, evidence-first tone and call out caveats."


def build_prompt(question, context):
    evidence = "\n".join(
        f"- [{doc['id']}] {doc['title']}: {doc['text']}" for doc in context
    )
    return (
        f"{ANSWER_STYLE}\n"
        "Answer only from the evidence. Include citation ids when relevant.\n\n"
        f"Question: {question}\n\n"
        f"Evidence:\n{evidence}"
    )
