# satminer
satMiner: A Toolkit to NGS satellite DNA mining and analysis

![My image](https://github.com/fjruizruano/satminer/blob/master/pipeline_satminer.png)

##Installation
* Copy script to your binaries folder.
* Dependencies: RepeatMasker, seqTK, DeconSeq, BLAT, Trimmomatic

##satDNA mining
* Preparing sequences to RepeatExplorer: rexp_prepare.py
* Get contigs: get_cluster.py, rexp_select_contigs.py
* Run DeconSeq: run_deconseq.py

##satDNA analysis
* Homology among consensus sequences: rm_homology.py
* Intragenomic variation: rm_getseq.py, sat_cutter.py
* Abundance and divergece: sat_subfam2fam.py, repeat_masker_run_big.py

