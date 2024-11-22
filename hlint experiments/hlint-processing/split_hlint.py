import pandas as pd
import re

# Sample output as a string
output = """
Main.hs:138:5-22: Suggestion: Use infix
Found:
  elem CliHelp flags
Perhaps:
  CliHelp `elem` flags

Main.hs:139:5-25: Suggestion: Use infix
Found:
  elem CliVersion flags
Perhaps:
  CliVersion `elem` flags

Main.hs:149:19-27: Warning: Redundant bracket
Found:
  (CliHelp)
Perhaps:
  CliHelp

Main.hs:150:19-30: Warning: Redundant bracket
Found:
  (CliVersion)
Perhaps:
  CliVersion

4 hints
"""

# Parse the output
warnings = []
current_warning = {}

lines = output.splitlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    if re.match(r'^\S+:\d+:\d+-\d+:', line):
        if current_warning:  
            warnings.append(current_warning)
        current_warning = {"Warning Name": line.split(": ", 1)[1]}
    elif line == "Found:":
        i += 1
        current_warning["Found"] = lines[i].strip()
    
    elif line == "Perhaps:":
        i += 1
        current_warning["Perhaps"] = lines[i].strip()
    
    i += 1

# Add the last warning
if current_warning:
    warnings.append(current_warning)

# Convert to DataFrame
df = pd.DataFrame(warnings, columns=["Warning Name", "Found", "Perhaps"])

print(df)
