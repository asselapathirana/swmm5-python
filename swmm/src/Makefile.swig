# Makefile for SWMM5
CC=gcc
CFLAGS=-fpic
LD=ld
LDFLAGS=shared
SOURCES = swmm5.c climate.c controls.c culvert.c datetime.c dynwave.c error.c findroot.c \
       flowrout.c forcmain.c gage.c gwater.c hash.c iface.c infil.c inflow.c \
       input.c inputrpt.c keywords.c kinwave.c landuse.c lid.c link.c massbal.c \
       mathexpr.c mempool.c node.c odesolve.c output.c project.c qualrout.c \
       rain.c rdii.c report.c routing.c runoff.c shape.c snow.c stats.c \
       statsrpt.c subcatch.c table.c toposort.c transect.c treatmnt.c xsect.c \
       swmm5_iface.c
OBJECTS=$(SOURCES:.c=.o)
@echo objects: $(OBJECTS)
library=swmm5.so

all: $(SOURCES) $(library)
$(library) : $(objs)
	  $(LD) $(LDFLAGS) $(OBJECTS) -o $@
%.c %.o:
	@echo Compiling $<..	
	$(CC) $(CFLAGS) $< -o $@

swmm5.o       : consts.h macros.h enums.h error.h datetime.h objects.h funcs.h text.h globals.h swmm5.h
climate.o     : headers.h
controls.o    : headers.h
culvert.o     : headers.h
datetime.o    : datetime.h
dynwave.o     : headers.h
error.o       : error.h
findroot.o    : findroot.h
flowrout.o    : headers.h
forcmain.o    : headers.h
gage.o        : headers.h
gwater.o      : headers.h odesolve.h
hash.o        : hash.h
iface.o       : headers.h
infil.o       : headers.h infil.h
inflow.o      : headers.h
input.o       : headers.h lid.h
inputrpt.o    : headers.h lid.h
keywords.o    : text.h
kinwave.o     : headers.h findroot.h
landuse.o     : headers.h
lid.o         : headers.h infil.h lid.h
link.o        : headers.h
massbal.o     : headers.h
mathexpr.o    : mathexpr.h
mempool.o     : mempool.h
node.o        : headers.h findroot.h
odesolve.o    : odesolve.h
output.o      : headers.h
project.o     : headers.h hash.h lid.h mempool.h
qualrout.o    : headers.h
rain.o        : headers.h
rdii.o        : headers.h
report.o      : headers.h
routing.o     : headers.h
runoff.o      : headers.h odesolve.h
shape.o       : headers.h
snow.o        : headers.h
stats.o       : headers.h
statsrpt.o    : headers.h lid.h
subcatch.o    : headers.h lid.h odesolve.h
table.o       : headers.h
toposort.o    : headers.h
transect.o    : headers.h
treatmnt.o    : headers.h
xsect.o       : headers.h findroot.h
