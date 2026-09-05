# AI-Based Multi-Temporal Land-Cover Change Detection and Boundary Disturbance Monitoring System

## PARIVESH Data Inventory

The PARIVESH Data Inventory utility (`src/data_inventory.py`) scans all raw environmental project datasets inside `data/raw/` (`Gondkhari`, `Gadchiroli`, and `Bhivpuri PSP`) and catalogs available documents and KML files without modifying the raw dataset.

### Running the Inventory Utility

From the project root directory, run:

```bash
python src/data_inventory.py
```

### Output Location

The inventory catalog is saved to:

```text
data/processed/data_inventory.csv
```

## PARIVESH Project Metadata & Boundary Audit

The Metadata & Boundary Audit utility (`src/metadata_audit.py`) extracts verified project details, clearance information, and candidate spatial boundary KML files directly from real PARIVESH documents and maps for all approved projects.

### Running the Metadata Audit Utility

From the project root directory, run:

```bash
python src/metadata_audit.py
```

### Output Locations

- `data/processed/project_metadata.csv`: Project identities, types, coordinates, areas, clearance status, and boundary statuses.
- `data/processed/boundary_candidates.csv`: Itemized candidate spatial KML/KMZ boundary files.

## KML Geometry Validation & Boundary Selection

The Boundary Validation utility (`src/boundary_validation.py`) parses candidate spatial geometries, reprojects coordinates to local projected UTM coordinate reference systems (EPSG:32643 / EPSG:32644), validates topology, cross-references stated PARIVESH document areas, and exports verified monitoring boundaries to GeoJSON.

### Running the Boundary Validation Utility

From the project root directory, run:

```bash
python src/boundary_validation.py
```

### Output Locations

- `data/processed/boundary_validation.csv`: Detailed validation report comparing calculated projected areas against document reference areas.
- `data/processed/project_boundaries/`: Validated GeoJSON spatial boundary files:
  - `gondkhari_boundary.geojson`
  - `gadchiroli_boundary.geojson`
  - `bhivpuri_boundary.geojson`

## Google Earth Engine Satellite Data Pipeline

The Satellite Pipeline utility (`src/satellite_pipeline.py`) connects to Google Earth Engine (`aqueous-aileron-505816-s1`) to extract, cloud-filter, and composite real multi-spectral Sentinel-2 (`COPERNICUS/S2_SR_HARMONIZED`) and Dynamic World (`GOOGLE/DYNAMICWORLD/V1`) observations for all three project boundaries across the 2021–2026 monitoring period.

### Running the Satellite Pipeline

From the project root directory, run:

```bash
python src/satellite_pipeline.py
```

### Output Locations

- `data/processed/satellite/satellite_metadata.csv`: Dataset provenance log recording scene availability, cloud filter counts, composite methods, actual date ranges, and band configurations.
- `data/processed/satellite/<project_id>/`: Composited GeoTIFF rasters (2021–2026):
  - `sentinel2_<year>.tif` (6 Base Multi-spectral Bands: B2, B3, B4, B8, B11, B12)
  - `dynamicworld_<year>.tif` (Reference baseline mode land-cover label)

## Monsoon Satellite Data Audit (June–October)

The Monsoon Audit utility (`src/monsoon_audit.py`) performs an empirical month-by-month Google Earth Engine audit of Sentinel-2 availability and pixel-level SCL cloud/shadow masked boundary coverage for June, July, August, September, and October across 2021–2026.

### Running the Monsoon Audit

From the project root directory, run:

```bash
python src/monsoon_audit.py
```

### Output Location

- `data/processed/satellite/monsoon_audit.csv`: Empirical monthly scene counts, SCL cloud-masked boundary pixel coverage percentages, and usability statuses.

## Real NDVI & Vegetation Baseline Analysis

The NDVI Analysis utility (`src/ndvi_analysis.py`) calculates real Sentinel-2 NDVI baselines ($\text{NDVI} = \frac{B8 - B4}{B8 + B4}$) using actual surface-reflectance raster data across all three project boundaries (2021–2026). It calculates distribution metrics, investigates candidate vegetation thresholds ($0.20, 0.25, 0.30, 0.35, 0.40$), calculates metric projected vegetation areas in hectares using UTM reprojection (`EPSG:32644` / `EPSG:32643`), and computes year-over-year baseline changes.

### Running the NDVI Analysis

From the project root directory, run:

```bash
python src/ndvi_analysis.py
```

### Output Locations

