import pandas as pd


class plateparser:
    @classmethod
    def findStart(self, df, drop_na=True):
        """
        Finds the starting position of a plate in a DataFrame by searching for the first occurrence of "A" or "a".

        Parameters:
        - df (DataFrame): The DataFrame containing the plate data.
        - drop_na (bool, optional): If True, drops rows and columns containing only NaN values before searching. Default is True.

        Returns:
        - list: A list containing the row and column indices of the first occurrence of "A" or "a", or None if not found.
        """

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
        """
        Converts a numeric row index to its corresponding uppercase letter representation.

        Parameters:
        - n (int): The numeric row index.

        Returns:
        - str: The letter corresponding to the row index, following an alphabetic sequence.
        """
        if n <= 26:
            row_letter = chr(64 + n)
        else:
            row_letter = chr(64 + (n - 1) // 26) + chr(65 + (n - 1) % 26)
        return row_letter

    @classmethod
    def getLowerRowLetter(self, n):
        """
        Converts a numeric row index to its corresponding lowercase letter representation.

        Parameters:
        - n (int): The numeric row index, starting from 1.

        Returns:
        - str: The lowercase letter corresponding to the row index, following an alphabetic sequence.
        """
        if n <= 26:
            row_letter = chr(96 + n)
        else:
            row_letter = chr(96 + (n - 1) // 26) + chr(97 + (n - 1) % 26)
        return row_letter

    @classmethod
    def getIdxList(self, start_idx, plateSize):
        """
        Generates a list of indices corresponding to all wells in a plate, based on the starting index and plate size.

        Parameters:
        - start_idx (list): A list containing the starting row and column indices of the plate.
        - plateSize (tuple): A tuple containing the number of rows and columns in the plate.

        Returns:
        - list: A list of tuples, each representing the row and column indices of a well.
        """
        indices_list = []
        for i in range(plateSize[0] + 1):
            for j in range((plateSize[1] + 1)):
                row = start_idx[0] + i
                col = start_idx[1] + j + 1
                indices_list.append((row, col))
        return indices_list

    @classmethod
    def parse(self, df):
        """
        Parses a DataFrame into a plate format by finding the starting index and determining the plate size.

        Parameters:
        - df (DataFrame): The DataFrame containing the plate data.

        Returns:
        - tuple: A tuple containing the plate size and a list of values corresponding to each well in the plate.
        """
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
        """
        Creates a list of indices corresponding to the wells of a plate, starting from a given index.

        Parameters:
        - start_idx (list): A list containing the starting row and column indices of the plate.
        - plateSize (tuple): A tuple containing the number of rows and columns in the plate.

        Returns:
        - list: A list of tuples, each representing the row and column indices of a well.
        """
        indices_list = []
        for i in range(plateSize[0] + 1):
            for j in range((plateSize[1] + 1)):
                row = start_idx[0] + i
                col = start_idx[1] + j
                indices_list.append((row, col))
        return indices_list

    @classmethod
    def findPlateSize(self, df, start_idx):
        """
        Determines the size of the plate based on the starting index by checking against standard plate sizes.

        Parameters:
        - df (DataFrame): The DataFrame containing the plate data.
        - start_idx (list): A list containing the starting row and column indices of the plate.

        Returns:
        - tuple: A tuple containing the number of rows and columns in the plate.
        """
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
        """
        Converts the plate data into a tidy DataFrame format, where each well is a row.

        Parameters:
        - df (DataFrame): The DataFrame containing the plate data.
        - save (str, optional): Optional path to save the parsed DataFrame as a CSV file.

        Returns:
        - DataFrame: A tidy DataFrame where each row corresponds to a well with its row, column, well ID, and value.
        """
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
        """
        Converts the plate data into a plate-like DataFrame format, retaining its structure.

        Parameters:
        - df (DataFrame): The DataFrame containing the plate data.
        - keep_index (bool, optional): If True, includes an index column with row letters. Default is False.
        - save (str, optional): Optional path to save the formatted DataFrame as a CSV file.

        Returns:
        - DataFrame: A DataFrame resembling the original plate format.
        """
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
