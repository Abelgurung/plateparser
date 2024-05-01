# plateparser

Dealing with raw microplate data can be cumbersome because it is not structured to facilitate further analysis. `plateparser` allows users to parse raw microplate data into a structured format. This automation eliminates manual data entry, reducing human error and time spent on processing.

## Features

1. **Tidy Format Conversion**: Converts plate data into a tidy format.
2. **Plate Format Conversion**: Converts plate data into a plate-like format, resembling its original structure.

## Installation

```bash
   pip install plateparser
```

## Usage

```python
import pandas as pd
import plateparser

#Load your data
raw_microplate_data = pd.read_csv('../examples/byonoy_absolute_example.csv')
# Parse the plates
parsed_data = plateparser.tidyFormat(raw_microplate_data)
#Output: Parsed data in tidy format
```

<p align="center">
    <img src="examples/raw_data_example.png?raw=true" style="width: 350px; height: 300px" hspace="30"/>
    <img src="examples/parsed_data_example.png?raw=true" style= "height: 300px" hspace="30" />
    <p align="center" style="text-align: center;">
        Raw Microplate Data 😟 (left) to structured Data 😀 (right)
    </p>
</p>

See the [notebooks](./notebooks/tidyFormat.ipynb) directory for more examples.

## Limitations

- plateparser currently does not support multi-plate data

## License

The `plateparser` package is open-source software licensed under the [MIT License](LICENSE).

## Acknowledgements

This project was inspired by [platechain](https://github.com/sphinxbio/platechain). </br>
Thanks to the [Sphinx Bio](https://www.sphinxbio.com) Team for letting us use their microplate data for testing.
