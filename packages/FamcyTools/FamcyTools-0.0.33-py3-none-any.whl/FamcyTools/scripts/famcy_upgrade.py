import subprocess
import pkg_resources
import FamcyTools

def main(args):
	famcy_id = args[0]
	script_output = subprocess.check_output(["bash", FamcyTools.FAMCYTOOLS_DIR+"/scripts/bash/"+"upgrade.sh", FamcyTools.FAMCY_DIR % (args[0]), famcy_id]) 
	print("[Famcy Upgrade] ", script_output.decode())