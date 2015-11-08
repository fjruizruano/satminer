# satminer
satMiner: A Toolkit to NGS satellite DNA mining and analysis

![My image](https://github.com/fjruizruano/satminer/blob/master/pipeline_satminer.png)

##Installation
* Copy script to your binaries folder.
* Dependencies: RepeatMasker, seqTK, DeconSeq, BLAT, Trimmomatic

##satDNA mining

### Preparing sequences to RepeatExplorer
```bash
$ rexp_prepare.py NumberOfPairedReads LibraryA_1.fastq LibraryA_2.fastq [Prefix]
```

### Get contigs
```bash
$ get_cluster.py
```

```bash
$ rexp_select_contigs.py
```

### Run DeconSeq
```bash
$ deconseq_run.py ListOfFastaFiles Reference Threads
```

##satDNA analysis

### Homology among consensus sequences

```bash
$ rm_homology.py FastaFile
```

### Intragenomic variation

```bash
$ rm_getseq.py FastaFile RepeatMaskerOut [LenMinimum]
```
Optionally:

```bash
$ sat_cutter.py AlignedFastaFile
```

### Abundance and divergece

```bash
$ repeat_masker_run_big.py ListOfFastaFiles FastaReference NumberOfThreads
```
Pattern File:

```
Sat-01A	Sat-01A
Sat-02A Sat-02A
Sat-02B	Sat-02A
```
Running script

```bash
$ sat_subfam2fam.py AlignFile Pattern File
```

