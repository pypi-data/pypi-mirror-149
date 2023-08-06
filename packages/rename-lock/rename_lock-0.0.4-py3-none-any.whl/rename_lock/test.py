
# Easy file exclusive locking tool [rename_lock]

import sys
from sout import sout
from ezpip import load_develop
# Easy file exclusive locking tool [rename_lock]
rename_lock = load_develop("rename_lock", "../", develop_flag = True)

# Easy file exclusive locking tool [rename_lock]
with rename_lock("./demo_file.txt") as rlock:
	# temporary file name
	temp_filename = rlock.filename
	# operation on locked file
	with open(temp_filename, "w") as f:
		f.write("something")

# method without "with" syntax
rlock = rename_lock("./demo_file.txt")
print(rlock.filename)
rlock.unlock()
