## Setup
1. Clone this repo 
2. Create a virtual environment: `python3 -m venv venv` 
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate` 
4. Install required packages: `pip install -r requirements.txt`

## Setup Mac/Linux or windows wsl with Makefile
1. Clone this repo
2. make # run this command to create environment and run python script
3. make run # execute python script
4. make fclean # cleanup the python environment

## Running the Code manually
1. Make sure the virtual environment is activated
2. Run `python3 main.py` to execute the data extraction 
3. The output CSV files will be generated in the current directory
