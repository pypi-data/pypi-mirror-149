cell 20

STRUCTURE
	include water.cfg pos 0. 0. 0. angle 90. 0. 0. stretch 2. 1. 1.
	repeat 3 pos 10. 0. 0. angle rand rand rand
END STRUCTURE

POTENTIAL
vdw 1
	OW HW lj 0.12 3.2963
END POTENTIAL