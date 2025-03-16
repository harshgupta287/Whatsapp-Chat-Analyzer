import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")
st.sidebar.markdown("Upload your exported WhatsApp chat file (txt format) for analysis.")

uploaded_file = st.sidebar.file_uploader("📂 Choose a file", type=["txt"])

if uploaded_file is None:
    st.markdown("## 📤 How to Export WhatsApp Chat")
    st.markdown("""
    1. **Open WhatsApp** on your phone.
    2. Go to the chat you want to export.
    3. Tap on **More Options (⋮) > More > Export Chat**.
    4. Choose whether to include **media** or export **without media**.
    5. Select a method to share (e.g., **Google Drive, Email, or File Manager**).
    6. **Download** the exported `.txt` file and upload it here.
    """)

    # Embed YouTube video with export guide
    st.markdown("## 🎥 Tutorial Video")
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <iframe width="560" height="315" src="https://www.youtube.com/embed/sTSbtl-jw0A" 
            frameborder="0" allowfullscreen></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Show analysis for", user_list)

    if st.sidebar.button("🔍 Show Analysis"):

        # Statistics Area
        st.markdown("## 📊 Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div style='padding: 15px; border-radius: 10px; background-color: #2c2f33; text-align: center; color: white;'>"
                        "<h4>Total Messages</h4>"
                        f"<h2>{num_messages}</h2>"
                        "</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='padding: 15px; border-radius: 10px; background-color: #2c2f33; text-align: center; color: white;'>"
                        "<h4>Total Words</h4>"
                        f"<h2>{words}</h2>"
                        "</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div style='padding: 15px; border-radius: 10px; background-color: #2c2f33; text-align: center; color: white;'>"
                        "<h4>Media Shared</h4>"
                        f"<h2>{num_media_messages}</h2>"
                        "</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div style='padding: 15px; border-radius: 10px; background-color: #2c2f33; text-align: center; color: white;'>"
                        "<h4>Links Shared</h4>"
                        f"<h2>{num_links}</h2>"
                        "</div>", unsafe_allow_html=True)
        
        # Monthly Timeline
        st.markdown("## 📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='blue', marker='o', linestyle='-')
        plt.xticks(rotation='vertical')
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        # Daily Timeline
        st.markdown("## 📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green', marker='o', linestyle='-')
        plt.xticks(rotation='vertical')
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        # Activity Map
        st.markdown("## ⏳ Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Most Busy Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple', alpha=0.7)
            plt.xticks(rotation='vertical')
            plt.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)

        with col2:
            st.markdown("### 📅 Most Busy Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange', alpha=0.7)
            plt.xticks(rotation='vertical')
            plt.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
        
        st.markdown("### 🔥 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, linewidths=0.5, linecolor='gray', ax=ax)
        st.pyplot(fig)

        # Most Busy Users
        if selected_user == 'Overall':
            st.markdown("## 🏅 Most Active Users")
            x, new_df = helper.most_busy_users(df)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red', alpha=0.7)
                plt.xticks(rotation='vertical')
                plt.grid(True, linestyle='--', alpha=0.5)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Most Common Words
        st.markdown("## 🔤 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue', alpha=0.7)
        plt.xticks(rotation='horizontal')
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        # Emoji Analysis
        st.markdown("## 😀 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(emoji_df["Count"].head(), labels=emoji_df["Emoji"].head(), autopct="%0.2f", colors=sns.color_palette("pastel"))
                st.pyplot(fig)
            else:
                st.info("No emojis found in the selected chat.") 