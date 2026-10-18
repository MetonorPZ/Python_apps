# Battery Degradation and RUL Dataset

## About Dataset

### Context
Predictive maintenance and accurate estimation of Remaining Useful Life (RUL) are critical challenges in the electric vehicle (EV) and energy storage industries. As lithium-ion batteries degrade over time through repeated charge and discharge cycles, accurate RUL forecasting is essential to prevent unexpected failures, optimize charging strategies, and ensure safe secondary-life applications.

This dataset provides a robust, synthetic Time-Series Benchmark for Battery Degradation and Remaining Useful Life (RUL). It is designed for machine learning evaluation and includes 200 distinct batteries exposed to diverse usage strategies, climate conditions, and chemistries.

### Dataset Overview
The dataset contains 172,779 cycle-level observations spanning 200 unique batteries. It is explicitly partitioned into Train, Validation, and Test sets to provide a consistent benchmark for comparing machine learning models.

The data is split across five interconnected CSV files:

- `battery_metadata.csv` (200 rows, 7 columns): static attributes for every battery, including `chemistry` (NMC, LFP, NCA), `manufacturer`, `climate_zone` (Temperate, Desert, Nordic, Equatorial), `usage_strategy`, and `nominal_capacity_kwh`.
- `battery_observations.csv` (172,779 rows, 31 columns): cycle-by-cycle operational data, including temperatures, charge/discharge C-rates, voltages, Depth of Discharge (DoD), State of Health (SoH) %, and internal resistance.
- `train_batteries.csv`: contains the 140 `battery_id`s designated for the training set (approximately 122,255 cycles).
- `validation_batteries.csv`: contains 30 `battery_id`s for model tuning and hyperparameter optimization (approximately 24,986 cycles).
- `test_batteries.csv`: contains 30 `battery_id`s strictly held out for final performance evaluation (approximately 25,538 cycles).

### Machine Learning Targets
This dataset supports multiple predictive maintenance tasks:

1. Remaining Useful Life (Regression): predict `remaining_useful_cycles` or `remaining_useful_efc` (Equivalent Full Cycles). Note: some rows purposely contain null targets to simulate ongoing real-world batteries that have not yet reached End of Life (EoL).
2. State of Health Forecasting (Regression): predict the `state_of_health_pct` (ranging from approximately 70% to 100%) at any given cycle.
3. Degradation Status (Classification): predict the `degradation_status` category (`Normal`, `Moderate`, `Severe`, `Critical`).

### Use Cases

- RUL Forecasting: train LSTMs, Transformers, or Gradient Boosting models (XGBoost, CatBoost, LightGBM) to predict how many cycles remain before EoL.
- Survival Analysis: apply statistical survival models such as Kaplan-Meier or Cox Proportional Hazards to estimate battery failure probabilities over time.
- Feature Engineering: determine which environmental or operational factors, such as `cumulative_high_temp_hours` or `high_soc_exposure_fraction`, are most predictive of accelerated degradation.
- Out-of-Distribution (OOD) Generalization: test whether a model trained primarily on Temperate climate batteries can generalize to predict degradation for Desert or Nordic climate batteries.

### Acknowledgment & Provenance
This is a synthetic benchmark dataset explicitly generated to mirror the complex, multivariate degradation curves of real-world lithium-ion batteries while ensuring complete data privacy and standardization for machine learning competitions and research.

---

## Instructions for Use

### 1. Data Loading
Load the CSV files into a data processing pipeline using a consistent `battery_id` key to join metadata and cycle-level observations.

Recommended workflow:

- Start with `battery_metadata.csv` for static descriptors.
- Join this table with `battery_observations.csv` on `battery_id`.
- Use `train_batteries.csv`, `validation_batteries.csv`, and `test_batteries.csv` to define the benchmark splits.

### 2. Recommended Modeling Approach
This dataset is well suited to:

