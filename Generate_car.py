import pandas as pd
import random
import numpy as np
import math

# ---------- Config ----------

brand_info = {
    "Proton":   {"resale_mult": 0.65,  "origin": "Malaysia"},
    "Perodua":  {"resale_mult": 0.75,  "origin": "Malaysia"},
    "Toyota":   {"resale_mult": 0.75,  "origin": "Japan"},
    "Honda":    {"resale_mult": 0.7,  "origin": "Japan"},
    "Nissan":   {"resale_mult": 0.55, "origin": "Japan"},
    "Mazda":    {"resale_mult": 0.65,  "origin": "Japan"},
    "BMW":      {"resale_mult": 0.525,  "origin": "Germany"},
    "Mercedes": {"resale_mult": 0.55,  "origin": "Germany"},
    "Volkswagen": {"resale_mult": 0.55,"origin": "Germany"},
    "BYD":      {"resale_mult": 0.6,  "origin": "China"},
    "Tesla":    {"resale_mult": 0.6,  "origin": "USA"},
}


# realistic models & per-model engine options: (engine_l, is_turbo, allowed_fuels)
model_specs = {
    # ===== Proton =====
    "Saga": {
        "make": "Proton",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "Standard", "engine_size": 1.3, "turbo": False, "base_price": 34000},
            {"trim": "Premium", "engine_size": 1.3, "turbo": False, "base_price": 41000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Manual", "CVT", "Automatic"],
    },
    "Persona": {
        "make": "Proton",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "Standard", "engine_size": 1.6, "turbo": False, "base_price": 47000},
            {"trim": "Executive", "engine_size": 1.6, "turbo": False, "base_price": 52000},
            {"trim": "Premium", "engine_size": 1.6, "turbo": False, "base_price": 58000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Manual", "CVT", "Automatic"],
    },
    "X50": {
        "make": "Proton",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "Standard", "engine_size": 1.5, "turbo": True, "base_price": 89000},
            {"trim": "Flagship", "engine_size": 1.5, "turbo": True, "base_price": 113000},
        ],
        "car_type": "Suv",
        "transmissions": ["DCT"],
    },
    "X70": {
        "make": "Proton",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "Executive", "engine_size": 1.5, "turbo": True, "base_price": 123000},
            {"trim": "Premium", "engine_size": 1.5, "turbo": True, "base_price": 140000},
        ],
        "car_type": "Suv",
        "transmissions": ["DCT"],
    },
    "Emas7": {
        "make": "Proton",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "Prime", "battery_kWh": 49.52, "base_price": 105800},
            {"trim": "Premium", "battery_kWh": 60.22, "base_price": 119800},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },

    # ===== Perodua =====
    "Myvi": {
        "make": "Perodua",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.3 G", "engine_size": 1.3, "turbo": False, "base_price": 49000},
            {"trim": "1.5 H", "engine_size": 1.5, "turbo": False, "base_price": 54000},
            {"trim": "1.5 AV", "engine_size": 1.5, "turbo": False, "base_price": 59000},
        ],
        "car_type": "Hatchback",
        "transmissions": ["CVT", "Automatic"],
    },
    "Axia": {
        "make": "Perodua",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.0 G", "engine_size": 1.0, "turbo": False, "base_price": 38000},
            {"trim": "1.0 AV", "engine_size": 1.0, "turbo": False, "base_price": 49000},
        ],
        "car_type": "Hatchback",
        "transmissions": ["Manual","CVT", "Automatic"],
    },
    "Bezza": {
        "make": "Perodua",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.0 G", "engine_size": 1.0, "turbo": False, "base_price": 43000},
            {"trim": "1.3 AV", "engine_size": 1.3, "turbo": False, "base_price": 55000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT", "Automatic"],
    },
    "Ativa": {
        "make": "Perodua",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "1.0 Turbo X", "engine_size": 1.0, "turbo": True, "base_price": 72000},
            {"trim": "1.0 Turbo AV", "engine_size": 1.0, "turbo": True, "base_price": 82000},
        ],
        "car_type": "Suv",
        "transmissions": ["CVT"],
    },

    # ===== Toyota =====
    "Vios": {
        "make": "Toyota",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "1.5 E", "engine_size": 1.5, "turbo": False, "base_price": 90000},
            {"trim": "1.5 G", "engine_size": 1.5, "turbo": False, "base_price": 95000},
            {"trim": "GR-S", "engine_size": 1.5, "turbo": False, "base_price": 100000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT", "Automatic"],
    },
    "Corolla": {
        "make": "Toyota",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "1.8 E", "engine_size": 1.8, "turbo": False, "base_price": 128000},
            {"trim": "1.8 G", "engine_size": 1.8, "turbo": False, "base_price": 136000},
            {"trim": "2.0 Hybrid", "engine_size": 2.0, "turbo": False, "base_price": 150000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT", "Automatic"],
    },
    "Camry": {
        "make": "Toyota",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "2.0 E", "engine_size": 2.0, "turbo": False, "base_price": 190000},
            {"trim": "2.5 V", "engine_size": 2.5, "turbo": False, "base_price": 220000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT", "Automatic"],
    },

    # ===== Honda =====
    "City": {
        "make": "Honda",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "1.5 S", "engine_size": 1.5, "turbo": False, "base_price": 84000},
            {"trim": "1.5 RS e:HEV", "engine_size": 1.5, "turbo": False, "base_price": 109000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT"],
    },
    "Civic": {
        "make": "Honda",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.5 E Turbo", "engine_size": 1.5, "turbo": True, "base_price": 130000},
            {"trim": "1.5 RS Turbo", "engine_size": 1.5, "turbo": True, "base_price": 150000},
            {"trim": "Type R", "engine_size": 2.0, "turbo": True, "base_price": 390000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT",],
    },
    "CR-V": {
        "make": "Honda",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "2.0 2WD", "engine_size": 2.0, "turbo": False, "base_price": 155000},
            {"trim": "1.5 TC-P", "engine_size": 1.5, "turbo": True, "base_price": 180000},
        ],
        "car_type": "Suv",
        "transmissions": ["CVT"],
    },

    # ===== Nissan =====
    "Almera": {
        "make": "Nissan",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.0 VL Turbo", "engine_size": 1.0, "turbo": True, "base_price": 85000},
            {"trim": "1.0 VLT Turbo", "engine_size": 1.0, "turbo": True, "base_price": 95000},
        ],
        "car_type": "Sedan",
        "transmissions": ["CVT", "Automatic"],
    },
    "X-Trail": {
        "make": "Nissan",
        "fuels": ["Petrol", "Hybrid"],
        "trims": [
            {"trim": "2.0 2WD", "engine_size": 2.0, "turbo": False, "base_price": 145000},
            {"trim": "2.5 4WD", "engine_size": 2.5, "turbo": False, "base_price": 170000},
        ],
        "car_type": "Suv",
        "transmissions": ["CVT"],
    },

    # ===== Mazda =====
    "Mazda2": {
        "make": "Mazda",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.5 Hatchback", "engine_size": 1.5, "turbo": False, "base_price": 105000},
        ],
        "car_type": "Hatchback",
        "transmissions": ["Automatic"],
    },
    "Mazda3": {
        "make": "Mazda",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "2.0 Sedan", "engine_size": 2.0, "turbo": False, "base_price": 143000},
            {"trim": "2.0 Liftback", "engine_size": 2.0, "turbo": False, "base_price": 150000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },
    "CX-5": {
        "make": "Mazda",
        "fuels": ["Petrol", "Diesel"],
        "trims": [
            {"trim": "2.0 2WD", "engine_size": 2.0, "turbo": False, "base_price": 150000},
            {"trim": "2.5 Turbo", "engine_size": 2.5, "turbo": True, "base_price": 195000},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },

    # ===== BMW =====
    "3 Series": {
        "make": "BMW",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "320i", "engine_size": 2.0, "turbo": True, "base_price": 250000},
            {"trim": "330i", "engine_size": 2.0, "turbo": True, "base_price": 290000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },
    "5 Series": {
        "make": "BMW",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "520i", "engine_size": 2.0, "turbo": True, "base_price": 330000},
            {"trim": "520", "engine_size": 2.0, "turbo": True, "base_price": 330000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },
    
    "5 series(D)": {
        "make": "BMW",
        "fuels": ["Diesel"],
        "trims": [
            {"trim": "520d", "engine_size": 2.0, "turbo": True, "base_price": 330000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },
    
    "IX": {
        "make": "BMW",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "xDrive40", "battery_kWh": 76.6, "base_price": 385000},
            {"trim": "xDrive50", "battery_kWh": 111.5, "base_price": 490000},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },
    "IX1": {
        "make": "BMW",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "eDrive20", "battery_kWh": 64.7, "base_price": 250800},
            {"trim": "xDrive30", "battery_kWh": 64.7, "base_price": 275800},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },

    # ===== Mercedes-Benz =====
    "A-Class": {
        "make": "Mercedes",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "A200 Progressive", "engine_size": 1.3, "turbo": True, "base_price": 230000},
            {"trim": "A250 AMG Line", "engine_size": 2.0, "turbo": True, "base_price": 270000},
        ],
        "car_type": "Hatchback",
        "transmissions": ["Automatic"],
    },
    "C-Class": {
        "make": "Mercedes",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "C200 Avantgarde", "engine_size": 2.0, "turbo": True, "base_price": 290000},
            {"trim": "C300 AMG Line", "engine_size": 2.0, "turbo": True, "base_price": 330000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },

    # ===== Volkswagen =====
    "Tiguan": {
        "make": "Volkswagen",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.4 TSI Highline", "engine_size": 1.4, "turbo": True, "base_price": 175000},
            {"trim": "2.0 R-Line", "engine_size": 2.0, "turbo": True, "base_price": 260000},
        ],
        "car_type": "Suv",
        "transmissions": ["DCT"],
    },
    "Golf": {
        "make": "Volkswagen",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.4 TSI", "engine_size": 1.4, "turbo": True, "base_price": 155000},
            {"trim": "GTI", "engine_size": 2.0, "turbo": True, "base_price": 220000},
            {"trim": "R", "engine_size": 2.0, "turbo": True, "base_price": 300000},
        ],
        "car_type": "Hatchback",
        "transmissions": ["DCT"],
    },
    "Passat": {
        "make": "Volkswagen",
        "fuels": ["Petrol"],
        "trims": [
            {"trim": "1.8 Comfortline", "engine_size": 1.8, "turbo": True, "base_price": 180000},
            {"trim": "2.0 Highline", "engine_size": 2.0, "turbo": True, "base_price": 200000},
        ],
        "car_type": "Sedan",
        "transmissions": ["DCT"],
    },
    
    # ===== BYD =====
    "Atto 3": {
        "make": "BYD",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "Standard Range", "battery_kWh": 49.9, "base_price": 150000},
            {"trim": "Extended Range", "battery_kWh": 60.5, "base_price": 170000},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },
    "Seal": {
        "make": "BYD",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "Premium", "battery_kWh": 82.5, "base_price": 230000},
            {"trim": "Performance AWD", "battery_kWh": 82.5, "base_price": 260000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },

    # ===== Tesla =====
    "Model 3": {
        "make": "Tesla",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "RWD", "battery_kWh": 57.5, "base_price": 190000},
            {"trim": "Long Range AWD", "battery_kWh": 75.0, "base_price": 250000},
        ],
        "car_type": "Sedan",
        "transmissions": ["Automatic"],
    },
    "Model Y": {
        "make": "Tesla",
        "fuels": ["Electric"],
        "trims": [
            {"trim": "RWD", "battery_kWh": 60.0, "base_price": 210000},
            {"trim": "Performance", "battery_kWh": 75.0, "base_price": 280000},
        ],
        "car_type": "Suv",
        "transmissions": ["Automatic"],
    },
}

