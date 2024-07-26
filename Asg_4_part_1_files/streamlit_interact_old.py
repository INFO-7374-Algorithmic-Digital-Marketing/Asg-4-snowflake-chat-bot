import streamlit as st
from database import run_query

def interact_streamlit():
    st.title("Assg-4 : Part 1.1 : Interactive Streamlit Page")
    st.write("Using Streamlit to dynamically change values and run queries")

    # User input for query selection
    query_options = [
        "Total sales by manufacturer ID, month of year, and year",
        "Calculate the total sales price for items managed by a specific manager ID, sold in a specific month, grouped by year, brand, and brand ID, and ordered by total sales price in descending order",
        "Calculate the total sales price for catalog sales in a specific year, grouped by the state of the warehouse",
        
        
        "Count the number of store sales to customers from the United States in 1998",
        "Calculate the total sales by warehouse and month of year",
        "Calculate the total quantity purchased by customer in a given date range",
        "List the customers' last names, first names, and city, along with the total quantity of items they bought and the total amount of money they spent on catalog sales in a specific year, ordered by the amount spent in descending order",
        "Count the number of purchases made in a specific year, grouped by store name and state, and ordered by the number of purchases in descending order"
    ]
    selected_query = st.selectbox("Select a query:", query_options)

    if selected_query == "Total sales by manufacturer ID, month of year, and year":
        manufact_id = st.text_input("Enter Manufacturer ID:", "128")
        moy = st.text_input("Enter Month of Year (1-12):", "11")
        year = st.text_input("Enter Year:", "2000")
        query_to_run = f"""
        SELECT SUM(cs_ext_sales_price) AS total_sales
        FROM catalog_sales
        JOIN date_dim ON catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
        JOIN item ON catalog_sales.cs_item_sk = item.i_item_sk
        WHERE d_year = {year}
        AND i_manufact_id = {manufact_id}
        AND d_moy = {moy};
        """
    elif selected_query == "Count the number of store sales to customers from the United States in 1998":
        birth_country = st.text_input("Enter Birth Country:", "UNITED STATES")
        year = st.text_input("Enter Year:", "1998")
        query_to_run = f"""
        SELECT
            COUNT(*)
        FROM
            store_sales
            JOIN customer ON store_sales.ss_customer_sk = customer.c_customer_sk
            JOIN date_dim ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
        WHERE
            c_birth_country = '{birth_country}'
            AND d_year = 1998;
        """
    elif selected_query == "Calculate the total sales by warehouse and month of year":
        query_to_run = """
        SELECT
            w_warehouse_name,
            d_moy,
            SUM(ss_sales_price)
        FROM
            store_sales
            JOIN warehouse ON store_sales.ss_warehouse_sk = warehouse.w_warehouse_sk
            JOIN date_dim ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
        GROUP BY
            w_warehouse_name, d_moy
        ORDER BY
            w_warehouse_name, d_moy;
        """
    elif selected_query == "Calculate the total quantity purchased by customer in a given date range":
        start_date = st.text_input("Enter start date (YYYYMMDD):", "20000101")
        end_date = st.text_input("Enter end date (YYYYMMDD):", "20001231")
        query_to_run = f"""
        SELECT
            c_last_name,
            c_first_name,
            SUM(cs_quantity) AS total_purchased
        FROM
            catalog_sales
            JOIN customer ON catalog_sales.cs_bill_customer_sk = customer.c_customer_sk
        WHERE
            cs_sold_date_sk BETWEEN {start_date} AND {end_date}
        GROUP BY
            c_last_name, c_first_name
        ORDER BY
            total_purchased DESC;
        """
    elif selected_query == "Calculate the total sales price for items managed by a specific manager ID, sold in a specific month, grouped by year, brand, and brand ID, and ordered by total sales price in descending order":
        manager_id = st.text_input("Enter Manager ID:", "7")
        month = st.text_input("Enter Month (1-12):", "11")
        query_to_run = f"""
        SELECT
            d_year,
            i_brand_id,
            i_brand,
            SUM(ss_ext_sales_price) AS ext_price
        FROM
            date_dim
            JOIN store_sales ON date_dim.d_date_sk = store_sales.ss_sold_date_sk
            JOIN item ON store_sales.ss_item_sk = item.i_item_sk
            JOIN store ON store_sales.ss_store_sk = store.s_store_sk
        WHERE
            i_manager_id = {manager_id}
            AND d_moy = {month}
        GROUP BY
            d_year, i_brand, i_brand_id
        ORDER BY
            d_year, ext_price DESC, i_brand_id
        LIMIT 100;
        """
    elif selected_query == "Calculate the total sales price for catalog sales in a specific year, grouped by the state of the warehouse":
        year = st.text_input("Enter Year:", "2001")
        query_to_run = f"""
        SELECT
            w_state,
            SUM(cs_sales_price) AS total_sales
        FROM
            catalog_sales
            JOIN warehouse ON catalog_sales.cs_warehouse_sk = warehouse.w_warehouse_sk
            JOIN date_dim ON catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
        WHERE
            d_year = {year}
        GROUP BY
            w_state
        ORDER BY
            total_sales DESC;
        """
    elif selected_query == "List the customers' last names, first names, and city, along with the total quantity of items they bought and the total amount of money they spent on catalog sales in a specific year, ordered by the amount spent in descending order":
        year = st.text_input("Enter Year:", "2002")
        query_to_run = f"""
        SELECT
            c_last_name,
            c_first_name,
            ca_city,
            bought_quantity,
            spent_money
        FROM
            (SELECT
                 cs_bill_customer_sk AS customer,
                 ca_city,
                 SUM(cs_quantity) AS bought_quantity,
                 SUM(cs_sales_price) AS spent_money
             FROM
                 catalog_sales
                 JOIN customer_address ON catalog_sales.cs_ship_addr_sk = customer_address.ca_address_sk
                 JOIN date_dim ON catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
             WHERE
                 d_year = {year}
             GROUP BY
                 cs_bill_customer_sk, ca_city) sales_data
            JOIN customer ON sales_data.customer = customer.c_customer_sk
        ORDER BY
            spent_money DESC;
        """
    elif selected_query == "Count the number of purchases made in a specific year, grouped by store name and state, and ordered by the number of purchases in descending order":
        year = st.text_input("Enter Year:", "2000")
        query_to_run = f"""
        SELECT
            s_store_name,
            s_state,
            COUNT(*) AS num_purchases
        FROM
            store_sales
            JOIN store ON store_sales.ss_store_sk = store.s_store_sk
            JOIN date_dim ON store_sales.ss_sold_date_sk = date_dim.d_date_sk
        WHERE
            d_year = {year}
        GROUP BY
            s_store_name, s_state
        ORDER BY
            num_purchases DESC;
        """

    if st.button("Run Query"):
        result = run_query(query_to_run)
        st.write("Query Result:")
        st.write(result)
