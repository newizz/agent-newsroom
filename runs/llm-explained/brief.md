# Brief: How Large Language Models Work

**Slug:** llm-explained
**Created:** 2026-06-03
**Template hint:** concept-explorer
**Ambiguity:** green
**Estimated depth:** standard

## Original prompt
> Explain how large language models actually work — for someone who knows what an LLM is but doesn't understand the internals.

## Refined question
What are the core mechanisms that let a large language model take an input prompt and produce coherent, useful text — at the level of mechanism, not mathematics?

## Scope
- **In scope:** Tokenization, embeddings, transformer attention (intuition), training vs inference, sampling, context windows
- **Out of scope:** Calculus / linear algebra details, specific model architectures (e.g. MoE), training infrastructure, alignment / RLHF

## Audience
A technically curious reader who has used ChatGPT/Claude. Comfortable with programming concepts. Wants intuition, not equations.

## Success criteria
A successful dashboard will:
- Demystify the "magic" — reader leaves understanding it's pattern completion at scale
- Use concrete mini-examples for tokenization and attention
- Glossary covers terms the reader will encounter elsewhere (tokens, embedding, attention, parameters)

## Key questions Research must answer
1. What is a token and why is it the unit of work?
2. How does the model represent meaning numerically?
3. What does "attention" actually do, in plain words?
4. What's the difference between training and inference?
5. How does the model pick its next word?
6. Why are context windows finite?

## Assumptions made
- Assumed audience is general-technical (used by Intake when topic didn't specify)

## Open risks
- None significant for this topic
