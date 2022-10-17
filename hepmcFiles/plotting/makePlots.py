# import ROOT
import sys

from matplotlib import pyplot as plt

import uproot3

filename = sys.argv[1]


f = uproot3.open(filename)
samplelabel = r"m($\tilde{t}$) = 1 TeV, m($\tilde{\chi}_1^0$) = 200 GeV, $\tau$($\tilde{\chi}_1^0$) = 100 ps"


def drawHist(tmph, norm=0, **kwargs):
	bins = tmph.edges
	counts = tmph.values
	if norm:
		counts = counts/norm
	plt.hist(bins[:-1], bins, weights=counts, **kwargs)

fig, ax = plt.subplots()


h = {}

##########################################

plt.clf()
h[0] = f["SRMET MET 0"]
h[1] = f["SRMET MET 1"]
h[2] = f["SRMET MET 2"]
h[3] = f["SRMET MET 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel("Truth MET [GeV]"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMET", transform=ax.transAxes)

plt.ylim(1e-4,5e-1)

plt.savefig("SRMET_MET.pdf")

##########################################

plt.clf()
h[0] = f["SRMET ntrk 0"]
h[1] = f["SRMET ntrk 1"]
h[2] = f["SRMET ntrk 2"]
h[3] = f["SRMET ntrk 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel(r"Track Multiplicity"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMET", transform=ax.transAxes)

plt.ylim(1e-4,5e-1)


plt.savefig("SRMET_ntrk.pdf")


##########################################

plt.clf()
h[0] = f["SRMET mvtx 0"]
h[1] = f["SRMET mvtx 1"]
h[2] = f["SRMET mvtx 2"]
h[3] = f["SRMET mvtx 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel(r"Vertex Mass [GeV]"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMET", transform=ax.transAxes)

plt.ylim(5e-4,1e0)


plt.savefig("SRMET_mvtx.pdf")


##########################################

plt.clf()
h[0] = f["SRMET maxd0 0"]
h[1] = f["SRMET maxd0 1"]
h[2] = f["SRMET maxd0 2"]
h[3] = f["SRMET maxd0 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel(r"Maximum Track d0 [mm]"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMET", transform=ax.transAxes)


plt.ylim(5e-4,1e-1)


plt.savefig("SRMET_maxd0.pdf")


##########################################

plt.clf()
h[0] = f["SRMET rxy 0"]
h[1] = f["SRMET rxy 1"]
h[2] = f["SRMET rxy 2"]
h[3] = f["SRMET rxy 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel(r"Transverse Decay Length [mm]"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMET", transform=ax.transAxes)

plt.ylim(5e-4,2e-1)


plt.savefig("SRMET_rxy.pdf")



##########################################

plt.clf()
h[0] = f["SRMU mupt 0"]
h[1] = f["SRMU mupt 1"]
h[2] = f["SRMU mupt 2"]
h[3] = f["SRMU mupt 3"]

drawHist(h[0],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls=":", label="Inclusive")
drawHist(h[1],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="--", label="+Event Selection")
drawHist(h[2],norm=h[0]._fEntries, histtype='step', color="tab:blue", ls="-", label="+Vertex Selection")
drawHist(h[3],norm=h[0]._fEntries, histtype='stepfilled', color="tab:blue", ls="-", label="+Muon Selection")

plt.xlabel(r"Muon Pt [mm]"); plt.ylabel("Fraction")
plt.yscale('log')
plt.legend(frameon=False)
plt.text(0.0,1.03,samplelabel+", SRMU", transform=ax.transAxes)

plt.ylim(5e-4,2e0)


plt.savefig("SRMU_mupt.pdf")




