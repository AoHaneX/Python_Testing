# gudlift-registration

## 1. Why

This is a proof of concept (POC) project to show a light-weight version
of our competition booking platform. The aim is to keep things as light
as possible and use user feedback to iterate.

------------------------------------------------------------------------

## 2. Getting Started

This project uses:

-   Python 3.x+
-   Flask
-   A Python virtual environment

Documentation: - Flask: https://flask.palletsprojects.com/ - Virtual
environments: https://docs.python.org/3/library/venv.html

------------------------------------------------------------------------

## 3. Installation

### Clone the repository

``` bash
git clone <repository-url>
cd gudlift-registration
```

### Create a virtual environment

#### Windows (PowerShell)

``` powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4. Running the application

Start the Flask server with:

``` powershell
python -m flask --app server:app run
```

The application is then available at:

``` text
http://127.0.0.1:5000
```

------------------------------------------------------------------------

## 5. Testing

### Unit tests

``` bash
pytest
```

### Test coverage

Generate a coverage report:

``` bash
coverage run -m pytest
coverage report
```

Generate an HTML coverage report:

``` bash
coverage html
```

The report is generated in:

``` text
htmlcov/index.html
```

### Performance tests (Locust)

Run the performance test:

``` powershell
locust --headless --host http://127.0.0.1:5000 --users 6 --spawn-rate 1 --run-time 1m
```

Generate an HTML report:

``` powershell
locust --headless --host http://127.0.0.1:5000 --users 6 --spawn-rate 1 --run-time 1m --html performance-report.html
```

Open the report (Windows):

``` powershell
start performance-report.html
```

------------------------------------------------------------------------

## 6. Current setup

The application currently stores its data in JSON files:

-   `clubs.json`
-   `competitions.json`

These files simulate a database for this proof of concept.