- `data/processed/vegetation/spatial_integrity_audit.csv`: Polygon boundary spatial area integrity audit log.
- `data/processed/vegetation/ndvi_statistics.csv`: Annual polygon-masked NDVI distribution summary.
- `data/processed/vegetation/ndvi_candidate_thresholds.csv`: Sensitivity analysis of candidate classification thresholds (0.20 to 0.40).
- `data/processed/vegetation/ndvi_change_analysis.csv`: Year-over-year baseline changes in median NDVI and vegetation area.
- `data/processed/vegetation/ndvi/<project_id>/ndvi_<year>.tif`: Derived spatial NDVI GeoTIFF rasters (EPSG:4326, 30m resolution).

## Real LULC Reference Dataset Preparation & Label Quality Audit

The LULC Dataset utility (`src/lulc_dataset.py`) extracts a high-confidence reference dataset for AI land-cover classification from Sentinel-2 multi-spectral composites and Dynamic World (`GOOGLE/DYNAMICWORLD/V1`) reference baseline labels across historical years (2021–2025). It filters samples using $3 \times 3$ neighborhood class homogeneity ($\text{confidence} \ge 0.60$), excludes water/clouds/unclassified pixels, performs spectral diagnostic checks (`NDVI`, `NDWI`, `NDBI`), and enforces spatially contiguous sub-grid block splits (`train`, `val`, `test`) with physical distance verification.

### Running Dataset Generation & Quality Audit

From the project root directory, run:

```bash
python src/lulc_dataset.py
```

### Output Locations

- `data/processed/training/training_samples.csv`: Patch-safe high-confidence reference training samples (79,406 multi-temporal observations / 17,540 unique spatial locations) containing WGS84 coordinates, grid positions, multi-spectral bands (`B2, B3, B4, B8, B11, B12`), `NDVI`, `NDWI`, `NDBI`, `dynamic_world_class`, `dynamic_world_confidence`, `spatial_block`, and `spatial_split` (`train`, `val`, `test`).
- `data/processed/training/class_availability_audit.csv`: Dynamic World raw class availability and pixel percentage audit across all 9 classes (2021–2025).
- `data/processed/training/bare_land_pipeline_trace.csv`: Full stage-by-stage pipeline trace of candidate bare land pixels across raw, confidence-filtered, and spatial-split stages.
- `data/processed/training/spatial_temporal_validation.csv`: Empirical spatial distance metric audit (UTM projected meters), CNN patch safety audit ($15 \times 15$ & $33 \times 33$), and temporal split consistency audit.
- `data/processed/training/freeze/`: Immutable freeze artifacts (`feature6_freeze_report.md`, `feature6_checksums_sha256.csv`, `feature6_freeze_metadata.json`). Feature 6 status: **FROZEN / PASS**.

## Multi-Spectral Temporal Change Baseline

The Multi-Spectral Change utility (`src/multispectral_change.py`) calculates polygon-masked NDWI ($\frac{B3 - B8}{B3 + B8}$) and NDBI ($\frac{B11 - B8}{B11 + B8}$) GeoTIFF rasters and computes year-over-year temporal delta rasters ($\Delta\text{NDVI}, \Delta\text{NDWI}, \Delta\text{NDBI}$) across consecutive historical baseline years (2021$\rightarrow$2022, 2022$\rightarrow$2023, 2023$\rightarrow$2024, 2024$\rightarrow$2025). Statistics are computed strictly inside validated project boundaries.

### Running Multi-Spectral Change Analysis

From the project root directory, run:

```bash
python src/multispectral_change.py
```

### Output Locations

- `data/processed/change/indices/<project_id>/ndwi_<year>.tif`: Polygon-masked spatial NDWI GeoTIFF rasters (EPSG:4326, 30m resolution).
- `data/processed/change/indices/<project_id>/ndbi_<year>.tif`: Polygon-masked spatial NDBI GeoTIFF rasters (EPSG:4326, 30m resolution).
- `data/processed/change/temporal/<project_id>/delta_<from>_<to>_<index>.tif`: Temporal index difference rasters ($\Delta\text{NDVI}, \Delta\text{NDWI}, \Delta\text{NDBI}$).
- `data/processed/change/multispectral_change_statistics.csv`: Annual temporal change statistics (mean, median, std, p10, p25, p75, p90, min, max, valid area in ha).
- `data/processed/change/multispectral_change_audit.csv`: Source Sentinel-2 raster band verification, pixel validity, and output existence audit.
- `data/processed/change/multispectral_change_spatial_integrity_audit.csv`: Metric UTM polygon-masked spatial area audit matching Feature 5 baselines.
- `data/processed/change/feature7_1_correction_report.md`: Detailed correction report. Status: **PASS — spatially and temporally valid**.

## Historical Change Signal & Disturbance Candidate Detection

