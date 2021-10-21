import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64
from PIL import Image

def page_set_up():
    st.title("Zhengran Ji's Page")
    st.markdown('[Zhengran Ji](https://github.com/jzr01)')
    file = st.file_uploader(label= 'upload',type = 'csv')
    return file

    
def make_chart(x_val,y_val,color_scale,df):
    chart = alt.Chart(df).mark_circle().encode(x = str(x_val),
            y = str(y_val),
            color = str(color_scale)
        )

    return chart
    

def can_be_numeric(c):
    try:
        pd.to_numeric(df[c])
        return True
    except:
        return False

def st_pandas_to_csv_download_link(_df:pd.DataFrame, file_name:str = "dataframe.csv"): 
    csv_exp = _df.to_csv(index=False)
    b64 = base64.b64encode(csv_exp.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}" > Download Sorted Dataframe (CSV) </a>'
    st.markdown(href, unsafe_allow_html=True)



if __name__ == '__main__':
    #page set up
    file = page_set_up()

    #convert the csv to df
    if file is not None:
        df = pd.read_csv(file)
        df = df.applymap(lambda x: np.nan if x == ' ' else x)
        good_cols = [c for c in df.columns if can_be_numeric(c)]
        df[good_cols] = df[good_cols].apply(pd.to_numeric, axis=0)

        x_val = st.selectbox('Choose the x_val you want',good_cols)
        y_val = st.selectbox('Choose the y_val you want',good_cols)
        color_scale = st.selectbox('Choose the color_scale you want',good_cols)


        plot_range = st.slider('How mant rows do you want to plot',0,df.shape[0]) 

    #plot the table
        message = st.write(f"The {str(file.name).split('.')[0]} file is displayed below")

        tabel = st.write(df)
        df = df.iloc[:plot_range]
    #make the chart
        chart = alt.Chart(df).mark_circle().encode(x = str(x_val),
            y = str(y_val),
            color = str(color_scale)
        )
        st.altair_chart(chart)

    #download the sorted csv
        st_pandas_to_csv_download_link(df.sort_values(str(x_val),ascending = False), file_name = "my_file.csv")
    
    
