
import  pandas as pd
class Exporter:
    def __init__(self):
        self.save_col = ['tweet']

    def save_csv(self, data, output):
        df = pd.DataFrame(data = data)
        save_df = df[self.save_col]
        save_df.to_csv(output+'.csv')
        return df