import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0,
                 names=['Date', 'Page Views'], index_col='Date')


# Clean data
df = df[(df['Page Views'] <= df['Page Views'].quantile(.975)) &
        (df['Page Views'] >= df['Page Views'].quantile(.025))]


# Convert "Date" column values from strings to dates to help with auto formatting
# If this step is skipped then all index rows will be added as "ticks" on the x-axis
# This will work without "format = '%Y-%m-%d" but adding it helps to ensure the format is as desired.
df.index = pd.to_datetime(df.index, format='%Y-%m-%d')


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(16, 6))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.plot(df.index, 'Page Views', data=df, color='red')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Group by month and take aggregate month avg. page views. Uncomment print command to see effect
    df_bar = df_bar.groupby(
        pd.Grouper(freq='M')).mean().rename(columns={'Page Views': 'Average Page Views'})
    # print(df_bar)

    # Create and populate columns "year" and "month" using datetime values from index column
    # The index must already be formatted as datetime for this to work.
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Reorder columns (not needed, but just makes it easier to read)
    df_bar = df_bar[['year', 'month', 'Average Page Views']]
    # print(df_bar)

    # Create dictionary for swap month value with month name and then pivot table.
    month_num_to_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                         5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df_bar_piv = df_bar.pivot(
        index='year', columns='month', values='Average Page Views').rename(columns=month_num_to_name)
    # print(df_bar_piv)

    # Plotting. ".get_figure()" allows the plot to be saved using ".savefig()" without the plot being setup as a plt.bar
    fig = df_bar_piv.plot(kind='bar', figsize=(10, 10)).get_figure()
    plt.ylabel('Average Page Views')
    plt.xlabel('Years')
    plt.legend(loc=2)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

# Draw box plots (using Seaborn)


def draw_box_plot():

    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.Date]
    df_box['month'] = [d.strftime('%b') for d in df_box.Date]

    # Set up Figure, subplots and axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    plt.subplots_adjust(left=0.07, right=0.970, bottom=0.17,
                        top=.755, wspace=0.16, hspace=0.195)

    plt.subplot(1, 2, 1)
    sns.boxplot(x='year', y='Page Views', data=df_box, hue='year',
                palette='tab10', flierprops={'marker': 'D', 'markersize': 2, 'markerfacecolor': 'black'})

    # Sort the data by month.
    # print(df_box.sort_values('Date', key=lambda x: x.dt.month))
    df_box = df_box.sort_values('Date', key=lambda x: x.dt.month)

    plt.subplot(1, 2, 2)
    sns.boxplot(x='month', y='Page Views', data=df_box, hue='month',
                palette='husl', flierprops={'marker': 'D', 'markersize': 2, 'markerfacecolor': 'black'})
    
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylim(0, 200000)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylim(0, 200000)
    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)
    y_ticks = [0, 20000, 40000, 60000, 80000, 100000,
               120000, 140000, 160000, 180000, 200000]
    ax1.set_yticks(y_ticks)
    ax2.set_yticks(y_ticks)
    
    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig