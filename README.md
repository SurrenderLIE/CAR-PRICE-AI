Author: AARON LIE HSU FA
This project is about developing a used car price prediction machine learning model and a user interface for users to predict their car value by selecting features

---

## Table of Contents
- [Dataset](#dataset)
- [Data Processing](#data-processing)
- [Model](#model)
- [Training and Evaluation](#training-and-evaluation)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Live Demo](#live-demo)
- [License](#license)

---

## Dataset
- The dataset was created using python coding, no open source datasets were used. 
- The dataset generation includes the following features: 
        "make"
        "model"
        "trim"
        "car_type"
        "year"
        "mileage"
        "transmission"
        "fuel_type"
        "engine_cc"
        "battery_kWh"
        "is_turbo"
        "origin_country"
        "location"
        "condition"
        "retail_price(RM)"
        "current_price(RM)"
- Data file of can be located as "\malaysia_used_cars.csv" containing 700 car example inputs in the CAR_PRICE_AI folder.


## Data Processing
- Missing values handled using mode for categorical and mean/median for numerical features.
- Only specific brands supported (`Proton`, `Perodua`, `Toyota`, `Honda`, `Nissan`, `Mazda`, `BMW`, `Mercedes`, `Volkswagen`, `BYD`, `Tesla`).
- Categorical features (`make`, `transmission`) encoded using label binarization or integer encoding.
- Feature engineering: included `depreciation` as a derived metric.

## Model

- **Architecture**: Random Forest Regressor
- **Input features**:
  - `is_turbo` (binary)
  - `mileage`
  - `make` (encoded)
  - `year`
  - `retail_price(RM)`
  - `transmission` (encoded)
  - `battery_kWh`
- **Output**: Predicted current price in RM

---

## Training and Evaluation

- **Training process**:
  - Split dataset into training and testing sets.
  - Trained Random Forest with default hyperparameters (or specify tuning if done).
- **Evaluation**:
  - Metrics: RMSE, MAE, R² score.
  - Model saved as `RF_regression.pkl`.

## Setup Instructions

1. Clone the repository: git clone <your_repo_url>
2. Enter directory: cd CAR_PRICE_AI
3. Create virtual environment: python -m venv venv
4. Enter environment: source venv/bin/activate (For Linux/Mac) OR venv\Scripts\activate (Windows)
5. Run streamlit app: streamlit run main.py