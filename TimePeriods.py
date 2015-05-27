# -------------------------------------------------------------------------------
# Name: TimePeriods.py
# Purpose: Manipulate and modify lists of time ranges
# Author:      Alexander Kim
# Created: 10 Oct 2014
# Version: v0.1
# -------------------------------------------------------------------------------


import calendar
from datetime import *


class TimePeriods:
    # Initiate class
    def __init__(self, list_of_periods):
        self.periods = list_of_periods

    def has(self, tm):
        check = False
        for period in self.periods:
            start = period[0]
            end = period[1]
            if start <= tm <= end:
                check = True
                break
        return check

    # Substract "another_list_of_periods" from self.periods
    def substract_with(self, another_list_of_periods):
        class IntervalTree:
            def __init__(self, h, left, right):
                self.h = h
                self.left = left
                self.right = right

        def merged(A, B, op, l=-float("inf"), u=float("inf")):
            if l > u:
                return None
            if not isinstance(A, IntervalTree):
                if isinstance(B, IntervalTree):
                    opT = op
                    A, B, op = B, A, (lambda x, y: opT(y, x))
                else:
                    return op(A, B)
            left = merged(A.left, B, op, l, min(A.h, u))
            right = merged(A.right, B, op, max(A.h, l), u)
            if left is None:
                return right
            elif right is None or left == right:
                return left
            return IntervalTree(A.h, left, right)

        def to_range_list(T, l=-float("inf"), u=float("inf")):
            if isinstance(T, IntervalTree):
                return to_range_list(T.left, l, T.h) + to_range_list(T.right, T.h, u)
            return [(l, u - 1)] if T else []

        def range_list_to_tree(L):
            return reduce(lambda x, y: merged(x, y, lambda a, b: a or b),
                          [IntervalTree(R[0], False, IntervalTree(R[1] + 1, True, False)) for R in L])

        def dt(u):
            return datetime.utcfromtimestamp(u)

        def ut(d):
            return calendar.timegm(d.timetuple())

        lst1 = []
        for time_period in self.periods:
            lst1.append([ut(time_period[0]), ut(time_period[1])])
        lst2 = []
        for time_period in another_list_of_periods:
            lst2.append([ut(time_period[0]), ut(time_period[1])])

        r1 = range_list_to_tree(lst1)
        r2 = range_list_to_tree(lst2)
        diff = merged(r1, r2, lambda a, b: a and not b)
        result = to_range_list(diff)
        datetime_diff = []
        for item in result:
            if dt(item[1]) > dt(item[0]):
                datetime_diff.append([dt(item[0]), dt(item[1])])

        self.periods = datetime_diff
        return self

    # Merge self.periods with "another_list_of_periods"
    def merge_with(self, another_list_of_periods):
        i = sorted(set([tuple(sorted(x)) for x in another_list_of_periods]))
        merged_periods = [i[0]]
        for c, d in i[1:]:
            a, b = merged_periods[-1]
            if c <= b < d:
                merged_periods[-1] = a, d
            elif b < c < d:
                merged_periods.append((c, d))
            else:
                pass
        self.periods = merged_periods

    #Merge self.periods with itself, i.e. reduce the number of time periods, but merging overlapping periods
    def merge(self):
        i = sorted(set([tuple(sorted(x)) for x in self.periods]))
        merged_periods = [i[0]]
        for c, d in i[1:]:
            a, b = merged_periods[-1]
            if c <= b < d:
                merged_periods[-1] = a, d
            elif b < c < d:
                merged_periods.append((c, d))
            else:
                pass
        self.periods = merged_periods
        return self

    # Merge self.periods with itself if time separation between periods
    # is less than ""min_separation"

    def merge_if(self, **keywords):
        key = keywords.keys()[0]
        new_periods = []
        if key == "min_separation":
            min_separation = keywords[key]
            for i, period in enumerate(self.periods):
                start = period[0]
                end = period[1]
                if i != len(self.periods) - 1:  #not last period
                    next_start = self.periods[i + 1][0]
                    if end + timedelta(seconds=min_separation) > next_start:
                        end = end + timedelta(seconds=min_separation)
                new_periods.append([start, end])
        self.periods = new_periods
        self.merge()
        return self

    # return list of periods' start times
    def get_start_times(self):
        start_times = []
        for period in self.periods:
            start_times.append(period[0])
        return start_times

    # return list of periods' end times
    def get_end_times(self):
        end_times = []
        for period in self.periods:
            end_times.append(period[1])
        return end_times

    # return list of periods' center times
    def get_center_times(self):
        center_times = []
        for period in self.periods:
            start = period[0]
            end = period[1]
            duration_sec = (end - start).total_seconds()
            center = start + timedelta(seconds=duration_sec / 2.0)
            center_times.append(center)
        return center_times

    # sort periods by either start (indx=0) or end (indx=1) times
    def sort_by_index(self, indx):
        if indx == 0 or indx == 1:
            self.periods.sort(key=lambda x: x[indx])
            return self
        else:
            raise ValueError('Incorrect index: should be 0 or 1')

    # time shift start times
    def shift_starts(self, **keywords):
        buffer_time_delta = timedelta(seconds=0)
        key = keywords.keys()[0]
        if key == 'seconds':
            buffer_time_delta = buffer_time_delta + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            buffer_time_delta = buffer_time_delta + timedelta(minutes=keywords[key])
        elif key == 'hours':
            buffer_time_delta = buffer_time_delta + timedelta(hours=keywords[key])
        new_periods = []
        for period in self.periods:
            start_tm = period[0]
            end_tm = period[1]
            buffered_start = start_tm + buffer_time_delta
            new_periods.append([buffered_start, end_tm])

        self.periods = new_periods
        return self


    def hasPeriodsShorterThan(self, **keywords):
        time_delta = timedelta(seconds=0)
        key = keywords.keys()[0]
        if key == 'seconds':
            time_delta = time_delta + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            time_delta = time_delta + timedelta(minutes=keywords[key])
        elif key == 'hours':
            time_delta = time_delta + timedelta(hours=keywords[key])

        for period in self.periods:
            duration = (period[1] - period[0])
            if duration < time_delta:
                return True
        return False

    # time shift end times
    def shift_ends(self, **keywords):
        buffer_time_delta = timedelta(seconds=0)
        key = keywords.keys()[0]
        if key == 'seconds':
            buffer_time_delta = buffer_time_delta + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            buffer_time_delta = buffer_time_delta + timedelta(minutes=keywords[key])
        elif key == 'hours':
            buffer_time_delta = buffer_time_delta + timedelta(hours=keywords[key])
        new_periods = []
        for period in self.periods:
            start_tm = period[0]
            end_tm = period[1]
            buffered_end = end_tm + buffer_time_delta
            new_periods.append([start_tm, buffered_end])
        self.periods = new_periods
        return self

    # time shift period, i.e. shift center times
    def shift(self, **keywords):
        buffer_time_delta = timedelta(seconds=0)
        key = keywords.keys()[0]
        if key == 'seconds':
            buffer_time_delta = buffer_time_delta + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            buffer_time_delta = buffer_time_delta + timedelta(minutes=keywords[key])
        elif key == 'hours':
            buffer_time_delta = buffer_time_delta + timedelta(hours=keywords[key])
        new_periods = []
        for period in self.periods:
            start_tm = period[0]
            end_tm = period[1]
            buffered_start = start_tm + buffer_time_delta
            buffered_end = end_tm + buffer_time_delta
            new_periods.append([buffered_start, buffered_end])
        self.periods = new_periods
        return self

    # extend (or trim) periods' duration
    def extend(self, **keywords):
        buffer_time_delta = timedelta(seconds=0)
        new_periods = []
        key = keywords.keys()[0]
        if key == 'seconds':
            buffer_time_delta = buffer_time_delta + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            buffer_time_delta = buffer_time_delta + timedelta(minutes=keywords[key])
        elif key == 'hours':
            buffer_time_delta = buffer_time_delta + timedelta(hours=keywords[key])
        elif key == 'percents':
            percents = keywords[key]
            for period in self.periods:
                start = period[0]
                end = period[1]
                duration_in_sec = (end - start).total_seconds()
                extend_time = duration_in_sec * percents / 100.0
                extended_start = start - timedelta(seconds=extend_time / 2.0)
                extended_end = end + timedelta(seconds=extend_time / 2.0)
                new_periods.append([extended_start, extended_end])

        if key != 'percents':
            for period in self.periods:
                start_tm = period[0]
                end_tm = period[1]
                buffered_start = start_tm - buffer_time_delta
                buffered_end = end_tm + buffer_time_delta
                new_periods.append([buffered_start, buffered_end])

        self.periods = new_periods
        return self

    # remove time periods that are shorter than sertain duration
    def remove_if_shorter(self, **keywords):
        key = keywords.keys()[0]
        min_duration = keywords[key]
        new_periods = []

        for period in self.periods:
            start = period[0]
            end = period[1]
            duration_in_sec = (end - start).total_seconds()
            if key == 'seconds':
                if duration_in_sec > min_duration:
                    new_periods.append(period)
            elif key == 'minutes':
                if duration_in_sec / 60.0 > min_duration:
                    new_periods.append(period)
            if key == 'hours':
                if duration_in_sec / 3600.0 > min_duration:
                    new_periods.append(period)

        self.periods = new_periods
        return self

    # round period's start and end time to either X seconds or X minutes
    def round(self, **keywords):
        td1 = timedelta(seconds=0)
        td2 = timedelta(seconds=0)
        new_periods = []
        key = keywords.keys()[0]
        if key == 'seconds':
            for period in self.periods:
                start_tm = period[0]
                td1 = timedelta(seconds=keywords[key] / 2.0)
                start_tm = start_tm + td1
                td2 = timedelta(seconds=start_tm.second % keywords[key], microseconds=start_tm.microsecond)
                start_tm = start_tm - td2

                end_tm = period[1]
                td1 = timedelta(seconds=keywords[key] / 2.0)
                end_tm = end_tm + td1
                td2 = timedelta(seconds=end_tm.second % keywords[key], microseconds=end_tm.microsecond)
                end_tm = end_tm - td2

                new_periods.append([start_tm, end_tm])
        elif key == 'minutes':
            for period in self.periods:
                start_tm = period[0]
                td1 = timedelta(minutes=keywords[key] / 2.0)
                start_tm = start_tm + td1
                td2 = timedelta(minutes=start_tm.minute % keywords[key], seconds=start_tm.second,
                                microseconds=start_tm.microsecond)
                start_tm = start_tm - td2

                end_tm = period[1]
                td1 = timedelta(minutes=keywords[key] / 2.0)
                end_tm = end_tm + td1
                td2 = timedelta(minutes=end_tm.minute % keywords[key], seconds=end_tm.second,
                                microseconds=end_tm.microsecond)
                end_tm = end_tm - td2
                new_periods.append([start_tm, end_tm])

        self.periods = new_periods
        return self

    # divide long period into smaller once by specifying max duration
    def divide(self, **keywords):
        td = timedelta(seconds=0)
        key = keywords.keys()[0]
        if key == 'seconds':
            td = td + timedelta(seconds=keywords[key])
        elif key == 'minutes':
            td = td + timedelta(minutes=keywords[key])
        elif key == 'hours':
            td = td + timedelta(hours=keywords[key])

        divided_periods = []
        for period in self.periods:
            start = period[0]
            end = period[1]
            start2 = start
            end2 = start2 + td
            if end2 < end:
                while end2 < end:
                    old_start2 = start2
                    old_end2 = end2
                    divided_periods.append([old_start2, old_end2])
                    start2 = old_end2 + timedelta(seconds=1)
                    end2 = start2 + td
                divided_periods.append([old_end2 + timedelta(seconds=1), end])
            else:
                divided_periods.append([start, end])
        self.periods = divided_periods
        return self

    # returns a center time of a time period that is the closest
    # to a given time 'tm'
    def get_closest_center(self, tm, **keywords):
        list_of_dt = []
        list_of_abd_dt = []
        for t in self.get_center_times():
            dt = tm - t
            list_of_dt.append(dt)
            list_of_abd_dt.append(abs(dt))

        min_distance = min(list_of_abd_dt)
        key = keywords.keys()[0]
        for dt in list_of_dt:
            if abs(dt) == min_distance:
                if keywords[key] == 'value':
                    return tm - dt
                elif keywords[key] == 'index':
                    return self.get_center_times().index(tm - dt)

    # returns list of periods' durations
    def get_durations(self):
        durations = []
        for period in self.periods:
            duration = (period[1] - period[0]).total_seconds()
            durations.append(duration)
        return durations

    # returns list of  formatted periods depending on a key ('STK' or 'ISO') provided
    def formatted_periods(self, key):
        formatted_times = []
        if key != 'STK' and key != 'ISO':
            raise ValueError('Incorrect key: should be "STK" or "ISO"')
        for period in self.periods:
            start = period[0]
            end = period[1]
            if key == 'STK':
                formatted_start = start.strftime('%d %b %Y %H:%M:%S')
                formatted_end = end.strftime('%d %b %Y %H:%M:%S')
            elif key == 'ISO':
                formatted_start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                formatted_end = end.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                raise ValueError('Invalid key: should be either "ISO" or "STK"')
            formatted_times.append([formatted_start, formatted_end])
        return formatted_times

    # Get an overall time period covered by all "self.periods"
    def get_boundary(self):
        start_times = self.get_start_times()
        end_times = self.get_end_times()
        left_boundary = min(start_times)
        right_boundary = max(end_times)
        return [left_boundary, right_boundary]

    # get time periods not covered by "self.periods"
    def get_outside_periods(self):
        return substract_datetime([self.get_boundary()], self.periods)


