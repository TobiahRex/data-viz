import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import openai


def static_bubble():
    # read data from csv file
    df = pd.read_csv('./youtube-data-categories.csv')

    # convert date column to datetime object
    df['date'] = pd.to_datetime(df['date'])

    # calculate time watched in seconds
    df['time_watched'] = df['date'].diff().dt.seconds.fillna(0)

    # df = df[df['channel'] != 'other']

    # group data by channel and date
    grouped = df.groupby(['channel', pd.Grouper(
        key='date', freq='D')]).sum().reset_index()

    # create bubble chart
    fig = px.scatter(grouped, x='date', y='time_watched',
                     size='time_watched', color='channel',
                     hover_name='channel', log_y=True, size_max=60,
                     title='YouTube Videos Watched')

    # set x and y axis labels
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Watch Time (seconds)')

    # display chart
    fig.show()


def animated_bubble():
    df = pd.read_csv('./youtube-data-categories.csv')
    # convert date column to datetime object
    df['date'] = pd.to_datetime(df['date'])

    # calculate time watched in seconds
    df['time_watched'] = df['date'].diff().dt.seconds.fillna(0)

    # group data by channel, date, and title
    grouped = df.groupby(['category', pd.Grouper(
        key='date', freq='D'), 'title']).sum().reset_index()

    # create scatter plot with animation
    fig = px.scatter(grouped, x='time_watched', y='title',
                     size='time_watched', color='category', animation_frame='date',
                     animation_group='title', hover_name='title', log_x=True, size_max=60,
                     title='YouTube Videos Watched')

    # set x and y axis labels
    fig.update_xaxes(title='Watch Time (seconds)')
    fig.update_yaxes(title='Video Title')

    # display chart
    fig.show()


def categories_plot():
    # set OpenAI API key
    openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxx'
    # read data from csv file
    df = pd.read_csv('./youtube-data-categories.csv')

    # categorize video titles using OpenAI
    # df['category'] = df['title'].apply(categorize_title)

    # convert date column to datetime object
    df['date'] = pd.to_datetime(df['date'])

    # calculate time watched in seconds
    df['time_watched'] = df['date'].diff().dt.total_seconds().fillna(0)

    # filter out negative values in the time_watched column
    df = df.loc[df['time_watched'] > 0]

    # group data by category, channel, and date
    grouped = df.groupby(['category', 'channel', pd.Grouper(
        key='date', freq='D')]).sum().reset_index()

    # create scatter plot with animation
    fig = px.scatter(grouped, x='time_watched', y='category',
                     size='time_watched', color='channel', animation_frame='date',
                     animation_group='channel', hover_name='channel', log_x=True, size_max=60,
                     title='YouTube Videos Watched')

    # set x and y axis labels
    fig.update_xaxes(title='Watch Time (seconds)')
    fig.update_yaxes(title='Video Category')

# define a function to categorize video titles using OpenAI


def categorize_title(title):
    categories = ['chess', 'coding', 'movies',
                  'documentaries', 'trading', 'tech', 'other']
    prompt = f"Categorize the following video title into one of the following categories: {', '.join(categories)}.\nTitle: {title}. \nCategory:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    label = response.choices[0].text.strip()
    if label in categories:
        return label
    else:
        return 'other'


if __name__ == '__main__':
    static_bubble()
