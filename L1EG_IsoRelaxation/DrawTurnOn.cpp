/*
g++ -Wall -o DrawTurnOn `root-config --cflags --glibs` -L $ROOTSYS/lib -lFoam -lMinuit -lMathMore CMS_lumi.C tdrstyle.C  DrawTurnOn.cpp
*/

#ifndef CMS_LUMI_H
#include "CMS_lumi.h"
#endif

#ifndef CMS_STYLE
#include "tdrstyle.h"
#endif

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <iostream>
#include <TLorentzVector.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TMath.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TROOT.h>
#include <TProfile.h>
#include <TLatex.h>
#include <sstream>
#include <TBranchElement.h>
#include <TGraphAsymmErrors.h>
#include <TEfficiency.h>
#include <fstream>
#include <iomanip>

//Pantelis
#include <string>


using namespace std;


void DrawSingleTurnOn(TEfficiency* inclusive, TEfficiency* EB, TEfficiency* EE, string title, bool useLeg2=0, bool integratedEfficiency=0)
{
  inclusive -> SetMarkerStyle(20);
  inclusive -> SetMarkerSize(1);
  inclusive -> SetMarkerColor(kBlack);
  //inclusive -> GetXaxis() -> SetRangeUser(5, 100);

  EB -> SetMarkerStyle(21);
  EB -> SetMarkerSize(1);
  EB -> SetMarkerColor(kRed + 1);

  EE -> SetMarkerStyle(22);
  EE -> SetMarkerSize(1);
  EE -> SetMarkerColor(kGreen + 2);


  TCanvas *c = new TCanvas();
  c -> cd();

  inclusive -> Draw("AP");
  EB -> Draw("P SAME");
  EE -> Draw("P SAME");

  TLegend *leg = new TLegend(0.6, 0.4, 0.9, 0.6);
  leg -> AddEntry(inclusive, "Inclusive", "p");
  leg -> AddEntry(EB, "EB", "p");
  leg -> AddEntry(EE, "EE", "p");

  TLegend *leg2 = new TLegend(0.75, 0.2, 0.95, 0.4);
  leg2 -> AddEntry(inclusive, "Inclusive", "p");
  leg2 -> AddEntry(EB, "EB", "p");
  leg2 -> AddEntry(EE, "EE", "p");

  if(useLeg2)
    leg2 -> Draw("SAME");
  else
    leg -> Draw("SAME");
  
  c->Update();
  inclusive->GetPaintedGraph()->GetYaxis()->SetRangeUser(0, 1.05);

  if(integratedEfficiency)
  {
     double eff = inclusive->GetCopyPassedHisto()->Integral()/inclusive->GetCopyTotalHisto()->Integral() ;
     stringstream ss;
     ss << std::setprecision(3) << eff*100 << "%" << endl;
     TString s = ss.str();
     TLatex* text = new TLatex(0.25,0.2, s);
     text->SetNDC();
     //text->Draw("SAME");
  }

  else
  {
    double pt95 = -1;
    double y = 0;
    for(int bin=1; bin<=18; bin++)
      {
	if(inclusive -> GetEfficiency(bin)>=0.95)
	  {
	    inclusive ->GetPaintedGraph() -> GetPoint(bin, pt95, y);
	    break;
	  }
      }

     stringstream ss;
     ss << std::setprecision(2)  << "P_{t 95%} = " << pt95 <<endl;
     TString s = ss.str();
     TLatex* text = new TLatex(0.2,0.85, s);
     text->SetNDC();
     text->Draw("SAME");
  }
  CMS_lumi(c, 0, 0);

  c -> SaveAs((title + ".png").c_str());
  c -> SaveAs((title + ".pdf").c_str());
}


