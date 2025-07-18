import PyPDF2
import pandas as pd
import glob
from Visuals import Visuals
from loguru import logger
class Reading:
    
    magic_words = ["Betalat","Total"]
    def read_data_from_pdf(self, filename):
      
      
        pdfFileObj = open(filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        num_pages = len(pdfReader.pages)
        logger.trace(f'Num_pages = {num_pages}')
        for page in range(num_pages):
            pageObj = pdfReader.pages[page]
            text = str(pageObj.extract_text())
            logger.trace(f"Text is \n {text}")
            lines = text.split('\n')
            result = []
            header = []
            logger.trace("Going through each line")
            for line in lines:
                if "Beskrivning" in line:
                    header = line.split()
                    logger.trace(header)
                    logger.trace("Iterating each line")
                    for l in lines[lines.index(line) + 1:]:
                        logger.trace(l)
                        if any(magic_word in l for magic_word in self.magic_words):
                            break
                        result.append(l)
            logger.trace(f"Result :{result}")
            output_string = '\n'.join(result)
            logger.trace(f"Output string is :{output_string}")
            
            
            
 
            
            #TODO : check the logic below its seems a bit off
            
            logger.trace(filename)
            filename_parts = filename.split('/')
            month = filename_parts[-2]
            logger.trace(f"Month is :{month}")
            
            column_values = 5;
            if month >= '2025-04':
                column_values = 4
            
            
            df = pd.DataFrame([x.rsplit(None, column_values) for x in output_string.split('\n')], columns=header)
            df[header[column_values]] = df[header[column_values]].astype(str)
            logger.trace(f"Data Frame : {df}")
            # new_df = df[[header[0], header[1], header[2], header[4]]]
            return df

    def read_monthly_grocery_data(self,month):
        all_df = pd.DataFrame()
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        total_cost=0.0;
        
        
        for filename in glob.glob(month+"/*.pdf"):
            logger.trace(f"Going through {filename}")
            
            df = self.read_data_from_pdf(filename)
            
            logger.trace("Data frame collected from pdf")
            logger.trace(df['Summa(SEK)'])
            
            
            
            
            ## Current problem
            
            
            df['Summa(SEK)'] = df['Summa(SEK)'].str.replace(',','.')
            logger.trace("Changing , to .")
            logger.trace(df)
            
            df = df.dropna(subset=['Summa(SEK)'])
            logger.trace("Removed na values")
            
        
        
            for i in df['Summa(SEK)']:
                if i=="None":
                    logger.trace("Empty")
                    df = df.drop(df[df['Summa(SEK)'] == i].index)
                    
                logger.trace(f"Length of {i} is {len(i)}")
            
            

            
            df['Summa(SEK)'] = df['Summa(SEK)'].astype(float)
            total_cost += df['Summa(SEK)'].sum()
            logger.trace("Total cost obtained as")
            
            
            
            logger.trace("Out of debug")
            
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
        item_costs_df.to_csv('../outputs/grocery_data.csv', index=False)
        # Plot a pie chart
        top_10_items = item_costs_df.nlargest(20, 'Total Cost')

        other_items = item_costs_df.iloc[10:]
        other_items_cost = other_items['Total Cost'].sum()
        # top_10_items.loc[len(top_10_items)] = ['Other', other_items_cost]
        # chart = Visuals();
        # chart.make_pi_chart(top_10_items,month)
        logger.trace("Month: ",month," Total cost : ", total_cost)

        return total_cost,item_costs_df

