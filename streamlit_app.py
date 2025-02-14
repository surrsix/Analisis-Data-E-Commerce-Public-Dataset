import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Analisis Data E-Commerce Public Dataset')

### Data Wrangling
# 1. Gathering Data
# 2. Assessing Data
# 3. Cleaning Data

### Gathering Data (Pengumpulan Data)

# Melakukan import dataset berformat .csv penggunakan pandas
product_categories = pd.read_csv('./sumber/product_category_name_translation.csv')
products = pd.read_csv('./sumber/products_dataset.csv')
geolocation = pd.read_csv('./sumber/geolocation_dataset.csv')
sellers = pd.read_csv('./sumber/sellers_dataset.csv')
customers = pd.read_csv('./sumber/customers_dataset.csv')
orders = pd.read_csv('./sumber/orders_dataset.csv')
order_items = pd.read_csv('./sumber/order_items_dataset.csv')
order_payments = pd.read_csv('./sumber/order_payments_dataset.csv')
order_reviews = pd.read_csv('./sumber/order_reviews_dataset.csv')

### Cleaning Data (Pembersihan Data)

# Mengatasi Missing value
order_reviews.fillna({'review_comment_title': ""}, inplace=True) # mengisi missing value order_reviews
order_reviews.fillna({'review_comment_message': ""}, inplace=True)

orders.fillna({'order_approved_at': orders['order_purchase_timestamp']}, inplace=True) # mengisi missing value orders
orders.fillna({'order_delivered_carrier_date': orders['order_approved_at']}, inplace=True)
orders.fillna({'order_delivered_customer_date': orders['order_delivered_carrier_date']}, inplace=True)

products.fillna({'product_category_name': ""}, inplace=True) # mengisi missing value products
products.fillna({'product_name_lenght': 0}, inplace=True)
products.fillna({'product_description_lenght': 0}, inplace=True)
products.fillna({'product_photos_qty': 0}, inplace=True)
products.fillna({'product_weight_g': 0}, inplace=True)
products.fillna({'product_length_cm': 0}, inplace=True)
products.fillna({'product_height_cm': 0}, inplace=True)
products.fillna({'product_width_cm': 0}, inplace=True)

# Mengatasi Duplicate Data
geolocation.drop_duplicates(inplace=True)  # Menghapus duplikasi lokasi
customers.drop_duplicates(subset='customer_unique_id', inplace=True)  # Menghapus duplikasi pelanggan
sellers.drop_duplicates(subset='seller_id', inplace=True)  # Menghapus duplikasi seller

# Konversi format tanggal
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Rename kolom
geolocation.rename(columns={'geolocation_zip_code_prefix': 'zip_code'}, inplace=True)  # Penamaan kolom lebih sederhana

tab1, tab2, tab3, tab4 = st.tabs(["Dataset", "Analisis Abdul Richard", "Analisis Prastia Zaman", "Analisis Suryana"])

with tab1 :
    st.header('Tabel Dataset')
    st.subheader('Product Category')
    st.write(product_categories.head(10))
    st.subheader('Product')
    st.write(products.head(10))
    st.subheader('Geolocation')
    st.write(geolocation.head(10))
    st.subheader('Sellers')
    st.write(sellers.head(10))
    st.subheader('Customers')
    st.write(customers.head(10))
    st.subheader('Orders')
    st.write(orders.head(10))
    st.subheader('Order Items')
    st.write(order_items.head(10))
    st.subheader('Order Payment')
    st.write(order_payments.head(10))
    st.subheader('Order Reviews')
    st.write(order_reviews.head(10))
    
