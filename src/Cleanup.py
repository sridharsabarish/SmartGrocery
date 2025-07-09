from loguru import logger
class Cleanup:
    
    def cleanup_dataframe(self,combined_df):
        combined_df['Item'] = combined_df['Item'].str.replace('*', '')
        combined_df['Item'] = combined_df['Item'].str.replace(',', '')
        combined_df['Item'] = combined_df['Item'].str.lstrip()
        combined_df['Item'] = combined_df['Item'].apply(lambda x: x.split()[0])
        logger.debug("Item cleaned")
        combined_df = combined_df.sort_values(by='Item', ascending=True)
        combined_df = combined_df[~combined_df['Item'].str.isdigit()]

        combined_df['Frequency'] = combined_df.groupby('Item')['Item'].transform('count')
        logger.debug("Frequency created")
        combined_df = combined_df.drop_duplicates(subset='Item')
        combined_df = combined_df[['Item', 'Frequency']].sort_values(by='Frequency', ascending=False)
        logger.debug("Now combined d contains item and frequency")
        return combined_df
