
# app.py
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

PARENT_PATH = os.getcwd()
DATA_PATH = os.path.join(PARENT_PATH, 'data')
USED_CAR = os.path.join(DATA_PATH, 'malaysia_used_cars.csv')

MODELS = os.path.join(PARENT_PATH, 'models')
RF_MODEL = os.path.join(MODELS, 'RF_regression.pkl')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-label {
        color: white;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    .prediction-value {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        color: #000000;
    }
    .feature-card strong {
        color: #000000;
    }
    .feature-card small {
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL
# ============================================================================
@st.cache_resource
def load_model(model_path=RF_MODEL):
    """Load the trained model"""
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please train and save the model first.")
        st.stop()
        return None

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Header
    st.markdown('<p class="main-header">🚗 Used Vehicle Price Predictor</p>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enter vehicle details to predict the current price</p>', 
                unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    # ========================================================================
    # LEFT COLUMN - INPUT FEATURES
    # ========================================================================
    with col1:
        st.markdown("### 📝 Vehicle Information")
        st.markdown("---")
        
        # Year
        st.markdown("#### 🗓️ Year")
        year = st.slider(
            "Select the manufacturing year",
            min_value=2015,
            max_value=2024,
            value=2021,
            step=1,
            help="The year the vehicle was manufactured",
            label_visibility="collapsed"
        )
        st.markdown(f"**Selected Year:** {year}")
        st.markdown("")
        
        # Battery Capacity
        st.markdown("#### 🔋 Battery Capacity (kWh) \nNote: Please input 0 for Non EV")
        battery_kwh = st.number_input(
            "Enter battery capacity in kilowatt-hours",
            min_value=0.0,
            max_value=120.0,
            value=65.62,
            step=0.1,
            help="Battery capacity determines the vehicle's range",
            label_visibility="collapsed"
        )
        st.markdown(f"**Battery Capacity:** {battery_kwh:.2f} kWh")
        st.markdown("")
        
        # Mileage
        st.markdown("#### 🛣️ Mileage (km)")
        mileage = st.number_input(
            "Enter total distance traveled",
            min_value=0,
            max_value=300000,
            value=50000,
            step=1000,
            help="Total kilometers the vehicle has traveled",
            label_visibility="collapsed"
        )
        st.markdown(f"**Mileage:** {mileage:,} km")
        st.markdown("")
        
        # Retail Price (NEW FEATURE)
        st.markdown("#### 💵 Original Retail Price (RM)")
        retail_price = st.number_input(
            "Enter the original retail price when new",
            min_value=30000.0,
            max_value=800000.0,
            value=250000.0,
            step=5000.0,
            help="The original manufacturer's retail price when the vehicle was new",
            label_visibility="collapsed"
        )
        st.markdown(f"**Retail Price:** RM {retail_price:,.2f}")
        st.markdown("")
        
        # -------------------------------
        # Make (Brand) - allowed list
        # -------------------------------
        allowed_brands = {
            "Proton": 0,
            "Perodua": 1,
            "Toyota": 2,
            "Honda": 3,
            "Nissan": 4,
            "Mazda": 5,
            "BMW": 6,
            "Mercedes": 7,
            "Volkswagen": 8,
            "BYD": 9,
            "Tesla": 10
        }

        st.markdown("#### 🏭 Make (Brand)")
        make_name = st.selectbox(
            "Select vehicle brand",
            options=list(allowed_brands.keys()),
            help="Vehicle manufacturer",
            label_visibility="collapsed"
        )

        make = allowed_brands[make_name]  # numeric code for model
        st.markdown(f"**Selected Brand:** {make_name}")
        st.markdown("")

        
        # turbo
        st.markdown("#### 🚀 Turbo")
        turbo = st.radio(
            "Does the vehicle have turbo?",
            options=["Yes", "No"],
            help="Does the vehicle have turbo?",
            label_visibility="collapsed"
        )
        turbo_value = 1 if turbo == "Yes" else 0
        st.markdown(f"**Turbo:** {turbo}")    
        st.markdown("")
        
        # Transmission
        st.markdown("#### ⚙️ Transmission")
    
        transmission = st.radio(
            "Select transmission type",
            options=["Automatic", "CVT", "DCT", "Manual"],
            help="Type of transmission system",
            label_visibility="collapsed"
        )
        st.markdown(f"**Selected Transmission:** {transmission}")
        st.markdown("")
        
        transmission_map = {
            "Automatic": 0,
            "CVT": 1,
            "DCT": 2,
            "Manual": 3
        }
        transmission_encoded = transmission_map[transmission]
        
        
        # Predict Button
        st.markdown("---")
        predict_button = st.button("🎯 PREDICT PRICE", use_container_width=True)
    
    # ========================================================================
    # RIGHT COLUMN - PREDICTION RESULTS
    # ========================================================================
    with col2:
        st.markdown("### 💰 Prediction Results")
        st.markdown("---")
        
        if predict_button:
            # Prepare input data (including retail_price)
            input_data = pd.DataFrame({
                'is_turbo': [turbo_value],
                'mileage': [mileage],
                'make': [make],
                'year': [year],
                'retail_price(RM)': [retail_price],
                'transmission': [transmission_encoded],
                'battery_kWh': [battery_kwh]
            })
            
            # # Prepare input data (without retail_price)
            # input_data = pd.DataFrame({
            #     'year': [year],
            #     'battery_kWh': [battery_kwh],
            #     'mileage': [mileage],
            #     'make': [make],
            #     'is_turbo': [turbo_value],
            #     'transmission': [transmission]
            # })
            
            # Make prediction
            with st.spinner('🔄 Calculating prediction...'):
                prediction = model.predict(input_data)[0]
            
            # Calculate depreciation
            depreciation_amount = retail_price - prediction
            depreciation_percent = (depreciation_amount / retail_price) * 100
            
            # Display main prediction
            st.markdown(f"""
            <div class="prediction-box">
                <p class="prediction-label">Predicted Current Price</p>
                <p class="prediction-value">RM {prediction:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display depreciation info
            col_dep1, col_dep2 = st.columns(2)
            with col_dep1:
                st.metric(
                    "Depreciation Amount", 
                    f"RM {depreciation_amount:,.0f}",
                    delta=f"-{depreciation_percent:.1f}%",
                    delta_color="inverse"
                )
            with col_dep2:
                retention_rate = 100 - depreciation_percent
                st.metric(
                    "Value Retention", 
                    f"{retention_rate:.1f}%",
                    delta=f"{retention_rate:.1f}%",
                    delta_color="normal"
                )
            
            # Display input summary
            st.markdown("#### 📋 Input Summary")
            summary_df = pd.DataFrame({
                'Feature': ['Year', 'Battery Capacity', 'Mileage', 'Retail Price', 'Make', 'Turbo', 'Transmission'],
                'Value': [
                    str(year),
                    f"{battery_kwh:.2f} kWh",
                    f"{mileage:,} km",
                    f"RM {retail_price:,.2f}",
                    make_name,
                    turbo,
                    transmission
                ]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            # Price Range Estimation
            st.markdown("#### 📊 Price Range Estimate")
            lower_bound = prediction * 0.90
            upper_bound = prediction * 1.10
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Lower", f"RM {lower_bound:,.0f}", delta="-10%")
            with col_b:
                st.metric("Predicted", f"RM {prediction:,.0f}")
            with col_c:
                st.metric("Upper", f"RM {upper_bound:,.0f}", delta="+10%")
            
            # Gauge Chart
            st.markdown("#### 📈 Price Indicator")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Price (RM)", 'font': {'size': 20}},
                number={'prefix': "RM ", 'font': {'size': 30}},
                gauge={
                    'axis': {'range': [None, retail_price * 1.2], 'tickwidth': 1},
                    'bar': {'color': "#667eea"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, retail_price * 0.3], 'color': '#ffcdd2'},
                        {'range': [retail_price * 0.3, retail_price * 0.6], 'color': '#fff9c4'},
                        {'range': [retail_price * 0.6, retail_price * 0.9], 'color': '#c8e6c9'},
                        {'range': [retail_price * 0.9, retail_price * 1.2], 'color': '#a5d6a7'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': prediction
                    }
                }
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional insights
            st.markdown("#### 💡 Insights")
            
            # Age-based insight
            vehicle_age = 2024 - year
            if vehicle_age <= 2:
                age_insight = "🟢 Very new vehicle - premium pricing expected"
            elif vehicle_age <= 4:
                age_insight = "🟡 Relatively new - good value retention"
            else:
                age_insight = "🟠 Older vehicle - depreciation affects price"
            
            # Mileage-based insight
            if mileage < 30000:
                mileage_insight = "🟢 Low mileage - excellent condition"
            elif mileage < 80000:
                mileage_insight = "🟡 Moderate mileage - average wear"
            else:
                mileage_insight = "🟠 High mileage - consider maintenance costs"
            
            # Battery-based insight
            if battery_kwh >= 75:
                battery_insight = "🟢 Large battery - extended range capability"
            elif battery_kwh >= 60:
                battery_insight = "🟡 Standard battery - adequate for daily use"
            else:
                battery_insight = "🟠 Smaller battery - limited range"
            
            # Depreciation insight
            if depreciation_percent < 20:
                depreciation_insight = "🟢 Excellent value retention - low depreciation"
            elif depreciation_percent < 40:
                depreciation_insight = "🟡 Normal depreciation rate for EVs"
            else:
                depreciation_insight = "🟠 High depreciation - consider negotiation"
            
            st.markdown(f"""
            <div class="feature-card">
                <strong>Vehicle Age:</strong> {vehicle_age} years<br>
                <span style="color: #000000;">{age_insight}</span>
            </div>
            <div class="feature-card">
                <strong>Mileage Status:</strong><br>
                <span style="color: #000000;">{mileage_insight}</span>
            </div>
            <div class="feature-card">
                <strong>Battery Assessment:</strong><br>
                <span style="color: #000000;">{battery_insight}</span>
            </div>
            <div class="feature-card">
                <strong>Depreciation Analysis:</strong><br>
                <span style="color: #000000;">{depreciation_insight}</span><br>
                <small style="color: #000000;">Depreciated by RM {depreciation_amount:,.0f} ({depreciation_percent:.1f}%)</small>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Show placeholder when no prediction yet
            st.info("* Fill in the vehicle details on the left and click 'PREDICT PRICE' to see results")
            
            # Show example
            st.markdown("#### 📖 Example Input")
            example_df = pd.DataFrame({
                'Feature': ['Year', 'Battery Capacity', 'Mileage', 'Retail Price', 'Make', 'Turbo', 'Transmission'],
                'Example Value': ['2021', '65.62 kWh', '50,000 km', 'RM 250,000', 'Tesla', 'Yes', 'Automatic']
            })
            st.dataframe(example_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p style="margin: 0;">🚗 <strong>Car Vehicle Price Predictor</strong></p>
        <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0;">
            Powered by Random Forest Machine Learning Model
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    main()
