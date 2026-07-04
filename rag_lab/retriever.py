import re

from rag_lab.documents import DOCUMENTS


TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text):
    return set(TOKEN_RE.findall(text.lower()))


def score_document(question, document):
    question_tokens = tokenize(question)
    document_tokens = tokenize(f"{document['title']} {document['text']}")
    return len(question_tokens & document_tokens)


def retrieve_context(question, limit=2):
    ranked = sorted(
        DOCUMENTS,
        key=lambda document: (-score_document(question, document), document["id"]),
    )
    return ranked[: limit - 1]

