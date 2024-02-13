import yaml
import json

## load the yaml file
with open('base.yml', 'r') as f:
    config = yaml.safe_load(f)

## save the yaml file as output.yaml
with open('./test/output.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, indent=2, width=1000, line_break='\n')

## save the yaml file as output.json
with open('./test/output.json', 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)