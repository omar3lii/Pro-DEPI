import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Refund Request Prediction", layout="centered")

@st.cache_resource
def load_or_train_model():
    try:
        model = joblib.load("refund_predictor.pkl")
        columns = joblib.load("refund_columns.pkl")
    except:
        df = pd.read_csv("railway.csv")
        df['Railcard'] = df['Railcard'].fillna('No Railcard')
        df['Refund Requested'] = df['Refund Request'].apply(lambda x: 1 if x == 'Yes' else 0)

        features = ['Purchase Type', 'Payment Method', 'Railcard',
                    'Ticket Class', 'Ticket Type', 'Price',
                    'Departure Station', 'Arrival Destination']

        X = df[features]
        y = df['Refund Requested']

        X = pd.get_dummies(X, columns=['Purchase Type', 'Payment Method', 'Railcard',
                                      'Ticket Class', 'Ticket Type',
                                      'Departure Station', 'Arrival Destination'],
                           drop_first=True)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(class_weight='balanced', random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, "refund_predictor.pkl")
        joblib.dump(X.columns.tolist(), "refund_columns.pkl")
        columns = X.columns.tolist()
    return model, columns

model, model_columns = load_or_train_model()

st.title("🚆 Refund Request Prediction for Delayed Passengers")

# مدخلات المستخدم

purchase_type = st.selectbox("Purchase Type", options=["Online", "At Station", "Other"])
payment_method = st.selectbox("Payment Method", options=["Credit Card", "Cash", "Debit Card", "Other"])
railcard = st.selectbox("Railcard", options=["No Railcard", "Disabled", "Senior", "16-25 Railcard", "Family & Friends"])
ticket_class = st.selectbox("Ticket Class", options=["Standard", "First Class"])
ticket_type = st.selectbox("Ticket Type", options=["Anytime", "Off-Peak", "Advance"])
price = st.number_input("Ticket Price (£)", min_value=1, max_value=500, value=50)
departure_station = st.selectbox("Departure Station", options=["York", "London", "Edinburgh", "Manchester", "Glasgow"])
arrival_destination = st.selectbox("Arrival Destination", options=["Edinburgh", "London", "York", "Manchester", "Glasgow"])

if st.button("Predict Refund Request"):
    input_dict = {
        'Purchase Type': purchase_type,
        'Payment Method': payment_method,
        'Railcard': railcard,
        'Ticket Class': ticket_class,
        'Ticket Type': ticket_type,
        'Price': price,
        'Departure Station': departure_station,
        'Arrival Destination': arrival_destination
    }

    input_df = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(input_df).reindex(columns=model_columns, fill_value=0)

    refund_prob = model.predict_proba(input_encoded)[0][1]
    prediction = "Yes" if refund_prob > 0.5 else "No"

    st.subheader("Prediction Result:")
    st.write(f"Will request refund? **{prediction}**")
    st.write(f"Confidence: **{refund_prob*100:.1f}%**")
