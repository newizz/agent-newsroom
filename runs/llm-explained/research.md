# Research: How Large Language Models Work

**Slug:** llm-explained
**Research date:** 2026-06-03
**Confidence:** high

## TL;DR
A large language model is, at its core, a very large statistical pattern-completer. It chops text into tokens, represents each token as a vector of numbers, and uses the **transformer attention mechanism** to let every token "look at" every other token to figure out what should come next. Training adjusts billions of parameters so the model's next-token guesses match real text; inference is just running that same guess over and over to produce a sentence.

## Key findings
1. **The atomic unit is a token, not a word.** Models work on sub-word pieces (e.g. "extraordinary" → "extra" + "ordinary"). This lets a finite vocabulary (~100k tokens) cover any text [^4].
2. **Meaning lives in vectors.** Each token maps to a learned embedding — a list of ~thousands of numbers — where similar meanings end up close together [^2].
3. **Attention is the breakthrough.** Each token's representation is updated by looking at every other token, weighted by relevance. This is what lets the model resolve "it" referring to "the cat" three sentences earlier [^1].
4. **One forward pass = one token.** Models generate text one token at a time. Each new token re-uses the previous tokens (with caching) to predict the next [^3].
5. **Training is gradient descent on next-token prediction.** Show the model trillions of text snippets, ask it to guess the next token, nudge its parameters whenever it's wrong [^3].
6. **Context windows are quadratic.** Vanilla attention costs O(n²) where n is sequence length, which is why model providers ship finite-but-growing context limits (2k → 32k → 200k → 1M+) [^5].

## Background / context

Before 2017, the dominant approaches to language were RNNs and LSTMs — networks that processed text left-to-right, one word at a time, with a hidden state that struggled to remember things from far back in the sequence. The Transformer architecture [^1] threw all that out and replaced it with **self-attention**, which let every word interact with every other word in parallel.

That parallelism is what made today's models possible. RNNs couldn't be efficiently trained on huge datasets; Transformers can. Scaled-up Transformers became GPT, BERT, Claude, Gemini, and every modern LLM.

## Deep dive

### 1. Tokenization — chopping text into pieces

Before the model sees your prompt, a **tokenizer** breaks it into integer IDs from a fixed vocabulary. Modern LLMs use Byte-Pair Encoding (BPE) or similar [^4]. Common words become single tokens; rare words become several.

A rough rule of thumb: **1 token ≈ 4 characters in English**, or ~¾ of a word. So a 1,000-word essay is ~1,300 tokens.

### 2. Embeddings — meaning as coordinates

Each token ID is looked up in a giant table (the embedding matrix) and replaced with a vector — typically 768 to 12,288 numbers depending on model size [^3]. Two key properties emerge from training:

- Tokens with similar meaning end up close in vector space
- Differences in meaning become directions (the classic example: `king − man + woman ≈ queen`)

### 3. Attention — every token looks at every other

This is the magic ingredient. For each token in the sequence, the model computes three vectors: a **Query**, a **Key**, and a **Value**. Then it asks: "How much should I care about every other token in this sequence?" by dotting each Query against every Key [^1]. The resulting attention scores weight a combination of Values to update the token's representation.

Stacking dozens of attention layers, each with multiple parallel "heads", produces representations rich enough to capture grammar, facts, tone, and intent — all without anyone explicitly programming those rules [^2].

### 4. Training vs inference

**Training** runs the model on trillions of tokens of text. For each position, the model predicts the next token; the loss compares that prediction against the actual next token; gradient descent tweaks all the parameters slightly in the direction that reduces the loss. Repeat for months on thousands of GPUs [^3].

**Inference** is what happens when you use the model. The trained parameters are frozen. The model just runs forward: prompt → predict next token → append it → predict the next token → ...

### 5. Sampling — picking the next token

At each step the model outputs a probability distribution over the entire vocabulary. To turn that into actual text, a sampler picks one token. Common strategies:

- **Greedy** — always pick the highest-probability token (deterministic, can be repetitive)
- **Temperature** — flatten or sharpen the distribution before picking (`temperature=0` is greedy, `temperature=1` is "natural")
- **Top-p / nucleus** — sample only from the top tokens whose probabilities sum to *p* (e.g., 0.9)

Higher temperature = more creative but more likely to hallucinate. Lower temperature = more reliable but more boring.

### 6. Context windows

Because attention is O(n²) in sequence length, doubling the context length quadruples compute. Providers spend significant engineering on tricks (sliding windows, sparse attention, KV caching) to push context up. As of 2026, frontier models routinely handle 200k–1M tokens [^5].

## Data / numbers

| Quantity | Typical value (frontier model) | Source |
|---|---|---|
| Vocabulary size | ~100,000 tokens | [^4] |
| Embedding dimension | 4,096–12,288 | [^3] |
| Number of layers | 80–120 | [^3] |
| Total parameters | 10¹¹ – 10¹² (100B–1T) | [^3][^5] |
| Training tokens | 10¹³ (~10 trillion) | [^3] |
| Context window | 200k–1M tokens | [^5] |

## Worked example

**Prompt:** `The cat sat on the`

1. Tokenizer: `["The", " cat", " sat", " on", " the"]` → `[464, 3797, 3332, 319, 262]`
2. Each ID is looked up to give a 4096-dim vector
3. The vectors flow through ~100 layers of attention + feed-forward blocks
4. The final layer projects to a 100k-dim vector — one logit per vocabulary token
5. Softmax turns logits into probabilities: ` mat` (0.41), ` floor` (0.18), ` chair` (0.09), ...
6. Sampler picks ` mat` (greedy or low-temp)
7. The new sequence `The cat sat on the mat` becomes the new prompt for the next token

## Open questions / limitations

- **Why does attention work so well?** We have intuition but no full theoretical explanation.
- **Scaling laws.** Performance keeps improving with more parameters / data / compute, with no clear ceiling so far [^3].
- **Hallucination.** Sampling from a probability distribution by definition can produce confident-but-wrong tokens.
- **Reasoning.** Whether large models "reason" or pattern-match is actively debated; recent reasoning models (o1, Claude with extended thinking) blur the line.

## Glossary

- **Token:** A sub-word piece of text; the atomic unit the model operates on.
- **Embedding:** A learned vector representation of a token.
- **Attention:** The mechanism that lets each token "look at" other tokens to update its representation.
- **Parameter:** A single trainable number in the model. Modern models have 10¹¹–10¹² of them.
- **Inference:** Running the trained model to produce output (vs training to update parameters).
- **Temperature:** A knob controlling how random the sampling step is.
- **Context window:** The maximum number of tokens the model can attend to at once.
