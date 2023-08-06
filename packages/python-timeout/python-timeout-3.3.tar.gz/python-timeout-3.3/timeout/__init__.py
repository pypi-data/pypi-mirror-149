from time import sleep
from random import random, uniform
from datetime import datetime, timedelta

class random_timeout:
    '''Random timeout between minimum and maximum values'''
    def __init__(self, minimum, maximum=None):
        if not maximum:
            maximum = minimum
        if minimum <= 0:
            minimum = random()
        else:
            minimum -= random() # Random float between 0 and 1
        maximum += random()
        timeout_in_seconds = uniform(minimum, maximum) # Random float between minimum and maximum
        if timeout_in_seconds > 3600:
            timeout_in_hours = round(timeout_in_seconds / 3600) # Convert sleep time in seconds to hours
            til = datetime.now() + timedelta(hours=timeout_in_hours)
            til = til.strftime('%H:%M')
            print('Sleeping', timeout_in_hours, 'hours until', til)
        elif timeout_in_seconds > 60:
            timeout_in_minutes = round(timeout_in_seconds / 60) # Convert sleep time in seconds to minutes
            til = datetime.now() + timedelta(minutes=timeout_in_minutes)
            til = til.strftime('%H:%M')
            print('Sleeping', timeout_in_minutes, 'minutes until', til)
        sleep(timeout_in_seconds)

class sleep_for:
    '''Sleep amount of time in minutes, prints when it will continue'''
    def __init__(self, minutes):
        til = datetime.now() + timedelta(minutes=minutes)
        til = til.strftime('%H:%M')
        print('Sleeping', minutes, 'minutes until', til)
        print()
        sleep(minutes * 60)