# Challenge Documentation

## Summary

### Deployment on Render

This application is deployed on [Render](https://render.com).
Render spins down free services after a period of inactivity. The first visit to the live site after a spin-down will experience a cold start delay while the server boots up (typically 30-60 seconds).
**Before starting stress testing:**
1.  Manually visit the [live site](https://latamairlineschallenge.onrender.com/) first.
2.  Wait for the initial load to complete.
3.  Once the site is responsive, you can begin your testing.

### Model Selection: XGBoost

For this challenge, I chose to use the **XGBoost** model with the top 10 most important features and class balancing.

The Jupyter notebook `exploration.ipynb` considered XGBoost and Logistic Regression models. While both models achieved similar peformance metrics after selecting the top 10 most important features (according to XGBoost) and balancing classes, I believe that XGBoost is more adequate as in the long term it is more likely to perform well if the data distribution changes in the future towards non-linearity. Other key observations of importance are that class balance is crucial as otherwise recall for class 1 is close to 0, which is the most important metric as flight delay should rather have false positives than false negatives.

### API Validation and Pydantic

In `challenge/api.py`, input validation is crucial to ensure the API receives data in the expected format and to prevent errors. We use Pydantic for this. Pydantic allows defining data schemas using Python type hints. This ensures that incoming request bodies conform to the `Flight` model, which specifies that `OPERA` and `TIPOVUELO` should be strings, and `MES` an integer. If the input data does not match the schema, FastAPI automatically returns a clear error response. 

## Stack and Main Dependencies

This project utilizes the following technologies and libraries:

*   **Python 3.10** 
*   **FastAPI** 
*   **Uvicorn** 
*   **Pandas** 
*   **Numpy** 
*   **XGBoost** 
*   **Scikit-learn** 
*   **Pydantic** 
*   **Pytest** 
*   **Coverage** 
*   **Locust**

## How to Run

### 1. Clone the Repository

First, clone the challenge repository to your local machine.


### 2. Set up a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies. We recommend using conda and Python 3.10.

```bash
conda create --prefix "path\to\project\venv" python=3.10
```

### 3. Install Dependencies

Activate your virtual environment and install the required Python packages:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-test.txt
pip install xgboost
pip install jupyter
pip install "anyio<4.0.0"
pip install jinja2<3.1.0
pip install itsdangerous==2.0.1
pip install werkzeug==2.0.3
```

### 4. Run Tests

You can run the model and API tests using `make`:
```bash
make model-test
make api-test
```

## Project Tree

```
.
├── Dockerfile
├── Makefile
├── README.md
├── requirements-dev.txt
├── requirements-test.txt
├── requirements.txt
├── challenge/
│   ├── __init__.py
│   ├── api.py
│   ├── exploration.ipynb
│   └── model.py
├── data/
│   └── data.csv
├── docs/
│   └── challenge.md
├── tests/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── model/
│       ├── __init__.py
│       └── test_model.py
└── workflows/
    ├── cd.yml
    └── ci.yml
```


