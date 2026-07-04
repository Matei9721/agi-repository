import unittest

from rag_lab.pipeline import answer_question
from rag_lab.retriever import retrieve_context


class RetrievalTests(unittest.TestCase):
    def test_retrieval_returns_requested_number_of_relevant_docs(self):
        context = retrieve_context("authentication launch support", limit=2)

        self.assertEqual(2, len(context))
        self.assertEqual(["policy-auth", "policy-support"], [doc["id"] for doc in context])


class PipelineTests(unittest.TestCase):
    def test_pipeline_answers_from_retrieved_context(self):
        result = answer_question("What should enterprise authentication include?")

        self.assertIn("SSO", result.answer)
        self.assertIn("policy-auth", result.citations)
        self.assertGreaterEqual(result.confidence, 0.5)


if __name__ == "__main__":
    unittest.main()

