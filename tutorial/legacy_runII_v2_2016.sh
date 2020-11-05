outdir=$CMSSW_BASE/src/tutorial/demo

fggRunJobs.py --load legacy_runII_v2_2016.json \
              -d $outdir \
              -n 100 \
              -q workday \
              --no-use-tarball --no-copy-proxy -D -P \
              -x cmsRun WHLeptonicDumper_cfg.py maxEvents=-1
