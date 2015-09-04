import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring("root://cmsxrootd.fnal.gov//store/data/Run2015B/MET/RECO/PromptReco-v1/000/251/163/00000/E83835E3-9F26-E511-B6F4-02163E0133BB.root"))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root')
)
process.outpath = cms.EndPath(process.out)

