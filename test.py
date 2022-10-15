import subprocess

main_prog = 'main.py'

try:
	subprocess.Popen(f"py {main_prog}", shell=True)
	subprocess.Popen(f"py {main_prog} 2", shell=True)
	subprocess.Popen(f"py {main_prog} 1 2", shell=True)
	
except Exception as e:
	print(e)
