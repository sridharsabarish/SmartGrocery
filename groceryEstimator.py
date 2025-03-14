import PyPDF2
import pandas as pd
import glob
import pandas as pd
import matplotlib.pyplot as plt

def read_data_from_pdf(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)
    for page in range(num_pages):
        pageObj = pdfReader.pages[page]
        text = str(pageObj.extract_text())
        lines = text.split('\n')
        result = []
        header = []
        for line in lines:
            if "Beskrivning" in line:
                header = line.split()
                for l in lines[lines.index(line) + 1:]:
                    if "Total" in l:
                        break
                    result.append(l)
        output_string = '\n'.join(result)
        df = pd.DataFrame([x.rsplit(None, 5) for x in output_string.split('\n')], columns=header)
        new_df = df[[header[0], header[1], header[2], header[5]]]
        return new_df


def make_charts(combined_df):
    # Plot a bar chart for item frequencies
    plt.figure(figsize=(12, 8))
    items_to_plot = combined_df[combined_df['Frequency'] >= 2]
    plt.bar(items_to_plot['Item'], items_to_plot['Frequency'], color='skyblue')
    plt.xlabel('Item')
    plt.ylabel('Frequency')
    plt.title('Frequency of Items Purchased (Frequency >= 2)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('outputs/item_frequencies.png')


    
def make_pi_chart(top_10_items):
    
    plt.figure(figsize=(16, 16))
    plt.pie(top_10_items['Total Cost'], labels=[f'{item}\n{cost:.2f} SEK' for item, cost in zip(top_10_items['Item'], top_10_items['Total Cost'])], autopct='%1.1f%%')
    plt.title('Total Cost per Top 10 Items')
    plt.legend(top_10_items['Item'], loc='upper left')
    plt.savefig('outputs/top_10_items'+month+'.png')   
    

def read_monthly_grocery_data(month):
    all_df = pd.DataFrame()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    total_cost=0.0;
    for filename in glob.glob(month+"/*.pdf"):
        #print(filename)
       
        df = read_data_from_pdf(filename)
        
        #print("Debugging here ...")
        total_cost += df['Summa(SEK)'].astype(float).sum()
       
        
        #print("Out of debug")
        
        # total_cost = df['Summa(SEK)'].sum()
        # all_df_list = []
        # all_df_list.append(total_cost)
        # print(all_df_list)
        all_df = pd.concat([all_df, df], ignore_index=True)
    
        
    #print(all_df)
    #print(all_df.describe())
    all_df['Summa(SEK)'] = all_df['Summa(SEK)'].astype(float)
    distinct_items = all_df['Beskrivning'].unique()
    item_costs = []
    for item in distinct_items:
        item_costs.append([item, all_df[all_df['Beskrivning'] == item]['Summa(SEK)'].sum()])

    item_costs_df = pd.DataFrame(item_costs, columns=['Item', 'Total Cost'])
    item_costs_df.to_csv('outputs/grocery_data.csv', index=False)
    # Plot a pie chart
    top_10_items = item_costs_df.nlargest(20, 'Total Cost')
   
    other_items = item_costs_df.iloc[10:]
    other_items_cost = other_items['Total Cost'].sum()
    top_10_items.loc[len(top_10_items)] = ['Other', other_items_cost]
    #make_pi_chart(top_10_items)
    print("Month: ",month," Total cost : ", total_cost)

    return total_cost,item_costs_df

import os
#months = [f for f in os.listdir('.') if os.path.isdir(f)]

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

    #Todo : Good to maybe create a folder called data and let the code figure out the names of the directory
    months=["July","August","September","October","November","December", "January", "February"]
    a=[]
    b =[]
    
    for m in months:
        #print("Going through ", m)
        total_cost, new_df = read_monthly_grocery_data(m)
        a.append(new_df)
        b.append(total_cost);
        
        
    combined_df = pd.concat(a, ignore_index=True)

    
    
    combined_df = cleanup_dataframe(combined_df)
    combined_df.to_csv('outputs/combined_grocery_data.csv', index=False)
    top_10_items = combined_df.nlargest(10, 'Frequency')
    top_10_items.to_csv('outputs/top_ten_item.csv',index=False);

    #make_charts(combined_df)
    
    from matplotlib import pyplot as plt
    plt.plot(months, b, marker='o', linestyle='-')
    plt.xlabel('Months')
    plt.ylabel('Total Cost')
    plt.title('Groceries')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
main()



'''
Todo :

1. Connect the Df to a database and store the information?
2. Make it easy to see the purchase trends? - Graph would be nice.
3. Refactor
'''
