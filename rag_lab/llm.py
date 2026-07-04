from dataclasses import dataclass
from random import Random

from rag_lab.retriever import tokenize


@dataclass
class LLMResponse:
    text: str
    used_citations: list[str]


class FakeLLM:
    """Small stand-in for an LLM so the exercise needs no API key."""

    def __init__(self, rng=None):
        self.rng = rng or Random()

    def generate(self, question, context):
        question_tokens = tokenize(question)
        selected = []

        for document in context:
            document_tokens = tokenize(f"{document['title']} {document['text']}")
            if question_tokens & document_tokens:
                selected.append(document)

        if not selected:
            return LLMResponse(
                text="I do not have enough evidence to answer.",
                used_citations=[],
            )

        self.rng.shuffle(selected)
        lead_in = self.rng.choice(
            [
                "Based on the retrieved evidence,",
                "The relevant policy signal is that",
                "A reasonable answer from the context is:",
            ]
        )
        joiner = self.rng.choice([" Also, ", " In addition, ", " "])
        summary = joiner.join(document["text"].split(".")[0] for document in selected)
        citations = [document["id"] for document in selected]
        citation_text = ", ".join(f"[{citation}]" for citation in citations)
        return LLMResponse(
            text=f"{lead_in} {summary}. Sources: {citation_text}",
            used_citations=citations,
        )
