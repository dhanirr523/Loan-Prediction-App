import streamlit as st
import streamlit.components.v1 as stc
import pickle

with open('Logistic_Regression_Model.pkl', 'rb') as file:
    Logistic_Regression_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Loan Eligibility Prediction App</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Credit Team</h4> 
                """

desc_temp = """ ### Loan Prediction App 
                This app is used by Credit team for deciding Loan Application
                
                #### Data Source
                Kaggle: Link <Masukkan Link>
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#000">Loan Eligibility Prediction</h1>
                    <h2 style="color:#000">Fill this simulation according to the actual condition</h1>
                </div
             """
    st.markdown(design, unsafe_allow_html=True)
    left, right = st.columns((2,2))
    gender = left.selectbox("Gender", ("Male","Female"))
    married = right.selectbox("Married", ("Yes","No"))
    dependent = left.selectbox("Dependents", ("0","1","2","3+"))
    education = right.selectbox("Education", ("Graduate","Not Graduate"))
    self_employed = left.selectbox("Self Employed", ("Yes","No"))
    applicant_income = right.number_input("Applicant Income", 0, 1000000, 0)
    coApplicant_income = left.number_input("Co-Applicant Income", 0, 1000000, 0)
    loan_amount = right.number_input("Loan Amount", 0, 1000000, 0)
    loan_amount_term = left.number_input("Loan Amount Term", 0, 500, 0)
    credit_history = right.selectbox("Credit History", (0.0,1.0))
    property_area = st.selectbox("Property Area", ("Urban","Rural","Semiurban"))
    button = st.button("Predict")


    #If button is clicked
    if button:
        result = predict(gender, married, dependent, education, self_employed,applicant_income, coApplicant_income, loan_amount, loan_amount_term, credit_history, property_area)
        if result == 'Eligible':
            st.success(f"Congratulations! You are {result} for the loan.")
        else:
            st.warning(f"Sorry! You are {result} for the loan.")

def predict(gender, married, dependent, education, self_employed, applicant_income, coApplicant_income
                         ,loan_amount, loan_amount_term, credit_history, property_area):
    
    #Making prediction
    gen = 0 if gender == "Male" else 1
    mar = 0 if married == "No" else 1
    dep = 3 if dependent == "3+" else int(dependent)
    edu = 0 if education == "Graduate" else 1
    sem = 0 if self_employed == "Yes" else 1
    pro = 0 if property_area == "Semiurban" else 1 if property_area == "Urban" else 2
    lam = loan_amount / 1000
    cap = coApplicant_income / 1000

    prediction = Logistic_Regression_Model.predict([[gen, mar, dep, edu, sem, applicant_income, cap,
                                                    lam, loan_amount_term, credit_history, pro]])
    # 1 means eligible, 0 means not eligible
    #Returning the result
    result = "Eligible" if prediction == 1 else "Not Eligible"
    return result

if __name__ == "__main__":
    main()
