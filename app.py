from flask import Flask, request, render_template
import joblib
import pandas as pd
from urllib.parse import urlparse
import ipaddress

app = Flask(__name__)

# --- LOAD MODELS AND COLUMNS ---
# Load the trained model
try:
    model = joblib.load('models/phishing_model.joblib')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Model file not found! Please run train_model.py first.")
    model = None

# Load the feature column names
try:
    model_columns = joblib.load('models/feature_columns.joblib')
    print("Model columns loaded successfully.")
except FileNotFoundError:
    print("Feature columns file not found! Please run train_model.py first.")
    model_columns = None


# --- SIMPLIFIED FEATURE EXTRACTOR ---
# We use the {1, 0, -1} logic from the dataset.
# 1 = Phishing (Bad), 0 = Suspicious, -1 = Legitimate (Good)

def extract_features(url):
    features = {}
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    # 1. UsingIP: 1 (Phishing) if IP, -1 (Legit) if not
    try:
        ipaddress.ip_address(domain)
        features['UsingIP'] = 1
    except ValueError:
        features['UsingIP'] = -1

    # 2. LongURL: 1 (Phishing) if long, -1 (Legit) if short
    # We will keep our aggressive threshold of 40
    features['LongURL'] = 1 if len(url) >= 40 else -1

    # 3. ShortURL: 1 (Phishing) if shortener, -1 (Legit) if not
    features['ShortURL'] = 1 if any(s in domain for s in ['bit.ly', 't.co']) else -1

    # 4. Symbol@: 1 (Phishing) if '@', -1 (Legit) if not
    features['Symbol@'] = 1 if '@' in url else -1

    # 5. Redirecting//: 1 (Phishing) if '//' in path, -1 (Legit) if not
    features['Redirecting//'] = 1 if '//' in path else -1

    # 6. PrefixSuffix-: 1 (Phishing) if '-', -1 (Legit) if not
    features['PrefixSuffix-'] = 1 if '-' in domain else -1

    # 7. SubDomains: 1 (Phishing) if 3+ dots, 0 (Suspicious) if 2 dots, -1 (Legit) if 1 dot
    num_dots = domain.count('.')
    if num_dots == 1:
        features['SubDomains'] = -1  # e.g., google.com
    elif num_dots == 2:
        features['SubDomains'] = 0   # e.g., www.google.com
    else:
        features['SubDomains'] = 1   # e.g., mail.archive.google.com

    # 8. HTTPS: 1 (Legit) if 'https', 0 (Suspicious) if 'http'
    features['HTTPS'] = 1 if parsed_url.scheme == 'https' else 0

    # --- Create the full 30-feature vector ---
    # Start with a dictionary of 0s for all 30 features
    final_features = {col: 0 for col in model_columns}
    
    # Update the dictionary with the 8 features we just extracted
    for feature, value in features.items():
        if feature in final_features:
            final_features[feature] = value
            
    # Convert the dictionary to a DataFrame (which is what the model expects)
    return pd.DataFrame([final_features], columns=model_columns)


# --- FLASK ROUTES ---
@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get URL from the form
        url_to_check = request.form['url']
        disclaimer_text = "This prediction is based on a simplified model with 8/30 features."

        if not url_to_check.startswith(('http://', 'https://')):
            url_to_check = 'http://' + url_to_check

        # --- *** NEW FIX #1: Hard-coded '@' rule *** ---
        # If the '@' symbol is in the URL, it's almost certainly phishing.
        if '@' in url_to_check:
            return render_template('index.html',
                                   prediction_text="This website is suspicious (Phishing).",
                                   disclaimer="Reason: The '@' symbol in the URL is a common phishing trick.",
                                   url=url_to_check)
                                   
        # --- *** NEW FIX #2: Hard-coded keyword rule *** ---
        # Checks for suspicious words in the domain name.
        suspicious_keywords = ['login', 'paypal', 'secure', 'update', 'verify', 'account', 'signin', 'bank']
        official_domains = ['paypal.com', 'google.com', 'amazon.com', 'bankofamerica.com']
        
        domain_name = urlparse(url_to_check).netloc
        
        # Check if any keyword is in the domain
        has_suspicious_keyword = any(keyword in domain_name for keyword in suspicious_keywords)
        # Check if the domain is NOT an official one
        is_not_official = not any(domain_name.endswith(official) for official in official_domains)

        if has_suspicious_keyword and is_not_official:
            return render_template('index.html',
                                   prediction_text="This website is suspicious (Phishing).",
                                   disclaimer="Reason: URL contains suspicious keywords (e.g., 'login', 'paypal') on an unverified domain.",
                                   url=url_to_check)
        # --- *** END OF NEW FIXES *** ---


        # Extract features (only if the heuristic rules above passed)
        try:
            features_df = extract_features(url_to_check)
        except Exception as e:
            # Handle errors in URL parsing
            return render_template('index.html',
                                   prediction_text="Error parsing URL",
                                   disclaimer=f"Details: {e}",
                                   url=url_to_check)

        # Make prediction
        if model:
            prediction = model.predict(features_df)
            result = prediction[0]  # Get the 0 or 1

            # Set result text
            if result == 1:
                result_text = "This website is suspicious (Phishing)."
            else:
                result_text = "This website seems legitimate."
        
        else:
            result_text = "Error: Model not loaded."
            disclaimer_text = "Please check the server console."


        # Send result back to the same page
        return render_template('index.html',
                               prediction_text=result_text,
                               disclaimer=disclaimer_text,
                               url=url_to_check)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)