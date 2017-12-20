#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TLine.h"
#include "TPolyLine.h"
#include "TGraphErrors.h"
#include "TROOT.h"
#include "TApplication.h"
#include "TString.h"
#include "TProfile.h"
#include "TMath.h"
#include "Riostream.h"
#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <sstream>
#include <string>
#include <TString.h>
#include "time.h"
#include <ctime>
#include <cstdlib>
#include "TLegend.h"
#include "TTree.h"
#include "TFile.h"
#include "TCut.h"
#include "TString.h"
#include "TLatex.h"

#include "RooFit.h"
#include "RooHist.h"
#include "RooHist.h"
#include "RooHistError.h"
#include "RooCurve.h"
#include "RooMsgService.h"

#include "TGraphAsymmErrors.h"
#include "RooPlotable.h"
#include "RooAbsData.h"
#include "RooPlot.h"

//#include "TurnonFit.h"

#include "RooCategory.h"
#include "RooEfficiency.h"
#include "RooDataSet.h"
#include "RooBinning.h"

{ 
 
      TFile *f=TFile::Open("./Run2017/fitOutput_1cut_check_barrel.root");
  
      emulated=(RooHist*)f->Get("histo_Stage2_vs_Pt_0GeV");
      unpacked=(RooHist*)f->Get("histo_Stage2_vs_Pt_40GeV");
     // HoE_Id=(RooHist*)f->Get("histo_Stage2_vs_Pt_20GeV");
    /*    
      std::cout<<"GetNShape: "<<Shape_Id->GetN()<<endl;
      std::cout<<"GetNFG: "<<FG_Id->GetN()<<endl;       
      std::cout<<"GetNHoE: "<<HoE_Id->GetN()<<endl;
    
     
      TH1D *eff_eff=new TH1D("eff_eff","Effective Efficiency",200,0.,100);
      eff_eff->Sumw2();

      TH1D *ShapeId=new TH1D("Shape","Shape",200,0.,100);
      ShapeId->Sumw2();
   
     */ 

      TH1D *Emulated=new TH1D("Emulated","Emulated",200,0.,100);
      Emulated->Sumw2();

      TH1D *Unpacked=new TH1D("Unpacked","Unpacked",200,0.,100);
      Unpacked->Sumw2();

      TH1D *Ratio=new TH1D("Ratio","Emulated/Unpacked",200,0.,100);
      Ratio->Sumw2();

      

      const Int_t n=emulated->GetN();
      Double_t x[100], y[100], errX[100], errY[100];
    //  TGraphErrors *Ratio2 = new TGraphErrors(n,x,y,errX,errY);

   //     RooHist *eff_eff=new RooHist;
    

      for(int ipt =0;ipt<emulated->GetN();++ipt)
          {
            double x_emulated, y_emulated;
            double x_unpacked, y_unpacked;
           // double x_HoE, y_HoE;   
            
            double ratio;  

            emulated->GetPoint(ipt,x_emulated,y_emulated);
            unpacked->GetPoint(ipt,x_unpacked,y_unpacked);
             
           // HoE_Id->GetPoint(ipt,x_HoE,y_HoE);
            ratio = y_emulated/y_unpacked;
          //  effective_eff=1-(1-y_shape)-(1-y_FG)-(1-y_HoE);
            if(ratio>=-1){
                 
                x[ipt] = x_emulated;
                y[ipt] = ratio;
                       
                double emulated_error = emulated->GetErrorY(ipt);
                double unpacked_error = unpacked->GetErrorY(ipt);  
               
                errX[ipt] = 0;
 
                double ratio_error = sqrt((pow((y_emulated/y_unpacked),2))*(pow((emulated_error/y_emulated),2)+pow((unpacked_error/y_unpacked),2)));
                errY[ipt] = ratio_error;
              
                std::cout<<"Ratio Error "<<ipt<<": "<<ratio_error<<endl; 
                    
                //std::cout<<"Error Emulated: "<<emulated_error<<endl;
               // std::cout<<"Error Unpacked: "<<unpacked_error<<endl<<endl;   
                
                //std::cout<<"Effective Efficiency: "<<effective_eff<<endl;
                //eff_eff->Fill(x_shape,effective_eff);
                //ShapeId->Fill(x_shape,y_shape);
                //FG->Fill(x_FG,y_FG);
                Ratio->Fill(x_emulated,ratio);
            }
            //std::cout<<"x: "<<x<<" ,"<<"y: "<<y<<endl; 
            
          }
       
       TGraphErrors *Ratio2 = new TGraphErrors(n,x,y,errX,errY);   
       TCanvas *c1=new TCanvas("c1","c1",1000,300);

       c1->SetGrid(0,1);
       
     /////  
       Ratio->SetMarkerColor(kBlack);
       Ratio->SetLineColor(kBlack);
       Ratio->SetLineWidth(1);   
       Ratio->SetMarkerStyle(kFullCircle);      
       Ratio->SetStats(0);
       Ratio->GetXaxis()->SetTitle("p_{T}^{offl}[GeV]");
      // eff_eff->GetYaxis()->SetTitle("eff=1-(1-eff_{shapeID})-(1-eff_{FG})-(1-eff_{HoE})");
       Ratio->GetYaxis()->SetTitle("Ratio");
       Ratio->SetMaximum(1.008);
       Ratio->SetMinimum(0.994);
      /////
/*
      ////
       ShapeId->SetMarkerColor(kGreen+1);
       ShapeId->SetLineColor(kGreen+1);
       ShapeId->SetLineWidth(1);   
       ShapeId->SetMarkerStyle(kFullSquare);      
       ShapeId->SetStats(0);
       ShapeId->GetXaxis()->SetTitle("p_{T}^{offl}[GeV]");
      // ShapeId->GetYaxis()->SetTitle("eff=1-(1-eff_{shapeID})-(1-eff_{FG})-(1-eff_{HoE})");

       ShapeId->SetMaximum(1.1);
       ShapeId->SetMinimum(0.);
       ////

     
       ////
       FG->SetMarkerColor(kRed+1);
       FG->SetLineColor(kRed+1);
       FG->SetLineWidth(1);
       FG->SetMarkerStyle(kFullTriangleUp);
       FG->SetStats(0);
       FG->GetXaxis()->SetTitle("p_{T}^{offl}[GeV]");
      // ShapeId->GetYaxis()->SetTitle("eff=1-(1-eff_{shapeID})-(1-eff_{FG})-(1-eff_{HoE})");

       ShapeId->SetMaximum(1.1);
       ShapeId->SetMinimum(0.);
       ////

       
       ////
       HoE->SetMarkerColor(kYellow+2);
       HoE->SetLineColor(kYellow+2);
       HoE->SetLineWidth(1);
       HoE->SetMarkerStyle(kFullTriangleDown);
       HoE->SetStats(0);
       HoE->GetXaxis()->SetTitle("p_{T}^{offl}[GeV]");
      // ShapeId->GetYaxis()->SetTitle("eff=1-(1-eff_{shapeID})-(1-eff_{FG})-(1-eff_{HoE})");

       HoE->SetMaximum(1.1);
       HoE->SetMinimum(0.);
       ////


       leg= new TLegend(0.4,0.4,0.78,0.6);
       leg->SetHeader("Efficiencies");
       leg->AddEntry(eff_eff,"Effective Efficiency","lep");
       leg->AddEntry(ShapeId,"Shape ID","lep");
       leg->AddEntry(FG,"FG ID","lep");
       leg->AddEntry(HoE,"HoE ID","lep");

*/
            
       //Ratio->Draw("hist p");
  //     ShapeId->Draw("hist p same");
    //   FG->Draw("hist p same");
      // HoE->Draw("hist p same");

       //leg->Draw();

//      c1->SaveAs("Ratio.pdf","pdf");













        //std::cout<<check->GetPoint(0,x,y)<<endl;        

       // TH1 *h1=check->createHistogram("x",100);
        //m_histo = (TH1*)check;
     // check2=(RooHist*)f->Get("histo_Stage2_vs_Pt_30GeV");
      
  //    RooHist *ratio = new RooHist;       
      //ratio->Sumw2();
    //  ratio->Divide(check2,check);
     Ratio2->SetMaximum(1.1);
     Ratio2->SetMinimum(0.9);
     Ratio2->GetXaxis()->SetRangeUser(0.,100.);
     Ratio2->SetMarkerColor(kBlack);
     Ratio2->SetLineColor(kBlack);
     Ratio2->SetLineWidth(1);
     Ratio2->SetMarkerStyle(kFullCircle);
     Ratio2->GetXaxis()->SetTitleSize(0.04);

     Ratio2->GetXaxis()->SetTitle("p_{T}^{offl}[GeV]");
     Ratio2->GetYaxis()->SetTitleSize(0.06);
     Ratio2->GetYaxis()->SetTitle("Ids disabled / With Shape Id");
     Ratio2->GetYaxis()->SetTitleOffset(0.5);

     Ratio2->Draw("AP"); 
     TLine *line = new TLine(0.,1.,105.5,1.);
     line->SetLineWidth(2);
     line->Draw();

     c1->SaveAs("Ratio_Shape.png","png");
/*
      Double_t bins =check->GetSize();      
      std::cout << "Bins: "<<bins<<endl;

      for (Int_t i=0;i<bins;i++){
          Double_t bin=check->GetBinContent(i);
          std::cout<<"Bin:"<<bin<<endl;
      }
   
*/
 //     check2->Draw();
     
}





