import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import joblib
from joblib import load
import os
from sklearn.metrics import accuracy_score

# load datset
df = pd.read_csv("diabetes_dataset00.csv")

st.title("Diabetic Retinopathy Dashboard")

# page configuration
st.set_page_config(
    page_title="Diabetic Retinopathy Dashboard",
    layout='wide'
)

tab1, tab2, tab3 = st.tabs(["Dataset Descriptive Statistics", "Model Prediction", "Overall Performance"])

# descriptive statistics
with tab1:
    # dropdown menu to select type
    diabetic_type = df['Target'].unique()
    diabetic_type_counts = df['Target'].value_counts()

    # get counts in the same order as .unique()
    ordered_counts = diabetic_type_counts.loc[diabetic_type].values

    diabetic_options = pd.DataFrame({
        "Type": diabetic_type,
        "Count": ordered_counts,
        "Desc": [
            "Steroids can cause high blood glucose (sugar) levels which go on to develop diabetes",
            "A rare disease that get diagnosed before 6 months and reflects severe β cell dysfunction",
            "A blood sugar level that is higher than what's considered healthy, but not high enough to be type 2 diabetes.",
            "Type 1 diabetes is an autoimmune disease that occurs when your body makes little or no insulin; occurs more commonly in children and young adults",
            "High blood sugar (glucose) levels resulting from a shortage of the hormone insulin (a condition called diabetes mellitus) and progressive vision loss due to degeneration of the nerves that carry information from the eyes to the brain (a condition called optic atrophy)",
            "Diabetes that starts in adulthood and slowly gets worse over time when the pancreas stops making insulin",
            "The most common type of diabetes in middle-aged and older people, is a disease that occurs when your blood glucose is too high",
            "Rare autosomal recessive disease, characterized by neonatal/early-onset non-autoimmune insulin-requiring diabetes associated with skeletal dysplasia and growth retardation",
            "Diabetes that results as a consequence of another medication, endocrine disease or hereditary disease",
            "Diabetes results from damage to your pancreas that is not autoimmune",
            "A type of diabetes that develops exclusively in pregnancy when blood sugar levels get too high",
            "Type of diabetes that develops in individuals with cystic fibrosis (CF),characterized by both insulin deficiency and, to some extent, insulin resistance",
            "A rare form of diabetes that caused by a mutation (or change) in a single gene and runs strongly in families"
        ]
    })

    # dropdown selection
    selected_diabetic_type = st.selectbox("Select Diabetic Type:", diabetic_options['Type'])

    # Descriptive info
    col1, col2 = st.columns((1,2), border=True)

    # total count corresponding to each type
    with col1:
        total_count = diabetic_options[diabetic_options['Type'] == selected_diabetic_type].iloc[0] 
        st.metric(label="Total Count", value=f"{total_count['Count']}")

    # display information about the type
    with col2:
        type_desc = diabetic_options[diabetic_options['Type'] == selected_diabetic_type].iloc[0]
        st.write(f"##### {type_desc['Type']}:")
        st.write(type_desc['Desc'])
    
    # Function to plot a histogram plot for descriptive stats based on the selected diabetic type
    def display_stats(col, title, df_column, color, selected_type):
        with col:
            # display distribution based on selected type
            if selected_type:
                type = df[df['Target'] == selected_type]
                fig = px.histogram(data_frame=type, x=df_column, 
                                nbins=10, title=title, barmode='overlay', 
                                histnorm="probability density", color_discrete_sequence=[color])
                st.plotly_chart(fig, theme='streamlit')
            

    st.write("### Descriptive Statistics")

    # metrics to display on charts
    metrics = [
        # (chart title, df_column, chart_color)
        ("Age Distribution", "Age", '#15B2D3'),
        ("BMI Distribution", "BMI", '#236E96'),
        ("Blood Pressure", "Blood Pressure", "#00896F"),
        ("Cholesterol Levels", "Cholesterol Levels", "#F3872F"),
        ("Blood Glucose Levels", "Blood Glucose Levels", "#FF598F"),
        ("Insulin Levels", "Insulin Levels", "#D45B12")
    ]

    # creating columns for displaying charts
    cols = st.columns(3, gap='medium')

    # loop through each cols and metrics and call to plot charts
    for i, (title, df_column, color) in enumerate(metrics):
        with cols[i%3]:
            display_stats(cols[i%3], title, df_column, color, selected_diabetic_type)
            

