## Getting Started

Follow the steps below to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-project-name.git
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