#! /bin/bash
nosetests &> nose.out; cat nose.out | less
