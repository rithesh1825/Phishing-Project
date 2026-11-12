# 🛡️ Phishing Website Detection System

A Machine Learning-based Phishing Website Detection System developed using Python, Flask, and Scikit-learn. This project analyzes website URLs and predicts whether a website is potentially phishing or legitimate.

The application combines URL feature extraction, rule-based checks, and a trained Random Forest Classification model to identify suspicious websites through a simple web interface.

## 📌 Project Overview

Phishing attacks are a common cybersecurity threat in which attackers create fraudulent websites to steal sensitive information such as passwords, banking details, and personal data.

This project aims to demonstrate how machine learning can help identify potentially malicious websites by analyzing URL characteristics and detecting suspicious patterns.

Users can enter a website URL through the web interface and receive a prediction indicating whether the website appears suspicious or legitimate.

## ✨ Key Features

- URL-based phishing detection.
- Machine Learning-based website classification.
- Random Forest Classifier.
- URL feature extraction and preprocessing.
- Detection of IP-based URLs.
- Suspicious URL length detection.
- URL shortening service detection.
- Suspicious symbol detection.
- Domain and subdomain analysis.
- HTTPS verification.
- Rule-based phishing detection.
- Interactive web interface using Flask.
- Model persistence using Joblib.

## 🛠️ Technologies Used

**Programming Language**
- Python

**Machine Learning**
- Scikit-learn
- Random Forest Classifier

**Data Processing**
- Pandas
- NumPy

**Backend Development**
- Flask

**Model Serialization**
- Joblib

**Frontend**
- HTML
- CSS

## 🧠 Machine Learning Approach

The project uses a Random Forest Classifier to classify website URLs based on extracted URL characteristics.

### Model Training Workflow

1. Load the phishing website dataset.
2. Preprocess the dataset.
3. Separate input features and target labels.
4. Split the dataset into training and testing sets.
5. Train the Random Forest Classification model.
6. Evaluate the model using accuracy.
7. Save the trained model using Joblib.

### Model Configuration

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Number of Estimators | 100 |
| Test Size | 20% |
| Random State | 42 |
| Evaluation Metric | Accuracy |

## 🔍 URL Feature Extraction

The application currently extracts the following eight URL characteristics:

| Feature | Description |
|---|---|
| UsingIP | Checks whether the URL uses an IP address |
| LongURL | Identifies unusually long URLs |
| ShortURL | Checks for known URL shorteners |
| Symbol@ | Detects the presence of the @ symbol |
| Redirecting// | Checks for suspicious redirection patterns |
| PrefixSuffix- | Detects hyphens in domain names |
| SubDomains | Analyzes the number of domain dots |
| HTTPS | Checks whether the URL uses HTTPS |

The application also applies additional rule-based checks for suspicious symbols and keywords.

**Note:** The current application extracts eight of the model's thirty training features and initializes the remaining features to zero. Therefore, predictions are based on a simplified feature representation and should not be considered fully validated phishing detection results.

## ⚙️ How the System Works

1. The user enters a website URL.
2. Flask receives the submitted URL.
3. The application parses the URL.
4. URL characteristics are extracted.
5. Additional rule-based checks identify suspicious patterns.
6. The trained Random Forest model generates a prediction.
7. The result is displayed on the web interface.

## 📂 Project Structure

```text
Phishing-Project/
│
├── app.py
│   └── Flask application and URL prediction
│
├── train_model.py
│   └── Machine learning model training
│
├── index.html
│   └── Frontend interface
│
├── requirements.txt
│   └── Python dependencies
│
├── data/
│   └── phishing.csv
│
├── models/
│   ├── phishing_model.joblib
│   └── feature_columns.joblib
│
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rithesh1825/Phishing-Project.git
```

### 2. Navigate to the Project Directory

```bash
cd Phishing-Project
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the Dataset

Place your phishing dataset at:

```text
data/phishing.csv
```

The dataset must contain the required training features and a target column named `class`.

### 6. Train the Machine Learning Model

```bash
python train_model.py
```

The training script generates the model files:

```text
models/phishing_model.joblib
models/feature_columns.joblib
```

Ensure the `data` and `models` directories exist before running the training script.

### 7. Run the Flask Application

The Flask application expects its HTML template inside a `templates` directory.

Place `index.html` inside:

```text
templates/index.html
```

Then execute:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

Enter a website URL and click the detection button to view the prediction.

## 🎯 Project Objectives

- Understand machine learning applications in cybersecurity.
- Develop a URL-based phishing detection system.
- Implement URL parsing and feature extraction.
- Train a Random Forest classification model.
- Build a web application using Flask.
- Integrate a trained machine learning model into a web interface.

## 🔮 Future Enhancements

- Implement complete extraction of all thirty training features.
- Improve phishing detection accuracy.
- Integrate domain reputation checking.
- Add real-time threat intelligence APIs.
- Implement WHOIS-based domain analysis.
- Develop a more advanced dashboard.
- Add phishing email detection.
- Improve model evaluation using precision, recall, F1-score and confusion matrices.

## 👨‍💻 Author

**Rithesh K**

GitHub: [@rithesh1825](https://github.com/rithesh1825)

Project Repository: [Phishing-Project](https://github.com/rithesh1825/Phishing-Project)

## ⚠️ Disclaimer

This project is developed for educational and research purposes. It is a demonstration of machine learning-based phishing detection and should not be used as the sole security mechanism for determining whether a website is safe.

---

⭐ If you find this project interesting, consider giving the repository a star!
