import subprocess
import FamcyTools

def main(args):
	famcy_id = args[0]
	init_script_output = subprocess.check_output(["bash", FamcyTools.FAMCYTOOLS_DIR +"/scripts/bash/"+"init.sh", famcy_id]) 
	print("[Famcy Init] ", init_script_output.decode())