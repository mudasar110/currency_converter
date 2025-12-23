import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# -------------------------------
# Past Housing Data (Embedded)
# -------------------------------
data = {
    "area": [
        "Clifton","Clifton","Clifton","Clifton","Clifton",
        "DHA","DHA","DHA","DHA","DHA",
        "Gulshan","Gulshan","Gulshan","Gulshan","Gulshan",
        "Saddar","Saddar","Saddar","Saddar","Saddar"
    ],
    "plot_size": [
        120,120,120,240,240,
        120,120,120,240,240,
        120,120,120,240,240,
        120,120,120,240,240
    ],
    "year": [
        2018,2020,2022,2018,2022,
        2018,2020,2022,2018,2022,
        2018,2020,2022,2018,2022,
        2018,2020,2022,2018,2022
    ],
    "price": [
        18000000,21000000,26000000,32000000,42000000,
        15000000,19000000,24000000,28000000,38000000,
        8000000,10000000,13000000,14000000,20000000,
        6000000,7500000,9500000,11000000,16000000
    ]
}

df = pd.DataFrame(data)

# -------------------------------
# Encoding Area Names
# -------------------------------
le = LabelEncoder()
df["area_encoded"] = le.fit_transform(df["area"])

# -------------------------------
# Train Model
# -------------------------------
X = df[["area_encoded", "plot_size", "year"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🏠 Housing Price Predictor")
st.write("Predict future house prices using past housing data")

area = st.selectbox("Select Area", df["area"].unique())
plot_size = st.selectbox("Select Plot Size (sq yards)", [120, 240])
year = st.selectbox(
    "Select Prediction Year",
    [2026, 2027, 2028, 2029, 2030]
)

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict"):
    area_encoded = le.transform([area])[0]
    predicted_price = model.predict([[area_encoded, plot_size, year]])

    st.success(
        f"Estimated House Price in {year}: **PKR {int(predicted_price[0]):,}**"
    )

st.caption("Note: Prediction is based on historical market trends")
