# satminer
satMiner: A Toolkit to NGS satellite DNA mining and analysis

![My image](https://github.com/fjruizruano/satminer/blob/master/pipeline_satminer.png)

##Installation
- Copy script to your binaries folder.
- Dependencies:
  * BioPython [http://biopython.org/wiki/Main_Page](http://biopython.org/wiki/Main_Page)
  * RepeatMasker [http://www.repeatmasker.org/RMDownload.html](http://www.repeatmasker.org/RMDownload.html)
  * seqTK [https://github.com/lh3/seqtk](https://github.com/lh3/seqtk)
  * DeconSeq [http://deconseq.sourceforge.net](http://deconseq.sourceforge.net)
  * BLAT [http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/blat/](http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/blat/)
  * Trimmomatic [http://www.usadellab.org/cms/?page=trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)

##satDNA mining

### Preparing sequences to RepeatExplorer
```
$ rexp_prepare.py NumberOfPairedReads LibraryA_1.fastq LibraryA_2.fastq [Prefix]
```

### Get contigs
```
$ get_cluster.py
```

```
$ rexp_select_contigs.py
```

### Run DeconSeq
```
$ deconseq_run.py ListOfFastaFiles Reference Threads
```

##satDNA analysis

### Homology among consensus sequences

```
$ rm_homology.py FastaFile
```

### Intragenomic variation

```
$ rm_getseq.py FastaFile RepeatMaskerOut [LenMinimum]
```
Optionally:

```
$ sat_cutter.py AlignedFastaFile
```

### Abundance and divergece

```
$ repeat_masker_run_big.py ListOfFastaFiles FastaReference NumberOfThreads
```
Pattern File with tab-separated names:

```
Sat-01A	Sat-01A
Sat-02A Sat-02A
Sat-02B	Sat-02A
```
Running script

```
$ sat_subfam2fam.py AlignFile PatternFile
```

