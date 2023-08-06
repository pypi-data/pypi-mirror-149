
import  pandas as pd
class Exporter:

    def save_csv(self, data, output):
        df = pd.DataFrame(data = data)
        df.to_csv(output+'.csv')
        return df