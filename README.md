# DV+mu Reinterpretation Effort

Taylor Sussmane, Karri Folan DiPetrillo, Lawrence Lee

We are working to take the results of the search [ATLAS SUSY-2018-33 ("DV+mu")](
https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2018-33/) and reinterpret them for the model shown in Figure 5 of [ATLAS-CONF-2018-003 ("RPC-RPV")](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CONFNOTES/ATLAS-CONF-2018-003/). To do this, we'd like to use [CHECKMATE](checkmate.hepforge.org) since it already has the DV+mu search implemented in its LLP version.

Since CHECKMATE has many dependencies, let's try to work in docker to simplify.

## Docker

To start off, install Docker and learn more [here](https://www.docker.com/101-tutorial).

## Generation of HEPMC Files (Running MadGraph+Pythia8)

Larry will take care of getting initial HepMC files and try to document how it's done here.

This will be done via the pre-packaged docker image available at `scailfin/madgraph5-amc-nlo:mg5_amc3.3.1`.

### Notes:

Initial MG commands.

```madgraph
convert model ./RPVMSSM_UFO/RPVMSSM_UFO/

import model ./RPVMSSM_UFO/RPVMSSM_UFO/

generate p p > t1 t1~, (t1 > t n1, (n1 > t b s) ), (t1~ > t~ n1, (n1 > t b s) )
output RPVStop
launch
```

Running the container:
```bash
docker run --rm -ti -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1
```

## Running of limits (in CHECKMATE)

This will be Taylor's primary focus at first. Because of the dependencies required, we can start from a docker image containing a full delphes installation available at `ghcr.io/scipp-atlas/mario-mapyde/delphes:latest`. Larry will attempt to create a docker image that contains CHECKMATE preinstalled made from this.



### Notes:

```bash
docker run --rm -ti -v $PWD:$PWD -w $PWD ghcr.io/scipp-atlas/mario-mapyde/delphes:latest
```


## Misc Notes

```
root@99d461f91cd0:/Users/leejr/work/DVMuReint# python -V
Python 2.7.18
root@99d461f91cd0:/Users/leejr/work/DVMuReint# root-config --prefix --has-minuit2
/opt/root yes
root@99d461f91cd0:/Users/leejr/work/DVMuReint# ls /usr/local/share/delphes/delphes/
```

Building HepMC (instructions from `INSTALL.cmake`):

```bash
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/share/HepMC-2/ \
      -Dmomentum:STRING=GEV \
      -Dlength:STRING=MM \
      ../HepMC-2.06.11/
make
make test
make install
```

Building CheckMate:

```bash
wget https://github.com/CheckMATE2/checkmate2-LLP/archive/refs/tags/LLP.tar.gz
tar -xzf LLP.tar.gz
mv checkmate2-LLP-LLP/ checkmate2-LLP
mv -T checkmate2-LLP /usr/local/share/checkmate/
cd /usr/local/share/checkmate/

apt-get install autoconf
autoconf
automake
./configure --with-rootsys=/opt/root/ --with-delphes=/usr/local/share/delphes/delphes/ --with-hepmc=/usr/local/share/HepMC-2/
make

```