void DrawEta(TEfficiency* inclusive, TString title)
{
  inclusive -> SetMarkerStyle(20);
  inclusive -> SetMarkerSize(1);
  inclusive -> SetMarkerColor(kBlue);
  //inclusive -> GetXaxis() -> SetRangeUser(5, 100);

  TCanvas *c = new TCanvas();
  c -> cd();

  inclusive -> Draw("AP");
  
  c->Update();
  inclusive->GetPaintedGraph()->GetYaxis()->SetRangeUser(0, 1.05);

  double eff = inclusive->GetCopyPassedHisto()->Integral()/inclusive->GetCopyTotalHisto()->Integral() ;
  stringstream ss;
  ss << std::setprecision(3) << eff*100 << "%" << endl;
  TString s = ss.str();
  TLatex* text = new TLatex(0.25,0.2, s);
  text->SetNDC();
  //text->Draw("SAME");

  CMS_lumi(c, 0, 0);

  c -> SaveAs(title + ".png");
  c -> SaveAs(title + ".pdf");
}


void DrawSingleRate(TH1F* t,  string title, TString title2)
{
  t -> SetLineWidth(2);
  t -> SetLineColor(kBlue);
  t -> GetXaxis() -> SetRangeUser(10, 40);

  TCanvas *c = new TCanvas();
  c -> cd();
  t -> GetXaxis() -> SetTitle("P_{T} (GeV)");
  t -> GetYaxis() -> SetTitle(title2);
  t -> GetYaxis() -> SetTitleOffset(1.5);

  t -> Draw("histo");

  CMS_lumi(c, 0, 0);
  //c -> SetLogy();
  c -> SaveAs((title + ".png").c_str());
  c -> SaveAs((title + ".pdf").c_str());
}

void DrawSingleRate2(TH1F* t, TH1F* t2, string title, TString title2)
{
  t -> SetLineWidth(2);
  t -> SetLineColor(kBlue);
  t -> GetXaxis() -> SetRangeUser(20, 40);
  t -> GetYaxis() -> SetRangeUser(0, 50);

  t2 -> SetLineWidth(2);
  t2 -> SetLineColor(kRed +1);
  t2 -> GetXaxis() -> SetRangeUser(20, 40);

  TCanvas *c = new TCanvas();
  c -> cd();
  t -> GetXaxis() -> SetTitle("P_{T} (GeV)");
  t -> GetYaxis() -> SetTitle(title2);
  t -> GetYaxis() -> SetTitleOffset(1.5);

  t -> Draw("histo");
  t2 -> Draw("SAME histo");

  TLegend *leg2 = new TLegend(0.55, 0.7, 0.95, 0.85);
  leg2 -> AddEntry(t, "Isolated Rate", "l");
  leg2 -> AddEntry(t2, "Pure NoIso Rate", "l");
  leg2 -> Draw("SAME");

  CMS_lumi(c, 0, 0);
  //c -> SetLogy();
  c -> SaveAs((title + ".png").c_str());
  c -> SaveAs((title + ".pdf").c_str());
}


void Draw5TurnOn(TEfficiency* t1, TEfficiency* t2, TEfficiency* t3, TEfficiency* t4, TEfficiency* t5, string title, bool useLeg2)
{
  t1 -> SetMarkerStyle(20);
  t1 -> SetMarkerSize(1);
  t1 -> SetMarkerColor(kBlack);

  t2 -> SetMarkerStyle(21);
  t2 -> SetMarkerSize(1);
  t2 -> SetMarkerColor(kAzure);

  t3 -> SetMarkerStyle(22);
  t3 -> SetMarkerSize(1);
  t3 -> SetMarkerColor(kRed +1);

  t4 -> SetMarkerStyle(23);
  t4 -> SetMarkerSize(1);
  t4 -> SetMarkerColor(kGreen +2);

  t5 -> SetMarkerStyle(34);
  t5 -> SetMarkerSize(1);
  t5 -> SetMarkerColor(kOrange -3);

  TCanvas *c = new TCanvas();
  c -> cd();

  t1 -> Draw("AP");
  t2 -> Draw("P SAME");
  t3 -> Draw("P SAME");
  t4 -> Draw("P SAME");
  t5 -> Draw("P SAME");


  TLegend *leg = new TLegend(0.6, 0.4, 0.9, 0.65);
  leg -> AddEntry(t1, "Isolation 2016", "p");
  leg -> AddEntry(t2, "New WP", "p");
  leg -> AddEntry(t3, "New WP for cross triggers", "p");
  leg -> AddEntry(t4, "Thight WP", "p");
  leg -> AddEntry(t5, "Hybrid WP", "p");



  TLegend *leg2 = new TLegend(0.6, 0.4, 0.9, 0.65);
  leg2 -> AddEntry(t1, "Isolation 2016", "p");
  leg2 -> AddEntry(t2, "Option 7", "p");
  leg2 -> AddEntry(t3, "Option 9", "p");
  leg2 -> AddEntry(t4, "Option 14", "p");
  leg2 -> AddEntry(t5, "Option 16", "p");



  if(useLeg2)
    leg2 -> Draw("SAME");
  else
    leg -> Draw("SAME");

  c->Update();
  t1->GetPaintedGraph()->GetYaxis()->SetRangeUser(0, 1.05);

  CMS_lumi(c, 0, 0);
  c -> SaveAs((title + ".png").c_str());
  c -> SaveAs((title + ".pdf").c_str());
}



