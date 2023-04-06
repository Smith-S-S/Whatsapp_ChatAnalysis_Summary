from urlextract import URLExtract
import pandas as pd
from collections import Counter
ex=URLExtract()
from wordcloud import WordCloud, STOPWORDS
import emoji




def fetch_stats(selected_user,df):
    if selected_user != "Over All":
        df=df[df["user"] == selected_user]

    num_meassage = df.shape[0]
    v = []
    for i in df["message"]:
        v.extend(i.split())

    #num of media
    media= df[df["message"]=="<Media omitted>\n"].shape[0]

    # for links
    links = []
    for i in df["message"]:
        links.extend(ex.find_urls(i))

    return num_meassage,len(v),media,len(links)

#Most Busy Users
def m_b_u(df):
    x=df["user"].value_counts().head()
    # Most Busy Users Presentage
    dl = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "presentage"})
    return x,dl


#creating wordcloud

def create_wordcloud(selected_user,df):
    if selected_user != "Over All":
        df=df[df["user"] == selected_user]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user != "Over All":
        df=df[df["user"] == selected_user]
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()



    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df




def emoji_helper(selected_user,df):
    if selected_user != "Over All":
        df=df[df["user"] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df




def time_line(selected_user,df):
    if selected_user != "Over All":
        df=df[df["user"] == selected_user]

    time_line = df.groupby(["year", "month"]).count()["message"].reset_index()
    t = []
    for i in range(time_line.shape[0]):
        t.append(time_line["month"][i] + "- " + str(time_line["year"][i]))

    time_line["time_year"] = t

    return time_line

def daily_timeline(selected_user, df):
    if selected_user != "Over All":
        df = df[df["user"] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



def week_activity_map(selected_user, df):
    if selected_user != "Over All":
        df = df[df["user"] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Over All":
        df = df[df["user"] == selected_user]

    return df['month'].value_counts()





def activity_heatmap(selected_user, df):
    if selected_user != "Over All":
        df = df[df["user"] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


# date to the message

from urlextract import URLExtract


def d_message(selected_user, df):
    if selected_user != "Over All":
        df = df[df["user"] == selected_user]
        df = df.groupby('user')
        df = df.get_group(selected_user)

    import datetime
    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)

    now = Previous_Date
    now = str(now)
    now = now[:10]

    c = URLExtract()  # object
    #filtered_df = df.loc[(df['date'] == now)]
    filtered_df = df.loc[(df['date'] >= '2023-01-27')
                         & (df['date'] < '2023-01-30')]
    d = []
    for i in filtered_df["message"]:
        if c.find_urls(i) or i == '<Media omitted>\n' or i == 'This message was deleted\n':
            continue
        " ".join(i)
        d.append(i[0:-1])
    if selected_user == "Over All":
        d = " ".join(d)
    return d
