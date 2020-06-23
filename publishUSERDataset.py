#!/usr/bin/env python2
from itertools import chain
import copy
import os.path
import uuid
from pprint import pformat
import argparse
import logging
logger = logging.getLogger(__name__)
import glob
import os, os.path
import subprocess

def publishFiles(dbsWrite,
        fileDictList,
        origin_site="T2_CH_CERN",
        primary_ds="CHANGEME1", ## no minuses, and no longer than 99
        processed_ds="username-primary_ds-md5sumInvention",
        data_tier="USER",
        primary_ds_type="mc", # or "data"
        acquisition_era="CRAB",
        acquisition_start_date=2020,
        processing_version=1,
        processing_description="test_injection",
        physics_group="CRAB3",
        dataset_access_type="VALID",
        global_tag="dummytag",
        output_module_label="out",
        pset_hash="dummyhash",
        application="Madgraph",
        release="Mad_20_20_20",
        open_for_writing=1,
        files_per_block=500,
        dry_run=False
        ):
    dataset = "/{0}/{1}/{2}".format(primary_ds, processed_ds, data_tier)
    blkRequest_empty = {
            "files" : None,
            "processing_era" : {
                "processing_version" : processing_version,
                "description" : processing_description
                },
            "primds" : {
                "primary_ds_type" : primary_ds_type,
                "primary_ds_name" : primary_ds,
                },
            "dataset" : {
                "physics_group_name" : physics_group,
                "dataset_access_type" : dataset_access_type,
                "data_tier_name" : data_tier,
                "processed_ds_name" : processed_ds,
                "dataset" : dataset
                },
            "dataset_conf_list" : [{
                "app_name" : application,
                "global_tag" : global_tag,
                "output_module_label" : output_module_label,
                "pset_hash" : "dummyhash",
                "release_version" : release
                }],
            "acquisition_era" : {
                "acquisition_era_name" : acquisition_era,
                "start_date" : acquisition_start_date
                },
            "block" : {
                "block_name" : None,
                "origin_site_name" : origin_site,
                "open_for_writing" : open_for_writing,
                "file_count" : None,
                "block_size" : None
                },
            "file_parent_list" : [], ## TODO fill?
            "file_conf_list" : []    ## TODO fill?
            }
    if files_per_block > 0:
        files_blocks = [ fileDictList[i:i+files_per_block] for i in range(0, len(fileDictList), files_per_block) ]
    elif files_per_block == -1:
        files_blocks = [ fileDictList ]
    else:
        raise ValueError("Only positive values and -1 are allowed for files_per_block, got {0:d}".format(files_per_block))
    for blockFiles in files_blocks:
        blockConfig = copy.deepcopy(blkRequest_empty)
        blockConfig["block"].update({
            "block_name" : "#".join((dataset, str(uuid.uuid4()))),
            "file_count" : len(blockFiles),
            "block_size" : sum(int(fd["file_size"]) for fd in blockFiles)
            })
        blockConfig["files"] = blockFiles
        logger.info("Inserting block for {0}".format(dataset))
        logger.debug(pformat(blockConfig))
        if dry_run:
            logger.info("Dry-run, not inserting after all")
        else:
            res = dbsWrite.insertBulkBlock(blockConfig)
            logger.info(pformat(res))

def getAdler32(pfn):
    for i in range(5):
        try:
            ad32 = subprocess.check_output(["adler32", pfn]).strip()
            logger.debug("adler32 for {0}: {1}".format(pfn, ad32))
            return pfn, ad32
        except subprocess.CalledProcessError as ex:
            pass
    logger.error("No adler32 for {0} after 5 tries".format(pfn))
    return pfn, "NOTSET"

def getChecksum(pfn):
    for i in range(5):
        try:
            checksum = subprocess.check_output(["cksum", pfn]).split()[0]
            logger.debug("checksum for {0}: {1}".format(pfn, checksum))
            return pfn, checksum
        except subprocess.CalledProcessError as ex:
            pass
    logger.error("No checksum for {0} after 5 tries".format(pfn))
    return pfn, "NOTSET"

