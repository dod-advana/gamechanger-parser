from policy_analytics_parser.parse import policy_text_pipeline
from text_extraction.extract_text import generate_extracted_text_from_directory

import json
from pathlib import Path

def writer(out_dir, extracted_text_dict):
    outname = Path(extracted_text_dict["filename"]).stem + ".json"

    p = Path(out_dir)
    if not p.exists():
        p.mkdir()
    print('writing to', p.joinpath(outname))
    with open(p.joinpath(outname), "w") as fp:
        json.dump(extracted_text_dict, fp, indent=4)


print("running examples")
try:
    # generates extract text dictionaries that can be used in a pipeline etc
    for extracted_text_dict in generate_extracted_text_from_directory(source="example_input/"):

        # example to write output of extracted text
        writer(out_dir="./example_output/", extracted_text_dict=extracted_text_dict)

        # use with an entire pipeline
        policy_text_pipeline(
            extracted_text_dict, 
            pipeline_args={"destination": "example_policy_analytics_output/"}
        )
        
except Exception as e:
    print(e)
finally:
    print("end example")
