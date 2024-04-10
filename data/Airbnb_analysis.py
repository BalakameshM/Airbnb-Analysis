import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def extract_month(date):
    return datetime.datetime.strptime(date, '%d-%m-%Y').month

def extract_year(date):
    return datetime.datetime.strptime(date, '%d-%m-%Y').year

def load_data(file_path):
    return pd.read_csv(file_path)

st.set_page_config(layout="wide")

def home_tab():
    st.title("AIRBNB DATA ANALYSIS")
    st.image("https://ichef.bbci.co.uk/news/976/cpsprodpb/B38D/production/_109556954_airbnb.png")
    st.subheader("Overview:")
    st.write("<h3>Airbnb Analysis is a comprehensive project that offers valuable insights into the dynamics of the short-term rental market. Through this project, users will gain proficiency in a wide range of skills essential for data analysis and visualization, including Python scripting, data preprocessing, exploratory data analysis (EDA), Streamlit application development, MongoDB integration, and visualization tools</h3>",unsafe_allow_html=True)
    st.write("<h3>This application is designed to provide insights into Airbnb data, allowing users to explore various aspects such as pricing trends, availability patterns, and geospatial visualization of listings. </h3>",unsafe_allow_html=True)
    

def price_analysis(df):
    st.title("Price Analysis and Visualization")

    
    df['last_review'] = pd.to_datetime(df['last_review'])

    years = df['last_review'].dt.year.unique()
    selected_year = st.selectbox("Select year", sorted(years), key="price_year_select")
    
    country = st.selectbox("Select country", df["country"].unique(), key="price_country_select")
    room_type = st.selectbox("Select room Type", df[df["country"] == country]["room_type"].unique(), key="price_room_type_select")
    market = st.selectbox("Select market", df[df["country"] == country]["market"].unique(), key="price_market_select")
    
    filtered_df = df[(df["country"] == country) & (df["room_type"] == room_type) & (df["market"] == market) & (df['last_review'].dt.year == selected_year)]
    avg_price_df = filtered_df.groupby("property_type")["price"].mean().reset_index()

    st.subheader("Price by Property Type")
    fig_bar = px.bar(avg_price_df, x="property_type", y="price", title="Price by Property Type", color="property_type",
                     labels={"price": "Price", "property_type": "Property Type"},
                     color_discrete_map={"Apartment": "blue", "House": "green", "Condo": "orange"})
    
    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(fig_bar)

    with col2:

        st.subheader("Seasonal Price Analysis")
        fig_seasonal = px.box(filtered_df, x=filtered_df['last_review'].dt.month, y='price', title='Seasonal Price Variation', labels={'x': 'Month', 'price': 'Price'})
        st.plotly_chart(fig_seasonal)

    st.subheader("Outlier Detection")
    
    z_scores = (filtered_df['price'] - filtered_df['price'].mean()) / filtered_df['price'].std()
    filtered_df['z_score'] = z_scores.abs()
    outliers = filtered_df[filtered_df['z_score'] > 3]  
    st.write("Number of outliers:", outliers.shape[0])
    st.write(outliers)
    plt.figure(figsize=(6, 3))
    sns.histplot(filtered_df['price'], kde=True, color='blue', bins=30)
    plt.title('Distribution of Prices with Outliers')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.axvline(x=outliers['price'].min(), color='red', linestyle='--', label='Outlier Threshold')
    plt.axvline(x=outliers['price'].max(), color='red', linestyle='--')
    plt.legend()
    st.pyplot(plt)

    st.subheader("Correlation Analysis")
    corr_data = filtered_df[['price', 'latitude', 'longitude']] 
    corr_matrix = corr_data.corr(method='pearson') 
    
    plt.figure(figsize=(4, 2))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix')
    st.pyplot(plt)

    st.subheader("Location Based Insights")
    fig_scatter = px.scatter(filtered_df, x='longitude', y='latitude', color='price', title='Price Distribution by Location',
                            hover_data=['longitude', 'latitude', 'price', 'street'], width=1000)
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.5))
    st.plotly_chart(fig_scatter)

