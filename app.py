import streamlit as st
import pandas as pd
from io import StringIO
import precessing_data,helper
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

from transformers import pipeline

summarizer = pipeline("summarization")

st.sidebar.title("Whatapp Chat Analysis")



uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #convert to string
    data=bytes_data.decode("utf-8")
    # prefrocessing

    df=precessing_data.preprocess(data)
    #st.dataframe(df)

    user_list= df["user"].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Over All") #it create new list in the list of index 0
    selected_user=st.sidebar.selectbox("Show Analysis Respect to users: ",user_list)
    n_days = st.sidebar.slider("Past How Many Days?: ", min_value=1, max_value=100)


    if st.sidebar.button("Show Analysis"):
        num_message,words,media,links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistic")
        cl1,cl2,cl3,cl4= st.columns(4)



        with cl1:
            st.header("Total Messages")
            st.title(num_message)

        with cl2:
            st.header("Total Words")
            st.title(words)

        with cl3:
            st.header("Total Media")
            st.title(media)

        with cl4:
            st.header("Total Links")
            st.title(links)


        # time line


        time_line=helper.time_line(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(time_line["time_year"],time_line["message"],color="green")
        plt.xticks(rotation="vertical")
        st.title("Time Line")
        st.pyplot(fig)

        # daily time line


        if n_days == 0:
            n_days=10

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'].tail(n_days), daily_timeline['message'].tail(n_days), color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



        # activity map

        st.title("Activity Map")
        cl1,cl2=st.columns(2)

        with cl1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with cl2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # most Active Users

        if selected_user=="Over All":
            st.title("Most Active Users")
            cl1,cl2= st.columns(2)
            x,dl=helper.m_b_u(df)
            fig, ax = plt.subplots()



            with cl1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)


            with cl2:
                st.dataframe(dl)
                # ax.bar(dl.index,dl.values)
                # plt.xticks(rotation="vertical")
                # st.pyplot(fig)


        #world cloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")


        # emoji analysis

        cl1,cl2=st.columns(2)

        with cl1:
            st.dataframe(emoji_df.head(10))

        with cl2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels= emoji_df[0].head(10))
            st.pyplot(fig)

        # Summerarixation

        di = helper.d_message(selected_user, df)
        v = summarizer(di, max_length=40, min_length=5, do_sample=False)
        v = v[0]["summary_text"]
        st.markdown("Past Day Summarization: ")
        st.write(v)














