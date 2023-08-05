import subprocess
import FamcyTools

def main(args):
	famcy_id = args[0]
	if "--dev" in args:
		_ = subprocess.check_output(["export", "FLASK_ENV=development"]) 
	_ = subprocess.check_output(["bash", FamcyTools.FAMCYTOOLS_DIR +"/scripts/bash/"+"run.sh", FamcyTools.FAMCY_DIR % (args[0]), famcy_id]) 