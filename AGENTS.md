# Permanent Engineering Rules & Agent Guidelines

## 1. Project Identity & Scientific Integrity
- **Scientific Research System**: This is the Environmental Monitoring research project. Treat the repository as a rigorous scientific/research decision-support system, not a demo or prototype mockup.
- **Zero Fabrication Policy**: Never fabricate data, coordinates, imagery, metrics, labels, boundaries, model results, or project statistics under any circumstances.
- **No Coordinate Hardcoding**: Never hard-code geographic coordinates, bounds, or offsets to make maps or UI components "look right". Map visualizations must render real geometries and coordinates from authoritative artifacts.
- **Authoritative Data Precedence**: Always use authoritative project artifacts where they exist. If authoritative data conflicts with an assumption or expectation, preserve the authoritative data and clearly explain the discrepancy.
- **No Guessing**: If something cannot be verified against artifacts, code, or tests, explicitly report it as unverified instead of guessing.

---

## 2. Immutability & ML Artifact Boundaries
- **Frozen Artifacts (Features 8–11)**: All Feature 8–11 datasets, models, weights, evaluation metrics, candidate patches, and prioritization queues are frozen and read-only unless explicitly instructed otherwise.
- **No UI-Driven Model Retraining**: Never retrain models merely to solve a dashboard, visualization, or UI problem.
- **No Dataset Tampering**: Never modify frozen ML datasets, prediction files, or checkpoints to make frontend outputs match expectations.
- **No Sample/Mock Data in Production Paths**: Never replace real project data with demo, synthetic, or mock sample data.
- **Backend Mutation Ban**: The backend (`dashboard/backend/`) is a read-only projection layer and must not mutate or write into ML artifacts or raw datasets.
- **Frontend ML Ban**: The frontend (`dashboard/frontend/`) must not perform ML inference, compute statistical metrics, or modify scientific data.
- **Integrity & Checksums**: Verify dataset/artifact checksums and integrity after any changes affecting the data projection pipeline or dashboard ingestion.

---

## 3. Scientific Interpretation & Claim Boundaries
- **Candidate & Ranking Signal**: CNN outputs represent candidate/ranking signals indicating spatial-temporal anomalies warranting further investigation.
- **No Legal / Compliance Claims**: Never claim environmental non-compliance, illegal activity, unauthorized land use, causality, or intent from CNN predictions.
- **Proxy Evidence vs Ground Truth**: NDVI trends and Dynamic World land cover transition metrics are supporting proxy evidence, NOT ground truth.
- **Decision-Support Classification**: The dashboard is a read-only decision-support system designed to assist human investigators, not an automated compliance determination engine.

---

## 4. Software Engineering & Verification Standards
- **Inspect Before Modifying**: Before changing existing functionality or fixing bugs, inspect the current implementation, dependencies, and file contents.
- **Empirical Verification Required**: Run actual unit tests, build commands, and browser/runtime verifications before reporting `PASS`. Never declare `PASS` based solely on static code inspection.
- **Maintainable & Minimal Architecture**: Prefer simple, robust, and maintainable architecture over unnecessary layers or complexity.

---

## 5. Workflow for Future AI Sessions & Agents

### At the Start of Every Session:
1. Read [`AGENTS.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/AGENTS.md).
2. Read [`docs/PROJECT_CONTEXT.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/docs/PROJECT_CONTEXT.md).
3. Inspect current repository and filesystem state (git status, directory contents, configuration files).
4. Identify the active feature and current progress.
5. Do NOT repeat or modify already completed, validated features.
6. Do NOT assume chat history contains the complete project context.
7. Continue strictly from the documented **CURRENT NEXT TASK**.

### After Completing a Feature / Task:
1. Update [`docs/PROJECT_CONTEXT.md`](file:///c:/Users/anshk/Desktop/Environmental-Monitoring/docs/PROJECT_CONTEXT.md) with:
   - Feature number and descriptive title
   - Final status
   - Files created, modified, or deleted
   - Automated tests and verification executed
   - Key architectural or technical decisions
   - Known limitations or audit findings
   - Next planned feature
2. Maintain historical context without deleting past feature records.
3. Keep the documentation concise, structured, and authoritative.
