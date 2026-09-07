# ============================================================
# CREDIT RISK PLATFORM - FLASK APPLICATION
# ============================================================

from flask import Flask, jsonify, request, render_template
import joblib
import pandas as pd
import numpy as np
import os


# ============================================================
# IMPORT NL-TO-SQL
# ============================================================

from src.nl_to_sql import answer_question


# ============================================================
# IMPORT CONVERSATION MEMORY
# ============================================================

from src.conversation_memory import (
    add_to_memory,
    get_memory,
    get_memory_text,
    clear_memory
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# BASE DIRECTORY
# ============================================================

# This always points to the project directory.
# On Windows:
# C:\Users\meera\Neostat\credit_risk_platform
#
# Inside Docker:
# /app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# MODEL PATHS
# ============================================================

MODEL_FILE = os.path.join(
    BASE_DIR,
    "model.pkl"
)

PREPROCESSOR_FILE = os.path.join(
    BASE_DIR,
    "preprocessor.pkl"
)

EXPLAINER_FILE = os.path.join(
    BASE_DIR,
    "explainer.pkl"
)


# ============================================================
# TRAINING DATA PATH
# ============================================================

TRAIN_FILE = os.path.join(
    BASE_DIR,
    "data",
    "home-credit-default-risk",
    "application_train.csv"
)


# ============================================================
# DEBUG PATH INFORMATION
# ============================================================

print("=" * 70)
print("CREDIT RISK PLATFORM")
print("=" * 70)

print("BASE_DIR:", BASE_DIR)
print("TRAIN_FILE:", TRAIN_FILE)
print("MODEL_FILE:", MODEL_FILE)
print("PREPROCESSOR_FILE:", PREPROCESSOR_FILE)
print("EXPLAINER_FILE:", EXPLAINER_FILE)

print("=" * 70)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# LOAD PREPROCESSOR
# ============================================================

print("Loading preprocessor...")

preprocessor = joblib.load(PREPROCESSOR_FILE)

print("Preprocessor loaded successfully.")


# ============================================================
# SHAP EXPLAINER
# ============================================================

# Loaded only when prediction is requested.

explainer = None


def get_explainer():

    global explainer

    if explainer is None:

        print("Loading SHAP explainer...")

        explainer = joblib.load(EXPLAINER_FILE)

        print("SHAP explainer loaded successfully.")

    return explainer


# ============================================================
# CHECK TRAINING DATA
# ============================================================

def check_training_file():

    if not os.path.exists(TRAIN_FILE):

        raise FileNotFoundError(
            f"Training dataset not found at: {TRAIN_FILE}"
        )


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_risk(input_data):

    # ------------------------------------------------------------
    # LOAD DATASET
    # ------------------------------------------------------------

    df = pd.read_csv(TRAIN_FILE)

    # Use the first applicant as a complete template
    applicant = df.drop(
        columns=["TARGET", "SK_ID_CURR"]
    ).iloc[0].copy()


    # ------------------------------------------------------------
    # MAP WEBSITE INPUTS TO HOME CREDIT COLUMNS
    # ------------------------------------------------------------

    input_mapping = {

        "gender": "CODE_GENDER",

        "income_type": "NAME_INCOME_TYPE",

        "family_status": "NAME_FAMILY_STATUS",

        "property": "FLAG_OWN_REALTY",

        "income": "AMT_INCOME_TOTAL",

        "credit": "AMT_CREDIT",

        "annuity": "AMT_ANNUITY"
    }


    # ------------------------------------------------------------
    # APPLY WEBSITE VALUES
    # ------------------------------------------------------------

    for web_key, dataset_column in input_mapping.items():

        if web_key in input_data:

            value = input_data[web_key]

            # Numeric values
            if dataset_column in [
                "AMT_INCOME_TOTAL",
                "AMT_CREDIT",
                "AMT_ANNUITY"
            ]:

                value = float(value)


            # Property ownership
            elif dataset_column == "FLAG_OWN_REALTY":

                value = 1 if str(value).lower() == "yes" else 0


            applicant[dataset_column] = value


    # ------------------------------------------------------------
    # AGE → DAYS_BIRTH
    # ------------------------------------------------------------

    if "age" in input_data:

        age = float(input_data["age"])

        # Home Credit stores age approximately as negative days
        applicant["DAYS_BIRTH"] = -age * 365


    # ------------------------------------------------------------
    # CREATE DATAFRAME
    # ------------------------------------------------------------

    input_df = pd.DataFrame(
        [applicant]
    )


    # ------------------------------------------------------------
    # PREPROCESS
    # ------------------------------------------------------------

    processed_data = preprocessor.transform(
        input_df
    )


    # ------------------------------------------------------------
    # PREDICTION
    # ------------------------------------------------------------

    probability = model.predict_proba(
        processed_data
    )[0, 1]


    # ------------------------------------------------------------
    # RISK SCORE
    # ------------------------------------------------------------

    score = probability * 100


    # ------------------------------------------------------------
    # RISK BAND
    # ------------------------------------------------------------

    if score < 30:

        band = "Low Risk"

    elif score < 60:

        band = "Medium Risk"

    else:

        band = "High Risk"


    # ------------------------------------------------------------
    # SHAP EXPLANATION
    # ------------------------------------------------------------
    # ============================================================
    # SHAP EXPLANATION
    # ============================================================

    current_explainer = get_explainer()

    shap_values = current_explainer.shap_values(processed_data)
    shap_array = np.array(shap_values)

    if shap_array.ndim == 3:
        shap_array = shap_array[0, :, 1]
    elif shap_array.ndim == 2:
        shap_array = shap_array[0]
    else:
        shap_array = shap_array.reshape(-1)

    # ------------------------------------------------------------
    # FEATURE NAMES
    # ------------------------------------------------------------

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )


    min_length = min(
        len(feature_names),
        len(shap_array)
    )


    feature_names = feature_names[
        :min_length
    ]

    shap_array = shap_array[
        :min_length
    ]


    # ------------------------------------------------------------
    # CREATE SHAP TABLE
    # ------------------------------------------------------------

    shap_df = pd.DataFrame({

        "Feature": feature_names,

        "SHAP Value": shap_array,

        "Absolute Impact": np.abs(
            shap_array
        )

    })


    shap_df = shap_df.sort_values(
        "Absolute Impact",
        ascending=False
    )


    # ------------------------------------------------------------
    # TOP 5 FEATURES
    # ------------------------------------------------------------

    top_features = shap_df.head(5)


    explanations = []


    for _, row in top_features.iterrows():

        explanations.append({

            "feature": row["Feature"],

            "impact":
                "increased"
                if row["SHAP Value"] > 0
                else "decreased",

            "shap_value":
                round(
                    float(row["SHAP Value"]),
                    4
                )

        })


    # ------------------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------------------

    return (
        probability,
        score,
        band,
        explanations
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "dataset_exists":
            os.path.exists(TRAIN_FILE),

        "dataset_path":
            TRAIN_FILE

    })


