# AI Glossary

A comprehensive static AI reference with **183 concepts** across foundations, models, training, agents, security, evaluation, operations, and governance. It has no dependencies, network requests, or tracking.

## Website

Visit the published site at [vinayak-g87.github.io/ai-glossary](https://vinayak-g87.github.io/ai-glossary/). The self-contained `index.html` can also be opened directly for offline use.

Features:
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

## Future Desktop Version

The earlier Python and Tk desktop implementation is retained in `future/` for possible later development. It is not required by the GitHub Pages site.

Run it with Python 3.10+ and Tk 8.6+:

```bash
./future/run.sh
```

Run its tests with:

```bash
cd future
python3 -m unittest -v test_glossary.py
```

All tests pass with 183 unique entries and full relationship integrity checked.