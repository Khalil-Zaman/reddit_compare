from page_source import *
from plotly import __version__
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import date


def subscriber_grow_plot(subreddits, difference=False):
    data = []
    diff1 = []
    diff2 = []
    for title in subreddits:
        byte_code = get_page_source(title)
        subscribers, dates = number_of_subscribers(byte_code)
        if difference is False:
            trace = Scatter(x=dates, y=subscribers, mode='lines', name=title)
            data.append(trace)
        else:
            if len(diff1) == 0:
                diff1 = subscribers
            else:
                diff2 = subscribers
    if difference is True:
        the_diff = []
        for i in range(0, len(diff1)):
            the_diff.append(abs(diff1[i] - diff2[i]))
        trace = Scatter(x=dates, y=the_diff, mode='lines', name=title)
        data.append(trace)
    plot(data)


# This one shows the change of subsribers as a percent of the total number of subscribers
# Can be specified for how many number of days. Plot_auto let's you automatically plot the data
# Or instead it'll return the data
def percent_change_plot(*subreddits, days=1, plot_auto=True):
    data = []
    for title in subreddits:
        byte_code = get_page_source(title)
        subscribers, dates = number_of_subscribers(byte_code)
        percent_change = []
        for i in range(0, len(subscribers)-days):
            percent = 100 * ((subscribers[i + days] - subscribers[i]) / subscribers[i])
            percent_change.append(percent)
        trace = Scatter(x=dates, y=percent_change, mode='lines', name=title)
        data.append(trace)
    if plot_auto is True:
        plot(data)
    else:
        return data

# How much bigger today's growth was than yesterdays
def growth_factor_plot(*subreddits, first_day=False, days=0):
    data = []
    sub = []
    rate = []
    for title in subreddits:
        byte_code = get_page_source(title)
        subscribers, dates = number_of_subscribers(byte_code)
        growth_factor = []
        if first_day is False:
            for i in range(0, len(subscribers) - 2):
                difference_1 = subscribers[i+1] - subscribers[i]
                difference_2 = subscribers[i+2] - subscribers[i+1]
                if difference_1 == 0:
                    difference_1 = 1
                growth = (difference_2/difference_1)
                growth_factor.append(growth)
            trace = Scatter(x=dates, y=growth_factor, mode='lines', name=title)
            data.append(trace)
        else:
            if days is 0:
                for i in range(1, len(subscribers)):
                    growth = subscribers[i]/subscribers[0]
                    growth_factor.append(growth)
            else:
                for i in range(days, len(subscribers)):
                    growth = subscribers[i] / subscribers[i-days]
                    growth_factor.append(growth)
            trace = Scatter(x=dates, y=growth_factor, mode='lines', name=title)
            data.append(trace)
    plot(data)


def moving_average_plot(subreddits, days=60, plot_auto=True, difference_plot=False):
    data = []
    for title in subreddits:
        byte_code = get_page_source(title)
        subscribers, dates = number_of_subscribers(byte_code)
        difference = []
        for i in range(0, len(subscribers)-1):
            diff = subscribers[i+1]-subscribers[i]
            difference.append(diff)
        moving_average = []
        for i in range(days, len(difference)):
            average = 0
            for i2 in range(i-days, i):
                average += difference[i2]
            average = average/days
            moving_average.append(average)
        trace = Scatter(x=dates[days:], y=moving_average, mode='lines', name=title)
        data.append(trace)
    if plot_auto is True:
        if difference_plot is True:
            dif = []
            for i in range(0, len(data[0].y)):
                dif1 = data[0].y[i] - data[1].y[i]
                dif.append(dif1)
            trace_new = Scatter(x=data[0].x[days:], y=dif, mode='lines', name='Difference')
            data = []
            data.append(trace_new)
            plot(data)
        else:
            plot(data)
    else:
        return data


def difference_percentage_plot(*subreddits):
    if len(subreddits) == 2:
        data = percent_change_plot(subreddits[0], subreddits[1], days=20, plot_auto=False)
        # trace 2 - trace 1
        trace_1 = data[0]
        trace_2 = data[1]
        percent_1 = trace_1.y
        percent_2 = trace_2.y
        difference = []
        for i in range(0, len(percent_1)):
            diff = percent_2[i] - percent_1[i]
            difference.append(diff)
        trace = Scatter(x=trace_2.x, y=difference, mode='lines', name='Difference')
        plot([trace])
    else:
        print("Please only provide two reddits")

