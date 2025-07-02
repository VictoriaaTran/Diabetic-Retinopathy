import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# load datset
df = pd.read_csv("diabetes_dataset00.csv")

st.title("Diabetic Retinopathy Dashboard")

# page configuration
st.set_page_config(
    page_title="Diabetic Retinopathy Dashboard",
    layout='wide'
)

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
        






