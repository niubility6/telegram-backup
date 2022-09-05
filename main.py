import os
from pathlib import Path
import yaml
import shutil
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from config import config

base_path = str(Path(__file__).parent.absolute())
autochoose = ["python3" , "py -3"]
for choose in autochoose:
    if 'Python 3.' in os.popen("{} --version".format(choose)).read():
        break
execute_tgarchive = "{} {}/sources/tgarchive.py".format(choose, base_path)

# 2. create floders
father_floder = config["telegram_name"]
current_path = base_path + "/{}/".format(father_floder)
current_session_path = current_path + "/tgarchive_store/session.session"
if not os.path.exists(father_floder):
    os.makedirs(father_floder)

os.chdir(father_floder)
subfloder = ["tgarchive_store", "sites"]
for onesub in subfloder:
    if not os.path.exists(onesub):
        os.makedirs(onesub)

for groupkey, onegroup in config["groups"].items():
    subfloder = "tgarchive_store/{}".format(onegroup["name"])
    if not os.path.exists(subfloder):
        os.makedirs(subfloder)
    
    # go to group
    group_path = current_path + "/" + subfloder + "/me/"
    if not os.path.exists(group_path):
        os.chdir(group_path + "/../")
        # if not ,init
        cmd_ = "{} --new --path=me".format(execute_tgarchive)
        os.system(cmd_)
    os.chdir(group_path)
    # update config.yaml
    with open("config.yaml", 'rt', encoding="utf8") as stream:
        config_yaml = yaml.safe_load(stream)

    for c_key, c_value in config["defaults"].items():
        config_yaml[c_key] = c_value

    config_yaml["group"] = groupkey
    with open("config.yaml", 'w') as outfile:
        yaml.dump(config_yaml, outfile, default_flow_style=False)

    # do sync work
    if onegroup["sync"] == True:
        cmd_ = "{} --session {} --sync".format(execute_tgarchive, current_session_path)
        os.system(cmd_)

    # do build work
    if onegroup["build"] == True:
        cmd_ = "{} --build".format(execute_tgarchive)
        os.system(cmd_)
        # copy to sites
        shutil.copytree("./site", current_path + "/sites/{}/site".format(onegroup["name"]),  dirs_exist_ok=True)
        shutil.rmtree("./site")
    os.chdir(current_path)

# go to sites, update index.html
os.chdir(current_path)
index_path = current_path + "/sites/index.html"
model = '''<html>{}</html>'''
str_model = '<a href="./{}/site/index.html">{}</a><br>'
result_ = ""
for name in os.listdir(current_path + "/sites"):
    if name == "index.html":
        continue
    result_ += str_model.format(name, name)

with open(index_path, "w") as f:
    f.write(model.format(result_))

# run server
def start_httpd(directory: Path, port: int = 18000):
    print(f"serving from {directory}...")
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    httpd = ThreadingHTTPServer(('localhost', port), handler) # ThreadingHTTPServer can use CTRL+C to stop it!
    httpd.serve_forever()

if __name__ == "__main__":
    print("\n Now Start!")
    start_httpd(current_path + "/sites")