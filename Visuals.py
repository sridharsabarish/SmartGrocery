class Visuals:
    def make_charts(self,combined_df):
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


        
    def make_pi_chart(self,top_10_items,month):
        
        plt.figure(figsize=(16, 16))
        plt.pie(top_10_items['Total Cost'], labels=[f'{item}\n{cost:.2f} SEK' for item, cost in zip(top_10_items['Item'], top_10_items['Total Cost'])], autopct='%1.1f%%')
        plt.title('Total Cost per Top 10 Items')
        plt.legend(top_10_items['Item'], loc='upper left')
        plt.savefig('outputs/top_10_items'+month+'.png')   
        
    def generate_purchase_trend(self,months, b):
        plt.plot(months, b, marker='o', linestyle='-')
        plt.xlabel('Months')
        plt.ylabel('Total Cost')
        plt.title('Groceries')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

#months = [f for f in os.listdir('.') if os.path.isdir(f)]
