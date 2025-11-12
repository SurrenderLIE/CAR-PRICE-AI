# Used Car Price Prediction

**Author:** AARON LIE HSU FA  
This project develops a machine learning model to predict used car prices in Malaysia, with a user interface allowing users to estimate car value by selecting features.

---

## Table of Contents
- [Dataset](#dataset)
- [Data Processing](#data-processing)
- [Training and Evaluation](#training-and-evaluation)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Live Demo](#live-demo)
- [License](#license)

---

## Dataset

### Dataset Generation and Summary

- A synthetic dataset of **700 used cars in Malaysia** was generated, covering 11 brands: Proton, Perodua, Toyota, Honda, Nissan, Mazda, BMW, Mercedes, Volkswagen, BYD, Tesla.  
- Each entry includes make, model, trim, car type, year, mileage, transmission, fuel type, engine size, battery capacity (for EVs), turbo option, origin country, location, condition, retail price, and simulated current price.

**Current price calculation** combines:
- Base price × brand resale multiplier
- Depreciation by age, adjusted for brand and fuel type
- Mileage factor (EVs penalized less)
- Engine size, turbo, and transmission adjustments
- Location and condition multipliers
- Random market noise (±12%)

- Dataset was generated programmatically; no external datasets were used.

---

## Data Processing

After dataset generation, extensive data inspection, visualization, and feature engineering were performed. The full code is available in `Data_process.ipynb`.

### Data Exploration and Visualization
- **Categorical variables** (`make`, `model`, `trim`, `fuel_type`, `transmission`, `condition`) were visualized using horizontal bar plots, revealing distributions, class imbalances, and popular trims/brands.  
- **Continuous variables** (`year`, `mileage`, `battery_kWh`, `retail_price(RM)`, `current_price(RM)`) were analyzed using combined boxplots and histograms with mean, median, and outlier highlights.  
- **Joint plots** examined the relationship between continuous features and the target `current_price(RM)`.  
- **Boxplots** compared categorical features with target prices, identifying price trends across brands, trims, and conditions.  

These visualizations guided feature selection and preprocessing.

### Data Cleaning and Encoding
- Missing categorical values were imputed with the **mode**, continuous values with the **mean**.  
- Categorical features were **label-binarized** to convert them into numeric format.  
- Encoders for each categorical column were saved for reproducibility.

### Feature Selection
- Continuous features with correlation > 0.3 with the target were selected.  
- Linear regression assessed categorical feature influence; features with low but meaningful impact were included.  
- Selected features were scaled using **MinMaxScaler**.  

### Train-Test Split
The processed dataset was split into **70% training** and **30% testing** sets.

---

## Training and Evaluation

### Model Training
- A **Random Forest Regressor** was trained on the training set (`X_train`, `y_train`) with a fixed random seed.  
- Predictions were generated for both training and test sets.

### Evaluation Metrics
- **MAE (Mean Absolute Error):** Average absolute prediction error in RM.  
- **RMSE (Root Mean Squared Error):** Penalizes larger errors, sensitive to outliers.  
- **R² Score:** Explains variance captured by the model.  
- **MAPE (Mean Absolute Percentage Error):** Average relative error.

#### Performance Results

| Dataset       | MAE (RM) | RMSE (RM) | R²    | MAPE (%) |
|---------------|-----------|------------|-------|----------|
| Training Set  | 2,520.91  | 3,438.99   | 0.994 | —        |
| Test Set      | 7,435.39  | 11,987.61  | 0.941 | 9.18     |

- **Overfitting Check:** R² difference = 0.052, indicating the model generalizes well.

### Visualization
A scatter plot of actual vs predicted prices confirms predictions closely follow actual values, with the diagonal line representing perfect prediction.

### Model Persistence
The trained model is saved as `RF_regression.pkl` for later inference or deployment.

---

## Setup Instructions

**Option 1: Live App**  
- Open the deployed Streamlit app:  
[https://car-price-ai-b8t4wsmgkgzzx8nh4h3giw.streamlit.app/]

**Option 2: Run Locally**
1. Clone repository:  
```bash
git clone https://github.com/SurrenderLIE/CAR-PRICE-AI.git
cd CAR-PRICE-AI

OR to run locally

1. Clone the repository:  
                                git clone <https://github.com/SurrenderLIE/CAR-PRICE-AI.git>

2. Enter directory: 
                                cd CAR_PRICE_AI

3. Create virtual environment: 
                                python -m venv venv

4. Enter environment: 
                                source venv/bin/activate (For Linux/Mac) 
                                venv\Scripts\activate (For Windows)

5. Run streamlit app: 
                                streamlit run main.py


