## Getting Started

Follow the steps below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/PaniMartyna/location-tracker.git
cd location-tracker
```

### 2. Create and activate virtual env

```bash
python3 -m venv venv
source ./venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Make migrations

```bash
python manage.py migrate
```

### 5. Run dev server

```bash
python manage.py runserver
```


## If I had more time...

I would write tests and think about more edge cases that should be handled.  

## To prevent location spam...

Upon receiving new ping I would check time span from the last ping received by this device. If the time span was shorter
than X, I would not save the ping to db. Such an event would be logged for further check.

Another idea would be counting pings within half an hour and sending error log if the number of pings exceeded set limit. 
This would limit error logs from the first idea to just one in a half hour, but would extend staff reaction time.


