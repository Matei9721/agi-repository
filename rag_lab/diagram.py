PIPELINE_STEPS = [
    ("Question", "User question"),
    ("Retriever", "Keyword retrieval over policy snippets"),
    ("Prompt", "Prompt builder with evidence and answer style"),
    ("FakeLLM", "Randomized mocked generator"),
    ("Result", "Answer, citations, confidence"),
]


def render_mermaid():
    lines = ["flowchart LR"]
    for index, (node_id, label) in enumerate(PIPELINE_STEPS):
        lines.append(f'    {node_id}["{label}"]')
        if index:
            previous = PIPELINE_STEPS[index - 1][0]
            lines.append(f"    {previous} --> {node_id}")
    return "\n".join(lines)


def main():
    print(render_mermaid())


if __name__ == "__main__":
    main()
