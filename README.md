# AI Glossary Widget

A comprehensive offline AI reference with **183 concepts** across foundations, models, training, agents, security, evaluation, operations, and governance. Available as both a compact desktop widget and a fully static webpage—no dependencies, no network, no tracking.

## Two Ways to Use

### Desktop Widget (Python + Tk)

**Run immediately:**
```bash
./run.sh
```

Or run directly:
```bash
python3 app.py
```

Requires Python 3.10+ and Tk 8.6+ (usually pre-installed).

**Add to Linux application menu:**
```bash
./install.sh
```

Remove with:
```bash
rm "${XDG_DATA_HOME:-$HOME/.local/share}/applications/ai-glossary.desktop"
```

**Controls:**
- Type to search terms, acronyms, meanings, categories, and related concepts.
- Press `Down` from search to browse results.
- Press `Ctrl+F` or `Ctrl+L` to return to search.
- Press `Escape` to clear search, then category filter.
- Press `Ctrl+R` for a random concept.
- Toggle **Keep on top** to pin or unpin the window.
- Hover over any related term to click and navigate.

### Static Webpage

**Open `index.html` in any browser.** Works fully offline once loaded.

**Features:**
- Search by term, alias, meaning, or category.
- Real-time result filtering.
- Click related terms to jump to them.
- Arrow keys to browse results.
- "Random" button to discover concepts.
- Mobile-friendly, no server required.

## Glossary Content

**183 essential AI concepts** including:
- **Foundations:** AI, Machine Learning, Deep Learning, Computer Vision, NLP, Robotics, AGI, ANI
- **Models:** Transformers, GANs, Vision Transformers, Diffusion, Embeddings, Knowledge Graphs
- **Training:** Supervised, Unsupervised, Self-Supervised, Transfer Learning, Fine-tuning, RLHF, DPO
- **Agents:** Tool Use, Planning, Multi-agent Systems, Human-in-the-Loop
- **Security:** Alignment, Bias, Explainability, Responsible AI, Prompt Injection, RAG Poisoning
- **Operations:** MLOps, LLMOps, Model Drift, Monitoring, Inference, Caching
- **Governance:** AI Ethics, Policy, AI Safety, Moderation, Model Cards

Each entry includes a clear definition, practical example, related concepts, and why the concept matters.

## Test & Validate

```bash
python3 -m unittest -v test_glossary.py
```

All tests pass with 183 unique entries and full relationship integrity checked.