The Candidate Detection utility (`src/candidate_detection.py`) evaluates empirical baseline distributions of multi-spectral change ($\Delta\text{NDVI}, \Delta\text{NDWI}, \Delta\text{NDBI}$) across historical baseline transitions ($2021\rightarrow2022, 2022\rightarrow2023, 2023\rightarrow2024, 2024\rightarrow2025$). It classifies transparent multi-spectral anomaly candidates ($\ge 2$ independent signals, e.g. vegetation loss + built-up increase), tracks multi-year temporal persistence, groups neighboring pixels into spatial clusters, and integrates Feature 6 LULC labels as reference context.

*Scientific Safety Disclaimer: This system identifies statistically unusual spectral change candidates. It does NOT establish causality, illegal activity, environmental violation, or confirmed land-use change.*

### Running Candidate Detection Pipeline

From the project root directory, run:

```bash
python src/candidate_detection.py
```

### Output Locations

- `data/processed/change/historical_change_distribution.csv`: Historical transition percentile distributions ($p_{01}, p_{05}, p_{10}, p_{25}, p_{75}, p_{90}, p_{95}, p_{99}$, mean, median, std).
- `data/processed/change/change_threshold_sensitivity.csv`: Empirical threshold sensitivity analysis across lower/upper tail percentiles.
- `data/processed/change/change_pixel_signals.csv`: Pixel-level standardized anomaly signals and Feature 6 LULC context map.
- `data/processed/change/disturbance_candidates.csv`: Project-level candidate pixel and spatial area summary.
- `data/processed/change/disturbance_candidate_clusters.csv`: Spatial candidate clusters (8-neighbor connected components, area in ha, centroids).
- `data/processed/change/candidates/<project_id>/candidate_<from>_<to>.tif`: Annual candidate category GeoTIFF rasters.
- `data/processed/change/candidates/<project_id>/persistent_candidate.tif`: Multi-year persistent candidate GeoTIFF rasters.
- `data/processed/change/feature7_2_correction_report.md`: Comprehensive Feature 7.2.1 bug fix and regression report. Status: **PASS — all 15 regression acceptance criteria satisfied**.
- `data/processed/change/freeze/`: Immutable freeze artifacts (`feature7_2_freeze_report.md`, `feature7_2_checksums_sha256.csv`, `feature7_2_freeze_metadata.json`). Feature 7.2 status: **FROZEN / PASS**.

## Candidate Validation & Disturbance Evidence Analysis

The Candidate Validation utility (`src/candidate_validation.py`) evaluates rule-based multi-source evidence scores across five independent dimensions (spectral persistence, Dynamic World LULC transitions, multi-spectral index agreement, spatial coherence, and robust change magnitude) for all 386 Feature 7.2 candidate clusters across historical baseline years (2021–2025).

*Scientific & Legal Safety Disclaimer: This system evaluates rule-based disturbance evidence strength across multi-source spatial datasets. It does NOT establish causality, illegal activity, environmental violation, or unauthorized land use.*

### Running Candidate Validation Pipeline

From the project root directory, run:

```bash
python src/candidate_validation.py
```

### Output Locations

- `data/processed/change/validation/candidate_evidence_validation.csv`: Cluster-level evidence dimension scores, weighted total score, and category.
- `data/processed/change/validation/candidate_evidence_summary.csv`: Project-level evidence category summary (Cat 0 to Cat 4).
- `data/processed/change/validation/candidate_lulc_transitions.csv`: Dynamic World reference LULC class transitions and confidence.
- `data/processed/change/validation/candidate_spectral_evidence.csv`: Cluster median index change metrics ($\Delta\text{NDVI}, \Delta\text{NDWI}, \Delta\text{NDBI}$) and signal agreement counts.
- `data/processed/change/validation/candidate_spatial_evidence.csv`: Spatial metric 30m cluster area, pixel count, and centroid coordinates.
- `data/processed/change/validation/feature7_3_validation_report.md`: Comprehensive Feature 7.3 validation report. Status: **PASS — all 16 acceptance criteria satisfied**.
- `data/processed/change/validation/audit/`: Audit artifacts (`feature7_3_methodology_audit.csv`, `feature7_3_threshold_sensitivity.csv`, `feature7_3_component_dependence.csv`, `feature7_3_score_reconstruction.csv`, `feature7_3_methodology_audit_report.md`). Status: **PASS — scientifically and computationally defensible**.
- `data/processed/change/validation/freeze/`: Immutable freeze artifacts (`feature7_3_freeze_report.md`, `feature7_3_checksums_sha256.csv`, `feature7_3_freeze_metadata.json`). Feature 7.3 status: **FROZEN / PASS**.