- sequence models such as LSTM, Temporal Convolutional Networks, or Transformers for time-series forecasting,
- gradient boosting models for tabular features built from historical battery behavior,
- survival models when modeling time-to-failure or failure risk,
- feature engineering pipelines that aggregate cycle history and environmental exposure.

### 3. Target Handling

- For regression tasks, drop or impute null targets carefully, depending on the intended task specification.
- For classification, map `degradation_status` to integer labels if required by the model.
- For time-series evaluation, ensure temporal leakage is avoided by splitting by battery or by using only earlier cycles within each battery for training.

### 4. Validation Strategy
Use the provided validation split for tuning and hyperparameter selection. Keep the test split untouched until final evaluation to avoid optimistic bias.

### 5. Data Quality Notes

- The dataset is synthetic but realistic, designed to exhibit degradation patterns seen in real lithium-ion battery systems.
- Different climate and usage conditions create realistic covariate shifts across batteries.
- Null target values are intentionally included to simulate incomplete degradation trajectories.

### 6. Suggested Output
When building models for this benchmark, track metrics such as:

- MAE / RMSE for RUL and SoH regression,
- R-squared for performance comparison,
- classification accuracy, precision, recall, and F1 for degradation status,
- generalization performance across climate zones or battery chemistries.

## Current RUL Prediction Script

`Battery_ML_app1` trains a regression model to predict `remaining_useful_cycles`
for each battery observation. Run it from the project directory with:

```shell
python Battery_ML_app1
```

The script expects the CSV files under `data/archive/` and writes
`predictions.csv` in the project directory.

### What the script does

1. Loads battery metadata, cycle observations, and the battery ID lists for
   the train, validation, and test splits.
2. Joins metadata to observations by `battery_id`, then selects rows for each
   split using its corresponding ID list. Rows without a known target are
   removed from training and validation, but retained in the test data so the
   model can predict them.
3. Uses these seven input features:
   `state_of_health_pct`, `usage_strategy`, `climate_zone`, `cycle_index`,
   `battery_age_days`, `internal_resistance_mOhm`, and `chemistry`. This feature
   set performed better on the supplied validation split than the earlier
   full-feature set in the experiments used for this update.
4. Builds a preprocessing and modeling pipeline. Missing numeric values are
   filled with the training median. Categorical values are filled with the
   training most-frequent value and one-hot encoded. Unseen categories are
   ignored during transformation rather than causing prediction to fail.
5. Fits a `GradientBoostingRegressor` with 100 boosting stages, learning rate
   `0.1`, maximum tree depth `5`, and random seed `42`.
6. Evaluates the model on the separate validation batteries using mean squared
   error (MSE) and mean absolute error (MAE). The script also reports
   permutation importance: the increase in validation MAE when each feature
   is shuffled. Higher positive values indicate the model relied more on that
   feature for this validation set; they do not establish causation.
7. After validation, fits the model again using labeled training and
   validation observations together, then predicts every test observation.
   The test split is not used to calculate the reported validation metrics.
8. Saves each prediction with its `battery_id`, `cycle_index`, and `timestamp`
   in `predictions.csv`. The prediction column is named
   `predicted_remaining_useful_cycles`.

### Interpreting and improving the results

The validation score is useful for comparing model or feature-set choices,
but the feature set was selected using this same validation split. Therefore,
the printed validation metrics are tuning results and may be optimistic as an
estimate of final performance. Keep the test split untouched until the model
and features have been finalized, then evaluate it once if ground-truth test
targets are available.

Feature permutation importance measures predictive reliance, not causal
impact. Features can share importance when they are correlated. Also confirm
that every selected input, especially `state_of_health_pct`, is available at
the time predictions will be made; otherwise the validation performance may
not represent the intended real-world task.

---

## Summary
This archive contains a realistic synthetic battery degradation benchmark for predictive maintenance and RUL estimation. It is intended for benchmarking ML models across regression, classification, and survival-analysis tasks in battery health forecasting.