location_price_map = {
    "Kuala Lumpur": 1.00,
    "Selangor": 1.00,
    "Penang": 1.02,
    "Johor": 1.01,
    "Perak": 1.04,
    "Pahang": 1.05,
    "Kelantan": 1.06,
    "Terengganu": 1.06,
    "Kedah": 1.05,
    "Negeri Sembilan": 1.03,
    "Melaka": 1.02,
    "Perlis": 1.05,
}

# --- Condition multipliers (based on real market distribution) ---
condition_price_map = {
    1: 0.93,   # Poor
    2: 0.95,   # Fair
    3: 0.98,   # Average
    4: 1.0,   # Good
    5: 1.08,   # Excellent
}
condition_weights = [0.03, 0.12, 0.42, 0.33, 0.10]

# --- Depreciation function calculator ---
def get_depreciation(age: int, brand_mult: float, fuel_type: str):
    """
    Returns depreciation multiplier (0–1).
    More lenient for newer and strong-resale brands.
    """
    # Base curve by age (realistic for Malaysia)
    
    if age <= 1:
        dep = 0.93  # new cars barely depreciate
    elif age <= 3:
        dep = 0.86 - (0.02 * (age - 3))  # around 10–15% loss
    elif age <= 5:
        dep = 0.78 - (0.02 * (age - 5))
    elif age <= 8:
        dep = 0.70 - (0.015 * (age - 8))
    else:
        dep = 0.63 - (0.01 * min(age - 8, 10))

    # Adjust by brand and fuel type
    dep *= (0.95 + brand_mult * 0.1)   # strong brands lose less

    # Keep realistic bounds
    return max(0.60, min(dep, 0.98))


