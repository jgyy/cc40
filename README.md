## Task 1
Located in task1 directory, run make or python3 command there

### Manual Setup and run
- `cd task1` change to this directory
- Create a virtual environment: `python3 -m venv venv` 
- Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate` 
- Install required packages: `pip install -r requirements.txt`
- `./venv/bin/python3 src/main.py` Execute the python script

### Setup Mac/Linux or windows wsl with Makefile
- `make` run this command to create environment and run python script
- `make run` execute python script
- `make test` to run unit tester
- `make fclean` cleanup the python environment

### Running the Code manually
- Make sure the virtual environment is activated
2. Run `python3 main.py` to execute the data extraction 
3. The output CSV files will be generated in data directory for task1

## Task 2
Located in task2 directory, currently it is all pseudo code
