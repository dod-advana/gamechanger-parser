import sys
sys.path.append('../') # Sets parent directory to reach parsers

from parsers.parse import parse, pdf_to_json
# from parsers.entity_extraction import entities

# out_dir = "parse_module_test/"

# print(entities.graph_relations_entities_dict)

# parse(f_name, out_dir=out_dir)
pdf_to_json(source="data/", destination="sample_output/")
