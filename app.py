# Power Analysis App
import streamlit as st  # pip install streamlit
import psutil
import numpy as np
from scipy.stats import norm

# -------------- SETTINGS --------------
page_title = "Power Analysis"
page_icon = "📶"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)


#%%
# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Define a function to get the current CPU and memory usage of the system
def get_system_usage():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    return cpu_percent, mem_percent

# Define a function to check if the app can serve a new user based on the current resource usage
def can_serve_user():
    cpu_percent, mem_percent = get_system_usage()
    # Check if the current CPU and memory usage are below the threshold
    if cpu_percent < 80 and mem_percent < 80:
        return True
    else:
        return False

def main():
# Check if the app can serve a new user
    if can_serve_user():    
        st.text('Mohamed Naser ©2024')
        n1 = st.number_input("Number of positive cases", min_value=0, value=100, format="%i", step=10)
        n2 = st.number_input("Number of negative cases", min_value=0, value=100, format="%i", step=10)
                
        AUC0 = st.number_input("Null hypothesis AUC", min_value=0.0, value=0.80, max_value=1.0)
        AUC1 = st.number_input("Alternative AUC", min_value=0.0, value=0.85, max_value=1.0)
        alpha = st.number_input("Significance level (one-sided)", min_value=0.0, value=0.05, max_value=1.0)
        
        # Calculate the standard error for AUC
        Q1 = AUC1 / (2 - AUC1)
        Q2 = 2 * AUC1**2 / (1 + AUC1)
        SE_AUC = np.sqrt((AUC1 * (1 - AUC1) + (n1 - 1) * (Q1 - AUC1**2) + (n2 - 1) * (Q2 - AUC1**2)) / (n1 * n2))

        # Calculate the z-score for the difference
        z = (AUC1 - AUC0) / SE_AUC

        # Calculate power using the cumulative distribution function of the standard normal distribution
        power = norm.cdf(z - norm.ppf(1 - alpha))
        st.write(f"Calculated power: {power}")
        
    else:
        st.write("Sorry, the app is currently overloaded. Please try again later.")

main()
    