## Disturbance Modeling Design & Feasibility Audit

The Modeling Feasibility Audit (`scratch/audit_feature8_design.py`) evaluates the scientific feasibility of building a research-level disturbance classification model using multi-spectral, temporal, spatial, and LULC reference features. It audits target options, label circularity risks, class imbalance, spatial/temporal leakage, patch size safety ($15 \times 15$ vs $33 \times 33$), project generalization, feature availability, and imbalance evaluation metrics.

### Output Locations

- `data/processed/modeling/feature8_target_options.csv`: Target options audit (Option A Binary vs Option B 3-class vs Option C Evidence).
- `data/processed/modeling/feature8_label_audit.csv`: Label source & circularity mitigation audit.
- `data/processed/modeling/feature8_class_distribution.csv`: Class counts and imbalance ratios by project.
- `data/processed/modeling/feature8_leakage_audit.csv`: Spatial patch overlap & temporal repeat coordinate leakage audit.
- `data/processed/modeling/feature8_project_generalization.csv`: Project-aware generalization & landscape domain shift audit.
- `data/processed/modeling/feature8_feature_availability.csv`: Feature availability & target leakage risk matrix.
- `data/processed/modeling/feature8_patch_feasibility.csv`: $15 \times 15$ vs $33 \times 33$ patch size safety audit.
- `data/processed/modeling/feature8_model_strategy.csv`: Baseline (Random Forest/XGBoost) vs CNN deep learning strategy.
- `data/processed/modeling/feature8_modeling_design_report.md`: Feasibility design report. Decision: **READY FOR BASELINE MODEL**.

## Tabular Disturbance Baseline Model

The Tabular Disturbance Baseline pipeline (`src/disturbance_baseline.py`) trains and evaluates tabular binary disturbance-candidate classifiers (Logistic Regression, Random Forest, XGBoost) using allowed Sentinel-2 multi-spectral reflectances ($B2, B3, B4, B8, B11, B12$), derived indices ($\text{NDVI}, \text{NDWI}, \text{NDBI}$), Dynamic World reference classes, and spatial coordinates across frozen spatial splits.

*Scientific Limitation: Baseline models train against Feature 7.2 rule-derived reference labels. They function as surrogate classifiers for historical disturbance candidate patterns and do NOT establish legal violations or confirmed land-use change.*

### Running Baseline Model Pipeline

From the project root directory, run:

```bash
python src/disturbance_baseline.py
```

### Output Locations