# ============================================================
# TEST PREDICTION
# ============================================================

@app.route("/test-predict")
def test_predict():

    try:

        check_training_file()


        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

        df = pd.read_csv(
            TRAIN_FILE
        )


        print(
            "Dataset shape:",
            df.shape
        )


        # ----------------------------------------------------
        # TAKE FIRST APPLICANT
        # ----------------------------------------------------

        test_applicant = df.drop(
            columns=[
                "TARGET",
                "SK_ID_CURR"
            ]
        ).iloc[0].to_dict()


        # ----------------------------------------------------
        # PREDICT
        # ----------------------------------------------------

        (
            probability,
            score,
            band,
            explanations
        ) = predict_risk(
            test_applicant
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "default_probability":
                float(probability),

            "risk_score":
                float(score),

            "risk_band":
                band,

            "explanations":
                explanations

        })


    except Exception as e:

        print(
            "Test prediction error:",
            str(e)
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# WEBSITE PREDICTION API
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # ----------------------------------------------------
        # GET DATA FROM WEBSITE
        # ----------------------------------------------------

        input_data = request.get_json()


        if not input_data:

            return jsonify({

                "success": False,

                "error":
                    "No applicant data received."

            }), 400


        print(
            "Received input:",
            input_data
        )


        # ----------------------------------------------------
        # RUN PREDICTION
        # ----------------------------------------------------

        (
            probability,
            score,
            band,
            explanations
        ) = predict_risk(
            input_data
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "default_probability":
                float(probability),

            "risk_score":
                float(score),

            "risk_band":
                band,

            "explanations":
                explanations

        })


    except Exception as e:

        print(
            "Prediction error:",
            str(e)
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# TALK-TO-DATA API
# ============================================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    try:

        # ----------------------------------------------------
        # GET QUESTION
        # ----------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No question data received."

            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        # ----------------------------------------------------
        # CHECK EMPTY QUESTION
        # ----------------------------------------------------

        if not question:

            return jsonify({

                "success": False,

                "error":
                    "Please enter a question."

            }), 400


        # ----------------------------------------------------
        # PRINT QUESTION
        # ----------------------------------------------------

        print()
        print("=" * 70)
        print("TALK-TO-DATA")
        print(
            "Question:",
            question
        )


        # ----------------------------------------------------
        # GET ANSWER
        # ----------------------------------------------------

        answer = answer_question(
            question
        )


        print(
            "Answer:",
            answer
        )


        # ----------------------------------------------------
        # STORE CONVERSATION
        # ----------------------------------------------------

        add_to_memory(
            question,
            answer
        )


        # ----------------------------------------------------
        # GET MEMORY
        # ----------------------------------------------------

        memory = get_memory()


        print()
        print("Conversation memory:")

        print(
            get_memory_text()
        )

        print(
            "=" * 70
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "question":
                question,

            "answer":
                answer,

            "conversation_length":
                len(memory)

        })


    except Exception as e:

        print(
            "Talk-to-Data error:",
            str(e)
        )


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# VIEW CONVERSATION MEMORY
# ============================================================

@app.route(
    "/memory",
    methods=["GET"]
)
def view_memory():

    try:

        memory = get_memory()


        return jsonify({

            "success": True,

            "conversation":
                memory,

            "conversation_text":
                get_memory_text(),

            "conversation_length":
                len(memory)

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# CLEAR CONVERSATION MEMORY
# ============================================================

@app.route(
    "/clear-memory",
    methods=["POST"]
)
def clear_memory_route():

    try:

        clear_memory()


        return jsonify({

            "success": True,

            "message":
                "Conversation memory cleared."

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# RUN FLASK APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )