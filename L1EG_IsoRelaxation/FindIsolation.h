//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sat May  9 11:16:50 2020 by ROOT version 6.12/07
// from TTree TagAndProbe/TagAndProbe
// found on file: IsoTreeOut.root
//////////////////////////////////////////////////////////

#ifndef FindIsolation_h
#define FindIsolation_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

Int_t Supercompress(Int_t val, const Int_t* compression, int length)
{
  Int_t compressedVal = -1;
  for(int i=0; i<length; i++)
    {  
      if(compression[i]<=val && compression[i+1]>val)
        {
	  compressedVal = i;
          break;
        }
    }
  if(compressedVal==-1) compressedVal = length-1;
  return compressedVal;
}



class FindIsolation {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           compressedsortedshape;
   Int_t           Run2EleId;
   Int_t           compressedshape;
   Int_t           compressedieta;
   Int_t           RawEt;
   Double_t        offlineEt;
   Int_t           nTT;
   Int_t           iEta;
   Int_t           UnpackedE;
   Int_t           shape;
   Int_t           compressedE;
   Int_t           iso;
   Double_t        rho;
   Int_t           passShapeVeto;
   Double_t        offlineEta;
   Float_t         nVtx;
   Double_t        CalibratedE;

   // List of branches
   TBranch        *b_compressedsortedshape;   //!
   TBranch        *b_Run2EleId;   //!
   TBranch        *b_compressedshape;   //!
   TBranch        *b_compressedieta;   //!
   TBranch        *b_RawEt;   //!
   TBranch        *b_offlineEt;   //!
   TBranch        *b_nTT;   //!
   TBranch        *b_iEta;   //!
   TBranch        *b_UnpackedE;   //!
   TBranch        *b_shape;   //!
   TBranch        *b_compressedE;   //!
   TBranch        *b_iso;   //!
   TBranch        *b_rho;   //!
   TBranch        *b_passShapeVeto;   //!
   TBranch        *b_offlineEta;   //!
   TBranch        *b_nVtx;   //!
   TBranch        *b_CalibratedE;   //!

   FindIsolation(TTree *tree=0);
   virtual ~FindIsolation();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef FindIsolation_cxx
FindIsolation::FindIsolation(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("IsoTreeOut.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("IsoTreeOut.root");
      }
      f->GetObject("TagAndProbe",tree);

   }
   Init(tree);
}

FindIsolation::~FindIsolation()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t FindIsolation::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t FindIsolation::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void FindIsolation::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("compressedsortedshape", &compressedsortedshape, &b_compressedsortedshape);
   fChain->SetBranchAddress("Run2EleId", &Run2EleId, &b_Run2EleId);
   fChain->SetBranchAddress("compressedshape", &compressedshape, &b_compressedshape);
   fChain->SetBranchAddress("compressedieta", &compressedieta, &b_compressedieta);
   fChain->SetBranchAddress("RawEt", &RawEt, &b_RawEt);
   fChain->SetBranchAddress("offlineEt", &offlineEt, &b_offlineEt);
   fChain->SetBranchAddress("nTT", &nTT, &b_nTT);
   fChain->SetBranchAddress("iEta", &iEta, &b_iEta);
   fChain->SetBranchAddress("UnpackedE", &UnpackedE, &b_UnpackedE);
   fChain->SetBranchAddress("shape", &shape, &b_shape);
   fChain->SetBranchAddress("compressedE", &compressedE, &b_compressedE);
   fChain->SetBranchAddress("iso", &iso, &b_iso);
   fChain->SetBranchAddress("rho", &rho, &b_rho);
   fChain->SetBranchAddress("passShapeVeto", &passShapeVeto, &b_passShapeVeto);
   fChain->SetBranchAddress("offlineEta", &offlineEta, &b_offlineEta);
   fChain->SetBranchAddress("nVtx", &nVtx, &b_nVtx);
   fChain->SetBranchAddress("CalibratedE", &CalibratedE, &b_CalibratedE);
   Notify();
}

Bool_t FindIsolation::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void FindIsolation::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t FindIsolation::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef FindIsolation_cxx