def getMD5(pfn):
    for i in range(5):
        try:
            checksum = subprocess.check_output(["md5sum", pfn]).split()[0]
            logger.debug("MD5 for {0}: {1}".format(pfn, checksum))
            return pfn, checksum
        except subprocess.CalledProcessError as ex:
            pass
    logger.error("No md5 for {0} after 5 tries".format(pfn))
    return pfn, "NOTSET"

def fileInfoDict(lfn, locPfn, nEvents=0, file_type="EDM", lumis=None, adler32="NOTSET", checkSum="NOTSET", md5="NOTSET"):
    fSize = int(os.path.getsize(locPfn))
    return {
        "logical_file_name" : lfn,
        "file_type"         : file_type,
        "check_sum"         : checkSum,
        "adler32"           : adler32,
        "md5"               : md5,
        "file_size"         : fSize,
        "event_count"       : nEvents,
        "file_lumi_list"    : lumis if lumis is not None else [{'lumi_section_num': 1, 'run_num': 1}]
        }

dbsHosts = {
        "dev"  : "dbs3-dev01.cern.ch",
        "int"  : "cmsweb-testbed.cern.ch",
        "prod" : "cmsweb.cern.ch"
        }
def getDbsApi(host="prod", write=False, instance="phys03"):
    from dbs.apis.dbsClient import DbsApi
    apiUrl = "https://{0}/dbs/{1}/{2}/{3}".format(dbsHosts[host], host, instance, ("DBSWriter" if write else "DBSReader"))
    return DbsApi(url=apiUrl)

try:
    from cppyy import gbl
except:
    pass
def getNEventsLumis_EDM(pfn):
    from cppyy import gbl
    f = gbl.TFile.Open(pfn)
    if not f:
        raise RuntimeError("Could not open file {0}".format(pfn))
    tEvt = f.Get("Events")
    if not tEvt:
        raise RuntimeError("Could not get 'Events' tree from file {0}".format(pfn))
    entries = tEvt.GetEntries()
    lumis = []
    tLS = f.Get("LuminosityBlocks")
    for i in range(tLS.GetEntries()):
        tLS.GetEntry(i)
        lumis.append({"run_num": tLS.run, "lumi_section_num": tLS.luminosityBlock})
    logger.debug("Entries in {0}: {1:d}; {2:d} luminosity blocks".format(pfn, entries, len(lumis)))
    return pfn, (entries, lumis)

getNEventsLumis = {
    "EDM" : getNEventsLumis_EDM
    }

## start with a method that's a lot like the original
def publishFilesAsDataset(lfnLocPfnList, file_type="EDM", host="prod", instance="phys03", nProc=1, do_adler32=False, do_cksum=False, do_md5sum=False, **kwargs):
    import multiprocessing.pool
    pool = multiprocessing.pool.Pool(nProc)
    logger.debug("Retrieving number of events in {0:d} files".format(len(lfnLocPfnList)))
    pfn_entriesLumis = dict((k,v) for k,v in pool.imap_unordered(getNEventsLumis[file_type], (pfn for lfn,pfn in lfnLocPfnList)))
    pfn_adler32, pfn_checksum, pfn_md5 = dict(), dict(), dict()
    if do_adler32:
        logger.debug("Making adler32 checksums for {0:d} files".format(len(lfnLocPfnList)))
        pfn_adler32 = dict((k,v) for k,v in pool.imap_unordered(getAdler32, (pfn for lfn,pfn in lfnLocPfnList)))
    if do_cksum:
        logger.debug("Making cksum checksums for {0:d} files".format(len(lfnLocPfnList)))
        pfn_checksum = dict((k,v) for k,v in pool.imap_unordered(getChecksum, (pfn for lfn,pfn in lfnLocPfnList)))
    if do_md5sum:
        logger.debug("Making md5sum for {0:d} files".format(len(lfnLocPfnList)))
        pfn_md5 = dict((k,v) for k,v in pool.imap_unordered(getMD5, (pfn for lfn,pfn in lfnLocPfnList)))
    filesInfo = [ fileInfoDict(lfn, locPfn, file_type=file_type, nEvents=pfn_entriesLumis[locPfn][0], lumis=pfn_entriesLumis[locPfn][1],
        adler32=pfn_adler32.get(locPfn, "NOTSET"), checkSum=pfn_checksum.get(locPfn, "NOTSET"), md5=pfn_md5.get(locPfn, "NOTSET")
        ) for lfn, locPfn in lfnLocPfnList ]
    writeApi = getDbsApi(host=host, write=True, instance=instance)
    publishFiles(writeApi, filesInfo, **kwargs)

