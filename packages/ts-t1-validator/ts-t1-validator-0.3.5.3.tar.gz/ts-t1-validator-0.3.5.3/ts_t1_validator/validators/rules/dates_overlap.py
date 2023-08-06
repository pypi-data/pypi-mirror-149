from datetime import datetime

from pytz import timezone

from .abstract_rule import ValidationRule
from ..exceptions import ValidationException


class DatesOverlapRule(ValidationRule):
    VALID_TIMEZONES = ['Pacific/Midway', 'Pacific/Honolulu', 'America/Anchorage', 'America/Los_Angeles',
                       'America/Denver', 'America/Chicago', 'America/New_York', 'America/Halifax',
                       'America/St_Johns', 'America/Sao_Paulo', 'Atlantic/South_Georgia', 'Atlantic/Cape_Verde',
                       'Etc/GMT', 'Europe/London', 'Europe/Paris', 'Europe/Kaliningrad', 'Europe/Moscow',
                       'Asia/Tehran', 'Asia/Dubai', 'Asia/Kabul', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Kathmandu',
                       'Asia/Dhaka', 'Asia/Bangkok', 'Asia/Shanghai', 'Asia/Tokyo', 'Australia/Adelaide',
                       'Australia/Sydney', 'Pacific/Pohnpei', 'Pacific/Auckland']

    def __init__(self, start_date, end_date, zone_name):

        self.start_date = start_date
        self.end_date = end_date

        self.zone_name = zone_name

    def execute(self):
        """
        rules:

        start_date is later than end_date. Message "start_date must be earlier than end_date"
        start_time is later than end_time. Message " start_time must be earlier than end_time"
        start_date is in the past. Message "start_date must be in the future"

        :return:
        """
        # validate timezone string
        if self.zone_name not in self.VALID_TIMEZONES:
            raise ValidationException("zone_name must be one of correct timezone names, e.g. 'America/New_York'")

        # combine dates
        tz = timezone(self.zone_name)
        try:
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%dT%H:%M")
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%dT%H:%M")
        except ValueError:
            raise ValidationException("dates must be provided in %Y-%m-%dT%H:%M format")

        start_date = datetime.combine(self.start_date, datetime.min.time())
        start_date = start_date.replace(hour=self.start_date.hour, minute=self.start_date.minute)
        start_date = tz.localize(start_date)

        end_date = datetime.combine(self.end_date, datetime.min.time())
        end_date = end_date.replace(hour=self.end_date.hour, minute=self.end_date.minute)
        end_date = tz.localize(end_date)

        # start_time is later than end_time
        if start_date >= end_date:
            # case: for the same date but time, "start_time must be earlier than end_time"
            if start_date.date() == end_date.date():
                raise ValidationException("start_time must be earlier than end_time")
            else:
                raise ValidationException("start_date must be earlier than end_date")

        if start_date.date() < datetime.now(tz=tz).date():
            raise ValidationException("start_date must be in future")
