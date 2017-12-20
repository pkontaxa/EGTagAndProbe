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
plots[-1].xRange = (0,999.9)
#plots[-1].legendPosition = (0.6,0.2,0.9,0.4)
plots[-1].legendPosition = (0.6,0.2,0.9,0.4)


inputFile = ROOT.TFile.Open("./Run2017/fitOutput_1cut_check_barrel.root")

	
histo = inputFile.Get("histo_Stage2_vs_Pt_40GeV")
histo.__class__ = ROOT.RooHist
	
fit   = inputFile.Get("fit_Stage2_vs_Pt_40GeV")
fit.__class__ = ROOT.RooCurve

turnon = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo, Fit=fit,
                                    MarkerColor=ROOT.kGreen+2, MarkerStyle=22, LineColor=ROOT.kGreen+2,LineStyle=1,
                                    Legend="Barrel w/ Shape Id")


histo2 = inputFile.Get("histo_Stage2_vs_Pt_30GeV")
histo2.__class__ = ROOT.RooHist
	
fit2   = inputFile.Get("fit_Stage2_vs_Pt_30GeV")
fit2.__class__ = ROOT.RooCurve

turnon2 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo2, Fit=fit2,
                                    MarkerColor=ROOT.kRed+2, MarkerStyle=23, LineColor=ROOT.kRed+2,LineStyle=1,
                                    Legend="Barrel w/ FG Id")


histo3 = inputFile.Get("histo_Stage2_vs_Pt_20GeV")
histo3.__class__ = ROOT.RooHist

fit3   = inputFile.Get("fit_Stage2_vs_Pt_20GeV")
fit3.__class__ = ROOT.RooCurve

turnon3 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo3, Fit=fit3,
                                    MarkerColor=ROOT.kBlue, MarkerStyle=23, LineColor=ROOT.kBlue,LineStyle=1,
                                    Legend="Barrel w/ HoE Id")


histo4 = inputFile.Get("histo_Stage2_vs_Pt_10GeV")
histo4.__class__ = ROOT.RooHist

fit4   = inputFile.Get("fit_Stage2_vs_Pt_10GeV")
fit4.__class__ = ROOT.RooCurve

turnon4 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo4, Fit=fit4,
                                    MarkerColor=ROOT.kYellow+2, MarkerStyle=22, LineColor=ROOT.kYellow+2,LineStyle=1,
                                    Legend="Barrel Unpacked")


histo5 = inputFile.Get("histo_Stage2_vs_Pt_0GeV")
histo5.__class__ = ROOT.RooHist

fit5   = inputFile.Get("fit_Stage2_vs_Pt_0GeV")
fit5.__class__ = ROOT.RooCurve

turnon5 = TurnOnPlot.TurnOn(Name="Stage2", Histo=histo5, Fit=fit5,
                                    MarkerColor=ROOT.kBlack, MarkerStyle=22, LineColor=ROOT.kBlack,LineStyle=1,
                                    Legend="Barrel Ids Disabled")






plots[0].addTurnOn(turnon)
plots[0].addTurnOn(turnon2)
plots[0].addTurnOn(turnon3)
plots[0].addTurnOn(turnon4)
plots[0].addTurnOn(turnon5)


canvas = []
for plot in plots:
    canvas.append(plot.plot())

inputFile.Close()

