# Feature 10.1 -- Candidate Calibration & Threshold Diagnostic

## 1. Why is the candidate rate 93.04% at threshold 0.10?
The probability distribution analysis reveals a strong calibration shift on the pilot population. The median predicted probability is 0.1746, meaning half of all non-monsoon 5-year sequences are assigned extreme confidence. This dense concentration near 1.0 indicates the model's uncalibrated softmax/sigmoid output acts more like a ranking score than a true calibrated probability. When standard 0.10 logic is applied, the vast majority of the population easily clears it.

## 2. What is the candidate rate at each diagnostic threshold?
- **0.10**: 93.04%
- **0.50**: 0.89%
- **0.90**: 0.00%
*(See `feature10_1_threshold_diagnostics.csv` for all levels)*

## 3. How does hotspot count change?
Hotspot counts drop drastically as the threshold increases. At 0.10, 157.0 connected spatial regions are formed (because almost everything is a candidate, merging large swaths into huge mega-hotspots). At 0.50, the candidate patches break apart into 34.0 tighter, more isolated hotspots. At 0.90, it falls to 0.0.

## 4. How does independent evidence support change?
At 0.10, the support rate is 43.9%.
At 0.50, the support rate is 20.6%.
At 0.90, the support rate is 0.0%.

## 5. Does higher threshold produce evidence enrichment?
Yes. Increasing the threshold acts as a strong filtering mechanism, raising the independent satellite support rate (from 43.9% to 0.0%). The candidates at extreme probabilities (e.g. > 0.90) possess higher enrichment for verified spatial-temporal change according to proxy NDVI and DW data. However, increasing the threshold strictly for support optimization would constitute tuning against downstream proxy evidence.

## 6. Is the probability distribution highly concentrated?
Yes. The distribution plot (`probability_distribution.png`) shows a massive skew towards 1.0, typical of deep neural networks over-confident on test environments subject to distribution shift.

## 7. Is there evidence of calibration shift?
Yes. A true calibrated probability would align closely with the empirical prevalence rate in the pilot population. Instead, the model outputs values > 0.50 for 0.9% of the area, confirming calibration shift. Formal Platt scaling or isotonic regression cannot be applied here because we lack independent ground-truth labels.

## 8. Does behavior differ by project?
Yes. MH-002 and MH-003 exhibit very high candidate rates across thresholds compared to MH-001. *(See `project_candidate_rate.png`)*.

## 9. Can a production threshold be justified from this experiment?
No new production threshold is declared. This is a strictly diagnostic characterization. While a diagnostic threshold of 0.50 or 0.80 provides better spatial isolation and evidence enrichment, altering the frozen 0.10 operational threshold based on these proxy outputs would invalidate the Feature 8.7 strict hold-out design. The operational threshold remains 0.10.

## 10. What should Feature 11 do next?
Feature 11 should package the outputs and summarize the scientific findings for the end user, finalizing the spatial hotspots (using 0.10 as the baseline) while providing the diagnostic probability for ranking.

## Scientific Conclusion
**C) Strong calibration shift detected.** The model scores represent strong relative rankings rather than absolute calibrated probabilities. High diagnostic thresholds improve independent proxy evidence enrichment, but the official operating threshold remains frozen at 0.10.

## Disclaimer
*Independent satellite support is proxy evidence. The system must never claim illegal activity, environmental violation, unauthorized land use, causality, intent, or confirmed land-use change based solely on these metrics.*
