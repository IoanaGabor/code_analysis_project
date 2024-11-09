import tree_sitter_haskell as tshaskell
from tree_sitter import Language, Parser

HS_LANGUAGE = Language(tshaskell.language())
parser = Parser(HS_LANGUAGE)

example = '''
main :: IO ()
main = do
  putStrLn "Enter your name:"
  name <- getLine
  putStrLn ("Hello, " ++ name ++ "!")
'''

tree = parser.parse(example.encode())

node = tree.root_node
print(node)