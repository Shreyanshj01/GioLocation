# GioLocation
## Shreynash Veerloop FDE Assignment
###### API that finds latitude and longitude of the Address passed

## Files Structure
- [**app.py**](https://github.com/Shreyanshj01/GioLocation/blob/master/app.py): Client App is implemented here.
- [**logger_class.py**](https://github.com/Shreyanshj01/GioLocation/blob/master/logger_class.py): Logger class is implemented here.
- [**schema_validation.py**](https://github.com/Shreyanshj01/GioLocation/blob/master/schema_validation.py): Validation for payload is implemented here.
- [**requirements.txt**](https://github.com/Shreyanshj01/GioLocation/blob/master/requirements.txt): Contains the dependency for this project.

## Pre-requisites

- Python >=3.7

## Installation

1.Clone the repository

```bash
git clone https://github.com/Shreyanshj01/GioLocation.git
```

2.Navigate to the directory

3.Create a virtual environment

4.Activate the virtual environment

5.Install dependencies

```bash
pip install -r requirements.txt
```

6.Setup config.json file

```bash
{
    "GOOGLE_GEOCODE_API_URL": "https://maps.googleapis.com/maps/api/geocode/",
    "API_KEY" : "YOUR API_KEY HERE"
}
```

7.Run app.py

8.The API can be accessed at `http://localhost:5000`
