# Can we build a model to predict which delayed passengers will request refunds vs. those who won’t? (1.2)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("railway.csv")

# Preprocess data
df['Railcard'] = df['Railcard'].fillna('No Railcard')
df['Refund Requested'] = df['Refund Request'].apply(lambda x: 1 if x == 'Yes' else 0)

# Select features available at booking time
features = ['Purchase Type', 'Payment Method', 'Railcard',
            'Ticket Class', 'Ticket Type', 'Price',
            'Departure Station', 'Arrival Destination']

X = df[features]
y = df['Refund Requested']

# One-hot encode categorical features
X = pd.get_dummies(X, columns=['Purchase Type', 'Payment Method', 'Railcard',
                              'Ticket Class', 'Ticket Type',
                              'Departure Station', 'Arrival Destination'],
                   drop_first=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model with class balancing
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
print("Model Performance Report:")
print(classification_report(y_test, predictions))

# Save model for production use
joblib.dump(model, 'refund_predictor.pkl')

# Prediction function
def predict_refund_request(input_data):
    # Convert input to DataFrame
    input_df = pd.DataFrame([input_data])

    # Align columns with training data
    input_encoded = pd.get_dummies(input_df).reindex(columns=X.columns, fill_value=0)

    # Predict probability
    refund_prob = model.predict_proba(input_encoded)[0][1]

    # Return prediction with probability
    return {
        'Prediction': 'Yes' if refund_prob > 0.5 else 'No',
        'Refund Probability': f"{refund_prob*100:.1f}%"
    }

# Example prediction
sample_input = {
    'Purchase Type': 'Online',
    'Payment Method': 'Credit Card',
    'Railcard': 'Disabled',
    'Ticket Class': 'First Class',
    'Ticket Type': 'Anytime',
    'Price': 93,
    'Departure Station': 'York',
    'Arrival Destination': 'Edinburgh'
}

result = predict_refund_request(sample_input)
print(f"\nPrediction: {result['Prediction']}")
print(f"Confidence: {result['Refund Probability']}")