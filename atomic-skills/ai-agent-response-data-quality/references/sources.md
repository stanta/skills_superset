# Sources and scope (reviewed 2026-09-29)

These sources support different parts of the skill. They do **not** show that one verifier model can guarantee factual correctness. Domain policies and acceptance thresholds are engineering decisions, not verbatim requirements of these sources.

1. [ISO/IEC 25012:2008 — Data quality model](https://www.iso.org/standard/35736.html). Structured-data quality requirements and evaluation; the ISO page reports review and confirmation in 2025. Not a standard for judging LLM-generated claims.
2. [NIST AI RMF Generative AI Profile, AI 600-1 (2024)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence). Risk-based generative-AI governance, measurement and evaluation.
3. [Min et al., FActScore, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.741/). Atomic-fact decomposition and evidence-supported factual precision.
4. [Google DeepMind, FACTS Benchmark Suite (2025-12-09)](https://deepmind.google/blog/facts-benchmark-suite-systematically-evaluating-the-factuality-of-large-language-models/). Distinguishes search, long-context grounding, parametric and multimodal factuality.
5. [Ragas — Faithfulness metric](https://github.com/vibrantlabsai/ragas/blob/main/docs/concepts/metrics/available_metrics/faithfulness.md). Measures response consistency with retrieved context; cannot establish whether the context itself is authentic or true.
6. [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Deterministic and model-based evaluators, human labels and judge calibration.
7. [Anthropic — Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations). Admit uncertainty, ground answers and verify citations.
8. [W3C PROV overview](https://www.w3.org/TR/prov-overview/) and [PROV-O](https://www.w3.org/TR/prov-o/). Provenance of entities, activities and agents.
9. [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and [OWASP RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html). Untrusted retrieved/tool content and protection boundaries.
10. [Great Expectations — Data quality use cases](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/dq_use_cases_lp/). Executable checks for schema, completeness, integrity, uniqueness and freshness of structured sources.

The gate states, evidence-packet format, retry policy and proposed release invariants are a documented synthesis for agent engineering; validate them against the project's actual risks.
