import pandas as pd
import streamlit as st
import plotly.express as px

# Function to load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Set page configuration
st.set_page_config(layout="wide")

# Function for the Home tab
def home_tab():
    st.title("AIRBNB DATA ANALYSIS")
    st.write("")

# Function for the Data Exploration tab
def data_exploration_tab(df):
    st.title("DATA EXPLORATION")
    st.subheader("PRICE ANALYSIS")
    price_analysis(df)
    
    st.subheader("AVAILABILITY ANALYSIS")
    availability_analysis(df)  # Call the availability analysis by season function here

def price_analysis(df):
    st.title("Price Analysis and Visualization")
    
    # Filter options
    country = st.selectbox("Select country", df["country"].unique())
    room_type = st.selectbox("Select room Type", df[df["country"] == country]["room_type"].unique())
    
    # Filtered dataframe
    filtered_df = df[(df["country"] == country) & (df["room_type"] == room_type)]
    
    # Visualization - Price by Property Type
    st.subheader("Price by Property Type")
    fig_bar = px.bar(filtered_df, x="property_type", y="price", title="Price by Property Type", color="property_type",
                     labels={"price": "Price", "property_type": "Property Type"},
                     color_discrete_map={"Apartment": "blue", "House": "green", "Condo": "orange"})
    
    st.plotly_chart(fig_bar)
    
    # Visualization - Price Distribution
    st.subheader("Price Distribution")
    fig_box = px.box(filtered_df, y="price", title="Price Distribution (Box Plot)")
    st.plotly_chart(fig_box)

# Function for availability analysis by season
def availability_analysis(df_a):
    st.title("**AVAILABILITY ANALYSIS**")
    col1, col2 = st.columns(2)

    with col1:
        country_a = st.selectbox("Select the Country_a", df_a["country"].unique())

        df1_a = df_a[df_a["country"] == country_a]
        df1_a.reset_index(drop=True, inplace=True)

        property_ty_a = st.selectbox("Select the Property Type", df1_a["property_type"].unique())

        df2_a = df1_a[df1_a["property_type"] == property_ty_a]
        df2_a.reset_index(drop=True, inplace=True)

        df_a_sunb_30 = px.sunburst(df2_a, path=["room_type", "bed_type", "is_location_exact"], values="availability_30",
                                    width=600, height=500, title="Availability_30",
                                    color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(df_a_sunb_30)

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        df_a_sunb_60 = px.sunburst(df2_a, path=["room_type", "bed_type", "is_location_exact"], values="availability_60",
                                    width=600, height=500, title="Availability_60",
                                    color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(df_a_sunb_60)

    col1, col2 = st.columns(2)

    with col1:
        df_a_sunb_90 = px.sunburst(df2_a, path=["room_type", "bed_type", "is_location_exact"], values="availability_90",
                                    width=600, height=500, title="Availability_90",
                                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
        st.plotly_chart(df_a_sunb_90)

    with col2:
        df_a_sunb_365 = px.sunburst(df2_a, path=["room_type", "bed_type", "is_location_exact"], values="availability_365",
                                     width=600, height=500, title="Availability_365",
                                     color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(df_a_sunb_365)

    roomtype_a = st.selectbox("Select the Room Type_a", df2_a["room_type"].unique())

    df3_a = df2_a[df2_a["room_type"] == roomtype_a]

    df_mul_bar_a = pd.DataFrame(
        df3_a.groupby("host_response_time")[["availability_30", "availability_60", "availability_90", "availability_365",
                                              "price"]].sum())
    df_mul_bar_a.reset_index(inplace=True)

    fig_df_mul_bar_a = px.bar(df_mul_bar_a, x='host_response_time',
                               y=['availability_30', 'availability_60', 'availability_90', "availability_365"],
                               title='AVAILABILITY BASED ON HOST RESPONSE TIME', hover_data="price",
                               barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r, width=1000)

    st.plotly_chart(fig_df_mul_bar_a)

# Function for the About tab
def about_tab():
    st.header("ABOUT THIS PROJECT")
    # Write your content for the About tab here

# Main function to run the Streamlit app
def main():
    st.sidebar.title("Main Menu")
    select = st.sidebar.radio("", ["Home", "Data Exploration", "About"])
    
    df = load_data(r'C:\python\sd.csv')
    
    if select == "Home":
        home_tab()
    elif select == "Data Exploration":
        data_exploration_tab(df)
    elif select == "About":
        about_tab()

if __name__ == "__main__":
    main()
