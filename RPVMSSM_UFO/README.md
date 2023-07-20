# RPVMSSM UFO
UFO (Universal FeynRules Output) file for the R-parity violating (RPV) extension of the Minimal Supersymmetric extension of the Standard Model (MSSM). Slightly modified from [the version on the FeynRules Model database](http://feynrules.irmp.ucl.ac.be/wiki/RPVMSSM).

Published papers whose results used this UFO files are [1712.04939](arxiv.org/abs/1712.04939), [1707.05783](arxiv.org/abs/1707.05783), [1601.03737](arxiv.org/abs/1601.03737).

The UFO model was originally written by Benjamin Fuks and published on the [FeynRules model database](http://feynrules.irmp.ucl.ac.be/wiki/RPVMSSM). The original model was defined in an SLHA2-compliant way (with squarks, e.g.  su1,su2,...,su6 sorted by their masses), with the mixing matrix (e.g. USQMIX block) defining the rotation to the flavor basis (ul,ur,...,t1,t2). I found this sub-optimal and preferred the SLHA1 notation, where the squark mixing matrices are by default diagonal apart from the stop mixing angle (which result in the (33,36,63,66) elements of the 6x6 USQMIX matrix), so I re-generated the UFO file from the Mathematica notebook provided at the link above, the only difference including a different parameter file (sps1a.dat instead of af1.dat used originally).

The UFO file has been validated in multiple ways, by comparing analytical expressions to numerical results computed in [Madgraph5_aMC@NLO](https://launchpad.net/mg5amcnlo) for RPV-specific processes:
 - 2- and 3-body RPV decays of squarks and gluinos/neutralinos, including phase space dependance on final state masses
 - resonant squark production
 
 ## parameter cards
Various param_cards are attached that can be used as input in MadGraph/MadEvent (param_card.dat):
- `param_card.dat`: default parameters from sps1a benchmark point from pre-LHC days, with all RPV couplings set to 0.1 (including the A-terms, in which case this corresponds to 0.1 GeV).
- `param_card.zero.dat`: all SUSY particles decoupled exactly at 10 TeV, all RPV couplings set to zero. Use this to change a few masses or couplings to get a simplified topology.
- `param_card.udd112.monophi.dat`: only light states are the right-handed up squark and the (bino-like) neutralino. Used in [1712.04939](arxiv.org/abs/1712.04939), [1707.05783](arxiv.org/abs/1707.05783). In the language of these papers, the up squark is the scalar triplet &phi; and the neutralino is &psi;. Masses are set to the benchmark value used in 1712.04939, (m<sub>&phi;</sub>,m<sub>&psi;</sub>)=(1250,900). By default the RPV coupling is &lambda;<sub>112</sub>=0.1, meaning that resonant &phi; production goes from *ds* initial state. Branching ratio of &phi;&rarr;u&psi; is set to 1, while the neutralino is made stable by setting its width to zero. As explained in 1707.05783, the neutralino cannot be stable and was there made to decay 100% to a hidden sector. When &psi; is on shell, this has no effect on the event.
- `param_card.udd312.stop_nomix.bino.dat` and `param_card.udd312.stop_nomix.hino.dat`: only light states are the right-handed stop and a bino- or higgsino-like neutralino (in which case there is also a chargino and another neutralino, all close in mass). The RPV coupling &lambda;<sub>312</sub> is the only non-zero coupling (*tds* operator). Modifications for the 313 and 323 couplings (*tdb* and *tbs*) are easily implemented (remember that RPV UDD couplings are antisymmetric in the last two indices!).  Used in [1601.03737](arxiv.org/abs/1601.03737).

## short example
See [example_monophi.md](example_monophi.md) for short instructions on how to generate events with the mono-&phi; topology described in [1712.04939](arxiv.org/abs/1712.04939), [1707.05783](arxiv.org/abs/1707.05783).

## Comments
### decay widths in madgraph
Note that decay widths hardcoded in the param_cards are for the default values of masses and couplings. They should be updated after having changed parameters, for example using the `compute_widths <particle_ID> (options)` in MadEvent, or by hand from analytical formulas.

When generating events for a particular topology (e.g. specifying decay chains), MadGraph computes the partial width for the given channel and then uses the branching ratio to compute the cross section. So a wrong total width would give a wrong cross section, although the events generated are perfectly fine otherwise. If you are not using the cross section info from Madgraph, this is not necessary and one can skip the `compute_widths` step.
 
### bug in pythia 8
Versions of [Pythia 8](http://home.thep.lu.se/~torbjorn/Pythia.html) until pythia8226 had a bug in the treatment of the baryon-number violating vertex (such as UDD in RPV SUSY) which would appear when generating events with a resonantly produced squark and additional jets (as one would need to do matching). This has been fixed in pythia8226 and following versions (thanks to Peter Skands for the help).
