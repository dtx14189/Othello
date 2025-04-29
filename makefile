Othello:
	echo "#!/bin/bash" > Othello
	echo "pypy3 test_script.py" >> Othello
	chmod u+x test_script.py
	chmod u+x Othello

clean:
	rm Othello
	