- `data/processed/modeling/baseline/baseline_dataset_audit.csv`: Pre-model dataset verification audit.
- `data/processed/modeling/baseline/baseline_model_comparison.csv`: Model validation and test set performance metrics (Naive Majority, Logistic Regression, Random Forest, XGBoost).
- `data/processed/modeling/baseline/baseline_project_metrics.csv`: Test set performance metrics evaluated by project.
- `data/processed/modeling/baseline/baseline_feature_importance.csv`: Top predictive feature importances.
- `data/processed/modeling/baseline/baseline_predictions.csv`: Model test predictions and probabilities.
- `data/processed/modeling/baseline/baseline_confusion_matrix.csv`: Detailed confusion matrix breakdown per model and split.
- `data/processed/modeling/baseline/feature8_1_baseline_report.md`: Baseline evaluation report. Decision: **BASELINE PROMISING — SPATIAL PATCH MODEL MAY BE JUSTIFIED**.
- `data/processed/modeling/baseline/audit/`: Audit artifacts (`feature8_1_metric_correction_audit.csv`, `feature8_1_feature_leakage_audit.csv`, `feature8_1_model_comparison_corrected.csv`, `feature8_1_project_metrics_corrected.csv`, `feature8_1_correction_report.md`). Status: **PASS — PR-AUC bug fixed & spatial leakage mitigated**.
- `data/processed/modeling/baseline/robustness/`: Robustness audit artifacts (`feature8_1_2_feature_ablation.csv`, `feature8_1_2_class_weight_sensitivity.csv`, `feature8_1_2_threshold_sensitivity.csv`, `feature8_1_2_project_generalization.csv`, `feature8_1_2_spatial_block_metrics.csv`, `feature8_1_2_temporal_metrics.csv`, `feature8_1_2_bootstrap_uncertainty.csv`, `feature8_1_2_robustness_audit.csv`, `feature8_1_2_robustness_report.md`, `feature8_1_2_checksums_sha256.csv`). Status: **BASELINE ROBUST — PROCEED TO FEATURE 8.2 SPATIAL PATCH DATASET**.
- `data/processed/modeling/patches/`: Initial Feature 8.2 dataset artifacts (`patches_train.npz`, `patches_val.npz`, `patches_test.npz`, `patch_metadata.csv`, `patch_spatial_leakage_audit.csv`, `feature8_2_patch_dataset_report.md`). Status: **FAIL — PATCH SPATIAL LEAKAGE DETECTED** (Point split inadequate for $450\text{m} \times 450\text{m}$ patches).
- `data/processed/modeling/patches_cnn/`: Corrected Feature 8.2.1 CNN spatial patch dataset (`patches_train.npz`, `patches_val.npz`, `patches_test.npz`, `cnn_patch_metadata.csv`, `cnn_spatial_split.csv`, `cnn_patch_dataset_audit.csv`, `cnn_patch_class_distribution.csv`, `cnn_patch_spatial_leakage_audit.csv`, `cnn_patch_temporal_leakage_audit.csv`, `cnn_patch_quality_audit.csv`, `cnn_patch_normalization_metadata.json`, `feature8_2_1_patch_leakage_correction_report.md`, `feature8_2_1_checksums_sha256.csv`). Status: **PASS — CNN PATCH DATASET READY FOR FEATURE 8.3**.
- `data/processed/modeling/patches_cnn/freeze/`: Freeze metadata artifacts (`feature8_2_2_freeze_report.md`, `feature8_2_2_freeze_metadata.json`, `feature8_2_2_checksums_sha256.csv`). Status: **FEATURE 8.2.2 — FROZEN / PASS**.
- `data/processed/modeling/cnn_baseline/`: Feature 8.3 2D CNN baseline artifacts (`model/cnn_baseline.pth`, `model/cnn_baseline_architecture.json`, `cnn_training_history.csv`, `cnn_validation_metrics.csv`, `cnn_test_metrics.csv`, `cnn_project_metrics.csv`, `cnn_temporal_metrics.csv`, `cnn_threshold_sensitivity.csv`, `cnn_confusion_matrix.csv`, `cnn_predictions.csv`, `cnn_preprocessing.json`, `cnn_training_config.json`, `cnn_baseline_report.md`, `cnn_baseline_checksums_sha256.csv`, `plots/*.png`). Status: **FEATURE 8.3 — CNN BASELINE TRAINED & EVALUATED** (Outcome: **A) CNN IMPROVES GENERALIZATION** — Val PR-AUC **0.2416** vs Tabular **0.1120**, Test PR-AUC **0.1977** vs Tabular **0.0730**).
- `data/processed/modeling/cnn_baseline/audit/`: Audit artifacts (`feature8_3_1_integrity_audit.csv`, `cnn_distribution_by_project.csv`, `cnn_distribution_by_year.csv`, `cnn_distribution_project_year.csv`, `model_test_population_comparison.csv`, `cnn_vs_tabular_comparison.csv`, `cnn_prediction_reconstruction.csv`, `cnn_confusion_matrix_reconstruction.csv`, `cnn_spatial_leakage_reaudit.csv`, `cnn_temporal_leakage_reaudit.csv`, `feature8_3_1_generalization_report.md`, `feature8_3_1_checksums_sha256.csv`). Status: **FEATURE 8.3.1 — PASS (AUDIT VALIDATED)** (Decision: **B) CNN IMPROVEMENT VALID BUT TEST POPULATION DIFFERS**).
- `data/processed/modeling/controlled_benchmark/`: Controlled benchmark artifacts (`common_population.csv`, `common_population_audit.csv`, `controlled_model_comparison.csv`, `controlled_project_metrics.csv`, `controlled_temporal_metrics.csv`, `controlled_bootstrap_comparison.csv`, `controlled_spatial_leakage_audit.csv`, `controlled_prediction_integrity.csv`, `feature8_4_controlled_benchmark_report.md`, `feature8_4_checksums_sha256.csv`). Status: **FEATURE 8.4 — CONTROLLED BENCHMARK PASSED** (Decision: **B) CNN ADVANTAGE PRESENT BUT STATISTICALLY UNCERTAIN** — CNN PR-AUC **0.1977** vs XGBoost **0.1565**, CNN F1 **0.2834** vs XGBoost **0.0047** on identical $N=8,121$ test patches).
- `data/processed/modeling/controlled_benchmark/audit/`: Controlled benchmark audit artifacts (`feature8_4_1_integrity_audit.csv`, `feature8_4_1_threshold_audit.csv`, `feature8_4_1_prediction_alignment.csv`, `feature8_4_1_metric_reconstruction.csv`, `feature8_4_1_confusion_matrix_reconstruction.csv`, `feature8_4_1_threshold_sensitivity.csv`, `feature8_4_1_bootstrap_comparison.csv`, `feature8_4_1_final_audit_report.md`, `feature8_4_1_checksums_sha256.csv`). Status: **FEATURE 8.4.1 — PASS (AUDIT VALIDATED)** (Decision: **A) METRICS VALID — CNN ADVANTAGE REMAINS**).
- `data/processed/modeling/cnn_baseline/robustness/`: CNN robustness artifacts (`feature8_5_spatial_metrics.csv`, `feature8_5_project_metrics.csv`, `feature8_5_temporal_metrics.csv`, `feature8_5_bootstrap_metrics.csv`, `feature8_5_probability_distribution.csv`, `feature8_5_threshold_sensitivity.csv`, `feature8_5_error_analysis.csv`, `feature8_5_robustness_summary.csv`, `feature8_5_robustness_report.md`, `feature8_5_checksums_sha256.csv`). Status: **FEATURE 8.5 — PASS (ROBUSTNESS EVALUATED)** (Decision: **B) CNN ADVANTAGE EXISTS BUT GENERALIZATION IS MIXED** — CNN wins in 7 of 12 spatial blocks vs XGBoost in 2 blocks).
- `data/processed/modeling/cross_project_generalization/`: Cross-project generalization artifacts (`cross_project_model_metrics.csv`, `cross_project_distribution_shift.csv`, `cross_project_predictions.csv`, `cross_project_confusion_matrices.csv`, `cross_project_error_analysis.csv`, `cross_project_preprocessing.csv`, `cross_project_summary.csv`, `feature8_6_cross_project_report.md`, `feature8_6_checksums_sha256.csv`). Status: **FEATURE 8.6 — PASS (EXPERIMENTS COMPLETED)** (Decision: **A) STRONG CROSS-PROJECT GENERALIZATION** — CNN outperforms XGBoost on ALL unseen held-out projects: Exp A `MH-001` PR-AUC **0.2121** vs **0.0910**, Exp B `MH-002` PR-AUC **0.3381** vs **0.1408**, Exp C `MH-003` PR-AUC **0.1470** vs **0.1145**).
- `data/processed/modeling/cross_project_generalization/audit/`: Cross-project audit artifacts (`feature8_6_1_population_lineage.csv`, `feature8_6_1_mh003_sample_reconciliation.csv`, `feature8_6_1_year_distribution.csv`, `feature8_6_1_target_reconciliation.csv`, `feature8_6_1_spatial_reconciliation.csv`, `feature8_6_1_leakage_audit.csv`, `feature8_6_1_integrity_summary.csv`, `feature8_6_1_report.md`, `feature8_6_1_checksums_sha256.csv`). Status: **FEATURE 8.6.1 — PASS (AUDIT VALIDATED)** (Decision: **B) POPULATION DIFFERENCE EXPLAINED BUT COMPARISON REQUIRES EXPLICIT QUALIFICATION**).
- `data/processed/modeling/temporal_spatial_cnn/`: Temporal-spatial 5-year dataset artifacts (`temporal_patches_train.npz`, `temporal_patches_val.npz`, `temporal_patches_test.npz`, `temporal_delta_train.npz`, `temporal_patch_metadata.csv`, `temporal_patch_dataset_audit.csv`, `temporal_patch_class_distribution.csv`, `temporal_spatial_leakage_audit.csv`, `temporal_leakage_audit.csv`, `temporal_year_availability.csv`, `temporal_project_distribution.csv`, `temporal_normalization_metadata.json`, `temporal_delta_metadata.json`, `temporal_dataset_summary.csv`, `temporal_ndvi_delta_metadata.csv`, `feature8_7_dataset_report.md`, `feature8_7_checksums_sha256.csv`). Status: **FEATURE 8.7-A — PASS (TEMPORAL DATASET PREPARED)**.
- `data/processed/modeling/temporal_spatial_cnn/model/`: Feature 8.7-B temporal models (`temporal_cnn_raw.pth`, `temporal_cnn_delta.pth`, `spatial_2025_control.pth`, `temporal_cnn_training_history.csv`, `temporal_cnn_test_metrics.csv`, `feature8_7_b_training_report.md`, etc.). Status: **FEATURE 8.7-B — PASS (EXPERIMENT COMPLETED)** (Decision: **A) TEMPORAL CNN IMPROVES PERFORMANCE** — Delta CNN PR-AUC **0.3791** vs Spatial-Only PR-AUC **0.2429**).
- `data/processed/modeling/temporal_spatial_cnn/audit/`: Feature 8.7.1 integrity audit artifacts (`feature8_7_1_integrity_audit.csv`, `feature8_7_1_prediction_alignment.csv`, `feature8_7_1_metric_reconstruction.csv`, `feature8_7_1_confusion_matrix_reconstruction.csv`, `feature8_7_1_threshold_audit.csv`, `feature8_7_1_population_comparison.csv`, `feature8_7_1_project_metrics.csv`, `feature8_7_1_spatial_metrics.csv`, `feature8_7_1_bootstrap_comparison.csv`, `feature8_7_1_error_analysis.csv`, `feature8_7_1_temporal_signal_analysis.csv`, `feature8_7_1_generalization_summary.csv`, `feature8_7_1_final_audit_report.md`, `feature8_7_1_checksums_sha256.csv`). Status: **FEATURE 8.7.1 — PASS (AUDIT VALIDATED)** (Decision: **A) TEMPORAL DELTA ADVANTAGE STATISTICALLY SUPPORTED** — Bootstrap 95% CI for Delta PR-AUC − Control PR-AUC = [0.0185, 0.2798], **excludes zero**; Delta wins **7/8** spatial blocks).
- `data/processed/modeling/temporal_spatial_cnn/audit/reconciliation/`: Feature 8.7.2 population reconciliation artifacts (`feature8_7_2_population_reconciliation.csv`, `feature8_7_2_missing_376_ids.csv`, `feature8_7_2_exclusion_reasons.csv`, `feature8_7_2_prediction_alignment.csv`, `feature8_7_2_metric_reconstruction_1226.csv`, `feature8_7_2_metric_reconstruction_1602.csv`, `feature8_7_2_project_reconciliation.csv`, `feature8_7_2_spatial_reconciliation.csv`, `feature8_7_2_bootstrap_1226.csv`, `feature8_7_2_bootstrap_1602.csv`, `feature8_7_2_integrity_summary.csv`, `feature8_7_2_final_reconciliation_report.md`, `feature8_7_2_checksums_sha256.csv`). Status: **FEATURE 8.7.2 — PASS (RECONCILIATION COMPLETE)** (Decision: **A) FEATURE 8.7.1 VALID — ORIGINAL POPULATION CONFIRMED** — The '1,602' figure was a pre-execution USER REQUEST spec estimate, never a frozen artifact; the actual frozen NPZ always contained **N=1,226**; Feature 8.7.1 audited the correct population; bootstrap 95% CI [0.0185, 0.2798] remains unchanged).
- `data/processed/modeling/temporal_spatial_cnn/cross_project/`: Feature 8.7-C leave-one-project-out temporal Delta CNN artifacts (`cross_project_temporal_metrics.csv`, `cross_project_temporal_predictions.csv`, `cross_project_temporal_confusion_matrices.csv`, `cross_project_temporal_project_metrics.csv`, `cross_project_temporal_distribution_shift.csv`, `cross_project_temporal_error_analysis.csv`, `cross_project_temporal_preprocessing.csv`, `cross_project_temporal_bootstrap.csv`, `cross_project_temporal_vs_spatial.csv`, `cross_project_temporal_summary.csv`, `feature8_7_c_cross_project_report.md`, `feature8_7_c_checksums_sha256.csv`, `model/experiment_{A,B,C}_delta_temporal_cnn.pth`). Status: **FEATURE 8.7-C — PASS (EXPERIMENTS COMPLETED)** (Decision: **B) TEMPORAL CROSS-PROJECT GENERALIZATION EXISTS BUT IS MIXED** — CNN outperforms XGBoost in all 3 experiments: Exp A MH-001 PR-AUC **0.2619** vs **0.0910**, Exp B MH-002 PR-AUC **0.2654** vs **0.1408**, Exp C MH-003 PR-AUC **0.4070** vs **0.1145**; temporal beats spatial CNN on MH-001 and MH-003 but not MH-002).
- `data/processed/modeling/temporal_spatial_cnn/final_audit/`: Feature 8.7-D final temporal CNN chain integrity audit artifacts (`feature8_7_d_population_lineage.csv`, `feature8_7_d_sample_overlap_audit.csv`, `feature8_7_d_normalization_audit.csv`, `feature8_7_d_threshold_audit.csv`, `feature8_7_d_metric_reconstruction.csv`, `feature8_7_d_xgboost_reconstruction.csv`, `feature8_7_d_spatial_cnn_comparison.csv`, `feature8_7_d_distribution_shift.csv`, `feature8_7_d_cross_project_summary.csv`, `feature8_7_d_integrity_summary.csv`, `feature8_7_d_final_audit_report.md`, `feature8_7_d_checksums_sha256.csv`). Status: **FEATURE 8.7-D — PASS (AUDIT VALIDATED)** (Decision: **B) FEATURE 8.7 CHAIN VALID WITH QUALIFICATIONS** — All F8.7-A/B/C and F8.7.1/8.7.2 metrics reconstruct, 0 sample overlaps across LOPO splits, normalization/threshold leakage confirmed zero; F8.6 vs F8.7-C classified as **CONDITIONAL** comparison due to different evaluation populations).
- `data/processed/modeling/final_model_selection/`: Feature 8.8 final model selection artifacts (`feature8_8_master_model_comparison.csv`, `feature8_8_evidence_matrix.csv`, `feature8_8_direct_vs_conditional_comparisons.csv`, `feature8_8_cross_project_summary.csv`, `feature8_8_temporal_evidence_summary.csv`, `feature8_8_limitations.csv`, `feature8_8_model_selection_decision.csv`, `feature8_8_final_report.md`, `feature8_8_checksums_sha256.csv`). Status: **FEATURE 8.8 — COMPLETE** (Decision: **SELECTED MODEL: Delta Temporal CNN (Feature 8.7-B)** — 7 models compared across 5 evidence dimensions; 13/13 upstream checksums PASS; Delta CNN beats XGBoost 3/3 LOPO, beats Spatial CNN 2/3 CONDITIONAL; deployment status: **B) READY FOR LIMITED RESEARCH/PILOT INFERENCE**).
- `data/processed/modeling/pilot_inference/`: Feature 9 pilot inference artifacts and hotspots. Contains `predictions/pilot_predictions.csv` (10,752 samples), `hotspots/pilot_hotspots.csv` (157 spatial hotspots generated via DBSCAN), `maps/` (GeoJSON spatial outputs), `reports/` (project summary and methodology report), and `audits/` (inference integrity and checksums). Status: **FEATURE 9 — PASS (PILOT INFERENCE COMPLETED)**. *Scientific Disclaimer: Predictions represent multispectral patterns associated with historical disturbance-candidate labels, not confirmed ground-truth or environmental non-compliance.*
- `data/processed/modeling/candidate_validation/`: Feature 10 independent candidate validation and hotspot quality assessment. Contains `validation/` (probability distribution audit, threshold sensitivity diagnostic), `hotspot_evidence/` (NDVI and DW independent satellite validation), `maps/` (validated hotspot GeoJSONs), `reports/` (project-wise validation summary and methodology report), and `audits/` (integrity checks and checksums). Status: **FEATURE 10 — PASS** (Finding: CNN candidate rate (93%) driven by calibration shift on pilot population; 69 out of 157 hotspots independently supported by NDVI/DW satellite evidence). *Scientific Disclaimer: Independent satellite evidence acts as supporting proxy data, not definitive ground truth. Verification required.*
- `data/processed/modeling/candidate_validation/calibration/`: Feature 10.1 candidate calibration & threshold diagnostic artifacts. Contains `feature10_1_threshold_diagnostics.csv`, `feature10_1_project_threshold_diagnostics.csv`, `feature10_1_hotspot_threshold_diagnostics.csv`, `feature10_1_evidence_enrichment.csv`, `feature10_1_probability_distribution.csv`, `feature10_1_input_manifest.csv`, `feature10_1_checksums_sha256.csv`, `feature10_1_calibration_report.md`, and diagnostic plots (`plots/`). Status: **FEATURE 10.1 — PASS** (Decision: **C) Strong calibration shift detected**. CNN outputs serve as ranking scores; extreme probability clustering observed. The official Feature 8.8 operational threshold remains strictly frozen at **0.10**).
- `data/processed/modeling/candidate_prioritization/`: Feature 11 evidence-based candidate prioritization and investigator queue artifacts. Contains `feature11_hotspot_priority.csv`, `feature11_project_summary.csv`, `feature11_evidence_breakdown.csv`, `feature11_priority_rules.json`, `maps/feature11_prioritized_hotspots.geojson`, and methodology report. Status: **FEATURE 11 — PASS** (Decision: 157 hotspots prioritized based on CNN signal and independent satellite support. Priority distribution: 8 HIGH, 15 MEDIUM, 46 LOW, 88 UNSUPPORTED. CNN signal utilized strictly as a spatial ranking mechanism).
- `docs/dashboard/` and `data/processed/modeling/dashboard/`: Feature 12-A dashboard architecture, data contracts, API specifications, map requirements, and provenance schemas. Status: **FEATURE 12-A — PASS** (Decision: Architecture designed around a strict read-only FastAPI backend interacting with immutable ML artifacts, decoupled from a React/MapLibre frontend to guarantee scientific provenance and integrity).






























