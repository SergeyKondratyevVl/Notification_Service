import pytz

TZone = [(tz.split('/')[-1], tz) for tz in pytz.common_timezones_set]