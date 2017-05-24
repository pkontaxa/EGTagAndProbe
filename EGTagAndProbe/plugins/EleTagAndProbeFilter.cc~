#ifndef TAUTAGANDPROBEFILTER_H
#define TAUTAGANDPROBEFILTER_H

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <FWCore/Utilities/interface/InputTag.h>
#include <DataFormats/PatCandidates/interface/Tau.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/PatCandidates/interface/MET.h>
#include <DataFormats/PatCandidates/interface/CompositeCandidate.h>

#include <iostream>
#include <utility>
#include <vector>

using namespace edm;
using namespace std;
// using namespace reco;


class TauTagAndProbeFilter : public edm::EDFilter {

    public:
        TauTagAndProbeFilter(const edm::ParameterSet &);
        ~TauTagAndProbeFilter();

    private:
        bool filter(edm::Event &, edm::EventSetup const&);

        float ComputeMT(math::XYZTLorentzVector visP4, const pat::MET& met);

        EDGetTokenT<pat::TauRefVector>   _tausTag;
        EDGetTokenT<pat::MuonRefVector>  _muonsTag;
        EDGetTokenT<pat::METCollection>  _metTag;
};

TauTagAndProbeFilter::TauTagAndProbeFilter(const edm::ParameterSet & iConfig) :
_tausTag  (consumes<pat::TauRefVector>  (iConfig.getParameter<InputTag>("taus"))),
_muonsTag (consumes<pat::MuonRefVector> (iConfig.getParameter<InputTag>("muons"))),
_metTag   (consumes<pat::METCollection> (iConfig.getParameter<InputTag>("met")))
{
    produces <pat::TauRefVector>  (); // probe
    produces <pat::MuonRefVector> (); // tag
}

TauTagAndProbeFilter::~TauTagAndProbeFilter()
{}

