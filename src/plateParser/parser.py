import pandas as pd


class plateParser:
    @classmethod
    def findStart(self, df, drop_na=True):
        if drop_na:
            df = df.dropna()
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                element = df.iloc[i, j]
                if element in ("A", "a"):
                    return [i, j]

        print("Couldn't find 'A' well row")
        return None

    @classmethod
    def getRowLetter(self, n):
        if n <= 26:
            row_letter = chr(64 + n)
        else:
            row_letter = chr(64 + (n - 1) // 26) + chr(65 + (n - 1) % 26)
        return row_letter

    @classmethod
    def getLowerRowLetter(self, n):
        if n <= 26:
            row_letter = chr(96 + n)
        else:
            row_letter = chr(96 + (n - 1) // 26) + chr(97 + (n - 1) % 26)
        return row_letter

    @classmethod
    def getIdxList(self, start_idx, plateSize):
        indices_list = []
        for i in range(plateSize[0] + 1):
            for j in range((plateSize[1] + 1)):
                row = start_idx[0] + i
                col = start_idx[1] + j + 1
                indices_list.append((row, col))
        return indices_list

    @classmethod
    def parse(self, df):
        startIdx = self.findStart(df)
        if startIdx == None:
            startIdx = self.findStart(df, drop_na=False)
        else:
            df = df.dropna()
        plateSize = self.findPlateSize(df, startIdx)

        indices_list = self.getIdxList(startIdx, plateSize)
        values = [(df.iloc[idx]) for idx in indices_list]
        return plateSize, values

    @classmethod
    def createIdxList(self, start_idx, plateSize):
        indices_list = []
        for i in range(plateSize[0] + 1):
            for j in range((plateSize[1] + 1)):
                row = start_idx[0] + i
                col = start_idx[1] + j
                indices_list.append((row, col))
        return indices_list

    @classmethod
    def findPlateSize(self, df, start_idx):
        standardPlates = [(47, 71), (31, 47), (15, 23),
                          (7, 11), (5, 7), (3, 5), (2, 3), (1, 2)]
        for i in standardPlates:
            try:
                idx = i[0] + start_idx[0]
                if df.iloc[idx, start_idx[1]] in (self.getRowLetter(idx - start_idx[0] + 1), self.getLowerRowLetter(idx - start_idx[0] + 1)):
                    plateSize = i
                    break
            except IndexError:
                continue
        return plateSize

    @classmethod
    def tidyFormat(self, df, save=None):
        plateSize, values = self.parse(df)

        row = plateSize[0] + 1
        col = plateSize[1] + 1
        print("Plate size recognized:", row, 'x', col)

        wells = []
        for i in range(1, row + 1):
            for j in range(1, col + 1):
                row_letter = self.getRowLetter(i)
                wells.append(f"{row_letter}{j}")

        rows = list(range(1, row + 1)) * col
        cols = list(range(1, col + 1)) * row

        parsed_df = pd.DataFrame({
            'row': rows,
            'column': cols,
            'well': wells,
            'values': values
        })

        if save:
            parsed_df.to_csv(save, index=False)
        return parsed_df

    @classmethod
    def plateFormat(self, df, keep_index=False, save=None):
        plateSize, values = self.parse(df)

        row = plateSize[0] + 1
        col = plateSize[1] + 1

        print("Plate size recognized:", row, 'x', col)

        if keep_index:
            col += 1
            startIdx = [0, 1]
            parsed_df = pd.DataFrame(
                index=range(0, row), columns=range(0, col))
            for i in range(row):
                parsed_df.iloc[i, 0] = self.getRowLetter(i+1)
        else:
            startIdx = [0, 0]
            parsed_df = pd.DataFrame(
                index=range(0, row), columns=range(0, col))

        indices_list = self.createIdxList(startIdx, plateSize)
        for (idx, (row_idx, col_idx)), value in zip(enumerate(indices_list), values):
            parsed_df.iloc[row_idx, col_idx] = value

        if save:
            parsed_df.to_csv(save, index=False)

        return parsed_df
