import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import gc

@st.cache_data(ttl=3600)
def calculate_basic_stats(products_df, ratings_df):
    stats = {
        'num_products': len(products_df),
        'num_categories': products_df['sub_category'].nunique(),
        'num_ratings': len(ratings_df),
        'num_users': ratings_df['user_id'].nunique()
    }
    return stats

@st.cache_data(ttl=3600)
def calculate_user_stats(ratings_df, products_df):
    try:
        # Merge with minimal columns
        eda_merged = ratings_df.merge(
            products_df[['product_id', 'price', 'product_name']],
            on='product_id',
            how='left'
        )
        most_rated_product_id = eda_merged['product_id'].value_counts().idxmax()
        least_rated_product_id = eda_merged['product_id'].value_counts().idxmin()
        
        stats = {
            'top_reviewer': ratings_df['user_id'].value_counts().idxmax(),
            'top_reviewer_count': ratings_df['user_id'].value_counts().max(),
            'top_spender': eda_merged.groupby('user_id')['price'].sum().idxmax(),
            'top_spend_amount': eda_merged.groupby('user_id')['price'].sum().max(),
            'top_five_star_user': ratings_df[ratings_df['rating'] == 5]['user_id'].value_counts().idxmax(),
            'top_five_star_count': ratings_df[ratings_df['rating'] == 5]['user_id'].value_counts().max(),
            'top_product_name': eda_merged.loc[eda_merged['product_id'] == most_rated_product_id, 'product_name'].values[0],
            'least_product_name': eda_merged.loc[eda_merged['product_id'] == least_rated_product_id, 'product_name'].values[0]
        }
        
        del eda_merged
        gc.collect()
        
        return stats
    except Exception as e:
        st.error(f"Error calculating user statistics: {str(e)}")
        return None


@st.cache_data(ttl=3600)
def data_insight(products_df, ratings_df):
    if products_df is None or ratings_df is None:
        st.error("Không thể tải dữ liệu. Vui lòng thử lại sau.")
        return

    try:
        st.image("images/insight.jpeg", width=1000)
        st.title("Một số thông tin về dữ liệu")
        
        st.markdown("### 🛍️ Dữ liệu sản phẩm mẫu")
        st.dataframe(products_df.head(10))
        st.markdown("### ⭐ Dữ liệu đánh giá mẫu")
        st.dataframe(ratings_df.head(10))
        
        # Basic Statistics
        stats = calculate_basic_stats(products_df, ratings_df)
        stats_user = calculate_user_stats(ratings_df, products_df)

        col1, col2, col3 = st.columns(3)
        
        # ---------- CỘT 1: THỐNG KÊ CHUNG ----------
        with col1:
            st.markdown("### 📊 Thống kê tổng quan")
            st.markdown(f"🛍️ **Số sản phẩm:**<br><span style='font-size:16px'>{stats['num_products']}</span>", unsafe_allow_html=True)
            st.markdown(f"🛍️ **Số nhóm sản phẩm:**<br><span style='font-size:16px'>{stats['num_categories']}</span>", unsafe_allow_html=True)
            st.markdown(f"👤 **Số người dùng:**<br><span style='font-size:16px'>{stats['num_users']}</span>", unsafe_allow_html=True)
            st.markdown(f"⭐ **Số lượt đánh giá:**<br><span style='font-size:16px'>{stats['num_ratings']}</span>", unsafe_allow_html=True)

        # ---------- CỘT 2: USER ----------
        with col2:
            st.markdown("### 🙋‍♂️ Người dùng nổi bật")
            st.markdown(f"✍️ **Review nhiều nhất:**<br><span style='font-size:15px'>{stats_user['top_reviewer']} ({stats_user['top_reviewer_count']} lần)</span>", unsafe_allow_html=True)
            st.markdown(f"💰 **Chi tiêu nhiều nhất:**<br><span style='font-size:15px'>{stats_user['top_spender']} ({stats_user['top_spend_amount']:,.0f} VNĐ)</span>", unsafe_allow_html=True)
            st.markdown(f"😍 **Rating 5⭐ nhiều nhất:**<br><span style='font-size:15px'>{stats_user['top_five_star_user']} ({stats_user['top_five_star_count']} lần)</span>", unsafe_allow_html=True)

        # ---------- CỘT 3: SẢN PHẨM ----------
        with col3:
            st.markdown("### 📦 Sản phẩm nổi bật")
            st.markdown(f"🔥 **Nhiều đánh giá nhất:**<br><span style='font-size:15px'>{stats_user['top_product_name'][:30]}...</span>", unsafe_allow_html=True)
            st.markdown(f"🥶 **Ít đánh giá nhất:**<br><span style='font-size:15px'>{stats_user['least_product_name'][:30]}...</span>", unsafe_allow_html=True)


        st.subheader("📦 Top 10 Nhóm Hàng Phổ Biến Nhất")
        st.image("images/top10_nhomhang.png", width=1000)

        st.subheader("🛍️ Top 20 Tên Sản Phẩm Phổ Biến Nhất")
        st.image("images/top20_ten_sp_pho_bien.png", width=1000)
        
        st.subheader("🎻 Phân bố giá theo nhóm sản phẩm")
        st.image("images/phanbogia.png", width=1000)
        
        st.subheader("📦 Phân bố Rating theo Nhóm Sản Phẩm")
        st.image("images/phanborating.png", width=1000)
        
        st.subheader("📈 Tương Quan giữa Giá và Rating theo Nhóm Sản Phẩm")
        st.image("images/tuongquan_gia_nhom_sp.png", width=1000)

        st.subheader("💰 Giá Trung Bình Theo Nhóm Sản Phẩm")
        st.image("images/gia_trung_binh_nhom.png", width=1000)

        st.subheader("⭐ Rating Trung Bình Theo Nhóm Sản Phẩm")
        st.image("images/rating_trung_binh_nhom.png", width=1000)

        st.subheader("⭐ Biểu đồ rating theo phần trăm")
        st.image("images/rating_percent.png", width=1000)

        st.subheader("⭐ Top Sản Phẩm Nhận Được Nhiều Đánh Giá 5 Sao")
        st.image("images/top_sp_5_star.png", width=1000)

        st.subheader("⭐ Top Nhóm Sản Phẩm Nhận Được Nhiều Đánh Giá 5 Sao")
        st.image("images/top_nhom_sp_5_star.png", width=1000)

        st.subheader("⚠️ Top Sản Phẩm Nhận Được Nhiều Đánh Giá 1 Sao")
        st.image("images/top_sp_1_star.png", width=1000)

        st.subheader("📊 Phân bố độ dài mô tả sản phẩm")
        st.image("images/phan_bo_do_dai_mo_ta.png", width=1000)

        st.markdown("### ☁️ Wordcloud mô tả sản phẩm")
        st.image("images/wordcloud.png", width=1000)
    except Exception as e:
        st.error(f"Error: {str(e)}")