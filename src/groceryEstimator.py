import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from Reading import Reading
from Visuals import Visuals
from loguru import logger
from Cleanup import Cleanup
from groceryHelper import groceryHelper
os.makedirs("logs", exist_ok=True)
logger.add("../logs/app.log", rotation="1 MB", retention="7 days", level="DEBUG")


class groceryEstimator:
    def create_monthly_shopping_list(self):
        # Todo : A template for what needs to be done.
        logger.error("Not Implemented!")

    def produce_top_10_items(self,combined_df,SIZE=10):
        top_10_items = combined_df.nlargest(SIZE, 'Frequency')
        strs = "../outputs/shoppinglist/top_"+str(SIZE)+"_item.csv"
        top_10_items.to_csv(strs, index=False);
    def produce_outputs(self,combined_df,months,b):
        chart = Visuals()
        chart.make_charts(combined_df)
        chart.generate_purchase_trend(months,b)
        
    def save_to_db(self):
        # Todo : A template for what needs to be done.
        logger.error("Not Implemented!")
        
    def export_as_CSV(self,df):
        df.to_csv('../outputs/combined_grocery_data.csv', index=False)
def main():

    groceryhelper = groceryHelper()
    groceryestimator = groceryEstimator()
    df = groceryhelper.get_df()
    logger.debug("Grocery Helper successfully initialized")
    groceryestimator.produce_top_10_items(combined_df=df)
    groceryestimator.produce_outputs(df, groceryhelper.get_months(),groceryhelper.get_b())
    groceryestimator.export_as_CSV(groceryhelper.get_df())

    
main()
