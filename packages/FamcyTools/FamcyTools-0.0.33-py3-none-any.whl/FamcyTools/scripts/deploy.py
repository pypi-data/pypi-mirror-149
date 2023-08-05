import os
import sys
import subprocess
import FamcyTools

LOCAL_USER = FamcyTools.HOME_DIR+"/.local/share/famcy"

def main(args):
	# Write famcy.ini
	content = """[uwsgi]
module = wsgi:app
master = true
processes = 5
socket = /tmp/%s.sock
chmod-socket = 660
vacuum = true
die-on-term = true
enable-threads = true
single-interpreter = true
http-websockets = false
""" % (args[0])

	f = open(FamcyTools.FAMCY_DIR % (args[0]) + "/famcy.ini", "w")
	f.write(content)
	f.close()
	
	# Write wsgi.py
	content = """from Famcy import create_app

app = create_app('%s',True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)"""% (args[0])

	f = open(FamcyTools.FAMCY_DIR % (args[0]) + "/wsgi.py", "w")
	f.write(content)
	f.close()

	print()
	print("== Copy the following part and setup system service == (Need to change path if necessary)")
	print("""
[Unit]
Description=uWSGI instance to serve famcy
After=network.target

[Service]
User=%s
Group=www-data
WorkingDirectory=%s/.local/share/famcy/%s/venv/lib/python3.7/site-packages/Famcy
Environment="PATH=%s/.local/share/famcy/%s/venv/bin"
ExecStart=%s/.local/share/famcy/%s/venv/bin/uwsgi --ini famcy.ini

[Install]
WantedBy=multi-user.target
""" % (FamcyTools.USERNAME, FamcyTools.HOME_DIR, args[0], FamcyTools.HOME_DIR, args[0], FamcyTools.HOME_DIR, args[0]))

	print()
	print("== Copy the following part to nginx configurations == (Need to change alias path if necessary)")
	print("""
location / {
	include uwsgi_params;
	uwsgi_pass unix:/tmp/%s.sock;
}

location /static  {
    alias %s/.local/share/famcy/%s/venv/lib/python3.7/site-packages/Famcy/static;
}
""" % (args[0], FamcyTools.HOME_DIR, args[0]))
	print("Deployed to wsgi")