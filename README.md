# Credit Risk Prediction Platform



## 1. Project Overview



The Credit Risk Prediction Platform is an AI-assisted application designed to evaluate the potential credit default risk of loan applicants.



The platform combines machine learning, explainable AI, natural-language data querying, and a web-based interface into a single application. It uses the Home Credit Default Risk dataset to predict the probability of loan default and present the result as a risk score and risk band.



The system also provides explanations for individual predictions using SHAP and allows users to ask natural-language questions about the underlying credit dataset.



\---



## 2. Key Features



\- Credit default risk prediction

\- Default probability calculation

\- Risk score generation

\- Risk classification into:

&#x20; - Low Risk

&#x20; - Medium Risk

&#x20; - High Risk

\- SHAP-based prediction explanations

\- Natural-language querying of credit data

\- SQL-based data retrieval

\- Five supported natural-language query patterns

\- SQLite database integration

\- Flask web application

\- Dockerized deployment

\- Conversation-memory support

\- Saved machine learning model and preprocessing artifacts



\---



## 3. Dataset



The project uses the Home Credit Default Risk dataset.



Main training file:



`data/home-credit-default-risk/application\_train.csv`



The dataset contains applicant-level information such as:



\- Gender

\- Age

\- Income

\- Income type

\- Family status

\- Property ownership

\- Credit amount

\- Loan annuity

\- Employment information

\- External source features

\- Other demographic and financial attributes



Target variable:



`TARGET`



Where:



\- `TARGET = 0` → Applicant did not default

\- `TARGET = 1` → Applicant defaulted



The dataset contains 307,511 applicant records.



\---



## 4. System Architecture



The overall system follows the architecture below:



```text

&#x20;                   +----------------------+

&#x20;                   |      Web Browser     |

&#x20;                   |     Flask UI         |

&#x20;                   +----------+-----------+

&#x20;                              |

&#x20;                +-------------+-------------+

&#x20;                |                           |

&#x20;                v                           v

&#x20;       +------------------+        +------------------+

&#x20;       | Risk Prediction  |        | Natural Language |

&#x20;       | Module           |        | Query Module     |

&#x20;       +--------+---------+        +---------+--------+

&#x20;                |                            |

&#x20;                v                            v

&#x20;       +------------------+        +------------------+

&#x20;       | Preprocessing    |        | SQL Generation   |

&#x20;       | Pipeline         |        | / Query Logic    |

&#x20;       +--------+---------+        +---------+--------+

&#x20;                |                            |

&#x20;                v                            v

&#x20;       +------------------+        +------------------+

&#x20;       | Logistic         |        | SQLite Database  |

&#x20;       | Regression Model |        | application\_train|

&#x20;       +--------+---------+        +------------------+

&#x20;                |

&#x20;                v

&#x20;       +------------------+

&#x20;       | SHAP Explainable |

&#x20;       | AI Module        |

&#x20;       +------------------+




```


## 5\. Machine Learning Layer



A Logistic Regression model is used for credit default prediction.



The machine learning pipeline includes:



Loading the applicant data

Separating the target variable

Removing the applicant identifier

Handling numerical and categorical features

Preprocessing the input data

Encoding categorical variables

Transforming the features

Generating default probability

Converting probability into a risk score

Assigning a risk band

Risk Score



The predicted default probability is converted into a score between 0 and 100.



Risk Score = Default Probability × 100

Risk Bands

0 – <30     → Low Risk

30 – <60    → Medium Risk

60 – 100    → High Risk





## 6\. Explainable AI



SHAP (SHapley Additive exPlanations) is used to explain individual model predictions.



For each prediction, the application identifies the strongest factors influencing the prediction.



The interface displays:



Feature name

Direction of influence

SHAP value



For example:



Feature                         Influence

\------------------------------------------------

DAYS\_EMPLOYED                   Decreased risk

FLAG\_EMP\_PHONE                  Increased risk

EXT\_SOURCE\_3                    Increased risk

NAME\_INCOME\_TYPE\_Pensioner      Increased risk

YEARS\_BUILD\_MEDI                Increased risk



SHAP values describe the contribution of features to the model prediction and should not be interpreted as direct causal relationships.



## 7\. Natural Language to SQL



The platform provides a natural-language interface for querying the credit dataset.



Users can enter questions such as:



How many applicants are there?

How many applicants defaulted?

How many applicants did not default?

What is the average income?

What is the average credit amount?



The system converts supported questions into SQL queries, executes them against the SQLite database, and presents the result as a readable business answer.



Supported Query Patterns

Total number of applicants

Number of defaulted applicants

Number of non-defaulted applicants

Average applicant income

Average credit amount

Example



User question:



How many applicants defaulted?



SQL:



SELECT COUNT(\*) AS defaulted\_applicants

FROM application\_train

