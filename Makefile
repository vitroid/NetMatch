# use gmake
BINTARGET	=netmatch5a # cookfragment.pl
ETCTARGET   =ice1h2.ngph ice1c.ngph ice1h.ngph
CDEBUGFLAGS	=-g -Wall -Werror -DDEBUG
CFLAGS=-DMAP=0,1,2,3,4,5,6,7,8,9,10,11,12 # $(CDEBUGFLAGS)
all: $(BINTARGET)
netmatch5a: netmatch5a.o Mark2.o dm.o NetMatch.o
	$(CC) $(CFLAGS) $^ -o $@ $(LOCALLDFLAGS) $(LDFLAGS)
clean:
	rm netmatch5a *.o

graph.sqlite3:
	./prepare_db.py
%.ngph: %.lammpstrj
	./lammps2ngph.py < $< > $@
%.cycles.json: %.ngph
	./cycles.py < $< > $@
%.poly.ngph: %.cycles.json
	./polyhed.py < $< > $@
%.poly.yap: %.poly.ngph %.lammpstrj
	./lammps2yap2.py $*.poly.ngph < $*.lammpstrj > $*.poly.yap
# %.ice1c.ngph:  %.ngph ice1c.ngph
# 	./netmatch5a ice1c.ngph $<  | ./cookfragment.py | ./frag2ngph.py ice1c.ngph > $@
# %.ice1h2.ngph:  %.ngph ice1h2.ngph
# 	./netmatch5a ice1h2.ngph $<  | ./cookfragment.py | ./frag2ngph.py ice1h2.ngph > $@
# %.barrelan.ngph:  %.ngph barrelan.ngph
# 	./netmatch5a barrelan.ngph $<  | ./cookfragment.py | ./frag2ngph.py barrelan.ngph > $@