with tab2 :
    st.header('Abdul Richard - 10123905')
    
    with st.container():
        st.subheader('1. Kota atau Negara Bagian Mana yang Memiliki Jumlah Pelanggan Terbanyak?')

        # Gabungkan Customers dan Geolocation dataset berdasarkan zip_code
        customers_geo = pd.merge(customers, geolocation, left_on='customer_zip_code_prefix', right_on='zip_code')

        # Hitung jumlah pelanggan unik per kota
        city_counts = customers_geo.groupby('geolocation_city')['customer_unique_id'].nunique().sort_values(ascending=False)

        # Tampilkan 10 kota teratas
        st.dataframe(city_counts.head(10))

        # Visualisasi jumlah pelanggan per kota
        fig, ax = plt.subplots(figsize=(10, 6))
        city_counts.head(10).plot(kind='bar',color='skyblue')
        ax.set_title('Top 10 Kota dengan Jumlah Pelanggan Terbanyak')
        ax.set_xlabel('Kota')
        ax.set_ylabel('Jumlah Pelanggan')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Hitung jumlah pelanggan unik per negara bagian
        state_counts = customers_geo.groupby('geolocation_state')['customer_unique_id'].nunique().sort_values(ascending=False)

        # Tampilkan hasil untuk negara bagian
        st.dataframe(state_counts)

        # Visualisasi jumlah pelanggan per negara bagian
        fig, bx = plt.subplots(figsize=(10, 6))
        state_counts.plot(kind='bar', color='green')
        bx.set_title('Jumlah Pelanggan per Negara Bagian')
        bx.set_xlabel('Negara Bagian')
        bx.set_ylabel('Jumlah Pelanggan')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        with st.expander("Conclusion"):
            st.write('''
                     Kota dengan jumlah pelanggan terbanyak biasanya terletak di wilayah urban atau kota besar yang lebih berkembang. Misalnya, kota seperti Jakarta atau Surabaya di Indonesia kemungkinan memiliki jumlah pelanggan yang lebih tinggi karena populasi yang lebih besar dan konsentrasi ekonomi.
Negara bagian dengan pelanggan terbanyak juga mengikuti tren serupa, dengan wilayah yang lebih padat penduduk atau memiliki infrastruktur yang lebih baik cenderung memiliki lebih banyak pelanggan.
            ''')

        st.divider()
        
    with st.container():
        st.subheader('2. Produk Kategori Apa yang Paling Laris?')
        
        # Gabungkan order_items dan products
        order_products = pd.merge(order_items, products, on='product_id')

        # Gabungkan dengan product_categories untuk mendapatkan nama kategori dalam bahasa Inggris
        order_products = pd.merge(order_products, product_categories, on='product_category_name')

        # Hitung jumlah produk terjual per kategori
        category_sales = order_products.groupby('product_category_name_english')['order_item_id'].count().sort_values(ascending=False)

        # Tampilkan kategori produk paling laris
        st.dataframe(category_sales.head(10))

        # Visualisasi kategori produk paling laris
        fig, cx = plt.subplots(figsize=(10, 6))
        category_sales.head(10).plot(kind='bar', color='purple')
        cx.set_title('Top 10 Kategori Produk Paling Laris')
        cx.set_xlabel('Kategori Produk')
        cx.set_ylabel('Jumlah Produk Terjual')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        with st.expander("Conclusion"):
            st.write('''
                     Penjual dengan volume penjualan tertinggi biasanya adalah yang menawarkan produk yang lebih populer, dengan harga yang kompetitif, atau memiliki promosi menarik. Penjual ini mungkin juga memiliki reputasi baik dalam memberikan layanan pelanggan atau pengiriman yang cepat.
Menganalisis penjual terbaik juga dapat membantu kita untuk memberikan insentif lebih pada penjual tersebut dan meningkatkan visibilitas mereka di platform.
            ''')
            
        st.divider()
        
    with st.container():
        st.subheader('3. Berapa jumlah pesanan yang dibatalkan?')
        
        # Menghitung jumlah pesanan yang dibatalkan
        cancelled_orders = orders[orders['order_status'] == 'canceled']

        # Menampilkan jumlah pesanan yang dibatalkan
        st.dataframe(cancelled_orders)
        st.subheader(f"Jumlah pesanan yang dibatalkan: {cancelled_orders.shape[0]}")

        with st.expander("Conclusion"):
            st.write('''
                     Berdasarkan hasil analisis data, jumlah pesanan yang dibatalkan sebanyak 625.
            ''')
    
