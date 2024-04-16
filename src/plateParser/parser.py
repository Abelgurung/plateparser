import pandas as pd

class plateParser:    
    @classmethod
    def findStart(self, df):
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                element = df.iloc[i, j]
                if element == "A":
                    print("Start Index Found...")
                    return [i, j]
    
        print("Couldn't find 'A' well row")
        return None

    @classmethod
    def getIdxList(self, start_idx, plateSize):
        indices_list = []
        for i in range(plateSize[0] + 1):
            for j in range((plateSize[1] + 1)):
                row = start_idx[0] + i
                col = start_idx[1]+ j + 1
                indices_list.append((row, col))
    
        return indices_list

    @classmethod
    def findPlateSize(self, df, start_idx):    
        standardPlates = [(47, 71), (31, 47), (15, 23), (7, 11), (5, 7), (3, 5), (2, 3), (1, 2)]
        for i in standardPlates:
            try:
                idx = i[0] + start_idx[0]
                if df.iloc[idx, start_idx[1]] == chr(64 + idx - start_idx[0] + 1):                                
                    plateSize = i
                    break
            except IndexError:
                continue
        return plateSize

    @classmethod
    def parse(self, df):
        df = df.dropna()
        start_idx = self.findStart(df)
        
        plateSize = self.findPlateSize(df, start_idx)
        
        row = plateSize[0] + 1
        col = plateSize[1] + 1
        
        print("Plate size recognized:", row,'x', col)
        indices_list = self.getIdxList(start_idx, plateSize)
        
        wells = []
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                row_letter = chr(64 + i)
                wells.append(f"{row_letter}{j}")
        
        rows = list(range(1, row + 1)) * col
        cols = list(range(1, col + 1)) * row
        
        values = [(df.iloc[idx]) for idx in indices_list]
        
        parsed_df = pd.DataFrame({
            'row': rows,
            'column': cols,
            'well': wells,
            'values': values
        })
        
        return parsed_df