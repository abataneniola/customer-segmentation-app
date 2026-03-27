import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load models
kmeans = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

# Page configuration
st.set_page_config(
    page_title="Customer Segmentation App",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .css-1r6slb0, .css-1v3fvcr {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Success message styling */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    
    /* Input field styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Card header */
    .card-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Welcome card styling */
    .welcome-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 40px 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .welcome-title {
        color: #667eea !important;
        font-size: 2em;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    .welcome-text {
        color: #555 !important;
        font-size: 1.2em;
        margin-bottom: 15px;
    }
    
    .welcome-highlight {
        color: #764ba2 !important;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .welcome-feature {
        color: #888 !important;
        margin-top: 20px;
        font-size: 1em;
    }
</style>
""", unsafe_allow_html=True)

# Cluster information with names, counts, and benefits
CLUSTER_INFO = {
    0: {
        "name": "🌟 Engaged Affluents",
        "count": 420,
        "percentage": 19.0,
        "benefits": [
            "💎 Exclusive VIP access to premium products",
            "🎁 Early access to new collections",
            "✨ Personalized shopping concierge service",
            "🏆 Double loyalty points on all purchases",
            "🎉 Invitations to exclusive events"
        ],
        "description": "High-income, frequent shoppers who engage across multiple channels"
    },
    1: {
        "name": "🛒 Budget-Conscious Shoppers",
        "count": 537,
        "percentage": 24.2,
        "benefits": [
            "💰 Special discount coupons on bulk purchases",
            "🏷️ Early bird sale notifications",
            "📦 Free shipping on orders above $50",
            "🎯 Targeted budget-friendly recommendations",
            "⭐ 5% cashback on every purchase"
        ],
        "description": "Value-seeking customers who prefer affordable options"
    },
    2: {
        "name": "⏰ Recent Budget Shoppers",
        "count": 574,
        "percentage": 25.9,
        "benefits": [
            "⚡ Flash sale alerts",
            "🎫 Welcome back bonus points",
            "📱 Mobile app exclusive deals",
            "🔄 Easy return policy extension",
            "🎨 First-time buyer discount vouchers"
        ],
        "description": "Newer customers with moderate spending habits"
    },
    3: {
        "name": "👴 Traditional High-Spenders",
        "count": 336,
        "percentage": 15.2,
        "benefits": [
            "👔 Premium product recommendations",
            "📞 Dedicated customer support hotline",
            "🎁 Anniversary bonus rewards",
            "🏛️ Exclusive in-store previews",
            "💎 Lifetime warranty on selected items"
        ],
        "description": "High-spending customers who prefer traditional shopping"
    },
    4: {
        "name": "💎 Premium Store Shoppers",
        "count": 348,
        "percentage": 15.7,
        "benefits": [
            "🏬 Priority in-store assistance",
            "✨ Personal stylist appointments",
            "🛍️ Early access to seasonal collections",
            "🎯 Curated luxury recommendations",
            "🌟 Complimentary gift wrapping"
        ],
        "description": "Luxury-focused customers who prefer physical stores"
    },
    5: {
        "name": "⚠️ Outlier",
        "count": 1,
        "percentage": 0.05,
        "benefits": [
            "🤝 Personalized engagement strategy",
            "📊 Customized analysis for better understanding",
            "🎯 Special attention from our team",
            "💡 Unique recommendations based on behavior"
        ],
        "description": "Unique customers with distinctive shopping patterns"
    }
}

# Title and header
st.title("🎯 Customer Segmentation App")
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="card-header">📝 Customer Details</div>', unsafe_allow_html=True)
    
    # Input fields in a nice container
    with st.container():
        age = st.number_input("Age", min_value=18, max_value=180, value=35)
        income = st.number_input("Income ($)", min_value=0, max_value=300000, value=50000, step=1000)
        total_spending = st.number_input("Total Spending ($)", min_value=0, max_value=5000, value=1000)
        num_web_purchases = st.number_input("Number of Web Purchases", min_value=0, max_value=100, value=10)
        num_store_purchases = st.number_input("Number of Store Purchases", min_value=0, max_value=100, value=10)
        num_web_visits = st.number_input("Number of Web Visits (per month)", min_value=0, max_value=100, value=3)
        recency = st.number_input("Recency (days since last purchase)", min_value=0, max_value=365, value=30)

with col2:
    # Right column header
    st.markdown('<div class="card-header">🎯 Prediction Results</div>', unsafe_allow_html=True)

# Initialize session state for prediction
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'predicted_cluster' not in st.session_state:
    st.session_state.predicted_cluster = None

# Prediction section
col_pred, col_reset = st.columns([3, 1])

with col_pred:
    predict_button = st.button("🔮 Predict the Segment", use_container_width=True)

# Handle prediction
if predict_button:
    input_data = pd.DataFrame({
        "Age": [age],
        "Income": [income],
        "Total_Spending": [total_spending],
        "NumWebPurchases": [num_web_purchases],
        "NumStorePurchases": [num_store_purchases],
        "NumWebVisitsMonth": [num_web_visits],
        "Recency": [recency]
    })
    
    input_scaled = scaler.transform(input_data)
    cluster = kmeans.predict(input_scaled)[0]
    
    st.session_state.prediction_made = True
    st.session_state.predicted_cluster = cluster

# Display in right column based on prediction state
with col2:
    if st.session_state.prediction_made:
        cluster = st.session_state.predicted_cluster
        cluster_info = CLUSTER_INFO[cluster]
        
        # Show prediction results
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; 
                    border-radius: 15px; 
                    color: white;
                    margin-bottom: 20px;">
            <h3 style="color: white; margin-bottom: 15px;">🎯 Your Predicted Segment</h3>
            <h1 style="color: white; font-size: 2.5em; margin-bottom: 10px;">{cluster_info['name']}</h1>
            <p style="font-size: 1.1em;">{cluster_info['description']}</p>
            <hr style="margin: 15px 0;">
            <p><strong>📊 Segment Size:</strong> {cluster_info['count']} customers ({cluster_info['percentage']}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; 
                    border-radius: 15px; 
                    color: white;">
            <h3 style="color: white; margin-bottom: 15px;"> Exclusive Benefits for You</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                {''.join([f'<li style="margin-bottom: 10px;">{benefit}</li>' for benefit in cluster_info['benefits']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Show welcome message when no prediction has been made - with proper text colors
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-title">👋 Welcome!</div>
            <div class="welcome-text">Enter customer details on the left and click</div>
            <div class="welcome-highlight">"Predict Segment"</div>
            <div class="welcome-text">to see results here</div>
            <br>
            <div class="welcome-feature"> Discover which customer segment you belong to</div>
            <div class="welcome-feature"> Unlock exclusive benefits tailored for you</div>
            <div class="welcome-feature"> Designed by Abatan EniolaNimi John | Data Scientist</div>
        </div>
        """, unsafe_allow_html=True)

# Reset button placement
with col_reset:
    if st.session_state.prediction_made:
        if st.button("🔄 Reset Prediction", use_container_width=True):
            st.session_state.prediction_made = False
            st.session_state.predicted_cluster = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: rgba(255,255,255,0.7);'>"
    " Powered by Machine Learning | Customer Segmentation Analysis"
    " Designed by Abatan EniolaNimi John | Data Scientist "
    "</p>",
    unsafe_allow_html=True
)