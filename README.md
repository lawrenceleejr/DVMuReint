# DV+mu Reinterpretation Effort

Taylor Sussmane, Karri Folan Di Petrillo, Lawrence Lee

We are working to take the results of the search [ATLAS SUSY-2018-33 ("DV+mu")](
https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2018-33/) and reinterpret them for the model shown in Figure 5 of [ATLAS-CONF-2018-003 ("RPC-RPV")](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/CONFNOTES/ATLAS-CONF-2018-003/). To do this, we'd like to use [CheckMATE](checkmate.hepforge.org) since it already has the DV+mu search implemented in its LLP version.

Since CheckMATE has many dependencies, let's try to work in docker to simplify.

## Docker

To start off, install Docker and learn more [here](https://www.docker.com/101-tutorial).

## Generation of HEPMC Files (Running MadGraph+Pythia8)

Larry will take care of getting initial HepMC files and try to document how it's done here.

This will be done via the pre-packaged docker image available at `scailfin/madgraph5-amc-nlo:mg5_amc3.3.1`.

There is a sample HepMC file containing two simulated events in this repository (`Sample_2Event.hepmc`). This will be useful for testing the CheckMATE workflow. A larger sample (10k events) is available here:

https://www.dropbox.com/s/uaa91743egy6op4/tag_1_pythia8_events.hepmc.gz?dl=0

(These events are `g g > t1 t1~` with no ISR. Decaying everything in P8.)

### Notes:

<details>
  <summary>Click to expand!</summary>
  
      Initial MG commands.

      Start container
      ```
      docker run --rm -ti -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1
      ```

      If you haven't done it yet in the docker image, you'll need to download a PDF set:

      ```bash
      lhapdf get NNPDF23_lo_as_0130_qed
      ```

      Start MG with

      ```
      mg5_aMC
      ```

      Then in there, you can run 

      ```madgraph

      # (you don't have to do this if you obtained RPVMSSM_UFO from this repo)
      # convert model ./RPVMSSM_UFO/RPVMSSM_UFO/

      import model ./RPVMSSM_UFO/RPVMSSM_UFO/

      generate p p > t1 t1~
      add process p p > t1 t1~ j
      add process p p > t1 t1~ j j
      output RPVStop
      launch

      # This is currently throwing an error when trying to have P8 on.
      # RuntimeError : Info file not found for PDF set 'NNPDF23_lo_as_0130_qed'
      # I've tried running at the madgraph prompt: install lhapdf6 but that doesn't seem to solve the issue

      lhapdf get NNPDF23_lo_as_0130_qed # this is needed at ther terminal

      # We have to edit the parameter card to force these decays to happen. 
      # ** There is a template param card in this repo under Cards/ Use it to get the decays right. **
      # This decay table gets handed to pythia for the decay of the N1
      
      # MAKE SURE to link the TWO cards in this repo into your cards directory. We need these params!

      ```

      Running the container:
      ```bash
      docker run --rm -ti -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1
      ```

</details>


## Running of limits (in CheckMATE)

This will be Taylor's primary focus at first. Because of the dependencies required, we can start from a docker image containing a full delphes installation available at `ghcr.io/scipp-atlas/mario-mapyde/delphes:latest`. Larry created a docker image that contains CheckMATE preinstalled made from that image. See [https://hub.docker.com/repository/docker/lawrenceleejr/checkmate](https://hub.docker.com/repository/docker/lawrenceleejr/checkmate). `v0.2` has a successful install of CheckMATE(-LLP) at commit [4299900](https://github.com/CheckMATE2/checkmate2-LLP/tree/4299900a98a38100c31bf75222a03d3494c39714).

CheckMATE is located in `/usr/local/share/checkmate/` and the actual executable can be found at `/usr/local/share/checkmate/bin/CheckMATE`.

DV+mu search has CheckMATE code `atlas_2003_11956`.

To start up a docker contain from this image, I recommend going into the directory of this repository and running:

```bash
docker run --rm -ti -v $PWD:$PWD -w $PWD lawrenceleejr/checkmate:latest
```

Once in the docker container, you'll have access to the files in this repo. Run the setup script:

```bash
source setup.sh
```

which will take care of the fix from that strange linking problem. Then you should be able to run CheckMATE with:

```bash
/usr/local/share/checkmate/bin/CheckMATE path/to/dat/file
```

from anywhere. Unfortunately was unable to get vim/emacs loaded into the image, so you can edit the files on the host machine in the shared folder (this repo, if you ran the `docker run` command here), and the changes will appear to the docker session as well.

When compiling CheckMATE, if you get an error that AnalysisBase.h doesn't exist, it's because it's pointing to a file on Dr. Lee's local computer. Run the following commands:

```bash
mkdir -p /Users/leejr/work/DVMuReint
```
```bash
ln -s /usr/local/share/checkmate /Users/leejr/work/DVMuReint/Checkmate
```


### Notes

<details>
  <summary>Click to expand!</summary>


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
      # This didn't compile. Trying commit 4299900 (which is current HEAD)
      # Also didn't. Trying ed3e43c.
      # Also didn't. Trying 62e1702.
      # Hrm. Got 4299900 to work with a fresh checkout and building with only one proc. make -j1
      tar -xzf LLP.tar.gz
      mv checkmate2-LLP-LLP/ checkmate2-LLP
      mv -T checkmate2-LLP /usr/local/share/checkmate/
      cd /usr/local/share/checkmate/

      apt-get install autoconf libtool automake
      autoconf
      automake
      ./configure --with-rootsys=/opt/root/ --with-delphes=/usr/local/share/delphes/delphes/ --with-hepmc=/usr/local/share/HepMC-2/
      make

      # I then moved everything to /usr/local/share/checkmate and successfully tested the installation with

      cd /usr/local/share/checkmate/bin
      ./CheckMATE -n example -ev=example_run_cards/auxiliary/testfile.hep -xs="1 fb" -wp8

      ```


</details>

