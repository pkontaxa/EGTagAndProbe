import ROOT
import TurnOnPlot_DATA as TurnOnPlot


plots = []
plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_plot"
plots[-1].xRange = (0,99.9)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)

plots.append(TurnOnPlot.TurnOnPlot())
plots[-1].name = "turnon_EBEE_plot"
plots[-1].xRange = (0,99.9)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)


inputFile = ROOT.TFile.Open("./TestTurnOn/fitOutput.root")

	
histo = inputFile.Get("histo_Stage2_vs_Pt_35GeV_1")
histo.__class__ = ROOT.RooHist
	
fit   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_1")
fit.__class__ = ROOT.RooCurve

turnon = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo, Fit=fit,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=20, LineColor=ROOT.kBlack,LineStyle=1,
                                    Legend="Test")

histo2 = inputFile.Get("histo_Stage2_vs_Pt_35GeV_2")
histo2.__class__ = ROOT.RooHist
	
fit2   = inputFile.Get("fit_Stage2_vs_Pt_35GeV_2")
fit2.__class__ = ROOT.RooCurve

turnon2 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo2, Fit=fit2,
                                    MarkerColor=ROOT.kRed, MarkerStyle=20, LineColor=ROOT.kRed,LineStyle=1,
                                    Legend="Test 2")


plots[0].addTurnOn(turnon)
plots[0].addTurnOn(turnon2)




canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()

