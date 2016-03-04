import os

direntries=os.listdir('.')

for e in direntries:
	name=e.split('.')
	if len(name)>1:
		if name[1]=="py":
			f=open(e)
			contents=f.read()
			o=open(e+".new", "w")
			for c in contents:
				if c=='\t':
					o.write('    ')
				else:
					o.write(c)

			f.close()
			o.close()
			os.system("mv "+e+".new"+" "+e)
