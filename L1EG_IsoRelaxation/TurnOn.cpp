/*
g++ -Wall -o TurnOn `root-config --cflags --glibs` -L $ROOTSYS/lib -lFoam -lMinuit -lMathMore CMS_lumi.C tdrstyle.C  TurnOn.cpp
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
#include <sstream>
#include <TBranchElement.h>
#include <TGraphAsymmErrors.h>
#include <TEfficiency.h>
#include <fstream>


using namespace std;

//Parameters for compression
const Int_t compressionnTT[33] = {0,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96,101,106,111,116,121,126,131,136,141,146,151,156,256};


const Int_t NbinsIEta = 16;
const Int_t NbinsIEt = 16;
const Int_t NbinsnTT = 32;//Acceptable LUT Thomas

 Int_t CompressnTT(Int_t val, const Int_t* compression, int length)
  { Int_t compressedVal = -1;
    for(int i=0; i<length; i++)
      {  if(compression[i]<=val && compression[i+1]>val)
	  { compressedVal = i;
	    break;
	  }
      }
  //      std::cout << "Val = " << val << " CompressedVal = " << compressedVal << std::endl; 

    if(compressedVal==-1) compressedVal = length-1;
    return compressedVal;
}



double Slope(double *Et, double* par)
{
  double Efficiency = 0.;
  double minPt = par[0];
  double minEff = par[1];
  double maxPt = par[2];

  if(Et[0]>=maxPt) Efficiency = 1.;
  else if(Et[0]<minPt) Efficiency = minEff;
  else
    {
      Double_t Slope = (1.-minEff)/(maxPt);
      Efficiency = Slope*Et[0] + (1. - Slope*maxPt);
    }

  if(Efficiency<0) Efficiency = 0.;
  if(Efficiency>=1) Efficiency = 1.;

  return Efficiency ;
}




int main()
{
  //
  writeExtraText = true;       // if extra text
  extraText  = "Preliminary Simulation";  // default extra text is "Preliminary"
  lumi_sqrtS = "";       // used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
  
  gStyle -> SetOptStat(0);
  setTDRStyle();
    
  TFile *f = new TFile("Iso_LUTs_Relaxed.root");
  TFile *f2 = new TFile("Hybrid.root");
  
  TH3F* LUT[22];
  for(int i=1; i<21; i++)
    LUT[i] = (TH3F*)f->Get(("LUT_Progression_" + to_string(i)).c_str());
  
  LUT[21] = (TH3F*)f2->Get("HybridLUT");
  LUT[22] = (TH3F*)f->Get("LUT_Progression_2016");
  
  //TFile *thr = new TFile("Thresholds.root");
  //TGraph *th = (TGraph*)thr->Get("thresholds");
  
  TFile *tree = new TFile("IsoTreeOut.root");
  TTree *events = (TTree*)tree->Get("TagAndProbe");
  
  double CalibratedE      = -99;
  int nTT      = -99;
  int iso      = -99;
  double OfflineEt = -99.;
  double OfflineEta = -99.;
  int compressedE      = -99;
  int compressedEta     = -99;
  int Run2EleId = -99;
  int passShapeVeto = -99;
  int RawEt = -99;
  int iEta = -99;
  float nVtx = -99;

  events -> SetBranchAddress("CalibratedE", &CalibratedE);
  events -> SetBranchAddress("nTT", &nTT);
  events -> SetBranchAddress("iso", &iso);
  events -> SetBranchAddress("offlineEt",&OfflineEt);
  events -> SetBranchAddress("offlineEta",&OfflineEta);
  events -> SetBranchAddress("compressedE", &compressedE);
  events -> SetBranchAddress("compressedieta", &compressedEta);
  events -> SetBranchAddress("Run2EleId", &Run2EleId);
  events -> SetBranchAddress("passShapeVeto", &passShapeVeto);
  events -> SetBranchAddress("RawEt", &RawEt);
  events -> SetBranchAddress("iEta", &iEta);
  events -> SetBranchAddress("nVtx", &nVtx);
  double ptThreshold = -1;
  double ptThreshold2 = 25;
  //double fake = -1;

  TEfficiency *inclusive[23];
  TEfficiency *EB[23];
  TEfficiency *EE[23];
  
  const double binning[19] = {5., 20., 22., 24., 26., 28., 30., 32.5, 35., 37.5, 40., 42.5, 45., 47.5, 50., 55., 60., 80., 100.};

  inclusive[0] = new TEfficiency("inclusive_NoCut", "; OfflineEt (GeV); #varepsilon", 18, binning);
  EB[0] = new TEfficiency("EB_NoCut", "; OfflineEt (GeV); #varepsilon", 18, binning);
  EE[0] = new TEfficiency("EE_NoCut", "; OfflineEt (GeV); #varepsilon", 18, binning);

  for(int i=1; i<22; i++)
  {
    inclusive[i] = new TEfficiency(("inclusive"+to_string(i)).c_str(), "; OfflineEt (GeV); #varepsilon", 18, binning);
    EB[i] = new TEfficiency(("EB"+to_string(i)).c_str(), "; OfflineEt (GeV); #varepsilon", 18, binning);
    EE[i] = new TEfficiency(("EE"+to_string(i)).c_str(), "; OfflineEt (GeV); #varepsilon", 18, binning);
 
  }

  inclusive[22] = new TEfficiency("inclusive_2016", "; OfflineEt (GeV); #varepsilon", 18, binning);
  EB[22] = new TEfficiency("EB_2016", "; OfflineEt (GeV); #varepsilon", 18, binning);
  EE[22] = new TEfficiency("EE_2016", "; OfflineEt (GeV); #varepsilon", 18, binning);



  TEfficiency *inclusiveVtx[23];
  TEfficiency *EBVtx[23];
  TEfficiency *EEVtx[23];
  
  const double binningVtx[13] = {10, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 50, 100.};
  inclusiveVtx[0] = new TEfficiency("inclusiveVtx_NoCut", "; n_{vtx}; #varepsilon", 12, binningVtx);
  EBVtx[0] = new TEfficiency("EBVtx_NoCut", "; n_{vtx}; #varepsilon", 12, binningVtx);
  EEVtx[0] = new TEfficiency("EEVtx_NoCut", "; n_{vtx}; #varepsilon", 12, binningVtx);

  for(int i=1; i<22; i++)
  {
    inclusiveVtx[i] = new TEfficiency(("inclusiveVtx"+to_string(i)).c_str(), "; n_{vtx}; #varepsilon", 12, binningVtx);
    EBVtx[i] = new TEfficiency(("EBVtx"+to_string(i)).c_str(), "; n_{vtx}; #varepsilon", 12, binningVtx);
    EEVtx[i] = new TEfficiency(("EEVtx"+to_string(i)).c_str(), "; n_{vtx} #varepsilon", 12, binningVtx);
 
  }

  inclusiveVtx[22] = new TEfficiency("inclusiveVtx_2016", "; n_{vtx}; #varepsilon", 12, binningVtx);
  EBVtx[22] = new TEfficiency("EBVtx_2016", "; n_{vtx}; #varepsilon", 12, binningVtx);
  EEVtx[22] = new TEfficiency("EEVtx_2016", "; n_{vtx}; #varepsilon", 12, binningVtx);


  TEfficiency *inclusivenTT[23];
  TEfficiency *EBnTT[23];
  TEfficiency *EEnTT[23];
  
  const double binningnTT[13] = {20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 100, 255.};
  inclusivenTT[0] = new TEfficiency("inclusivenTT_NoCut", "; nTT; #varepsilon", 12, binningnTT);
  EBnTT[0] = new TEfficiency("EBnTT_NoCut", "; nTT; #varepsilon", 12, binningnTT);
  EEnTT[0] = new TEfficiency("EEnTT_NoCut", "; nTT; #varepsilon", 12, binningnTT);

  for(int i=1; i<22; i++)
  {
    inclusivenTT[i] = new TEfficiency(("inclusivenTT"+to_string(i)).c_str(), "; nTT; #varepsilon", 12, binningnTT);
    EBnTT[i] = new TEfficiency(("EBnTT"+to_string(i)).c_str(), "; nTT; #varepsilon", 12, binningnTT);
    EEnTT[i] = new TEfficiency(("EEnTT"+to_string(i)).c_str(), "; nTT; #varepsilon", 12, binningnTT);
 
  }

  inclusivenTT[22] = new TEfficiency("inclusivenTT_2016", "; nTT; #varepsilon", 12, binningnTT);
  EBnTT[22] = new TEfficiency("EBnTT_2016", "; nTT; #varepsilon", 12, binningnTT);
  EEnTT[22] = new TEfficiency("EEnTT_2016", "; nTT; #varepsilon", 12, binningnTT);


  TEfficiency *inclusiveiEta[23];
  
  inclusiveiEta[0] = new TEfficiency("inclusiveiEta_NoCut", "; iEta; #varepsilon", 64, -33.1, 32.9);
  for(int i=1; i<22; i++)
    inclusiveiEta[i] = new TEfficiency(("inclusiveiEta"+to_string(i)).c_str(), "; iEta; #varepsilon",  64, -33.1, 32.9);
  inclusiveiEta[22] = new TEfficiency("inclusiveiEta_2016", "; iEta; #varepsilon",  64, -33.1, 32.9);


  TEfficiency *inclusiveEta[23];

  inclusiveEta[0] = new TEfficiency("inclusiveEta_NoCut", "; #eta; #varepsilon", 50, -2.5, 2.5);
  for(int i=1; i<22; i++)
    inclusiveEta[i] = new TEfficiency(("inclusiveEta"+to_string(i)).c_str(), "; #eta; #varepsilon", 50, -2.5, 2.5);
  inclusiveEta[22] = new TEfficiency("inclusiveEta_2016", "; #eta; #varepsilon", 50, -2.5, 2.5);



  int fail[23] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  int pass[23] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    for(int ev=0; ev<events->GetEntries(); ev++)
    {
      if(ev%10000==0) cout << "Processing " << ev << "th event out of " << events->GetEntries() << endl;
      
      events -> GetEntry(ev);
      int compressednTT = CompressnTT(nTT, compressionnTT, NbinsnTT);
      
      std::cout << "compressednTT = "<<compressednTT<<std::endl;
      
      if(compressednTT>NbinsnTT || compressedE>NbinsIEt || abs(compressedEta)>NbinsIEta) continue;
      
      std::cout << "Passed 1"<<std::endl;
      
      for(int i=0; i<23; i++)
        {	    
	  ptThreshold = 35;
	  // th -> GetPoint(i, fake, ptThreshold);
	  bool passPt = 1;
	  bool passIso = 1;

	  if( (CalibratedE)<ptThreshold) passPt = 0;
	  if(i==0)
	  {  inclusive[0] -> Fill(passPt, OfflineEt);
	     if(OfflineEt > ptThreshold2)
	     {  inclusiveEta[0] -> Fill(passPt, OfflineEta );
	        inclusiveVtx[0] -> Fill(passPt, nVtx );
		inclusivenTT[0] -> Fill(passPt, nTT);
		inclusiveiEta[0] -> Fill(passPt, iEta);
	     }
	  }
	  else
	  {
	    int isoCut = LUT[i] -> GetBinContent(abs(compressedEta)+1, compressedE+1, compressednTT+1);
	    if(iso>isoCut) passIso=0;
	    if(iso>isoCut) fail[i]++;
	    else pass[i] ++;
	    //cout << iso << " " << isoCut << " " << OfflineEt << " " << CalibratedE << " " << RawEt << " " << compressedE << " " << i << endl;
	    inclusive[i] -> Fill(passPt && passIso, OfflineEt);
	    if(OfflineEt > ptThreshold2)
	    {  inclusiveEta[i] -> Fill(passPt && passIso, OfflineEta);
	       inclusiveVtx[i] -> Fill(passPt && passIso, nVtx);
	       inclusivenTT[i] -> Fill(passPt && passIso, nTT);
	       inclusiveiEta[i] -> Fill(passPt && passIso, iEta);
	    }
	  }
	   
	  if(abs(OfflineEta)<1.4442)
	  {
	    if(i==0)
	    {   EB[0] -> Fill(passPt, OfflineEt);
	        if(OfflineEt > ptThreshold2)
		{  EBVtx[0] -> Fill(passPt, nVtx);
		   EBnTT[0] -> Fill(passPt, nTT);
		}
	    }
	    else
	      {  
		passIso = 1;
		int isoCut = LUT[i] -> GetBinContent(abs(compressedEta)+1, compressedE+1, compressednTT+1);
		if(iso>isoCut) passIso=0;
		EB[i] -> Fill(passPt && passIso, OfflineEt);
		if(OfflineEt > ptThreshold2)
		{  EBVtx[i] -> Fill(passPt && passIso, nVtx);
		   EBnTT[i] -> Fill(passPt && passIso, nTT);
		}
	      }
	  }

	  else if(abs(OfflineEta)>1.556)
	  {
	    if(i==0)
	    { EE[0] -> Fill(passPt, OfflineEt);
	      if(OfflineEt > ptThreshold2)
	      {  EEVtx[0] -> Fill(passPt, nVtx);
		 EEnTT[0] -> Fill(passPt, nTT);
	      }
	    }
	    else
	      {
		passIso = 1;
		int isoCut = LUT[i] -> GetBinContent(abs(compressedEta)+1, compressedE+1, compressednTT+1);
		if(iso>isoCut) passIso=0;
		EE[i] -> Fill(passPt && passIso, OfflineEt);
		if(OfflineEt>ptThreshold2)
		{  EEVtx[i] -> Fill(passPt && passIso, nVtx);
		   EEnTT[i] -> Fill(passPt && passIso, nTT);
	        }
	      }
	  }
	}
   }

    TFile *outfile = new TFile("TurnOns.root", "recreate");
    for(int i=0; i<23; i++)
      {  inclusive[i] -> Write();
         EB[i] -> Write();
	 EE[i] -> Write();
	 inclusiveVtx[i] -> Write();
	 EBVtx[i] -> Write();
	 EEVtx[i] -> Write();
	 inclusivenTT[i] -> Write();
	 EBnTT[i] -> Write();
	 EEnTT[i] -> Write();
	 inclusiveEta[i] -> Write();
	 inclusiveiEta[i] -> Write();
      }
    outfile -> Close();
    
    //return 1;
}
