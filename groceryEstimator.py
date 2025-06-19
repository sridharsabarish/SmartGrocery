import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from Reading import Reading
from Visuals import Visuals
from loguru import logger
def create_monthly_shopping_list():
    # Todo : A template for what needs to be done.
    print("TBD")
    


def cleanup_dataframe(combined_df):
    combined_df['Item'] = combined_df['Item'].str.replace('*', '')
    combined_df['Item'] = combined_df['Item'].str.replace(',', '')
    combined_df['Item'] = combined_df['Item'].str.lstrip()
    combined_df['Item'] = combined_df['Item'].apply(lambda x: x.split()[0])
    combined_df = combined_df.sort_values(by='Item', ascending=True)
    combined_df = combined_df[~combined_df['Item'].str.isdigit()]

    combined_df['Frequency'] = combined_df.groupby('Item')['Item'].transform('count')

    combined_df = combined_df.drop_duplicates(subset='Item')
    combined_df = combined_df[['Item', 'Frequency']].sort_values(by='Frequency', ascending=False)
    return combined_df

def main():

    # Pre processing
    reader = Reading();

    
    
   
    directory = './input'

    months = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    months.sort(key=lambda x: datetime.strptime(os.path.basename(x), "%Y-%m"))
    
    months_full = [os.path.join(directory, folder) for folder in months]
    logger.info(f"The folders are: {months}")
    
   
    
    
    #Todo : Good to maybe create a folder called data and let the code figure out the names of the directory
    #months=["July","August","September","October","November","December", "January", "February"]
    a=[]
    b =[]
    
    for m in months_full:
        logger.debug(f"Going through{m}")
        total_cost, new_df = reader.read_monthly_grocery_data(m)
        a.append(new_df)
        b.append(total_cost);
         
    combined_df = pd.concat(a, ignore_index=True)
    logger.info("Combined df looks like {combined_df}")

    
    
    combined_df = cleanup_dataframe(combined_df)
    combined_df.to_csv('outputs/combined_grocery_data.csv', index=False)
    top_10_items = combined_df.nlargest(20, 'Frequency')
    top_10_items.to_csv('outputs/shoppinglist/top_twenty_item.csv',index=False);

    #make_charts(combined_df)
    
    from matplotlib import pyplot as plt
    chart = Visuals()
    chart.generate_purchase_trend(months,b)
    
main()
'''
Todo :

1. Connect the Df to a database and store the information?
'''
