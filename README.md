# csv_parser
Csv parser for coding challenge

# Running script locally:
1. Create venv
```
python -m venv name_of_venv
```
2. Activate venv
For Linux:
```
source name_of_venv/bin/activate 
```
For Windows
```
source name_of_venv/Scripts/activate  
```
3. Install requirements.txt
```
pip install -r requirements.txt
```
4. Run main.py and just copy the .csv you want to parse in the main.py folder. The script will create the necessary folders and parse your .csv.

# Running script in Docker:

1. Docker compose
```
docker-compose up 
```
If the Docker container needs to be rebuilt you can run it with 
```
docker-compose up --build
```
2. And you are ready to use it just copy wanted .csv from local pc to docker container inside /bidnamic folder

# Bonus for Windows:
We can easily create a .exe file for our script with pyinstaller(already added in requirements.txt).
```
pyinstaller --onefile main.py
```
You can move the .exe file to the main folder or wherever you want and the script should work.

# Conclusion:
Copy .csv in main folder, and script will save parsed .csv files in format processed/$currency/search_terms/$timestamp.csv. Can be easily modified to work with Flask.