void Draw5TurnOnZoom(TEfficiency* t1, TEfficiency* t2, TEfficiency* t3, TEfficiency* t4, TEfficiency* t5, string title, bool useLeg2)
{
  t1 -> SetMarkerStyle(20);
  t1 -> SetMarkerSize(1);
  t1 -> SetMarkerColor(kBlack);

  t2 -> SetMarkerStyle(21);
  t2 -> SetMarkerSize(1);
  t2 -> SetMarkerColor(kAzure);

  t3 -> SetMarkerStyle(22);
  t3 -> SetMarkerSize(1);
  t3 -> SetMarkerColor(kRed +1);

  t4 -> SetMarkerStyle(23);
  t4 -> SetMarkerSize(1);
  t4 -> SetMarkerColor(kGreen +2);

  t5 -> SetMarkerStyle(34);
  t5 -> SetMarkerSize(1);
  t5 -> SetMarkerColor(kOrange -3);

  TCanvas *c = new TCanvas();
  c -> cd();

  t1 -> Draw("AP");
  t2 -> Draw("P SAME");
  t3 -> Draw("P SAME");
  t4 -> Draw("P SAME");
  t5 -> Draw("P SAME");


  c->Update();
  t1->GetPaintedGraph()->GetXaxis()->SetRangeUser(20, 50);

  TLegend *leg = new TLegend(0.2, 0.6, 0.4, 0.8);
  leg -> AddEntry(t1, "Isolation 2016", "p");
  leg -> AddEntry(t2, "Option 7", "p");
  leg -> AddEntry(t3, "Option 9", "p");
  leg -> AddEntry(t4, "Option 14", "p");
  leg -> AddEntry(t5, "Option 16", "p");


  TLegend *leg2 = new TLegend(0.2, 0.6, 0.4, 0.8, "EE");
  leg2 -> AddEntry(t1, "Isolation 2016", "p");
  leg2 -> AddEntry(t2, "Option 7", "p");
  leg2 -> AddEntry(t3, "Option 9", "p");
  leg2 -> AddEntry(t4, "Option 14", "p");
  leg2 -> AddEntry(t5, "Option 16", "p");


  if(useLeg2)
    leg2 -> Draw("SAME");
  else
    leg -> Draw("SAME");

  CMS_lumi(c, 0, 0);
  c -> SaveAs((title + "Zoom.png").c_str());
  c -> SaveAs((title + "Zoom.pdf").c_str());
}




