import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--name",help="The name of the development enviroment to setup")
args = parser.parse_args()
if not os.path.exists("DevEnv"):
    os.mkdir("DevEnv")
os.chdir("DevEnv")
os.mkdir(args.name)
os.chdir(args.name)
jsn = open(f"{str(args.name)}.json", "w")
jsn.writelines(f"""
{{
    "File": "{str(args.name)}",
    "Modules": [""],
    "OSversion": 
}}
""")
jsn.close()
mpy = open(f"{args.name}.py", "w")
mpy.close()