with tab3 :
    st.header('10124909 - Prastia Zaman')
    
    with st.container():
        st.subheader('1. Order barang apa yang memiliki price dibawah 50.00?')
        
        # Filter barang dengan harga di bawah 50.00
        items_below_50 = order_items[order_items['price'] < 50.00][['product_id', 'price']]

        # Hitung total barang dengan harga di bawah 50.00
        total_items = len(items_below_50)

        # Tampilkan hasil
        st.dataframe(items_below_50)
        st.subheader(f"Total barang dengan harga di bawah 50.00 ada: {total_items}")
        
        with st.expander("Conclusion"):
            st.write('''
                     Jumlah total barang dengan harga di bawah 50.00 adalah 39.024 item.
Barang-barang tersebut tersebar dalam berbagai kategori produk (product_id) yang terdapat di dataset. Untuk menyebutkan produk secara spesifik, diperlukan informasi tambahan tentang deskripsi atau nama produk, karena dataset saat ini hanya mencakup product_id.
            ''')
            
        st.divider()
    
    with st.container():
        st.subheader('2. Top 10 Penjualan Mana yang memiliki sellerstate dan Kota Terbanyak?')
        
        # Hitung jumlah penjual per negara bagian dan per kota
        top_states = sellers['seller_state'].value_counts().head(10)
        top_cities = sellers['seller_city'].value_counts().head(10)

        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Grafik pertama: Negara Bagian
        top_states.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title('10 Negara Bagian dengan Jumlah Penjual Terbanyak', fontsize=14)
        ax1.set_xlabel('Negara Bagian', fontsize=12)
        ax1.set_ylabel('Jumlah Penjual', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Grafik kedua: Kota
        top_cities.plot(kind='bar', color='lightgreen', ax=ax2)
        ax2.set_title('10 Kota dengan Jumlah Penjual Terbanyak', fontsize=14)
        ax2.set_xlabel('Kota', fontsize=12)
        ax2.set_ylabel('Jumlah Penjual', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        # Menyesuaikan tata letak
        plt.tight_layout()

        # Tampilkan grafik di Streamlit
        st.pyplot(fig)
        
        with st.expander("Conclusion"):
            st.write('''
                     Berdasarkan analisis data, negara bagian dengan penjual terbanyak adalah **São Paulo (SP)**, diikuti oleh **Rio de Janeiro (RJ)**, **Minas Gerais (MG)**, dan beberapa negara bagian lainnya. Selain itu, kota dengan jumlah penjual terbanyak adalah **São Paulo**, yang juga mendominasi dalam hal penjual, diikuti oleh **Rio de Janeiro**, **Belo Horizonte**, dan kota-kota besar lainnya seperti **Curitiba** dan **Porto Alegre**. Distribusi penjual ini menunjukkan dominasi wilayah urban besar di Brasil, dengan São Paulo sebagai pusat utama. Grafik batang yang dibuat menggambarkan penjualan terbesar di kota dan negara bagian ini.
            ''')

with tab4 :
    st.header('10124911 - Suryana')
    
    with st.container():
        st.subheader('1. Pada Bulan apa mendapatkan pendapatan tertinggi?')
        
        # Gabungkan data orders dengan order_payments
        merged_data = orders.merge(order_payments, on='order_id')

        # Ekstrak bulan dari order_purchase_timestamp
        merged_data['order_purchase_month'] = pd.to_datetime(merged_data['order_purchase_timestamp']).dt.to_period('M')

        # Hitung total pendapatan per bulan
        monthly_revenue = merged_data.groupby('order_purchase_month')['payment_value'].sum()

        # Mengurutkan dari pendapatan tertinggi ke terendah
        monthly_revenue = monthly_revenue.sort_values( ascending=False)
        st.dataframe(monthly_revenue)
        
        # Konversi Period ke string untuk visualisasi
        monthly_revenue.index = monthly_revenue.index.astype(str)

        # Visualisasi dengan bar chart
        fig, dx = plt.subplots(figsize=(10, 6))
        dx.bar(monthly_revenue.index, monthly_revenue.values, color='purple')
        dx.set_title('Pendapatan Bulan Tertinggi Sampai Terendah', fontsize=16)
        dx.set_xlabel('Bulan', fontsize=14)
        dx.set_ylabel('Total Pendapatan', fontsize=14)
        dx.set_xticks(range(len(monthly_revenue.index)))
        dx.set_xticklabels(monthly_revenue.index, rotation=90)
        dx.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
        with st.expander("Conclusion"):
            st.write('''
                     Berdasarkan analisis data, total pendapatan bulan tertinggi adalah **November 2017** dengan total pendapatan sebesar **1194882.80**, diikuti oleh **April 2018** dengan pendapatan **1160785.48**, dan **Maret 2018** dengan pendapatan **1159652.12**.
        ''')
        
        st.divider()
    
    with st.container():
        st.subheader('2. Kategori produk apa dengan rata-rata ulasan tertinggi?')
        
        # Gabungkan data order_reviews, order_items, dan products
        merged_data = order_reviews.merge(order_items, on='order_id').merge(products, on='product_id')

        # Hitung rata-rata skor ulasan per kategori produk
        avg_review_score = merged_data.groupby('product_category_name')['review_score'].mean().sort_values(ascending=False).head(10)
        st.dataframe(avg_review_score)
        
        # Visualisasi dengan bar chart
        fig, ex = plt.subplots(figsize=(10, 6))
        ex.bar(avg_review_score.index, avg_review_score.values, color='green')
        ex.set_title('Top 10 Kategori Produk dengan Rata-Rata Ulasan Tertinggi', fontsize=16)
        ex.set_xlabel('Kategori Produk', fontsize=14)
        ex.set_ylabel('Rata-Rata Skor Ulasan', fontsize=14)
        ex.set_xticks(range(len(avg_review_score.index)))
        ex.set_xticklabels(avg_review_score.index, rotation=45)

        st.pyplot(fig)
        
        with st.expander("Conclusion"):
            st.write('''
                     Berdasarkan analisis data, kategori produk dengan rata-rata ulasan tertinggi adalah **cds_dvds_musicais** dengan skor rata-rata **4.64**, diikuti oleh **fashion_roupa_infanto_juvenil** dengan skor **4.5**, dan **livros_interesse_geral** dengan skor **4.44**. Kategori-kategori ini menunjukkan tingkat kepuasan pelanggan yang tinggi, yang dapat menjadi indikator kualitas produk atau layanan yang baik.
            ''')
            
