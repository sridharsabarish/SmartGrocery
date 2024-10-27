import PyPDF2
import pandas as pd
import glob
import pandas as pd
import matplotlib.pyplot as plt

def parseGroceryPDF(filename):
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




def process_grocery_data(month):
    all_df = pd.DataFrame()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    for filename in glob.glob(month+"/*.pdf"):
        print(filename)
        df = parseGroceryPDF(filename)
        all_df = pd.concat([all_df, df], ignore_index=True)
        
    print(all_df)
    print(all_df.describe())
    all_df['Summa(SEK)'] = all_df['Summa(SEK)'].astype(float)
    distinct_items = all_df['Beskrivning'].unique()
    item_costs = []
    for item in distinct_items:
        item_costs.append([item, all_df[all_df['Beskrivning'] == item]['Summa(SEK)'].sum()])

    item_costs_df = pd.DataFrame(item_costs, columns=['Item', 'Total Cost'])
    item_costs_df.to_csv('grocery_data.csv', index=False)
    # Plot a pie chart
    top_10_items = item_costs_df.nlargest(10, 'Total Cost')
    plt.figure(figsize=(16, 16))
    other_items = item_costs_df.iloc[10:]
    other_items_cost = other_items['Total Cost'].sum()
    top_10_items.loc[len(top_10_items)] = ['Other', other_items_cost]
    plt.pie(top_10_items['Total Cost'], labels=[f'{item}\n{cost:.2f} SEK' for item, cost in zip(top_10_items['Item'], top_10_items['Total Cost'])], autopct='%1.1f%%')
    plt.title('Total Cost per Top 10 Items')
    plt.legend(top_10_items['Item'], loc='upper left')
    plt.savefig('top_10_items'+month+'.png')
    return item_costs_df

import os
months = [f for f in os.listdir('.') if os.path.isdir(f)]
#months=["July","August","September","October"]
a=[]
for m in months:
    a.append(process_grocery_data(m))

combined_df = pd.concat(a, ignore_index=True)

#combined_df = pd.concat([a, b, c, d], ignore_index=True)
print(combined_df)


combined_df.to_excel('combined_grocery_data.xlsx', index=False)
