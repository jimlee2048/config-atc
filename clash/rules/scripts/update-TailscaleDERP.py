import requests
import json
import ruamel.yaml

def save_yaml(list, output_file, quoted=False):
    print(f"Updating: {output_file}")
    if quoted:
        yaml_data = {"payload": [ruamel.yaml.scalarstring.SingleQuotedScalarString(i) for i in list]}
    else:
        yaml_data = {"payload": list}
    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=2, offset=2)
    with open(output_file, "w") as f:
        yaml.dump(yaml_data, f)

def save_text(list, output_file):
    print(f"Updating: {output_file}")
    with open(output_file, "w") as f:
        for i in list:
            f.write(f"{i}\n")

if __name__ == "__main__":
    try:
        json_data = requests.get(
            'https://login.tailscale.com/derpmap/default').json()
    except Exception as e:
        print("Error: Unable to fetch data from Tailscale")
        raise e

    list_domain = []
    list_ip_cidr = []
    list_ip_cidr6 = []

    for region in json_data["Regions"].values():
        for node in region["Nodes"]:
            list_domain.append(node['HostName'])
            list_ip_cidr.append(f"{node['IPv4']}/32")
            list_ip_cidr6.append(f"{node['IPv6']}/128")

    list_ip = list_ip_cidr + list_ip_cidr6
    list_classical = ["DOMAIN,"+d for d in list_domain] + ["IP-CIDR,"+i+",no-resolve" for i in list_ip_cidr] + ["IP-CIDR,"+i+",no-resolve" for i in list_ip_cidr6]

    # save in clash text format (.list)
    save_text(list_domain, "../TailscaleDERP_domain.list")
    save_text(list_ip, "../TailscaleDERP_ip.list")
    save_text(list_classical, "../TailscaleDERP_classical.list")

    # save in clash yaml format
    save_yaml(list_domain, "../TailscaleDERP_domain.yaml", quoted=True)
    save_yaml(list_ip, "../TailscaleDERP_ip.yaml", quoted=True)
    save_yaml(list_classical, "../TailscaleDERP_classical.yaml")

    print("Finished")
