import os
import streamlit as st

# EDA Pkgs
import pandas as pd

# Viz Pkgs
#import matplotlib.pyplot as plt
#import matplotlib

#import seaborn as sns


def main():
    """ Common ML Dataset Explorer """
    st.title("Common ML Dataset Explorer")
    st.subheader("Simple Data Science Explorer with Streamlit")

    html_temp = """
    <div style="background-color:tomato;"><p style="color:white;font-size:60px;"> Streamlit is Awesome</p></div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    def file_selector(folder_path="./datasets"):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select a file:", filenames)
        return os.path.join(folder_path,selected_filename)
    
    filename = file_selector()
    st.info("You selected {}".format(filename))

    # Read Data
    df = pd.read_csv(filename)

    # Show Dataset
    if st.checkbox('Show Dataset'):
        number = st.number_input('Number of rows to view', 1)
        st.dataframe(df.head(number))

    # Show Columns
    if st.button("Column name"):
        st.write(df.columns)

    # Show Shape
    if st.checkbox("Shape Dataset"):
        data_dim = st.radio("Show Dimension By:", ("Rows", "Columns"))
        if data_dim == "Rows":
            st.text("Number of rows")
            st.write(df.shape[0])
        elif data_dim == "Columns":
            st.text("Number of columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)

    # Select Columns
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.to_list()
        selected_list = st.multiselect("Select", all_columns)
        new_df = df[selected_list]
        st.dataframe(new_df)

    # Show Values
    if st.button("Value counts"):
        st.text("Value count by Target/Class")
        st.write(df.iloc[:,-1].value_counts())

    # Show Data Types
    if st.button("Data Types"):
        st.write(df.dtypes)

    # Show Summary
    if st.checkbox("Summary"):
        st.write(df.describe().T)

    ## Plot and Visualization
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader("Data Visualization")

    # Correlation
    # Seaborn Plot
    if st.checkbox("Correlation Plot['seaborn']"):
        st.write(sns.heatmap(df.corr(),annot=True))
        st.pyplot()

    # Count Plot
    if st.checkbox("Plot of Value Counts"):
        st.text("Value Counts By Target")
        all_column_names = df.columns.to_list()
        primary_col =  st.selectbox("Primary Column to GroupBy", all_column_names)
        selected_column_names = st.multiselect("Select column", all_column_names)
        if st.button("Count Plot"):
            st.text("Generate Plot")
            if selected_column_names:
                vc_plot = df.groupby(primary_col)[selected_column_names].count()
            else:
                vc_plot = df.iloc[:,-1].value_counts()
            st.write(vc_plot.plot(kind="bar"))
            st.pyplot()

    # Pie Chart
    if st.checkbox("Pie Plot"):
        all_column_names = df.columns.to_list()
        if st.button("Pie Plot"):
            st.success("Generating A Pie Plot")
            st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
            st.pyplot()
        

    # Customizable Plot
    st.subheader("Customizable Plot")
    all_column_names = df.columns.to_list()
    type_of_plot = st.selectbox("Select Type of Plot", ["area", "bar", "line", "hist", "box", "kde"])
    selected_column_names = st.multiselect("Select Columns to Plot", all_column_names)
    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot, selected_column_names))

        # Plot by Streamlit
        if type_of_plot == "area":
            cust_data = df[selected_column_names]
            st.area_chart(cust_data)
        
        elif type_of_plot == "bar":
            cust_data = df[selected_column_names]
            st.bar(cust_data)

        elif type_of_plot == "line":
            cust_data = df[selected_column_names]
            st.line_chart(cust_data)

        # Custom Plot
        elif type_of_plot:
            cust_plot = df[selected_column_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()


if __name__ == "__main__":
    main()
