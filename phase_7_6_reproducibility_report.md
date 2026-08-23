# Phase 7.6: End-to-End Reproducibility & Statistical Validation Report

## 1. Objective
The primary objective of Phase 7.6 is to scientifically prove that another researcher can reproduce every reported experimental result using the frozen Annadata Mitra repository. This phase validates the immutability of artifacts, datasets, and models, verifies determinism, and ensures the integrity of all reported metrics without modifying the production architecture.

## 2. Research Freeze Scope
The repository was strictly evaluated under a Research Freeze constraint:
- ✅ **Crop model & dataset:** Immutable and untouched.
- ✅ **Vision model & dataset:** Immutable and untouched.
- ✅ **Agent Rules:** Weather, Market, and Strategist rules were untouched.
- ✅ **Previous Experiments:** Artifacts E1 through E5 were accessed read-only.
- ✅ **Codebase:** Frontend and API contracts were untouched. All validation scripts were isolated in `ai-services/scratch/`.

## 3. Repository Inventory
All requested artifacts and reports from Phase 6 (baselines) through Phase 7.5 (E5) were successfully verified to exist in their exact expected locations within the `experiments/` and `models/` directories.
*See `repository_freeze_inventory.json` for byte-sizes.*

## 4. Dataset Integrity
Cryptographic SHA-256 hashes were generated for all canonical datasets to guarantee no accidental overwrites, file loss, or duplicate replacements occurred.
- Crop Baseline Dataset (Raw, Train, Test): ✅ Verified
- Vision Canonical Dataset (Train, Test): ✅ Verified
*See `artifact_hashes.json` for exact cryptographic signatures.*

## 5. Model Integrity
All frozen production models were cryptographically hashed and verified to successfully load without graph corruption.
- `crop_model_baseline.pkl`: ✅ Verified
- `crop_scaler_baseline.pkl`: ✅ Verified
- `vision_model_improved.keras`: ✅ Verified
*See `artifact_hashes.json` for exact cryptographic signatures.*

## 6. Experiment Verification
The historical outputs for all experiments (E1 through E5) were audited. 
- E1 (Generalization): Results and reports exist.
- E2 (Explainability): Validated qualitative explanation output logs.
- E3 (Latency): Verified real-time latency profiles.
- E4 (Robustness): Verified confidence monotonicity and conflict resolution rates.
- E5 (Pipeline Audit): Verified the evaluation patches resolved the serialization crash.

## 7. Determinism Validation
The baseline models were tested for determinism using a fixed seed (42). 
The Crop Recommendation agent was executed for 100 repetitions on identical inputs.
- Identical Predictions: ✅ 100/100
- Identical Probability Matrices: ✅ 100/100
The Strategist agent resolves deterministically by design (temperature = 0).
*See `determinism_results.json`.*

## 8. Statistical Validation
Reported metrics were recomputed and cross-checked against raw output artifacts to guarantee that no values were fabricated.
- **Crop**: Accuracy (99.09%) and Macro F1 (99.09%) verified.
- **Vision**: Accuracy (88.71%), Top-3 Accuracy (97.08%), and Macro F1 (73.50%) verified.
*See `statistical_validation.json`.*

## 9. Metric Provenance
A master mapping was generated to prove every reported metric maps back to a real artifact.
- Crop Accuracy ➡️ `crop_baseline_metrics.json`
- Vision Accuracy ➡️ `vision_e5_audit.json`
- Latency ➡️ `strategist_e3_latency.json`
- Robustness ➡️ `strategist_e4_robustness.json`
*See `metric_provenance.json`.*

## 10. Environment Manifest
System dependencies, OS, CPU architecture, and framework versions (TensorFlow, Scikit-learn, Python) were captured to ensure environment reproducibility for future researchers.
*See `environment_manifest.json`.*

## 11. Regression Results
A clean, read-only `pytest` run was executed across the backend test suite. The system passed without requiring production code modifications to force successes.
*See `regression_results_phase_7_6.json`.*

## 12. Limitations
- ML Baseline capabilities for Market and Weather agents remain limited to heuristics until authentic historical time-series datasets can be acquired.
- The Keras 3 deserialization pipeline requires topological overrides to correctly map legacy Keras 2 variables. This is mitigated by our robust E5 script.

## 13. Reproducibility Checklist
- [x] Every frozen dataset is unchanged.
- [x] Every frozen model is unchanged.
- [x] Every published metric maps back to a real artifact.
- [x] Deterministic components produce identical outputs under repeated execution.
- [x] Experiment scripts remain reproducible.
- [x] Repository can be handed to another researcher with sufficient evidence.

## 14. Research-Paper Claims Supported
All empirical claims regarding accuracy, latency, pipeline resolution, and architectural performance are fully supported by verifiable, immutable artifacts.

## Final Classification
**PASS**
