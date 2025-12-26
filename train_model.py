import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # Used for saving the model

print("--- [Step 1] Loading Data ---")
# Load from the data/ folder
try:
    data = pd.read_csv('data/phishing.csv')
except FileNotFoundError:
    print("Error: 'data/phishing.csv' not found.")
    print("Please download the dataset and place it in the 'data/' folder.")
    exit()

print("--- [Step 2] Preprocessing Data ---")
# Change target label from -1 to 0 for 'legitimate'
data['class'] = data['class'].apply(lambda x: 0 if x == -1 else 1)

# X (Features) = all columns except 'class' and 'Index'
X = data.drop(['class', 'Index'], axis=1)
# y (Target) = only the 'class' column
y = data['class']

# Save the feature column names for later use in the app
# This is a crucial step!
joblib.dump(X.columns, 'models/feature_columns.joblib')
print(f"Model will be trained on {len(X.columns)} features.")

print("--- [Step 3] Splitting Data ---")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training on {X_train.shape[0]} samples.")

print("--- [Step 4] Training Model ---")
# We use RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

print("--- [Step 5] Evaluating Model ---")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

print("--- [Step 6] Saving Model ---")
# Save the trained model to the models/ folder
joblib.dump(model, 'models/phishing_model.joblib')
print("Model saved successfully to 'models/phishing_model.joblib'")