void Draw5Rate(TH1F* t1, TH1F* t2, TH1F* t3, TH1F* t4, TH1F* t5, string title, bool useLeg2)
{

  t1 -> SetMarkerStyle(20);
  t1 -> SetMarkerSize(1);
  t1 -> SetMarkerColor(kBlack);

  t2 -> SetMarkerStyle(21);
  t2 -> SetMarkerSize(1);
  t2 -> SetMarkerColor(kAzure);

  t3 -> SetMarkerStyle(22);
  t3 -> SetMarkerSize(1);
  t3 -> SetMarkerColor(kRed +1);

  t4 -> SetMarkerStyle(23);
  t4 -> SetMarkerSize(1);
  t4 -> SetMarkerColor(kGreen +2);

  t5 -> SetMarkerStyle(34);
  t5 -> SetMarkerSize(1);
  t5 -> SetMarkerColor(kOrange -3);


  TCanvas *c = new TCanvas();
  c -> cd();

  t1 -> GetXaxis() -> SetTitle("P_{T} (GeV)");
  t1 -> GetYaxis() -> SetTitle("Rate (kHz)");
  t1 -> GetYaxis() -> SetTitleOffset(1.5);
  t1 -> GetYaxis() -> SetRangeUser(0, 50);
  t1 -> GetXaxis() -> SetRangeUser(20, 40);

  t1 -> Draw("P");
  t2 -> Draw("P SAME");
  t3 -> Draw("P SAME");
  t4 -> Draw("P SAME");
  t5 -> Draw("P SAME");

  c->Update();

  TLine *l = new TLine(c->GetUxmin(), 17, c->GetUxmax(), 17);
  l -> SetLineWidth(4);
  l -> SetLineStyle(5);
  l -> SetLineColor(kViolet);
  l -> Draw("SAME");

  TLegend *leg = new TLegend(0.7, 0.7, 0.9, 0.9);
  leg -> AddEntry(l, "17 KHz", "l");
  leg -> AddEntry(t1, "NoIso", "l");  
  leg -> AddEntry(t2, "2016", "p");
  leg -> AddEntry(t3, "Option 1", "p");
  leg -> AddEntry(t4, "Option 11", "p");
  leg -> AddEntry(t5, "Option 16", "p");


  TLegend *leg2 = new TLegend(0.7, 0.7, 0.9, 0.9);
  leg2 -> AddEntry(l, "17 KHz", "l");
  leg2 -> AddEntry(t1, "NoIso", "p");
  leg2 -> AddEntry(t2, "2016", "p");
  leg2 -> AddEntry(t3, "Option 4", "p");
  leg2 -> AddEntry(t4, "Option 5", "p");
  leg2 -> AddEntry(t5, "Option 12", "p");

  if(useLeg2)
    leg2 -> Draw("SAME");
  else
    leg -> Draw("SAME");


  CMS_lumi(c, 0, 0);
  //c -> SetLogy();
  c -> SaveAs((title + ".png").c_str());
  c -> SaveAs((title + ".pdf").c_str());
}








