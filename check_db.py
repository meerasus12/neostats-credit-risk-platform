import pandas as pd
df = pd.read_csv("data/home-credit-default-risk/application_train.csv")
template = df.drop(columns=["TARGET", "SK_ID_CURR"]).iloc[[0]]
template.to_csv("data/applicant_template.csv", index=False)