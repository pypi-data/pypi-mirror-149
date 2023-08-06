"""UtilDatetimeFormat class"""

import unittest
from datetime import timezone, timedelta
from time import localtime


class UtilDatetime(unittest.TestCase):
    @staticmethod
    def datetime_to_local_timezone(dt):
        # Get POSIX timestamp of the specified datetime.
        epoch = dt.timestamp()

        # Get struct_time for the timestamp.
        # This will be created using the system's locale and it's time zone.
        st_time = localtime(epoch)

        # Create a timezone object with the computed offset in the struct_time.
        tz = timezone(timedelta(seconds=st_time.tm_gmtoff))

        # Move the datetime instance to the new time zone.
        dt_ltz = dt.astimezone(tz)

        return dt_ltz

    @staticmethod
    def datetime_to_local_tz_str(dt):
        # Get datetime already in the new time zone.
        dt_ltz = UtilDatetime.datetime_to_local_timezone(dt)

        dt_ltz_str = dt_ltz.isoformat()

        # Replace microseconds -> not currently handled by the application
        # '2016-01-10T19:44:59.193982+01:00' => '2016-01-10T19:44:59.000+01:00'
        dt_ltz_str = dt_ltz_str[:-12] + '000' + dt_ltz_str[-6:]

        return dt_ltz_str

    @staticmethod
    def datetime_to_specific_timezone(dt, seconds_offset=7200):
        # Get POSIX timestamp of the specified datetime.
        epoch = dt.timestamp()

        # Get struct_time for the timestamp.
        # This will be created using the system's locale and it's time zone.
        st_time = localtime(epoch)

        # Create a timezone object with the computed offset in the struct_time.
        tz = timezone(timedelta(seconds=seconds_offset))

        # Move the datetime instance to the new time zone.
        dt_ltz = dt.astimezone(tz)

        return dt_ltz


if __name__ == '__main__':
    unittest.main()
