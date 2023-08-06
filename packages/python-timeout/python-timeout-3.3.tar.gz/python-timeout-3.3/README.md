### Timeout
Random timeout between minimum and maximum values

Installation:
`pip install python-timeout`

Usage:
```
from timeout import random_timeout, sleep_for

random_timeout(10, 20) # Random timeout between 10 and 20 seconds
random_timeout(60, 120) # Random timeout between one minute (60 seconds) and two minutes (120 seconds)
random_timeout(1) # Random timeout for around one second

sleep_for(5) # Sleep for five minutes
sleep_for(15) # Sleep for fifteen minutes
```
