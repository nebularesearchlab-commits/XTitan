# XTitan

**Distributed Hydrogeophysical Inference for Titan Subsurface Exploration**

Reproducible simulation framework for evaluating distributed geophysical inference in Titan-like environments under communication and observational constraints.

## Research focus

- Synthetic Titan subsurface environments (cryogenic materials, hydrocarbon reservoirs, porous ice)
- Forward geophysical models (radar, EM/dielectric, gravimetric signals)
- Distributed autonomous sensing with M5-style belief exchange
- Centralized vs. distributed reconstruction comparison

## Documentation

| File | Purpose |
|------|---------|
| [`PROJECT_BASE.md`](PROJECT_BASE.md) | Formal scientific project base |
| [`ExploreTitan Experiment.md`](ExploreTitan%20Experiment.md) | Experiment abstract |
| [`Explore Titan Research.md`](Explore%20Titan%20Research.md) | Research framing and architecture |
| [`AUDIO_EXTRACTION_PROMPT.md`](AUDIO_EXTRACTION_PROMPT.md) | Prompt for extracting seminar audio into experiment inputs |

## Repository layout (planned)

```
data/           # Synthetic Titan environments
src/            # environment, forward_model, drone_agent, m5_network, inversion, evaluation
experiments/    # Centralized, distributed, constrained, failure scenarios
results/        # Generated maps, metrics, figures (gitignored)
notebooks/      # Visualization
```

## License

MIT — see [LICENSE](LICENSE).
