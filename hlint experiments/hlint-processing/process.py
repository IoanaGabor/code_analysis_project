import pandas as pd
import subprocess
import tempfile

import polars as pl

splits = {
    'train': 'hf://datasets/blastwind/deprecated-github-code-haskell-function/data/train-*-of-*.parquet',
    'test': 'hf://datasets/blastwind/deprecated-github-code-haskell-function/data/test-*-of-*.parquet',
    'valid': 'hf://datasets/blastwind/deprecated-github-code-haskell-function/data/valid-00000-of-00001-636cb804972d8982.parquet'
}


df = pl.read_parquet(splits['train'])

dataframe = df.to_pandas()

dataframe = dataframe.loc[
    (dataframe["is_commented"] == True) & (dataframe["n_ast_nodes"] < 50),
    ["full_code", "uncommented_code", "function_only_code"]
]

dataframe = dataframe.head(100)


def run_hlint_on_snippet(haskell_code):
    """Runs hlint on a single Haskell code snippet."""
    with tempfile.NamedTemporaryFile(suffix=".hs", mode="w", delete=True) as temp_file:
        temp_file.write(haskell_code)
        temp_file.flush()  
        try:
            result = subprocess.run(
                ["hlint", temp_file.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            return result.stdout.strip()  # Return the output from hlint
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"  # Return the error message

# Apply hlint to each code snippet in the DataFrame
dataframe["hlint_output"] = dataframe["function_only_code"].apply(run_hlint_on_snippet)

# Save or print the results
# Example: df.to_csv('hlint_results.csv', index=False)
print(df)
