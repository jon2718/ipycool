import math, random, ping, socket
from matplotlib.pyplot import *
from termcolor import colored

def percentiles(n, num_percentiles, a, b):
    percentiles = []
    values = []
    for i in range(num_percentiles-1):
        values.append(n*(i+1)/num_percentiles)
    #print 'Values are:', values
    sum = 0
    count = 0
    for percent in values:
        while sum < percent:
            sum += a[count]
            count += 1
        percentiles.append(b[count-1])
    final_tail_events = n-sum
    worst_event = max(b)
    return percentiles, final_tail_events, worst_event


def quartiles(n, a, b):
    q1 = n/4
    q2 = n/2
    q3 = 3*n/4
    sum = 0
    count = 0
    while sum < q1:
        sum += a[count]
        count += 1
    q1 = b[count]
    while sum < q2:
        sum += a[count]
        count += 1
    q2 = b[count]
    while sum < q3:
        sum += a[count]
        count += 1
    q3 = b[count]
    return q1, q2, q3
           

def updatebins(bins, binsize, x):
    i = math.floor(x / binsize)
    if i in bins:
        bins[i] += 1
    else:
        bins[i] = 1


def finalizebins(bins, binsize):
    imin = min(bins.keys())
    imax = max(bins.keys())
    print imin, imax
    imin = int(imin)
    imax = int(imax)
    a = [0] * (imax - imin + 1)
    b = [binsize * k for k in range(imin, imax + 1)]
    for i in range(imin, imax + 1):
        if i in bins:
            a[i - imin] = bins[i]
    return a, b


def run_ping(n, cut, host):
    bins = {}
    binsize = 1
    count = 0
    cur_avg = 0
    cur_avg2 = 0
    timeout = 100
    packetsize=100
    #ion()
    #show()
    for i in range(n):
        ping_result = ping.do_one(host, timeout, packetsize)
        if ping_result is None:
            return
        x = 1000*ping_result
        if x < cut:
            count += 1
            cur_avg = (cur_avg*(count-1) + x)/count
            cur_avg2 = (cur_avg2*(count-1) + math.pow(x, 2))/count
            updatebins(bins, binsize, int(x))
            print bins
            #if count % 10 == 0:
            #    b, a = finalizebins(bins, binsize)
            #    print b,a
            #    pause(0.0001)
            #    bar(b,a)
            #    draw()
    b, a = finalizebins(bins, binsize)
    std = math.sqrt(cur_avg2-math.pow(cur_avg, 2))
    return b, a, cur_avg, std


def ping_histogram(trials, cut, host):
    a, b, avg, std = run_ping(trials, cut, host)
    q1, q2, q3 = quartiles(trials, a, b)
    p, final_tail_events, worst_event = percentiles(trials, 100, a, b)

# Plot the data
    #print b, a
    print colored('\nAverage is:', 'green'),
    print colored (avg, 'red')
    print colored ('\nStandard deviation is:', 'green'),
    print colored(std, 'red')
    print colored ('\nQuartiles:', 'green'),
    print colored (q1, 'red'),
    print colored (q2, 'red'),
    print colored (q3, 'red')

    print colored('\nPercentiles are:', 'green'),
    print colored(p, 'red')
    print colored ('\nNumber of final tail events:', 'green'),
    print colored(final_tail_events, 'red')
    print colored('\nWorst event:', 'green'), 
    print colored (worst_event, 'red')

    bar(b,a)
    show()