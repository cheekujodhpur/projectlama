 
from game import TestMaster
import sys

if __name__ == "__main__":
 
    with TestMaster() as test:
    	test.init()
    	test.run()