######################################
# modeling prediction
with tab2:
    st.write("## Machine Learning Prediction Models")

    # load models
    model_names = list()
    with open("models/best_tree.pkl", "rb") as file:
        tree_model_package = joblib.load(file)
        tree_model = tree_model_package["model"]
        tree_X_test = tree_model_package['x_test']
        tree_y_test = tree_model_package['y_test']
    with open("models/log_reg_model.pkl", "rb") as file:
        log_reg_model_package = joblib.load(file)
        log_reg_model = log_reg_model_package['model']
        log_reg_x_test = log_reg_model_package['x_test']
        log_reg_y_test = log_reg_model_package['y_test']
    with open("models/rf_model.pkl", "rb") as file:
        rf_model_package = joblib.load(file)
        rf_model = rf_model_package['model']
        rf_x_test = rf_model_package['x_test']
        rf_y_test = rf_model_package['y_test']
    with open("models/xgb_model.pkl", "rb") as file:
        xgb_model_package = joblib.load(file)
        xgb_model = xgb_model_package["model"]
        xgb_model_x_test = xgb_model_package['x_test']
        xgb_model_y_test = xgb_model_package['y_test']


    col1, col2 = st.columns(2)

    with col1:
        # creating user inputs
        st.write("#### Input data")
        insulin_input = st.number_input("Insulin", value=None, min_value=0, max_value=1000, placeholder="Enter 0-1000")
        age_input = st.number_input("Age", value=None, min_value=0, max_value=110)
        bmi_input = st.number_input("BMI", value=None, min_value=10, max_value=60, placeholder="Enter 10-60")
        bp_input = st.number_input("Blood Pressure", value=None, min_value=60, max_value=200, placeholder="Enter 60-200")
        cholesterol_input = st.number_input("Cholesterol", value=None, min_value=100, max_value=400, placeholder="Enter 100-400")
        blood_glucose_input = st.number_input("Blood Glucose", value=None, min_value=70, max_value=300, placeholder="Enter 70-300")
        
        # input values for prediction analysis
        df_pred = pd.DataFrame({
            "Insulin Levels": insulin_input,
            "Age": age_input,
            "BMI": bmi_input,
            "Blood Pressure": bp_input,
            "Cholesterol Levels": cholesterol_input,
            "Blood Glucose Levels": blood_glucose_input
            
        }, index=[0])

        models = ["Decision Tree", "Logistic Regression", "Random Forest", "Gradient Boosting"]
        model_selection = st.selectbox("Select model", models)

        # label mapping for logistic regression model
        label_mapping = {
            1: "Cystic Fibrosis-Related Diabetes (CFRD)",
            2: "Gestational Diabetes",
            3: "LADA",
            4: "MODY",
            5: "Neonatal Diabetes Mellitus (NDM)",
            6: "Prediabetic",
            7: "Secondary Diabetes",
            8: "Steroid-Induced Diabetes",
            9: "Type 1 Diabetes",
            10: "Type 2 Diabetes",
            11: "Type 3c Diabetes (Pancreatogenic Diabetes)",
            12: "Wolcott-Rallison Syndrome",
            13: "Wolfram Syndrome"
        }
        def predicting_result(model_selection):
            # check if any input is None
            if (age_input is None or bmi_input is None or bp_input is None or 
                cholesterol_input is None or blood_glucose_input is None or insulin_input is None):
                return None
            if model_selection == "Decision Tree":
                prediction = tree_model.predict(df_pred.to_numpy())[0]
                return prediction
            elif model_selection == "Logistic Regression":
                prediction = log_reg_model.predict(df_pred.to_numpy())[0]
                prediction = prediction.astype(int)  # Ensure the prediction is an integer
                result = label_mapping[prediction]
                return result
            elif model_selection == "Random Forest":
                prediction = rf_model.predict(df_pred.to_numpy())[0]
                return prediction
            elif model_selection == "Gradient Boosting":
                prediction = xgb_model.predict(df_pred.to_numpy())[0]
                return prediction

        # button to predict
        if st.button("Predict"):
            result = predicting_result(model_selection)
            if result is not None:
                st.write("Parameters:", insulin_input,age_input, bmi_input, bp_input, cholesterol_input, blood_glucose_input)
                st.write(model_selection)
                st.success(f"Predicted Diabetic Type: {result}")
            else:
                st.error("Please fill all input fields before predicting.")