# ---------- Generator ----------
rows = []
N = 700
for _ in range(N):
    model = random.choice(list(model_specs.keys()))
    spec = model_specs[model]
    make = spec["make"]
    car_type = spec.get("car_type", "Sedan")
    transmission = random.choice(spec["transmissions"])

    # choose trim
    trim = random.choice(spec["trims"])
    base_price = trim["base_price"]
    resale_mult = brand_info[make]["resale_mult"]
    fuel_type = random.choice(spec["fuels"])

    # random other attributes
    if fuel_type == "Electric":
        mileage = random.randint(3000, 150000)
        year = random.randint(2022, 2024)
        age = 2025 - year
    else:
        year = random.randint(2016, 2024)
        age = 2025 - year
        if age <= 1:
            mileage = random.randint(5000, 25000)
        elif age <= 3:
            mileage = random.randint(20000, 70000)
        elif age <= 6:
            mileage = random.randint(50000, 140000)
        elif age <= 10:
            mileage = random.randint(80000, 220000)
        else:
            mileage = random.randint(150000, 300000)
    
    location = random.choice(list(location_price_map.keys()))
    condition = random.choices(list(condition_price_map.keys()), weights=condition_weights, k=1)[0]

    depreciation = get_depreciation(age, resale_mult, fuel_type)
    
   # --- Price calculation ---
    if fuel_type == "Electric":
        engine_val = np.nan
        is_turbo = np.nan  # EVs have no turbo
        battery_val = trim["battery_kWh"]

        depreciation = get_depreciation(age, resale_mult, fuel_type)

        # small condition effect on depreciation
        depreciation *= (1 + (0.02 * (3 - condition)))

        # gentler mileage factor (EVs less punished for higher mileage)
        mileage_factor = max(0.7, 1 - (mileage / 400000))
        price = base_price * resale_mult * depreciation * mileage_factor
        price *= 1 + ((trim["battery_kWh"] - 60) * 0.005)  # battery size scaling

    else:
        engine_val = trim.get("engine_size", np.nan)
        battery_val = np.nan
        engine_size = trim["engine_size"]
        is_turbo = trim["turbo"]

        depreciation = get_depreciation(age, resale_mult, fuel_type)
        depreciation *= (1 + (0.012 * (3 - condition)))

        # gentler mileage factor (ICE cars last longer in Malaysia)
        mileage_factor = max(0.65, 1 - (mileage / 800000))

        price = base_price * resale_mult * depreciation * mileage_factor
        price *= 1 - ((engine_size - 1.5) * 0.015)  # larger engine = lower price (roadtax penalty)
        
        # turbocharged adjustments
      
        # fuel adjustments
        if fuel_type == "Hybrid":
            price *= 0.95
        if fuel_type == "Diesel":
            price *= 0.97

    # transmission adjustment
    if "DCT" in transmission:
        price *= 1.05
    elif "CVT" in transmission:
        price *= 1.03
    elif "Manual" in transmission:
        price *= 0.95

    # location & condition effects
    price *= location_price_map[location]
    price *= condition_price_map[condition]

    # market noise
    price *= random.uniform(0.88, 1.12)

    rows.append({
        "make": make,
        "model": model,
        "trim": trim["trim"],
        "car_type": car_type,
        "year": year,
        "mileage": mileage,
        "transmission": transmission,
        "fuel_type": fuel_type,
        "engine_cc": engine_val,
        "battery_kWh": trim.get("battery_kWh", None),
        "is_turbo": is_turbo,
        "origin_country": brand_info[make]["origin"],
        "location": location,
        "condition": condition,
        "retail_price(RM)": base_price,
        "current_price(RM)": round(max(5000, price), 2)
    })

df = pd.DataFrame(rows)
df.to_csv("malaysia_used_cars.csv", index=False)
print("Saved malaysia_used_cars.csv with", len(df), "rows")
print(df.sample(6))
