# M5 Inference Algorithm Core Alignment

**Purpose:** Convert the ExploreTitan scientific framing, `MODIFICATION_DESIGN.md`, and `Inference_Data/Scholar References.md` into a concrete inference algorithm design for the M5 module.

**Hayes science anchor:** Alexander G. Hayes, *The Lakes and Seas of Titan* ([PDF](https://sseh.uchicago.edu/doc/Hayes_2016.pdf)).

**Status:** Design bridge before implementation. This document explains what the first M5 inference algorithm should do and why each part is scientifically justified.

---

## 1. Core Alignment

The M5 implementation should not begin as a neural network or mission-control simulator. It should begin as a controlled inference experiment:

> Given sparse local radar / EM observations over a synthetic Titan subsurface, compare a centralized MAP inversion against a distributed local-agent inversion fused through the M5 communication topology.

This directly supports the `PROJECT_BASE.md` research questions:

| Project question | Algorithm requirement | M5 implementation target | Reference support |
|---|---|---|---|
| Accuracy | Compare distributed reconstruction against centralized reconstruction | Experiment 01 vs Experiment 02 | Hothorn ensemble framing; Boukabara hybrid ML / physics framing |
| Communication | Measure how message limits change convergence | Experiment 03 with `msg_budget` and M5 compression | Gardill edge data spaces; Olfati-Saber consensus stability |
| Coherence | Test when local agreement becomes a globally coherent map | Experiment 04 and `local_global_gap` | Olfati-Saber spanning-tree / connectivity theory |
| Titan realism | Keep observation and priors physically plausible | `environment.py`, `forward_model.py`, `inversion.py` priors | Hayes Titan lake / radar / liquid constraints |

---

## 2. First Algorithmic Claim

The first defensible algorithmic claim is:

> M5 can act as a selective belief-exchange layer that preserves enough communication structure for distributed hydrogeophysical MAP estimates to approach a centralized reconstruction baseline under sparse Titan-like observations.

This claim is narrow enough to implement and test. It avoids unsupported operational claims about autonomous Titan drones, while preserving the project contribution: distributed geophysical inference under constraints.

---

## 3. Data Model

Each grid cell in `TitanGrid` should hold the hidden truth state:

```python
m_true[i] = {
    "depth": depth_i,
    "porosity": porosity_i,
    "hydrocarbon_fraction": hydrocarbon_fraction_i,
    "dielectric_constant": dielectric_constant_i,
}
```

Each agent observes only local or sparse measurements:

```python
d_i = {
    "radar": radar_return_i,
    "em": em_response_i,
    "sigma": observation_uncertainty_i,
}
```

Each agent maintains a local belief vector:

```python
theta_i = [
    depth_estimate,
    porosity_estimate,
    hydrocarbon_fraction_estimate,
    dielectric_constant_estimate,
    posterior_uncertainty,
]
```

The first implementation should keep this vector small and interpretable. That makes RMSE, uncertainty, and communication cost easy to verify before adding more complex physics or ML.

---

## 4. Layer-by-Layer Algorithm Design

### Layer 1: Synthetic Titan Environment

**Module target:** `src/environment.py`

Generate or load a small synthetic Titan subsurface grid. Phase 1 should use a 10 x 10 or 20 x 20 grid.

Required fields:

| Field | Purpose |
|---|---|
| `x`, `y` | Spatial position |
| `depth` | Reservoir or layer depth |
| `porosity` | Available pore volume |
| `hydrocarbon_fraction` | Liquid methane / ethane occupancy proxy |
| `dielectric_constant` | Radar / EM response driver |

Hayes alignment:

- Titan liquids are methane / ethane / nitrogen mixtures, not water.
- Titan hydrocarbon reservoirs have low microwave loss relative to terrestrial groundwater.
- Lake and basin structure should be treated as clustered and spatially uneven, not uniformly random.

Phase 1 simplification:

Use generated fields with smooth spatial structure plus clustered reservoir regions. Do not require real Cassini masks until Phase F.

---

### Layer 2: Forward Observation Model

**Module target:** `src/forward_model.py`

Forward model goal:

```python
d = G(m_true) + noise
```

Phase 1 functions:

```python
def forward_radar(dielectric_constant, hydrocarbon_fraction, params):
    """Approximate radar return from dielectric contrast and liquid fraction."""

def forward_em(depth, porosity, params):
    """Approximate EM attenuation from depth and pore structure."""

def forward_model(truth, materials, noise_config, sparsity_mask=None):
    """Generate sparse local observations for agents."""
```

Hayes alignment:

Use Hayes as the physical guide for Titan-specific constraints:

| Hayes concept | Algorithm use |
|---|---|
| Low liquid loss tangent | Keep radar attenuation low for hydrocarbon-rich regions |
| Methane / ethane / nitrogen ternary liquids | Parameterize liquid mixture effects instead of water assumptions |
| Altimetry uncertainty | Inject observation uncertainty into `sigma` |
| Basin clustering | Build non-uniform spatial priors and test sparse coverage |

Phase 1 simplification:

The first forward model can be linear and noisy. It only needs to produce observations that are sensitive to the hidden state.

---

### Layer 3: Centralized and Local MAP Inversion

**Module target:** `src/inversion.py`

Centralized baseline:

```text
min_m ||W_d (d - G(m))||^2 + alpha ||L m||^2 + lambda * physics_penalty(m)
```

Local agent inversion:

```text
min_theta_i ||W_i (d_i - G_i(theta_i))||^2
            + alpha ||theta_i - prior_i||^2
            + lambda * physics_penalty(theta_i)
```

Physics penalty should enforce simple invariants:

| Constraint | Reason |
|---|---|
| `0 <= porosity <= 1` | Porosity is a fraction |
| `0 <= hydrocarbon_fraction <= porosity` | Liquid cannot exceed available pore volume |
| dielectric bounds from materials | Prevent impossible material estimates |
| optional phreatic prior | Hayes-based liquid level / basin consistency |

Reference support:

- Boukabara supports hybrid physics plus ML / optimization constraints.
- Hayes supports Titan-specific prior constraints.
- Hothorn supports treating local inversions as weak estimators that can be fused.

Phase 1 simplification:

Use deterministic MAP / least-squares first. Add posterior sampling only after Experiment 01 and 02 run reliably.

---

### Layer 4: M5 Communication and Distributed Fusion

**Module targets:** existing M5 protocol plus `src/distributed_fusion.py`

The existing M5 protocol should remain the topology layer:

| Existing M5 output | Inference use |
|---|---|
| `critical_nodes` | Agents whose beliefs get priority message slots |
| `significant_edges` | Must-preserve belief exchange links |
| `compressed_graph` | Community-level belief exchange graph |
| `partitions` | Super-node aggregation groups |

Distributed consensus update:

```python
for k in range(max_iter):
    for node in agents:
        local = local_invert(obs[node], prior=beliefs[node])
        neighbor = weighted_neighbor_mean(beliefs, node, graph=m5_graph)
        beliefs[node] = (1 - beta) * local + beta * neighbor
    if converged(beliefs, tol):
        break
```

Olfati-Saber alignment:

Use graph consensus theory to choose stable update behavior:

```text
theta_i(k+1) = theta_i(k) + epsilon * sum_j a_ij * (theta_j(k) - theta_i(k))
```

Stability guard:

```text
0 < epsilon < 1 / Delta
```

where `Delta` is the maximum node degree in the active communication graph.

Interpretation:

- If the graph fragments, local clusters may agree internally but fail globally.
- If M5 compression preserves critical bridges, distributed inference should keep better global coherence.
- If message budget is too low, RMSE and `local_global_gap` should degrade.

---

### Layer 5: Evaluation

**Module target:** `src/evaluation.py`

Metrics should match `PROJECT_BASE.md` and `MODIFICATION_DESIGN.md`:

| Metric | Meaning | Experiment |
|---|---|---|
| `rmse` | Reconstruction error against synthetic truth | All |
| `coverage` | Fraction of grid below uncertainty threshold | All |
| `uncertainty_reduction` | Posterior uncertainty decrease over iterations | 02-04 |
| `comm_cost` | Messages x estimated bytes | 03-04 |
| `converged` | Stable belief map within horizon | 02-04 |
| `local_global_gap` | Local agreement minus global correctness | RQ3 |
| `inference_preservation` | Compressed graph performance vs full graph | M5 Stage 3 extension |

Critical distinction:

Stable graph metrics alone are not enough. The M5 Stage 3 output must report inference preservation, not only network efficiency preservation.

---

## 5. Experiment Matrix

| Experiment | Purpose | Algorithm path | Primary result |
|---|---|---|---|
| 01 | Centralized baseline | `forward_model -> centralized_invert -> evaluate` | RMSE ceiling |
| 02 | Distributed full communication | `local_invert_all -> full_graph_consensus -> evaluate` | Distributed vs centralized gap |
| 03 | Communication-constrained M5 | `local_invert_all -> execute_m5_protocol -> selective_consensus` | RMSE vs communication cost |
| 04 | Network failure | `run_percolation_test -> failure_consensus -> evaluate` | RMSE degradation under topology loss |

Implementation rule:

Do not start Experiment 03 or 04 until Experiment 01 produces a valid RMSE on synthetic truth and Experiment 02 runs on the same grid.

---

## 6. Reference-to-Algorithm Crosswalk

| Scholar reference | Keep for algorithm | Do not overuse yet |
|---|---|---|
| Hothorn | Ensemble logic, weak local learners, OOB validation | Do not implement full Random Forest first |
| Boukabara | Physics-constrained loss, forward-model emulation framing, uncertainty | Do not train ML emulators before the stub works |
| Krejcar | Feature compression and multimodal fusion ideas | Do not start with CNN / autoencoder implementation |
| Hayes | Titan liquid, basin, radar, altimetry, and composition priors | Do not rely on the poor PDF text extraction as the only source |
| Gardill | Quantization, lookahead sensing, edge data-space constraints | Use later for message limits and selective sampling |
| Olfati-Saber | Laplacian consensus, step-size stability, spanning-tree coherence | Use immediately for distributed fusion |

Note: `Scholar References.md` holds one canonical entry per paper (Hayes 2016 is the Titan science anchor for Layers 1–2, 3 priors, and 5 observation noise).

---

## 7. First Build Sequence

### Phase A: Minimal Data Inputs

Create:

- `data/environments/environment_001.csv`
- `data/materials/titan_materials.csv`

Success:

- Loader returns a validated DataFrame with required fields.

### Phase B: Forward Model Stub

Create:

- `forward_radar()`
- `forward_em()`
- `forward_model()`

Success:

- Observations generated for every observed grid cell.

### Phase C: Centralized Inversion

Create:

- `centralized_invert()`
- `evaluate_rmse()`

Success:

- Experiment 01 logs RMSE against synthetic truth.

### Phase D: Local Inversion and Full Consensus

Create:

- `local_invert()`
- `local_invert_all()`
- `distributed_consensus()`

Success:

- Experiment 02 runs and reports distributed-vs-centralized gap.

### Phase E: M5 Integration

Wire:

- `build_agent_graph()`
- `execute_m5_protocol()`
- `selective_consensus()`
- `failure_consensus()`

Success:

- Experiment 03 reports RMSE vs `comm_cost`.
- Experiment 04 reports RMSE under graph degradation.
- M5 Stage 3 includes inference preservation percentage.

---

## 8. Minimal Orchestrator Contract

```python
def run_exploretitan_experiment(config):
    truth = load_environment(config.env_path)
    materials = load_materials(config.materials_path)
    obs = forward_model(truth, materials, config.noise, config.sparsity_mask)

    centralized = centralized_invert(obs, config)
    local_beliefs = local_invert_all(obs, config)

    graph = build_agent_graph(truth, comm_radius=config.comm_radius)
    m5 = execute_m5_protocol(graph, preserve_top_k=config.preserve_top_k)

    if config.mode == "centralized":
        predicted = centralized
    elif config.mode == "distributed_full":
        predicted = distributed_consensus(local_beliefs, graph, config)
    elif config.mode == "distributed_constrained":
        predicted = selective_consensus(local_beliefs, m5, config)
    elif config.mode == "network_failure":
        predicted = failure_consensus(local_beliefs, m5, config)

    return evaluate(truth, predicted, centralized, m5, config)
```

---

## 9. Definition of Algorithmic Done

The inference algorithm is ready for the first research run when:

- `centralized_invert()` reconstructs a 10 x 10 synthetic grid with logged RMSE.
- `local_invert_all()` produces one belief vector per agent.
- `distributed_consensus()` reduces disagreement over iterations.
- `selective_consensus()` uses M5 outputs rather than the full graph.
- `evaluate()` reports RMSE, coverage, uncertainty, communication cost, convergence, and local-global gap.
- Stage 3 reports inference preservation, not just graph metric preservation.

---

## 10. Design Boundary

This algorithm supports the intended claim:

> We developed a reproducible simulation framework for evaluating distributed hydrogeophysical inference under Titan-like observation constraints.

It does not claim:

> We designed operational autonomous Titan drones.

That distinction should remain visible in implementation, experiments, and final writing.