def availability_analysis(df):
    
    st.title("Availability Analysis by Season")
    df['last_review'] = pd.to_datetime(df['last_review'])
    years = df['last_review'].dt.year.unique()
    selected_year = st.selectbox("Select year", sorted(years), key="availability_year_select")
    country = st.selectbox("Select country", df["country"].unique(), key="availability_country_select")
    room_type = st.selectbox("Select room Type", df[df["country"] == country]["room_type"].unique(), key="availability_room_type_select")
    
    col1, col2= st.columns(2)

    with col1:

        filtered_df = df[(df["country"] == country) & (df["room_type"] == room_type) & (df['last_review'].dt.year == selected_year)]
        filtered_df['month'] = filtered_df['last_review'].dt.month
        filtered_df['occupancy'] = filtered_df['number_of_reviews'] / filtered_df['availability_365'] * 100
        
        occupancy_df = filtered_df.groupby(['month', 'country', 'room_type'])['occupancy'].mean().reset_index()
        pivot_df = occupancy_df.pivot_table(index="country", columns="month", values="occupancy", aggfunc="mean")

        st.subheader("Occupancy Rates by Month")
        fig_heatmap = px.imshow(pivot_df, labels=dict(x="Month", y="Country", color="Occupancy Rate"),
                                x=pivot_df.columns, y=pivot_df.index,
                                title='Occupancy Rates by Month (Heatmap)',
                                color_continuous_scale='Viridis')
        
        st.plotly_chart(fig_heatmap)

    with col2:
        booking_counts = filtered_df.groupby('month')['number_of_reviews'].sum().reset_index()
        st.subheader("Booking Patterns by Month")
        fig_booking_patterns = px.bar(booking_counts, x='month', y='number_of_reviews', 
                                title='Booking Patterns by Month', 
                                labels={'month': 'Month', 'number_of_reviews': 'Total Bookings'})
        st.plotly_chart(fig_booking_patterns)

    col3, col4= st.columns(2)

    with col3:
        st.subheader("Occupancy Rates by Month (Line Chart)")
        fig_line = px.line(occupancy_df, x='month', y='occupancy', color='country',
                        title='Occupancy Rates by Month (Line Chart)',
                        labels={'month': 'Month', 'occupancy': 'Occupancy Rate', 'country': 'Country'})
        st.plotly_chart(fig_line)

    with col4:
        demand_df = filtered_df.groupby('month')[['occupancy', 'price']].mean().reset_index()
        st.subheader("Demand Fluctuations")
        fig_demand_fluctuations = px.line(demand_df, x='month', y=['occupancy', 'price'], 
                                    title='Demand Fluctuations over Time',
                                    labels={'month': 'Month', 'value': 'Value', 'variable': 'Metric'},
                                    color_discrete_map={'occupancy': 'blue', 'price': 'orange'})
        st.plotly_chart(fig_demand_fluctuations)

def geospatial_visualization(df):
    st.title("Geospatial Visualization")

    df['last_review'] = pd.to_datetime(df['last_review'])

    years = df['last_review'].dt.year.unique()
    selected_year = st.selectbox("Select year", sorted(years), key="geospatial_year_select")
    filtered_df = df[df['last_review'].dt.year == selected_year]

    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", hover_name="country",
                            hover_data=["name", "price", "review_scores", "government_area", "market", "street","host_response_rate"],
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            color="price",
                            size_max=15, zoom=10)

   
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=10,
                      mapbox_center={"lat": filtered_df['latitude'].mean(), "lon": filtered_df['longitude'].mean()},width=1700, height=600)

    st.plotly_chart(fig)

    filtered_df['month'] = filtered_df['last_review'].dt.month

    avg_host_response_rate_df = filtered_df.groupby("month")["host_response_rate"].mean().reset_index()
    
    st.subheader("Host Response Rate Over Time")
    fig_line = px.line(avg_host_response_rate_df, x="month", y="host_response_rate",
                   labels={"host_response_rate": "Response Rate", "month": "Month"},
                   line_shape="spline")
    fig_line.update_traces(name="Host Response Rate") 
    fig_line.update_layout(title="Host Response Rate Over Time") 
    st.plotly_chart(fig_line)

    avg_review_scores_df = filtered_df.groupby("month")["review_scores"].mean().reset_index()
    
    st.subheader("Review scores Over Time")
    fig_bar = px.bar(avg_review_scores_df, x="month", y="review_scores", title="Review scores Over Time",
                     labels={"month": "Month", "review_scores": "Review Score"},color="month",color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_bar)
    

def data_exploration_tab(df):
    st.title("DATA EXPLORATION")
    
    
    tabs = st.tabs(["Price Analysis", "Availability Analysis", "Geospatial Visualization"])
    
    with tabs[0]:
        price_analysis(df)
    
    with tabs[1]:
         availability_analysis(df)
        
    with tabs[2]:
         geospatial_visualization(df)
    
     

def main():

    st.sidebar.title("Main Menu")
    select = st.sidebar.radio("", ["Home", "Data Exploration"])

    df = load_data(r'C:\python\AirbnbAnalysis.csv')

    if select == "Home":
        home_tab()
    elif select == "Data Exploration":
        data_exploration_tab(df)
        
   

if __name__ == "__main__":
            main()