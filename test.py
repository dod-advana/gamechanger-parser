from policy_analytics_parser.parse import policy_text_pipeline
from text_extraction.extract_text import generate_extracted_text_from_directory

print("running test")
try:
    for extracted_text_dict in generate_extracted_text_from_directory(source="data_input/"):
        policy_text_pipeline(
            extracted_text_dict, 
            pipeline_args={"destination": "policy_analytics_processed/"}
        )
        
except Exception as e:
    print(e)
finally:
    print("end test")
