import random
import time
from copy import deepcopy

from gregory.dataclass.time_series_data import TimeSeriesData
from gregory.granularity.granularity import *
from gregory.timeseries.batches import split, aggregate, pick_a_weekday, pick_a_day
from gregory.timeseries.expr import union, intersection, list_intersection, list_union
from gregory.timeseries.time_series import TimeSeries


if __name__ == '__main__':
    # GENERATE INPUT
    start_date = '2020-01-07'
    years = 5
    data = {}
    z = []
    i = 0
    print("Generating input time series...")
    for x in range(365*5):
        i += 1
        if i % 2 > 0:
            data = {'pippo': random.randint(200, 300), 'pluto': 2}
        else:
            data = {}
        day = TimeSeriesData(day=datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=x), data=data)
        z.append(day)

    tsl = TimeSeries(z)
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    a = tsl[:20]
    b = tsl[10:30]
    c = tsl[15:35]

    d = list_intersection([a,b])
    d = list_intersection([a,b,c])
    d = list_union([a,b,c])

    print("Testing deepcopy...")
    t = time.time()
    x = deepcopy(tsl)
    print(f"*** Executed in: {round(time.time() - t, 4)}s.")
    print("* Check objects are different...", id(tsl), id(x), id(x) != id(tsl))
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing cut (with inplace=False)...")
    min_date = datetime.strptime("2020-01-11", "%Y-%m-%d").date()
    max_date = datetime.strptime("2021-01-11", "%Y-%m-%d").date()
    t = time.time()
    y = tsl.cut(min_date=min_date, max_date=max_date, inplace=False)
    print(f"*** Executed in: {round(time.time() - t, 4)}s.")
    print("* Check min date is correct -", y[0].day == min_date)
    print("* Check max date is correct -", y[-1].day == max_date)
    print("* Check original time series did not change -", tsl[0].day != min_date, tsl[-1].day != max_date)
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing cut (with inplace=True)...")
    min_date = datetime.strptime("2020-01-11", "%Y-%m-%d").date()
    max_date = datetime.strptime("2021-01-11", "%Y-%m-%d").date()
    y = deepcopy(tsl)
    t = time.time()
    y.cut(min_date=min_date, max_date=max_date, inplace=True)
    print("* Check min date is correct -", y[0].day == min_date)
    print("* Check max date is correct -", y[-1].day == max_date)
    print(f"*** Executed in: {round(time.time() - t, 4)}s.")
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing resample (with inplace=True)...")
    min_date = datetime.strptime("2020-01-11", "%Y-%m-%d").date()
    max_date = datetime.strptime("2021-01-11", "%Y-%m-%d").date()
    y = deepcopy(tsl)
    t = time.time()
    y.resample(granularity=MonthlyGranularity(), inplace=True)
    print("* Check expected dates -", all([y[0].day == datetime.strptime("2020-02-01", "%Y-%m-%d").date(), y[1].day == datetime.strptime("2020-03-01", "%Y-%m-%d").date(), y[-1].day == datetime.strptime("2025-01-01", "%Y-%m-%d").date()]))
    print(f"*** Executed in: {round(time.time() - t, 4)}s.")
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing batch operations...")
    print("\tTesting split...")
    y = deepcopy(tsl)
    t = time.time()
    res = split(y, granularity=MonthlyGranularity())
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("\t* Check expected number of batches -", len(res) == 61)
    print("\t* Check expected dates -", all([res[0][0].day == datetime.strptime("2020-01-07", "%Y-%m-%d").date(), res[0][-1].day == datetime.strptime("2020-01-31", "%Y-%m-%d").date(), res[-1][0].day == datetime.strptime("2025-01-01", "%Y-%m-%d").date(), res[-1][-1].day == datetime.strptime("2025-01-04", "%Y-%m-%d").date()]))
    print("\tTesting aggregate...")
    y = deepcopy(tsl)

    def agg_func(list_):
        return {"len": len(list_)}

    t = time.time()
    res = aggregate(y, method=agg_func, granularity=MonthlyGranularity(), store_day_of_batch=-1)
    print(res[:10])
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("\tTesting pick_a_day...")
    y = deepcopy(tsl)
    t = time.time()
    res = pick_a_day(y, granularity=MonthlyGranularity(), day_of_batch=-1)
    print(res[:10])
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("\tTesting pick_a_weekday...")
    y = deepcopy(tsl)
    t = time.time()
    res = pick_a_weekday(y, granularity=MonthlyGranularity(), day_of_batch=-1, weekday=1)
    print(res[:10])
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing granularity inference...")
    t = time.time()
    print("\t* Expected Daily Granularity -", isinstance(tsl.data_granularity, DailyGranularity))
    rs = tsl.resample(WeeklyGranularity())
    print("\t* Expected Weekly Granularity -", isinstance(rs.data_granularity, WeeklyGranularity))
    rs = tsl.resample(MonthlyGranularity())
    print("\t* Expected Monthly Granularity -", isinstance(rs.data_granularity, MonthlyGranularity))
    rs = tsl.resample(QuarterlyGranularity())
    print("\t* Expected Quarterly Granularity -", isinstance(rs.data_granularity, QuarterlyGranularity))
    rs = tsl.resample(YearlyGranularity())
    print("\t* Expected Yearly Granularity -", isinstance(rs.data_granularity, YearlyGranularity))
    rs = TimeSeries()
    print("\t* Expected no Granularity for empty time series -", not rs.data_granularity)
    rs = TimeSeries([tsl[0]])
    print("\t* Expected no Granularity for single element time series -", not rs.data_granularity)
    print("Done.")

    print("\n----------------------------------------------------------------\n")

    print("Testing expressions...")
    print("\tTesting Union...")
    a = tsl[:10]
    b = tsl[5:15]
    t = time.time()
    res = union(a, b)
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("\t* Expected length -", len(res) == 15)
    print("\t* Expected first element -", res[0] == a[0])
    print("\t* Expected last element -", res[-1] == b[-1])
    print("\tTesting Intersection...")
    t = time.time()
    res = intersection(a, b)
    print(f"\t*** Executed in: {round(time.time() - t, 4)}s.")
    print("\t* Expected length -", len(res) == 5)
    print("\t* Expected first element -", res[0] == a[5])
    print("\t* Expected last element -", res[-1] == b[4])
    print("Done.")

    print("\n----------------------------------------------------------------\n")