# mono-&phi; example

Generate events in Madgraph as done for 1712.04939, 1707.05783:

### resonant production in Madgraph, decay in Pythia
```
# first define process
import model RPVMSSM_UFO
define p = u d s c b u~ d~ s~ c~ b~ g
generate p p >  ur
add process p p > ur~
output monophi_example

launch
# point pythia to file with custom decay table
# path-to-file
done
param_card.monophi.dat
set nevents 10000
done
```

To have the &phi;  (a right-handed squark in the UFO) decay as in our simplified model (to a jet and missing energy) we need to give a custom decay to Pythia, by having Pythia read the following
`pythia.readstring("2000002:oneChannel = on 1.0 102  2 1000022")`

The cross section from the above example is `0.125pb` and is independent of the invisible particle mass. The resulting events do not have spin correlations, but it is a small difference from fully generating the evnets in Madgraph.

Note that even though the RPV couplings in param_card.monophi.dat are 0.1 by default, the production cross section (times branching ratio) is a free parameter in the likelihood evaluation (through the cross section multiplier &mu;). For example, at (1250,900) the best-fit cross section multiplier is <hat>&mu;</hat>=2.87, which (with 100% BR of &phi;&rarr;u&psi;) corresponds to &lambda;<sub>112</sub>=0.17.

### generate everything in Madgraph
One can also generate the entire event topology in Madgraph:

```
# first define process
import model RPVMSSM_UFO
define p = u d s c b u~ d~ s~ c~ b~ g
generate p p >  ur, ur > u n1
add process p p > ur~, ur~ > u~ n1
output monophi_example
```

```
# now run madevent
launch
# do not turn on pythia/delphes...
done
# import param_card at benchmark point (1250,900), set number of events per run
param_card.monophi.dat
set nevents 10000
done
```

If everything worked correctly, the output cross section would be around `0.1227pb` (each run will be slightly different because of MonteCarlo sampling). This is the same as above, because the width of &psi; was hard-coded in the `param_card.monophi.dat`. When madgraph generates the decay of &phi;, it computes the partial width into the given decay channel and finds the branching ratio by comparing to the `param_card` width value to give the final cross section. Here I hardcoded the &phi; width to the q&psi; partial width (as computed below).

The UFO model used here is inherently supersymmetric, meaning that the &phi;&psi;q coupling is the bino coupling.
In general, &phi; would have two decay channels open, `qq` and `q psi` but in the simplified model discussed in our papers, the &phi;&psi;q coupling is general and it would be possible to have BR~1 for the missing energy topology.


For scans over parameter space, one will want to modify the masses at each step.
A small subtlety is that the hardcoded &psi; width used above is incorrect for any other choice of masses. As explained above and in the [README](./README.md), cross sections reported by Madgraph could be wrong if the total width stored in the card is not the same as the width that it calculates for this decay chain.
In any case, we are only interested in the cross section times branching ratio into this signal. A simple solution is to set the total width of the squark to the partial width to quark-neutralino, which in turn can be computed by Madgraph by temporarily setting the RPV coupling to zero (or, one can also compute the partial width analytically and use `set width 2000002 <analytical_width>`). For example:

```
launch
# do not turn on pythia/delphes...
done
set nevents 10000
param_card.monophi.dat
# new masses
set mass 2000002 1500.0
set mass 1000022 1200.0
set width 1000022 0.0
# set RPV couplings to zero, compute width
set RLDD1x1x2  0.
set RLDD1x2x1  0.
compute_widths 2000002 --body_decay=2.1
#reset RPV couplings to 0.1
set RLDD1x1x2  0.1
set RLDD1x2x1  -0.1
done
```
With the commands above the neutralino width should come out as `DECAY  2000002   4.286695e-01`, and the total cross section should be around `0.052 pb`.
