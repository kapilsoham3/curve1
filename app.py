import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

st.set_page_config(page_title="Nerdy Curvy App", page_icon="🤓")

# Title and Information About the App
st.title("Low Budget Excel")
st.markdown("1) This app lets you find the curve of best fit")
st.markdown("2) You can choose from a variety of different types of curves")
st.markdown("3) You can also choose to have a histogram representation")
st.markdown("4) You can add the data manually or by uploading a file")

# Initialize Session State
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["x", "y"])  # Default empty data table

if "degree" not in st.session_state:
    st.session_state["degree"] = 1  # Default degree for the polynomial

if "plot_ready" not in st.session_state:
    st.session_state["plot_ready"] = False  # Indicates if the graph should be displayed

# Different fitting functions 
def fit_polynomial(x, scatter_y, degree):
    coeffs = np.polyfit(x, scatter_y, degree)
    equation_terms = []
    for i in range(degree, -1, -1):
        coef = coeffs[degree - i].round(4)
        if coef != 0:  # Include only non-zero terms
            term = f"{coef}" if i == 0 else f"{coef}x^{i}"
            equation_terms.append(term)
    equation = " + ".join(equation_terms) 
    x_dense = np.linspace(min(x), max(x), 500)
    y = np.polyval(coeffs, x)
    y_dense = np.polyval(coeffs, x_dense)
    rmse = np.sqrt(np.mean(np.abs((scatter_y - y) ** 2)))
    avg_error = np.mean(scatter_y - y)
    MAE = np.mean(np.abs(scatter_y-y))
    maximum_error = np.max(np.abs(scatter_y-y))
    fig, ax = plt.subplots()
    ax.scatter(x, scatter_y, color="red", label="Scatter Data")
    ax.plot(x_dense, y_dense, color="red", label="Polynomial of best fit")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Polynomial Fit")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    return equation, rmse,avg_error,MAE, maximum_error

def exponential_function(x, a, b,c,d):
    return a * np.exp(b * (x-d)) + c  

def fit_exponential_curve(x, y):
    params, covariance = curve_fit(exponential_function, x, y)
    a,b,c,d = params 
    x_dense = np.linspace(min(x), max(x), 500)
    y_fitted = exponential_function(x_dense, a, b,c,d)
    y_fit = exponential_function(x, a, b,c,d)
    equation = str(a.round(4)) + "e^[" + str(b.round(4)) + "(x - " + str(d.round(4)) + ")]" +" + " + str(c.round(4))
    rmse = np.sqrt(np.mean((np.abs(y-y_fit) ** 2)))
    avg_error = np.mean(y_fit - y)
    MAE = np.mean(np.abs(y_fit-y)) 
    maximum_error = np.max(np.abs(y_fit-y))
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="red", label="Scatter Data")
    ax.plot(x_dense, y_fitted, color="red", label="Exponential Function of best fit")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(y) - 5, max(y) + 5)
    ax.set_title("Exponential Fit")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    return equation, rmse,avg_error,MAE, maximum_error

def ln(x, a, b,c,d):
    return a * np.log(b * (x-d)) + c

def fit_ln_curve(x, y):
    bounds = bounds = ([0, 0, -np.inf, min(x) - 1], [np.inf, np.inf, np.inf, max(x) + 1])
    params, covariance = curve_fit(ln, x, y,p0 = [1, 1, 0, min(x)-1], bounds = bounds )
    a, b,c,d = params
    x_dense = np.linspace(min(x), max(x), 500)
    y_fitted = ln(x_dense, a, b, c,d)
    y_fit = ln(x, a, b, c,d)
    
    equation = str(a.round(4)) + "ln[" + str(b.round(4)) + "(" + "x -" + str(d.round(4)) + ")]  + " + str(c.round(4))
    rmse = np.sqrt(np.mean((np.abs(y-y_fit) ** 2)))
    avg_error = np.mean(y_fit - y)
    MAE = np.mean(np.abs(y_fit-y)) 
    maximum_error = np.max(np.abs(y_fit-y))
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="red", label="Scatter Data")
    ax.plot(x_dense, y_fitted, color="red", label="Logarithmic Function of best fit")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_title("Natural Logarithmic Fit")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    return equation, rmse, avg_error, MAE, maximum_error

def Histogram(x):
    fig, ax = plt.subplots()
    ax.hist(x, bins="auto")
    ax.set_title("Histogram")
    st.pyplot(fig)

