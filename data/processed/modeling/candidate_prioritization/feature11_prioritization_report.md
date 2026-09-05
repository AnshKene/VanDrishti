# Feature 11 -- Evidence-Based Candidate Prioritization & Investigator Queue

## 1. Objective
Establish a deterministic, evidence-based prioritization system for the 157 Feature 9 hotspots. This operational decision-support tool ranks hotspots based on CNN signal strength combined with independent satellite (NDVI/DW) support.

## 2. Prioritization Framework
The priority score (0-100) is deterministically calculated using:
- **CNN Signal (Max 40 pts)**: Scales with max CNN score and spatial extent (patch count).
- **Independent Evidence (Max 60 pts)**:
  - Suspicious Dynamic World transition (Vegetation to Bare/Built): +30 pts
  - Strong NDVI decline (< -0.10): +30 pts
  - Moderate NDVI decline (< -0.05): +20 pts
  - Minor NDVI decline (< 0.0): +10 pts

### Priority Levels
- **HIGH PRIORITY** (8): Score >= 60 & Evidence >= 30. Action: *Prioritize independent field/regulatory verification.*
- **MEDIUM PRIORITY** (15): Score >= 40 & Evidence >= 20. Action: *Review satellite evidence and historical imagery.*
- **LOW PRIORITY** (46): Evidence > 0 but low score. Action: *Monitor / retain for future analysis.*
- **UNSUPPORTED / MONITOR** (88): No independent satellite evidence (Evidence = 0). Action: *No independent evidence; do not escalate without additional evidence.*

## 3. Top 3 Candidates
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>hotspot_id</th>
      <th>project_id</th>
      <th>priority_score</th>
      <th>evidence_summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MH-003-HS-0019</td>
      <td>MH-003</td>
      <td>83.2</td>
      <td>CNN max 0.16 (41.1th pct) over 30 patches. Vegetation-to-bare/built transition detected. Strong NDVI decline (-0.25).</td>
    </tr>
    <tr>
      <td>MH-001-HS-0059</td>
      <td>MH-001</td>
      <td>68.6</td>
      <td>CNN max 0.43 (97.2th pct) over 37 patches. Vegetation-to-bare/built transition detected. Minor NDVI decline (-0.01).</td>
    </tr>
    <tr>
      <td>MH-003-HS-0025</td>
      <td>MH-003</td>
      <td>68.2</td>
      <td>CNN max 0.11 (11.0th pct) over 3 patches. Vegetation-to-bare/built transition detected. Strong NDVI decline (-0.30).</td>
    </tr>
  </tbody>
</table>

## 4. Project-Wise Distribution
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>project_id</th>
      <th>hotspot_count</th>
      <th>high_priority</th>
      <th>medium_priority</th>
      <th>low_priority</th>
      <th>unsupported</th>
      <th>mean_priority_score</th>
      <th>mean_CNN_score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MH-001</td>
      <td>73</td>
      <td>1</td>
      <td>5</td>
      <td>16</td>
      <td>51</td>
      <td>20.53</td>
      <td>0.2443</td>
    </tr>
    <tr>
      <td>MH-002</td>
      <td>28</td>
      <td>2</td>
      <td>2</td>
      <td>11</td>
      <td>13</td>
      <td>28.52</td>
      <td>0.3154</td>
    </tr>
    <tr>
      <td>MH-003</td>
      <td>56</td>
      <td>5</td>
      <td>8</td>
      <td>19</td>
      <td>24</td>
      <td>27.09</td>
      <td>0.1365</td>
    </tr>
  </tbody>
</table>

## 5. Scientific and Legal Disclaimer
**IMPORTANT: The prioritization system identifies locations that warrant additional investigation based on model-derived spatial signals and independent satellite proxy evidence.**

**It does NOT establish illegal activity, environmental non-compliance, unauthorized land use, causality, intent, or confirmed land-use change.**

**Independent field/regulatory verification remains strictly necessary before any compliance determination is made.**
