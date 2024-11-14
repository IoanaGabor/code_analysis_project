import polars as pl
from ast_processing import extract_tree_features

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


dataframe["comments"] = dataframe.apply(
    lambda row: row["full_code"].replace(row["uncommented_code"], "").strip(), axis=1
)

dataframe = dataframe.head(10000)

dataframe.to_csv('data-small.csv', index=False) 

dataframe["nodes"], dataframe["adjacency_matrix"] = zip(*dataframe["function_only_code"].apply(extract_tree_features))