WHERE TARGET = 1;



Business answer:



There are 24,825 defaulted applicants.





## 8\. Database



The project uses SQLite for structured credit-data querying.



Database:



credit\_risk.db



Main table:



application\_train



The database contains 307,511 applicant records.



Example query:



SELECT COUNT(\*)

FROM application\_train;



Result:



307511





## 9\. Exploratory Data Analysis



The project includes exploratory analysis of the credit dataset.



The analysis covers:



Dataset structure

Numerical and categorical features

Missing-value analysis

Data quality

Default distribution

Applicant demographics

Income characteristics

Credit characteristics

Business-oriented insights



Examples of analysed relationships include:



Default rate by education level

Default rate by income type

Default rate by credit amount

Default rate by property ownership

Default rate by gender



The EDA is intended to identify patterns relevant to credit-risk assessment while avoiding unsupported causal conclusions.





## 10\. Project Structure



credit\_risk\_platform/

│

├── data/

│   └── home-credit-default-risk/

│       └── application\_train.csv

│

├── documents/

│

├── models/

│

├── notebooks/

│

├── src/

│   ├── nl\_to\_sql.py

│   ├── prompts.py

│   ├── conversation\_memory.py

│   └── config.py

│

├── templates/

│   └── index.html

│

├── app.py

├── model.pkl

├── preprocessor.pkl

├── explainer.pkl

├── credit\_risk.db

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── .env

├── .gitignore

└── README.md





## 11\. Technologies Used



Programming Language

Python 3.11

Machine Learning

Scikit-learn

Logistic Regression

Explainable AI

SHAP

Data Processing

Pandas

NumPy

Web Application

Flask

HTML

CSS

JavaScript

Database

SQLite

Natural Language Querying

Natural-language query processing

SQL generation and execution

Prompt-based query components

Deployment

Docker

Docker Compose





## 12\. Model Artifacts



The trained components are stored as serialized files:



model.pkl

preprocessor.pkl

explainer.pkl

model.pkl



Contains the trained Logistic Regression model.



preprocessor.pkl



Contains the preprocessing pipeline used to transform applicant data.



explainer.pkl



Contains the SHAP explanation model used for prediction interpretation.





## 13\. Running the Application Locally



Install the required Python packages:



pip install -r requirements.txt



Run the Flask application:



python app.py



Open the application in a browser:



http://localhost:5000





## 14\. Running with Docker



Build the Docker image:



docker compose build



Start the application:



docker compose up -d



Check the running container:



docker compose ps



The application is available at:



http://localhost:5000



To view application logs:



docker compose logs --tail=50 credit-risk-platform



To stop the application:



docker compose down





## 15\. Environment Configuration



Sensitive configuration values are stored in the .env file.



Example:



OPENAI\_API\_KEY=your\_api\_key\_here



The .env file should not be committed to a public Git repository.





## 16\. Example Prediction Workflow



The user enters applicant information through the web interface.



Example:



Gender: Female

Age: 30

Income Type: Working

Family Status: Married

Own Property: Yes

Annual Income: 500000

Credit Amount: 500000

Loan Annuity: 25000



The application then:



Applicant Input

&#x20;     ↓

Data Preparation

&#x20;     ↓

Preprocessing Pipeline

&#x20;     ↓

Logistic Regression

&#x20;     ↓

Default Probability

&#x20;     ↓

Risk Score

&#x20;     ↓

Risk Band

&#x20;     ↓

SHAP Explanation



The result is displayed in the web interface.





## 17\. Example Dataset Query Workflow



Natural Language Question

&#x20;         ↓

Query Processing

&#x20;         ↓

SQL Query

&#x20;         ↓

SQLite Database

&#x20;         ↓

Query Result

&#x20;         ↓

Readable Business Answer



Example:



Question:

How many applicants did not default?



Answer:

There are 282,686 non-defaulted applicants.





## 18\. Limitations

The model is intended as a demonstration credit-risk system and not as a production lending decision engine.

Model predictions depend on the quality and representativeness of the training data.

SHAP values indicate model contribution and do not establish causality.

The natural-language query component currently supports defined query patterns.

Risk thresholds are application-level thresholds used to categorize the predicted probability.





## 19\. Future Improvements



Possible future enhancements include:



More advanced machine-learning models

Model calibration

Additional risk features

Expanded natural-language query coverage

More advanced LLM integration

Stronger SQL validation

Authentication and authorization

Production database deployment

Model monitoring

Fairness and bias analysis

Automated model retraining





## 20\. Conclusion



The Credit Risk Prediction Platform integrates machine learning, explainable AI, natural-language data querying, database operations, and web deployment into a unified credit-risk application.



The platform demonstrates an end-to-end workflow from applicant data processing and risk prediction to explanation, data querying, and Dockerized deployment.