def substract_datetime(datetime_lst1, datetime_lst2):
    class IntervalTree:
        def __init__(self, h, left, right):
            self.h = h
            self.left = left
            self.right = right

    def merged(A, B, op, l=-float("inf"), u=float("inf")):
        if l > u:
            return None
        if not isinstance(A, IntervalTree):
            if isinstance(B, IntervalTree):
                opT = op
                A, B, op = B, A, (lambda x, y: opT(y, x))
            else:
                return op(A, B)
        left = merged(A.left, B, op, l, min(A.h, u))
        right = merged(A.right, B, op, max(A.h, l), u)
        if left is None:
            return right
        elif right is None or left == right:
            return left
        return IntervalTree(A.h, left, right)

    def to_range_list(T, l=-float("inf"), u=float("inf")):
        if isinstance(T, IntervalTree):
            return to_range_list(T.left, l, T.h) + to_range_list(T.right, T.h, u)
        return [(l, u - 1)] if T else []

    def range_list_to_tree(L):
        return reduce(lambda x, y: merged(x, y, lambda a, b: a or b),
                      [IntervalTree(R[0], False, IntervalTree(R[1] + 1, True, False)) for R in L])

    def dt(u):
        return datetime.utcfromtimestamp(u)

    def ut(d):
        return calendar.timegm(d.timetuple())

    lst1 = []
    for time_period in datetime_lst1:
        lst1.append([ut(time_period[0]), ut(time_period[1])])
    lst2 = []
    for time_period in datetime_lst2:
        lst2.append([ut(time_period[0]), ut(time_period[1])])

    r1 = range_list_to_tree(lst1)
    r2 = range_list_to_tree(lst2)
    diff = merged(r1, r2, lambda a, b: a and not b)
    result = to_range_list(diff)
    datetime_diff = []
    for item in result:
        if dt(item[1]) > dt(item[0]):
            datetime_diff.append([dt(item[0]), dt(item[1])])
    return datetime_diff


if __name__ == '__main__':
    lst1 = [(datetime(2014, 6, 20, 12, 36, 23), datetime(2014, 6, 20, 14, 15, 12)),
            (datetime(2014, 6, 20, 15, 30, 43), datetime(2014, 6, 20, 16, 35, 34)),
            (datetime(2014, 6, 20, 16, 40, 00), datetime(2014, 6, 20, 18, 50, 00))]

    a = TimePeriods(lst1)
    print a.get_durations()
    print a.hasPeriodsShorterThan(seconds=3892)
