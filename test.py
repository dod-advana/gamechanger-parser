import sys
sys.path.append('../') # Sets parent directory to reach parsers

from parsers.parse import parse, pdf_to_json

out_dir = "parse_module_test/"

# parse(f_name, out_dir=out_dir)
pdf_to_json(source="data/", destination="sample_output/")
