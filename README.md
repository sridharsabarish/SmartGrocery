# About 
- This project helps you parse your grocery reciepts pdf and helps you understand your purchase pattern and generate a shopping list!


# Quick Start (WIP)

## Requirements


### Software
- Install the requirements for PyPDF2, pandas, glob, datetime #todo

### Data collection and one time setups
- Download your grocery pdfs from your grocerer or take a photo of the bill (Not tested).

- Create the input folder 
    - `mkdir -p input`
- For every month create a folder and save as `2025-03` and so on, keep your receipts inside this for the corresponding month.
- Create the output folders
    - `mkdir -p outputs && mkdir -p outputs/shoppinglist`


## Running the code    
- Run the `groceryEstimator.py` using `python groceryEstimator.py`


## End results
- The program ends with a Graph of your purchase patterns and you can find the top 20 items you purchased as your shopping list!

# Future Goal
- Automatic fetch from grocery store API #todo
