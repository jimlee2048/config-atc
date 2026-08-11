# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "ruamel.yaml",
# ]
# ///

import json
from pathlib import Path
from urllib.request import urlopen

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString

DERP_MAP_URL = "https://login.tailscale.com/derpmap/default"
RULES_DIR = Path(__file__).resolve().parents[1] / "clash" / "rules"


def fetch_derp_map() -> dict:
    try:
        with urlopen(DERP_MAP_URL, timeout=30) as response:
            return json.load(response)
    except Exception as error:
        print("Error: Unable to fetch data from Tailscale")
        raise error


def build_rule_payloads(derp_map: dict) -> tuple[list[str], list[str], list[str]]:
    domain_rules = []
    ipv4_cidr_rules = []
    ipv6_cidr_rules = []

    for region in derp_map["Regions"].values():
        for node in region["Nodes"]:
            domain_rules.append(node["HostName"])
            ipv4_cidr_rules.append(f"{node['IPv4']}/32")
            ipv6_cidr_rules.append(f"{node['IPv6']}/128")

    cidr_rules = ipv4_cidr_rules + ipv6_cidr_rules
    classical_rules = (
        [f"DOMAIN,{domain}" for domain in domain_rules]
        + [f"IP-CIDR,{cidr},no-resolve" for cidr in ipv4_cidr_rules]
        + [f"IP-CIDR,{cidr},no-resolve" for cidr in ipv6_cidr_rules]
    )

    return domain_rules, cidr_rules, classical_rules


def write_yaml_rules(values: list[str], output_file: Path, quoted: bool = False) -> None:
    print(f"Updating: {output_file}")
    if quoted:
        yaml_data = {"payload": [SingleQuotedScalarString(value) for value in values]}
    else:
        yaml_data = {"payload": values}

    yaml = YAML()
    yaml.indent(sequence=2, offset=2)
    with output_file.open("w") as file:
        yaml.dump(yaml_data, file)


def write_text_rules(values: list[str], output_file: Path) -> None:
    print(f"Updating: {output_file}")
    output_file.write_text("".join(f"{value}\n" for value in values))


def main() -> None:
    domain_rules, cidr_rules, classical_rules = build_rule_payloads(fetch_derp_map())

    # save in clash text format (.list)
    write_text_rules(domain_rules, RULES_DIR / "TailscaleDerpDomain.list")
    write_text_rules(cidr_rules, RULES_DIR / "TailscaleDerpCidr.list")
    write_text_rules(classical_rules, RULES_DIR / "TailscaleDerpClassical.list")

    # save in clash yaml format
    write_yaml_rules(domain_rules, RULES_DIR / "TailscaleDerpDomain.yaml", quoted=True)
    write_yaml_rules(cidr_rules, RULES_DIR / "TailscaleDerpCidr.yaml", quoted=True)
    write_yaml_rules(classical_rules, RULES_DIR / "TailscaleDerpClassical.yaml")

    print("Finished")


if __name__ == "__main__":
    main()