def DataToPlot(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
def DataTable(data): 
    data = {
    "col 1": [
        "Equation of best fit",
        "Root Mean Square Error",
        "Average Error",
        "Mean Absolute Error",
        "Maximum Error"
    ],
    "col 2": [data[0], data[1], data[2], data[3], data[4]]  # Placeholder values
}
    df = pd.DataFrame(data)
    st.table(df)
    
st.title("Step 1: Adjust the Data!")
option = st.selectbox(
    "What type of graph would you like?",
    ("None Selected", "Exponential Curve", "Polynomial Curve", "Logarithmic Curve", "Histogram"),
)

# Reset data structure dynamically based on graph type
if option == "Histogram":
    if st.session_state["data"].shape[1] != 1:
        st.session_state["data"] = pd.DataFrame(columns=["x"])
        st.session_state["plot_ready"] = False
elif option != "None Selected":
    if st.session_state["data"].shape[1] != 2:
        st.session_state["data"] = pd.DataFrame(columns=["x", "y"])
        st.session_state["plot_ready"] = False

if "uploaded_file" in st.session_state:
    del st.session_state["uploaded_file"]

if option != "Histogram" and option != "None Selected":
    choice = st.radio(
        "Would you like to enter data manually or upload a file?",
        ["Manually", "Uploading a file"],
    )

    if choice == "Manually":
        st.write("Input your data below:")
        edited_data = st.data_editor(st.session_state["data"], num_rows="dynamic")
        submit = st.button("See Plot")
        if submit:
            st.session_state["data"] = edited_data
            st.session_state["plot_ready"] = not edited_data.empty
    elif choice == "Uploading a file":
        try:
            uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
            if uploaded_file is not None:
                dataframe = pd.read_csv(uploaded_file, header=None)
                dataframe.columns = ["x", "y"]
                st.session_state["data"] = dataframe
                st.session_state["plot_ready"] = True
        except ValueError:
            st.warning("Fill all the blank areas.")
        except RuntimeError: 
            st.warning("Apropriate Curve Can't be made")

    if option == "Polynomial Curve":
        try:
            st.session_state["degree"] = st.slider(
                "What degree do you want?", 1, 10, st.session_state["degree"]
            )
            if st.session_state["plot_ready"]:
                data = st.session_state["data"]
                if not data.empty and len(data) > 1:
                    st.title("Step2: Check the graph and other information")
                    x = data["x"].values.astype(float)
                    y = data["y"].values.astype(float)
                    data  = fit_polynomial(x, y, st.session_state["degree"])
                    st.title("Step 3: View Details about the plot")
                    DataTable(data)
                else:
                    st.warning("Please enter at least two data points.")
        except ValueError:
            st.warning("Fill all the blank areas.")
        except RuntimeError: 
            st.warning("Apropriate Curve Can't be made")
    if option == "Exponential Curve":
        try:
            if st.session_state["plot_ready"]:
                data = st.session_state["data"]
                if not data.empty and len(data) > 1:
                    st.title("Step2: Check the graph and other information")
                    x = data["x"].values.astype(float)
                    y = data["y"].values.astype(float)
                    data = fit_exponential_curve(x, y)
                    st.title("Step 3: View Details about the plot")
                    DataTable(data)
                else:
                    st.warning("Please enter atleast two datat points")
        except ValueError:
            st.warning("Fill all the blank areas.")
        except RuntimeError: 
            st.warning("Apropriate Curve Can't be made")
            DataToPlot(x,y)
    if option == "Logarithmic Curve":
      try:
            if st.session_state["plot_ready"]:
                data = st.session_state["data"]
                if not data.empty and len(data) > 1:
                    st.title("Step2: Check the graph and other information")
                    x = data["x"].values.astype(float)
                    y = data["y"].values.astype(float)
                    data  = fit_ln_curve(x, y)
                    st.title("Step 3: View Details about the plot")
                    DataTable(data)
                else:
                    st.warning("Please enter atleast two data points")
      except ValueError: 
          st.warning("Please Fill all the blank areas")  
      except RuntimeError: 
          st.warning("Apropriate Curve Can't be made")
          DataToPlot(x,y)
      
    
elif option == "Histogram":
    choice = st.radio(
        "Would you like to enter data manually or upload a file?",
        ["Manually", "Uploading a file"],
    )

    if choice == "Manually":
        st.write("Input your data below:")
        edited_data = st.data_editor(st.session_state["data"], num_rows="dynamic")
        submit = st.button("See Plot")
        if submit:
            st.session_state["data"] = edited_data
            st.session_state["plot_ready"] = not edited_data.empty;
    elif choice == "Uploading a file":
        try:
            uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
            if uploaded_file is not None:
                dataframe = pd.read_csv(uploaded_file, header=None)
                dataframe.columns = ["x"]
                st.session_state["data"] = dataframe
                st.session_state["plot_ready"] = True
        except: 
            st.warning("Please upload an apropriate file")

    if st.session_state["plot_ready"]:
        data = st.session_state["data"]
        x = data["x"].values.astype(float)
        st.title("Step2: Check the graph")
        Histogram(x)
