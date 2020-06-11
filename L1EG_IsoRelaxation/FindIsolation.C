#define FindIsolation_cxx
#include "FindIsolation.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

// Compression parameters
const Int_t compressionnTT[33] = {0,6,11,16,21,26,31,36,41,46,51,56,61,66,71,76,81,86,91,96,101,106,111,116,121,126,131,136,141,146,151,156,256};
const Int_t compressionEta[17] = {0, 5, 6, 9 , 10, 12, 13, 14, 17, 18, 19, 20, 23, 24, 25, 26, 32};
const Int_t compressionE[17]   = {0, 18, 20, 22, 28, 32, 37, 42, 52, 63, 73, 81, 87, 91, 111, 151, 255};

const Int_t supercompressionnTT[9] = {0,16,26,31,36,41,51,61, 256};
const Int_t supercompressionEta[5] = {0, 3, 7, 12, 16};
const Int_t supercompressionE[6]   = {0, 8, 9, 11, 13, 16};

const Int_t NbinsIEta = 4+1;
const Int_t NbinsIEt  = 5+1;
const Int_t NbinsnTT  = 8+1;

const Int_t NbinsIEt2  = 16+1;
const Int_t NbinsIEta2 = 16+1;
const Int_t NbinsnTT2  = 32+1;

void FindIsolation::Loop()
{
//   In a ROOT session, you can do:
//      root> .L FindIsolation.C
//      root> FindIsolation t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   
   std::cout << "Number of entries = "<<nentries<<std::endl;
   
   std::map<TString,TH1F*> Histos_PerBin;
   for(UInt_t i = 0 ; i < NbinsIEta-1 ; ++i)
     {
       for(UInt_t j = 0 ; j < NbinsIEt-1 ; ++j)
	 {
	   for(UInt_t k = 0 ; k < NbinsnTT-1 ; ++k)
	     {
	       TString Name_Histo = "Hist_";
	       
	       stringstream ss_i;
	       ss_i << i;
	       TString Appendix_i = TString(ss_i.str());
	       Name_Histo += Appendix_i;
	       Name_Histo += "_";
	       
	       stringstream ss_j;
	       ss_j << j;
	       TString Appendix_j = TString(ss_j.str());
	       Name_Histo += Appendix_j;
	       Name_Histo += "_";
	       
	       stringstream ss_k;
	       ss_k << k;
	       TString Appendix_k = TString(ss_k.str());
	       Name_Histo += Appendix_k;
	       
	       TH1F* temp_histo = new TH1F(Name_Histo.Data(),Name_Histo.Data(),100,0.,100.);
	       Histos_PerBin.insert(make_pair(Name_Histo,temp_histo));
	     }
	 }
     }
   
   std::map<Int_t,TH3F*>   IsoCut_PerBin;   
   std::map<Int_t, std::map<TString,Int_t> > IsoCut_PerEfficiency_PerBin;
   
   TProfile* hprof_IEt  = new TProfile("hprof_IEt",  "Profile L1_Iso vs. L1_IEt", 100, 0.0, 200.0, 0,20);
   TProfile* hprof_IEta = new TProfile("hprof_IEta", "Profile L1_Iso vs. L1_IEta", 28, 0.0, 28.0, 0,20);
   TProfile* hprof_nTT  = new TProfile("hprof_nTT",  "Profile L1_Iso vs. L1_IEta", 70, 0.0, 70.0, 0,20);
   
   int compressedE        = -99;
   int compressedEta      = -99;
   int supercompressednTT = -99;
   int supercompressedEta = -99;
   int supercompressedE   = -99;
   
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++)
     {
       Long64_t ientry = LoadTree(jentry);
       if (ientry < 0) break;
       
       nb = fChain->GetEntry(jentry);   nbytes += nb;
       
       compressedEta      = abs(compressedieta);
       supercompressednTT = Supercompress((int)nTT, supercompressionnTT, NbinsnTT-1);
       supercompressedEta = Supercompress((int)compressedieta, supercompressionEta, NbinsIEta-1);
       supercompressedE   = Supercompress((int)compressedE, supercompressionE, NbinsIEt-1);
       
       std::cout << "entry = "<<ientry<<"  compressedEta = "<<compressedEta<<"  supercompressednTT="<<supercompressednTT<<"   supercompressedEta="<<supercompressedEta<< "  supercompressedE="<<supercompressedE<<std::endl;
       
       hprof_IEt  -> Fill(RawEt, iso, 1);
       hprof_IEta -> Fill(iEta,  iso, 1);
       hprof_nTT  -> Fill(nTT,   iso, 1);
       
       std::vector<Int_t> binForIsolation;
       binForIsolation.clear();
       binForIsolation.push_back(supercompressedEta);
       binForIsolation.push_back(supercompressedE);
       binForIsolation.push_back(supercompressednTT);
       
       TString Name_Histo = "Hist_";

       stringstream ss_i;
       ss_i << binForIsolation.at(0);
       TString Appendix_i = TString(ss_i.str());
       Name_Histo += Appendix_i;
       Name_Histo += "_";

       stringstream ss_j;
       ss_j << binForIsolation.at(1);
       TString Appendix_j = TString(ss_j.str());
       Name_Histo += Appendix_j;
       Name_Histo += "_";

       stringstream ss_k;
       ss_k << binForIsolation.at(2);
       TString Appendix_k = TString(ss_k.str());
       Name_Histo += Appendix_k;
       
       Histos_PerBin[Name_Histo] -> Fill(iso);
     
     } // Loop over entries
   
   // Save profile histograms
   TFile f_out("Iso_LUTs_WP.root","RECREATE");
   
   hprof_IEt  ->Write();
   hprof_IEta ->Write();
   hprof_nTT  ->Write();
   
   Int_t NumberOfHistosWithLowStats = 0;
   
   for (UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       std::map<TString,Int_t> temp;
       
       for(UInt_t i = 0 ; i < NbinsIEta-1 ; ++i)
	 {
	   for(UInt_t j = 0 ; j < NbinsIEt-1 ; ++j)
	     {
	       for(UInt_t k = 0 ; k < NbinsnTT-1 ; ++k)
		 {
		   TString Name_Histo = "Hist_";
		   
		   stringstream ss_i;
		   ss_i << i;
		   TString Appendix_i = TString(ss_i.str());
		   Name_Histo += Appendix_i;
		   Name_Histo += "_";
		   
		   stringstream ss_j;
		   ss_j << j;
		   TString Appendix_j = TString(ss_j.str());
		   Name_Histo += Appendix_j;
		   Name_Histo += "_";

		   stringstream ss_k;
		   ss_k << k;
		   TString Appendix_k = TString(ss_k.str());
		   Name_Histo += Appendix_k;

		   temp.insert(make_pair(Name_Histo,-1));
		 }
	     }
	 }
       
       IsoCut_PerEfficiency_PerBin.insert( make_pair(iEff, temp));
       temp.clear();
     } // Loop over efficiency histograms
   
   
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       ostringstream convert;
       convert << iEff ;
       TString NameEff = "Eff_";
       TString TempStr(convert.str());
       NameEff += TempStr;
       TH3F* temp = new TH3F(NameEff.Data(), NameEff.Data(), NbinsIEta-1, 0, NbinsIEta-1, NbinsIEt-1, 0, NbinsIEt-1, NbinsnTT-1, 0, NbinsnTT-1);
       IsoCut_PerBin.insert(make_pair(iEff,temp));
     }
   
   for(UInt_t i = 0 ; i < NbinsIEta-1 ; ++i)
     {
       for(UInt_t j = 0 ; j < NbinsIEt-1 ; ++j)
	 {
	   for(UInt_t k = 0 ; k < NbinsnTT-1 ; ++k)
	     {
	       TString Name_Histo = "Hist_";

	       stringstream ss_i;
	       ss_i << i;
	       TString Appendix_i = TString(ss_i.str());
	       Name_Histo += Appendix_i;
	       Name_Histo += "_";

	       stringstream ss_j;
	       ss_j << j;
	       TString Appendix_j = TString(ss_j.str());
	       Name_Histo += Appendix_j;
	       Name_Histo += "_";

	       stringstream ss_k;
	       ss_k << k;
	       TString Appendix_k = TString(ss_k.str());
	       Name_Histo += Appendix_k;

	       for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
		 {
		   Float_t Efficiency = 0.01*iEff;

		   for(UInt_t iIso = 0 ; iIso < 100 ; ++iIso)
		     {
		       if(Histos_PerBin[Name_Histo]->Integral(1,iIso+1)/Histos_PerBin[Name_Histo]->Integral(1,100+1)>=Efficiency)
			 {
			   if(IsoCut_PerEfficiency_PerBin[iEff][Name_Histo]==-1)
			     {
			       cout<<"Efficiency = "<<Efficiency<<", bin = "<<Name_Histo<<", cut = "<<iIso<<endl;
			       if(iEff==97) cout<<"IsoCut = "<<iIso<<endl;
			       IsoCut_PerEfficiency_PerBin[iEff][Name_Histo]=iIso;
			       IsoCut_PerBin[iEff]->SetBinContent(i+1,j+1,k+1,iIso);
			       if(iIso==0 && iEff>15) cout << "WARNING! IsoCut=0 in bin " << i+1 << " " << j+1 << " " << k+1 << " and efficiency WP " << iEff << endl;
			       cout<<"IsoCut_PerEfficiency_PerBin[iEff][Name_Histo] = "<<IsoCut_PerEfficiency_PerBin[iEff][Name_Histo]<<endl;                                                            
			     }
			 }
		     }
		 }
	       
	       // IsoCut_PerBin_90pc.insert(make_pair(Name_Histo,-1));
	       // IsoCut_PerBin_80pc.insert(make_pair(Name_Histo,-1));
	       
	       // for(UInt_t iIso = 0 ; iIso < 100 ; ++iIso)
	       //        {
	       //          // cout<<"testing iIso = "<<iIso<<endl;
	       //          // cout<<"Histos_PerBin[Name_Histo]->Integral(1,iIso+1) = "<<Histos_PerBin[Name_Histo]->Integral(1,iIso+1)<<endl;
	       //          // cout<<"Histos_PerBin[Name_Histo]->Integral(1,100+1) = "<<Histos_PerBin[Name_Histo]->Integral(1,100+1)<<endl;
	       //          if(Histos_PerBin[Name_Histo]->Integral(1,iIso+1)/Histos_PerBin[Name_Histo]->Integral(1,100+1)>=0.9)
	       //            {
	       //              if(IsoCut_PerBin_90pc[Name_Histo]==-1) IsoCut_PerBin_90pc[Name_Histo]=Histos_PerBin[Name_Histo]->GetBinLowEdge(iIso+1);
	       //            }
	       //          if(Histos_PerBin[Name_Histo]->Integral(1,iIso+1)/Histos_PerBin[Name_Histo]->Integral(1,100+1)>=0.8)
	       //            {
	       //              if(IsoCut_PerBin_80pc[Name_Histo]==-1) IsoCut_PerBin_80pc[Name_Histo]=Histos_PerBin[Name_Histo]->GetBinLowEdge(iIso+1);
	       //            }
	       //        }
	       // cout<<"50% iso cut for "<<Name_Histo<<" is = "<<IsoCut_PerBin_90pc[Name_Histo]<<endl;  
	       
	       if(Histos_PerBin[Name_Histo]->GetEntries()<20)
		 // if(Histos_PerBin[Name_Histo]->GetEntries()<40)
		 {
		   NumberOfHistosWithLowStats++;
		   cout<<"Histo "<<Name_Histo<<" has low stat.: "<<Histos_PerBin[Name_Histo]->GetEntries()<<endl;
		 }
	       Histos_PerBin[Name_Histo]->Write();
	     }
	 }
     } // IEta bins
   
   // Efficiency as function of pT
   std::map<Int_t,TH1F*> pt_pass_efficiency ;
   std::map<Int_t,TH1F*> pt_pass_efficiency_TH3 ;
   
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "pt_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;
       
       TString nameHisto_TH3 = "pt_pass_efficiency_TH3_";
       nameHisto_TH3 += temp;
       
       TH1F* temp_histo = new TH1F(nameHisto.Data(),nameHisto.Data(),100,0,200);
       TH1F* temp_histo_TH3 = new TH1F(nameHisto_TH3.Data(),nameHisto_TH3.Data(),100,0,200);
       
       pt_pass_efficiency.insert(make_pair(iEff,temp_histo));
       pt_pass_efficiency_TH3.insert(make_pair(iEff,temp_histo_TH3));
     }
   
   std::map<Int_t,TH1F*> eta_pass_efficiency ;
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "eta_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;

       TH1F* temp_histo = new TH1F(nameHisto.Data(),nameHisto.Data(),100,0,100);
       eta_pass_efficiency.insert(make_pair(iEff,temp_histo));
     }

   std::map<Int_t,TH1F*> nTT_pass_efficiency ;
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "nTT_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;

       TH1F* temp_histo = new TH1F(nameHisto.Data(),nameHisto.Data(),100,0,100);
       nTT_pass_efficiency.insert(make_pair(iEff,temp_histo));

     }

   TH1F* h_pt  = new TH1F("h_pt",  "pt", 100,0,200);
   TH1F* h_eta = new TH1F("h_eta", "eta", 100,0,100);
   TH1F* h_nTT = new TH1F("h_nTT", "nTT", 100,0,100);
   
   for (Long64_t jentry=0; jentry<nentries;jentry++)
     {
       Long64_t i = LoadTree(jentry);
       if (i < 0) break;
       
       std::vector<Int_t> binForIsolation ;
       binForIsolation.clear();
       binForIsolation.push_back(supercompressedEta);
       binForIsolation.push_back(supercompressedE);
       binForIsolation.push_back(supercompressednTT);
       
       TString Name_Histo = "Hist_";

       stringstream ss_i;
       ss_i << binForIsolation.at(0);
       TString Appendix_i = TString(ss_i.str());
       Name_Histo += Appendix_i;
       Name_Histo += "_";

       stringstream ss_j;
       ss_j << binForIsolation.at(1);
       TString Appendix_j = TString(ss_j.str());
       Name_Histo += Appendix_j;
       Name_Histo += "_";
       
       stringstream ss_k;
       ss_k << binForIsolation.at(2);
       TString Appendix_k = TString(ss_k.str());
       Name_Histo += Appendix_k;

       for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
	 {
	   if(iso <= IsoCut_PerEfficiency_PerBin[iEff][Name_Histo])
	     {
	       eta_pass_efficiency[iEff]->Fill(iEta);
	       pt_pass_efficiency[iEff]->Fill(RawEt);
	       nTT_pass_efficiency[iEff]->Fill(nTT);
	     }
	   
	   if(iso <= IsoCut_PerBin[iEff]->GetBinContent(binForIsolation.at(0)+1,binForIsolation.at(1)+1,binForIsolation.at(2)+1)) pt_pass_efficiency_TH3[iEff]->Fill(RawEt);
	 }
       h_pt  -> Fill(RawEt);
       h_eta -> Fill(iEta);
       h_nTT -> Fill(nTT);
     }
   
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "pt_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;
       
       TGraphAsymmErrors* temp_histo = new TGraphAsymmErrors(pt_pass_efficiency[iEff], h_pt,"cp");
       TGraphAsymmErrors* temp_histo_TH3 = new TGraphAsymmErrors(pt_pass_efficiency_TH3[iEff], h_pt,"cp");
       temp_histo->Write();
       temp_histo_TH3->Write();
     }
   
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "eta_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;
       
       TGraphAsymmErrors* temp_histo = new TGraphAsymmErrors(eta_pass_efficiency[iEff], h_eta,"cp");
       temp_histo->Write();
     }
   
   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       TString nameHisto = "nTT_pass_efficiency_";
       ostringstream convert;
       convert << iEff;
       TString temp(convert.str());
       nameHisto += temp;

       TGraphAsymmErrors* temp_histo = new TGraphAsymmErrors(nTT_pass_efficiency[iEff], h_nTT,"cp");
       temp_histo->Write();

     }

   for(UInt_t iEff = 0 ; iEff < 101 ; ++iEff)
     {
       IsoCut_PerBin[iEff]->Write();
     }

   h_pt->Write();
   h_eta->Write();
   h_nTT->Write();

   cout<<"NumberOfHistosWithLowStats/Tot = "<<NumberOfHistosWithLowStats<<"/"<<NbinsIEta*NbinsIEt*NbinsnTT<<endl;
}