int main()
{

  writeExtraText = true;       // if extra text
  extraText  = "Preliminary";  // default extra text is "Preliminary"
  lumi_sqrtS = "221 pb^{-1} (13 TeV)";       // used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

  gStyle -> SetOptStat(0);
  setTDRStyle();


  TFile *f = new TFile("TurnOns.root");
  TEfficiency *inclusive[23];
  TEfficiency *EB[23];
  TEfficiency *EE[23];
  TEfficiency *inclusiveVtx[23];
  TEfficiency *EBVtx[23];
  TEfficiency *EEVtx[23];
  TEfficiency *inclusivenTT[23];
  TEfficiency *EBnTT[23];
  TEfficiency *EEnTT[23];
  TEfficiency *inclusiveEta[23];
  TEfficiency *inclusiveiEta[23];

  inclusive[0] = (TEfficiency*) f -> Get("inclusive_NoCut");
  EB[0] = (TEfficiency*) f -> Get("EB_NoCut");
  EE[0] = (TEfficiency*) f -> Get("EE_NoCut");

  for(int i=1; i<22; i++)
  {
    inclusive[i] = (TEfficiency*) f -> Get(("inclusive" + to_string(i)).c_str());
    EB[i] = (TEfficiency*) f -> Get(("EB" + to_string(i)).c_str());
    EE[i] = (TEfficiency*) f -> Get(("EE" + to_string(i)).c_str());
  }

  inclusive[22] = (TEfficiency*) f -> Get("inclusive_2016");
  EB[22] = (TEfficiency*) f -> Get("EB_2016");
  EE[22] = (TEfficiency*) f -> Get("EE_2016");

  inclusiveVtx[0] = (TEfficiency*) f -> Get("inclusiveVtx_NoCut");
  EBVtx[0] = (TEfficiency*) f -> Get("EBVtx_NoCut");
  EEVtx[0] = (TEfficiency*) f -> Get("EEVtx_NoCut");

  for(int i=1; i<22; i++)
  {
    inclusiveVtx[i] = (TEfficiency*) f -> Get(("inclusiveVtx" + to_string(i)).c_str());
    EBVtx[i] = (TEfficiency*) f -> Get(("EBVtx" + to_string(i)).c_str());
    EEVtx[i] = (TEfficiency*) f -> Get(("EEVtx" + to_string(i)).c_str());
  }

  inclusiveVtx[22] = (TEfficiency*) f -> Get("inclusiveVtx_2016");
  EBVtx[22] = (TEfficiency*) f -> Get("EBVtx_2016");
  EEVtx[22] = (TEfficiency*) f -> Get("EEVtx_2016");

  inclusivenTT[0] = (TEfficiency*) f -> Get("inclusivenTT_NoCut");
  EBnTT[0] = (TEfficiency*) f -> Get("EBnTT_NoCut");
  EEnTT[0] = (TEfficiency*) f -> Get("EEnTT_NoCut");

  for(int i=1; i<22; i++)
  {
    inclusivenTT[i] = (TEfficiency*) f -> Get(("inclusivenTT" + to_string(i)).c_str());
    EBnTT[i] = (TEfficiency*) f -> Get(("EBnTT" + to_string(i)).c_str());
    EEnTT[i] = (TEfficiency*) f -> Get(("EEnTT" + to_string(i)).c_str());
  }

  inclusivenTT[22] = (TEfficiency*) f -> Get("inclusivenTT_2016");
  EBnTT[22] = (TEfficiency*) f -> Get("EBnTT_2016");
  EEnTT[22] = (TEfficiency*) f -> Get("EEnTT_2016");



  inclusiveEta[0] = (TEfficiency*) f -> Get("inclusiveEta_NoCut");

  for(int i=1; i<22; i++)
    inclusiveEta[i] = (TEfficiency*) f -> Get(("inclusiveEta" + to_string(i)).c_str());
 
  inclusiveEta[22] = (TEfficiency*) f -> Get("inclusiveEta_2016");

  inclusiveiEta[0] = (TEfficiency*) f -> Get("inclusiveiEta_NoCut");

  for(int i=1; i<22; i++)
    inclusiveiEta[i] = (TEfficiency*) f -> Get(("inclusiveiEta" + to_string(i)).c_str());
 
  inclusiveiEta[22] = (TEfficiency*) f -> Get("inclusiveiEta_2016");


  TFile *f2 = new TFile("histos_rate_2017_ShapeVeto.root");
  TH1F *Rate[23];
  TH1F *Pt[23];
  TH1F* PureRate[23];

  Rate[0] = (TH1F*)f2 -> Get("rate_Progression_NoCut");
  Pt[0] = (TH1F*)f2 -> Get("pt_Progression_NoCut");

  for(int i=1; i<22; i++)
  {
    Rate[i] = (TH1F*)f2 -> Get(("rate_Progression_" + to_string(i)).c_str());
    Pt[i] = (TH1F*)f2 -> Get(("pt_Progression_" + to_string(i)).c_str());
    PureRate[i] = (TH1F*)f2 -> Get(("pureRate_Progression" + to_string(i)).c_str());
  }

  Rate[22] = (TH1F*)f2 -> Get("rate_Progression_2016");
  Pt[22] = (TH1F*)f2 -> Get("pt_Progression_2016");
  PureRate[22] = (TH1F*)f2 -> Get("pureRate_Progression_2016");

  system("mkdir TurnOnPlots");
  


  for(int i=0; i<23; i++)
  {
    if(i==0)
      {  DrawSingleTurnOn(inclusive[i], EB[i], EE[i], "NoCut_TurnOn", 0);
	 DrawSingleTurnOn(inclusiveVtx[i], EBVtx[i], EEVtx[i], "NoCut_Vtx", 1, 1);
	 DrawSingleTurnOn(inclusivenTT[i], EBnTT[i], EEnTT[i], "NoCut_nTT", 1, 1);
         DrawEta(inclusiveEta[i], "NoCut_Eta");
         DrawEta(inclusiveiEta[i], "NoCut_iEta");
         DrawSingleRate(Rate[i], "NoCut_Rate", "Rate (kHz)");
         DrawSingleRate(Pt[i],"NoCut_Pt", "Counts");
    }

    else 
    {  if(i<22)
      {  DrawSingleTurnOn(inclusive[i], EB[i], EE[i], ( to_string(i) + "_TurnOn").c_str());
	 DrawSingleTurnOn(inclusiveVtx[i], EBVtx[i], EEVtx[i], (to_string(i) + "_Vtx").c_str(), 1, 1);
         DrawSingleTurnOn(inclusivenTT[i], EBnTT[i], EEnTT[i], (to_string(i) + "_nTT").c_str(), 1, 1);
         DrawEta(inclusiveEta[i], (to_string(i) + "_Eta").c_str());
         DrawEta(inclusiveiEta[i], (to_string(i) + "_iEta").c_str());
	 DrawSingleRate2(Rate[i],PureRate[i],(to_string(i) + "_Rate").c_str(), "Rate (kHz)");
         DrawSingleRate(Pt[i],(to_string(i) + "_Pt").c_str(), "Counts");
      }
      else
      {  DrawSingleTurnOn(inclusive[i], EB[i], EE[i], "2016_TurnOn");
	 DrawSingleTurnOn(inclusiveVtx[i], EBVtx[i], EEVtx[i], "2016_Vtx", 1, 1);
	 DrawSingleTurnOn(inclusivenTT[i], EBnTT[i], EEnTT[i], "2016_nTT", 1, 1);
         DrawEta(inclusiveEta[i], "2016_Eta");
         DrawEta(inclusiveiEta[i], "2016_iEta");
	 DrawSingleRate2(Rate[i], PureRate[i], "2016_Rate", "Rate (kHz)");
	 DrawSingleRate(Pt[i], "2016_Pt", "Counts");
      }
    }
  }


  Draw5TurnOnZoom((TEfficiency*)inclusive[0]->Clone(), inclusive[22], inclusive[1], inclusive[11], inclusive[16], "Options_TurnOn", 0);
  Draw5TurnOn(inclusiveVtx[0], inclusiveVtx[22], inclusiveVtx[1], inclusiveVtx[11], inclusiveVtx[16], "Optinos_Vtx", 0); 
  Draw5TurnOn(inclusiveEta[0], inclusiveEta[22], inclusiveEta[1], inclusiveEta[11], inclusiveEta[16], "Options_Eta", 0); 
  Draw5Rate(Rate[0], (TH1F*)Rate[22]->Clone(), Rate[1], Rate[11], Rate[16], "Options_Rate", 0);
  Draw5TurnOn(inclusive[0], inclusive[22], inclusive[4], inclusive[5], inclusive[12], "Options2_TurnOn", 0); 
  Draw5TurnOnZoom(inclusive[0], inclusive[22], inclusive[4], inclusive[5], inclusive[12], "Options2_TurnOn", 0); 
  Draw5TurnOn(inclusiveVtx[22], inclusiveVtx[7], inclusiveVtx[9], inclusiveVtx[14], inclusiveVtx[16], "Options2_Vtx", 0); 
  Draw5TurnOn(inclusiveEta[22], inclusiveEta[7], inclusiveEta[9], inclusiveEta[14], inclusiveEta[16], "Options2_Eta", 0); 
  Draw5Rate(Rate[0], (TH1F*)Rate[22]->Clone(), Rate[4], Rate[5], Rate[12], "Options2_Rate", 1);


  Draw5TurnOn(EB[22], EB[14], EB[15], EB[16], EB[21], "OptionsEB", 0); 
  Draw5TurnOn(EE[22], EE[14], EE[15], EE[16], EE[21], "OptionsEE", 0); 



  system("mv *.pdf ./TurnOnPlots");
  system("mv *.png ./TurnOnPlots");
}