def cli_publish_from_dirs(args=None):
    parser = argparse.ArgumentParser(description="Publish the files in a directory to DBS")
    parser.add_argument("path", nargs="+")
    parser.add_argument("--site", required=True, help="Origin site")
    parser.add_argument("--primary", required=True, help="Primary dataset name (first part of the DAS path)")
    parser.add_argument("--processed", required=True, help="Processed dataset name (will become the second part of the DAS path)")
    parser.add_argument("--tier", default="USER", help="Data tier")
    parser.add_argument("--type", required=True, choices=("data", "mc"), help="Dataset type")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Stop before adding to DBS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--pattern", default="*/*.root", help="Glob pattern to collect files from the path(s)")
    parser.add_argument("--storeroot", required=True, help="Site CMS store root (path before '/store/...')")
    parser.add_argument("-j", "--nProcesses", default=4, type=int, help="Number of processes in the pool (to get the number of events and calculate checksums)")
    parser.add_argument("--procVersion", default=1, help="Processing version")
    parser.add_argument("--procDescription", default="test_injection", help="Processing description")
    parser.add_argument("--application", default="CMSSW", help="Application")
    parser.add_argument("--release", help="Application release (CMSSW_X_Y_Z)")
    parser.add_argument("--addAdler32", action="store_true", help="Calculate adler32 checksums")
    parser.add_argument("--addMD5", action="store_true", help="Calculate md5 checksums")
    parser.add_argument("--addChecksum", action="store_true", help="Calculate checksums with the cksum tool")
    parser.add_argument("--globalTag", help="Global tag")
    parser.add_argument("--host", default="prod", choices=["prod", "dev", "int"], help="CMSWEB instance")
    parser.add_argument("--instance", default="phys03", help="DBS instance (phys03 for USER files)")
    args = parser.parse_args(args=args)
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO))

    storageroot = args.storeroot.rstrip(os.sep)

    filenames = []
    for path in args.path:
        pFiles = glob.glob(os.path.join(os.path.abspath(path), args.pattern))
        if len(pFiles) == 0:
            logger.warning("No files matching {0!r} found in directory {1}".format(args.pattern, path))
        else:
            logger.debug("Found {0:d} files matching {1!r} in directory {2}".format(len(pFiles), args.pattern, path))
        filenames += pFiles
    logger.info("Found {0:d} files in total".format(len(filenames)))
    if not all(fn.startswith(storageroot) for fn in filenames):
        raise RuntimeError("Not all files start with {0}, cannot convert to LFNs (offending files are {1})".format(storageroot, ", ".join(fn for fn in filenames if not fn.startswith(storageroot))))
    lfnpfns = [ (fn[len(storageroot):], fn) for fn in filenames ]
    logger.debug("Full list of LFNs and local paths:")
    logger.debug(pformat(lfnpfns))

    publishFilesAsDataset(lfnpfns,
            origin_site=args.site,
            primary_ds=args.primary,
            processed_ds=args.processed,
            data_tier=args.tier,
            primary_ds_type=args.type,
            processing_version=args.procVersion,
            processing_description=args.procDescription,
            application=args.application,
            release=args.release if args.release else os.environ.get("CMSSW_VERSION", "CMSSW_X_Y_Z"),
            global_tag=args.globalTag,
            nProc=args.nProcesses,
            do_adler32=args.addAdler32,
            do_cksum=args.addChecksum,
            do_md5sum=args.addMD5,
            dry_run=args.dry_run)

if __name__ == "__main__":
    cli_publish_from_dirs()