bool TauTagAndProbeFilter::filter(edm::Event & iEvent, edm::EventSetup const& iSetup)
{
    int _indexevents = iEvent.id().event();
    // int _runNumber = iEvent.id().run();
    // int _lumi = iEvent.luminosityBlock();

    cout<<"EventNumber = "<<_indexevents<<endl;

    std::unique_ptr<pat::MuonRefVector> resultMuon ( new pat::MuonRefVector );
    std::unique_ptr<pat::TauRefVector>  resultTau  ( new pat::TauRefVector  );
    // auto_ptr<pat::MuonRefVector> resultMuon ( new pat::MuonRefVector );
    // auto_ptr<pat::TauRefVector>  resultTau  ( new pat::TauRefVector  );

    // ---------------------   search for the tag in the event --------------------
    Handle<pat::MuonRefVector> muonHandle;
    iEvent.getByToken (_muonsTag, muonHandle);

    // reject events with more than 1 mu in the event (reject DY)
    // or without mu (should not happen in SingleMu dataset)
    if (muonHandle->size() != 1) return false;

    cout<<"pass muonHandle"<<endl;

    // for loop is now dummy, leaving it for debug
    // for (size_t imu = 0; imu < muonHandle->size(); ++imu )
    // {
    //     const pat::MuonRef mu = (*muonHandle)[imu] ;
    //     cout << "### FILTERED MUON PT: " << mu->pt() << endl;
    // }

    const pat::MuonRef mu = (*muonHandle)[0] ;

    //---------------------   get the met for mt computation etc. -----------------
    Handle<pat::METCollection> metHandle;
    iEvent.getByToken (_metTag, metHandle);
    const pat::MET& met = (*metHandle)[0];
    cout<<"met.pt() = "<<met.pt()<<endl;
    cout<<"met.uncorPt() = "<<met.uncorPt()<<endl;
    cout<<"met.uncorPhi() = "<<met.uncorPhi()<<endl;

    float mt = ComputeMT (mu->p4(), met);

    cout<<"mt = "<<mt<<endl;

    if (mt >= 30) return false; // reject W+jets

    cout<<"pass mT"<<endl;

    Handle<pat::TauRefVector> tauHandle;
    iEvent.getByToken (_tausTag, tauHandle);
    if (tauHandle->size() < 1) return false;

    //vector<pair<float, int>> tausIdxPtVecSS;
    //vector<pair<float, int>> tausIdxPtVecOS;
    vector<pair<float, int>> tausIdxPtVec;
    for (uint itau = 0; itau < tauHandle->size(); ++itau)
    {
        const pat::TauRef tau = (*tauHandle)[itau] ;
        math::XYZTLorentzVector pSum = mu->p4() + tau->p4();
        if (pSum.mass() <= 40 || pSum.mass() >= 80) continue; // visible mass in (40, 80)
        if (deltaR(*tau, *mu) < 0.5) continue;

        // max pt
//        if (mu -> charge() / tau -> charge() > 0 ){
//            tausIdxPtVecSS.push_back(make_pair(tau -> pt(), itau));
//        } else {
//             tausIdxPtVecOS.push_back(make_pair(tau -> pt(), itau));
//        }

        // min iso
        //float isoMVA = tau->tauID("byIsolationMVArun2v1DBoldDMwLTraw");
        //if (mu -> charge() / tau -> charge() > 0 ){
        //    tausIdxPtVecSS.push_back(make_pair(isoMVA, itau));
        //} else {
        //    tausIdxPtVecOS.push_back(make_pair(isoMVA, itau));
        //}

        // min iso
        float isoMVA = tau->tauID("byIsolationMVArun2v1DBoldDMwLTraw");
        tausIdxPtVec.push_back(make_pair(isoMVA, itau));

    }


    pat::TauRef tau;

    /*
    if (tausIdxPtVecOS.size() != 0)
    {
        if (tausIdxPtVecOS.size() > 1) sort (tausIdxPtVecOS.begin(), tausIdxPtVecOS.end()); // will be sorted by first idx i.e. highest pt
        // int tauIdx = tausIdxPtVecOS.back().second; // max pt
        int tauIdx = tausIdxPtVecOS.at(0).second; // min iso
        tau = (*tauHandle)[tauIdx];
    } else if (tausIdxPtVecSS.size() != 0 )
    {
        if (tausIdxPtVecSS.size() > 1) sort (tausIdxPtVecSS.begin(), tausIdxPtVecSS.end()); // will be sorted by first idx i.e. highest pt
        // int tauIdx = tausIdxPtVecSS.back().second; // max pt
        int tauIdx = tausIdxPtVecSS.at(0).second; // min iso
        tau = (*tauHandle)[tauIdx];
    } else return false;//They are both 0!
    */

    if (tausIdxPtVec.size() == 0) return false; //No tau found
    if (tausIdxPtVec.size() > 1) sort (tausIdxPtVec.begin(), tausIdxPtVec.end()); //Sort if multiple taus
    int tauIdx = tausIdxPtVec.back().second; // min iso --> max MVA score
    tau = (*tauHandle)[tauIdx];

    resultTau->push_back (tau);
    resultMuon->push_back (mu);
    iEvent.put(std::move(resultMuon));
    iEvent.put(std::move(resultTau));
    // iEvent.put(resultMuon);
    // iEvent.put(resultTau);

    return true;
}

float TauTagAndProbeFilter::ComputeMT (math::XYZTLorentzVector visP4, const pat::MET& met)
{
  math::XYZTLorentzVector METP4 (met.uncorPt()*TMath::Cos(met.uncorPhi()), met.uncorPt()*TMath::Sin(met.uncorPhi()), 0, met.uncorPt());
  cout<<"MET Px = "<<met.uncorPt()*TMath::Cos(met.uncorPhi())<<endl;
    float scalSum = met.uncorPt() + visP4.pt();

    // math::XYZTLorentzVector METP4 (met.px(), met.py(), 0, met.pt());
    // float scalSum = met.pt() + visP4.pt();

    math::XYZTLorentzVector vecSum (visP4);
    vecSum += METP4;
    float vecSumPt = vecSum.pt();
    return sqrt (scalSum*scalSum - vecSumPt*vecSumPt);
}

#include <FWCore/Framework/interface/MakerMacros.h>
DEFINE_FWK_MODULE(TauTagAndProbeFilter);

#endif
