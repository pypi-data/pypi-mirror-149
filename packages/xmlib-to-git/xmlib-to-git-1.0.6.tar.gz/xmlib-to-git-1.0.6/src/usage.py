# usage.py

def usage():
    print("usage :")
    print("src -f <input_xml_file> -n <app_name> [-c <customer_id>]")
    print("\t-o, --out-folder=\t\toutput folder")
    print(
        "\t-n, --name=\t\tapplication name, permit application merge in case of name change"
        " (ex core_app"
    )
    print("\t-f, --file=\t\t:XML file to convert")
    print("\t-g, --git-repository-ssh=\t\t: ssh url of the repository")
    print("\t-c, --customer-id=\t\tOPTIONEL : customer id, to create a new branch")
