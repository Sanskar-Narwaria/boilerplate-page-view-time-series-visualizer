import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",parse_dates=['date'],index_col='date')

lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

# Clean data
df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]


def draw_line_plot():
    
    # Draw line plot
    fig,ax=plt.subplots(figsize=(15,10))
    ax.plot(df.index,df['value'],color='red',linewidth=1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df['month']=df.index.month
    df['year']=df.index.year
    df_bar=df.groupby(['year','month']).mean()
    df_bar=df_bar.unstack()

    fig = df.plot.bar(legend=True,figsize=(13,6),ylabel="Average page Views",xlabel="Years").figure
    plt.legend(['January','February','March','April','May','June','July','August','September','October','November','December'])
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box['month_num']=df_box['date'].dt.month
    df_box=df_box.sort_values('month_num')

    fig,ax=plt.subplots(1,2,figsize=(15,5))

    sns.boxplot(data=df_box,x='year',y='value',ax=ax[0],hue='year',legend=False,palette=['blue', 'orange','green','red'],flierprops={"marker": "d", "markersize": 2,"markerfacecolor": "black"})
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page View")
    ax[0].grid(False)
    
    sns.boxplot(data=df_box,x='month',y='value',ax=ax[1],hue='month',legend=False,flierprops={"marker": "d", "markersize": 2,"markerfacecolor": "black"})
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel("Month")
    ax[2].set_ylabel("Page View")
    ax[1].grid(False)



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
