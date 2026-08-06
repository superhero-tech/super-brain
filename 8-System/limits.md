# Limits

What this method does badly. Read it once, then read it again the first time the wiki tells you something confidently wrong.

The method works. It is also a nascent pattern, not a finished product - Karpathy called his own version "a hacky collection of scripts". These are the five ways it breaks.

---

## 1. Error compounding

**The biggest risk, by a distance.**

The AI writes a page with a subtle mistake. You ask a question, the answer inherits the mistake. You file the answer back. Now two pages agree on the wrong thing. Two months later five pages reinforce it and it reads like consensus.

Linting helps, but the AI running the lint has the same blind spots as the AI that made the error. It will not catch its own reasoning failure - only the structural ones.

**What to do**

- Run Lint monthly. Not "when you remember".
- `status: reviewed` means *you* read the page. Not that the AI is happy with it. Keep it honest or the field is worthless.
- Before any decision that costs money or time, open the source in `5-Raw/` and check the claim yourself.

## 2. Hallucination does not disappear

Grounding answers in your own sources reduces invention. It does not remove it. The AI can still synthesise a connection that exists in neither source.

The danger is the packaging. A wiki page with clean markdown, `[source: ...]` citations and cross-links *looks* authoritative, so you check it less than you would check a chat reply. A citation proves the AI wrote a file name next to a claim. It does not prove the source says it.

**What to do**

- Spot-check citations against `5-Raw/` at random, especially on pages you are about to act on.
- Treat `source_count: 1` pages as one person's opinion, because that is what they are.

## 3. Context ceiling

The index-first approach works to roughly 100 pages on one domain - that is where Karpathy's own wiki sits. Past that the index stops being a sufficient map, the agent starts reading whole pages to answer one question, and cost and latency go up while answer quality goes down.

Long inputs also degrade in the middle. Things buried mid-document get deprioritised. Your query results will have blind spots.

**What to do**

- One vault per domain. Two unrelated research areas means two vaults, not one with subfolders.
- Keep `index.md` descriptions to one line. It is a map, and a map you have to read in full is not a map.

## 4. Cost

Every ingest, query and lint spends tokens. A single source that properly touches ten pages is not a cheap operation, and doing it right is more expensive than doing it badly.

**What to do**

- Frontier model for ingest and hard queries. A cheaper model is fine for mechanical updates and for reformatting.
- Batch mode is cheaper and produces worse pages. Use it for backlog, not for sources you care about.

## 5. Single-model blind spot

The entire wiki is one model's reading of your sources, with that model's tendencies baked in. You will not see the bias, because everything you read has been through the same filter.

**What to do**

- For a decision that matters, ask the same question of a second model against the same wiki, and compare. Where they disagree is where to look.

---

## Why it is still worth it

Humans abandon wikis because the maintenance grows faster than the value. It feels great for two weeks and then the upkeep kills it. LLMs do not get bored, do not forget to update a cross-reference, and will touch fifteen files in one pass without complaining.

That is the whole trade. Just do not confuse a tidy wiki with a correct one.
