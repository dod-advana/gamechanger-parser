import sys
import os

# absolute path two levels up
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))

sys.path.insert(0, parent_dir)

from policy_analytics_parser.parse import pdf_to_json

source_dir = os.path.join(current_dir, "..", "..", "data_input")
destination_dir = os.path.join(current_dir, "..", "..", "sample_output")

pdf_to_json(source=source_dir, destination=destination_dir)

print('done')
