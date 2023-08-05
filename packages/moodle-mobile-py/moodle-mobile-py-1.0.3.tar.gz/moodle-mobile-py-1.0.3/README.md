# MoodleCrawler
A Python Wrapper for the Moodle Mobile API

## Installation
Install using pip:
```shell
pip install moodle-mobile-py
```

## First Steps
Start by creating an instance of the moodle crawler and logging in:
```python
import moodle


# initialise moodle crawler object
m = moodle.MoodleCrawler("<username>", "<password>", "https://moodle.example.com")
await m.login()

# print whether the current user an an admin of the moodle page
print(m.site_info.is_admin)
```

Note that the wrapper is written in an async/await style, and you have to call specific functions
from coroutines.