def times_bigger_plot(*subreddits):
    if len(subreddits) == 2:
        data = []
        subs = []
        dates = None
        for title in subreddits:
            byte_code = get_page_source(title)
            subscribers, dates = number_of_subscribers(byte_code)
            subs.append(subscribers)
        times_bigger = []
        sub1 = subs[0]
        sub2 = subs[1]
        for i in range(0, len(sub1)):
            p = sub1[i]/sub2[i]
            times_bigger.append(p)
        trace = Scatter(x=dates, y=times_bigger, mode='lines', name=title)
        data.append(trace)
        plot(data)

def rate_of_increase(subreddits, sub_diff=1000):
    data = []
    for title in subreddits:
        y_days = []
        x_subs = []
        rate = []
        s1 = s2 = 0
        d1 = d2 = []
        byte_code = get_page_source(title)
        subscribers, dates = number_of_subscribers(byte_code)
        for i in range(0, len(subscribers)):
            if i == 0:
                s1 = subscribers[0]

                d1 = dates[0].split("-")
                d1 = date(int(d1[0]), int(d1[1]), int(d1[2]))

            if subscribers[i]-s1 >= sub_diff:
                d2 = dates[i].split("-")
                d2 = date(int(d2[0]), int(d2[1]), int(d2[2]))
                delta = d2 - d1
                y_days.append(delta.days)
                s1 = subscribers[i]
                d1 = d2
        print (y_days)
        trace = Scatter(y=y_days, mode='lines', name=title)
        data.append(trace)
        plot(data)



"""OTHER GRAPHS. """
sub1 = ""
sub2 = ""
#difference_percentage_plot(sub1, sub2)
#growth_factor_plot(sub1, sub2, first_day=False, days=1)
#percent_change_plot(subs)



option = int(input("Select a number:\n"
      +"\t1: Rate of increase (Number of days it takes [X] number of [subs] to gain an extra [X] subscribers)\n"
      +"\t2: Times bigger (How many times bigger [sub1] is from [sub2]) \n"
      +"\t3: Subscribers growth (Growth of subscribers over time for [X] number of [subs]\n"
      +"\t4: Subrcribers difference (Absolute difference in # subscribers of [sub1] and [sub2] over time) \n"
      +"\t5: Moving average ([X] number of [subs] for [Y] days\n"
      +"Option selected: "))

print("")

if option == 1:
    X = int(input("Number of different subreddit?: "))
    sub = []
    for i in range (0, X):
        sub.append(input("Type in a subreddit (number " + str(i+1) + ") (e.g. r/AskReddit would be AskReddit): "))
    no_subs = int(input("Type in the number of subscribers): "))
    rate_of_increase(sub, sub_diff=no_subs)
elif option == 2:
    sub1 = input("Type in a the first subreddit (e.g. r/AskReddit would be AskReddit): ")
    sub2 = input("Type in a the second subreddit (e.g. r/AskReddit would be AskReddit): ")
    times_bigger_plot(sub1, sub2)
elif option == 3:
    X = int(input("Number of different subreddit?: "))
    sub = []
    for i in range(0, X):
        sub.append(input("Type in a subreddit (number " + str(i+1) + ") (e.g. r/AskReddit would be AskReddit): "))
    subscriber_grow_plot(sub, difference=False)
elif option == 4:
    sub = []
    for i in range(0, 2):
        sub.append(input("Type in a subreddit (number " + str(i+1) + ") (e.g. r/AskReddit would be AskReddit): "))
    subscriber_grow_plot(sub, difference=True)
elif option == 5:
    X = int(input("Number of different subreddit?: "))
    sub = []
    for i in range(0, X):
        sub.append(input("Type in a subreddit (number " + str(i+1) + ") (e.g. r/AskReddit would be AskReddit): "))
    no_days = int(input("Type in the number of days for the moving average: "))
    moving_average_plot(sub, days=no_days)