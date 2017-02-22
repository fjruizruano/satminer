#!/usr/bin/python

import sys, os
from subprocess import call, Popen
from os import listdir
from os.path import isfile, join

print "Usage: SE_deconseq_run.py FastqFile Reference Threads"

try:
    file = sys.argv[1]
except:
    file = raw_input("Introduce a Fastq file: ")

try:
    ref = sys.argv[2]
except:
    ref = raw_input("Introduce FASTA reference: ")

try:
    thr = sys.argv[3]
except:
    thr = raw_input("Introduce number of threads: ")

refp = ref.split(".")
refpoints = refp[0:-1]
refname = ".".join(refpoints)

#files = open(files).readlines()

dsdir = "deconseq-standalone-0.4.3"

elements = os.listdir(".")
if dsdir not in elements:
    call("cp -r /homes/ashah/install_files/%s ." % dsdir, shell=True)
    call("mkdir %s/db" % dsdir, shell=True)

os.chdir(dsdir+"/db")
call("ln -sf ../../%s" % ref, shell=True)
call("../bwa64 index -p %s -a is  %s" % (refname,ref), shell=True)
os.chdir("../")
conf = open("DeconSeqConfig.pm").readlines()
conf_out = open("tmp_conf.txt", "w")
line1 = " "*21+"%s => {name => \047%s\047,\n" % (refname,refname)
line2 = " "*30+"db => \047%s\047},\n" % (refname)
conf.insert(20, line1+line2)
conf_out.write("".join(conf))
conf_out.close()
call("mv tmp_conf.txt DeconSeqConfig.pm", shell=True)
os.chdir("../")

file1 = file
ext1 = file1.split(".")
if ext1[-1] == "gz":
    file1_n = ext1[0:-1]
    file1_n = ".".join(file1_n)
    print "Uncompressing file %s" % file1
    call("seqtk seq %s > %s" % (file1, file1_n), shell=True)
    file1 = file1_n

filename = file1.split(".")
filename = filename[0]
call("mkdir %s/%s" % (dsdir,filename), shell=True)
os.chdir("%s/%s" % (dsdir,filename))

call("ln -sf ../../%s ." % file1 , shell=True)

call("FastQ.split.pl %s tmp_queries_1 %s" % (file1, thr), shell=True)

onlyfiles = [f for f in listdir(".") if isfile(join(".",f))]
splits = []
for f in onlyfiles:
    if f.startswith("tmp_queries_1") and f.endswith(".fastq"):
        splits.append(f)
splits.sort()

commands = []
for round in range(0,2):
    commands.append([])

for n in range(0,len(splits)):
    fq = splits[n]
    com = "perl deconseq.pl -f ./%s -out_dir %s.dir -dbs %s" % (fq, fq, refname)
    rr = n/int(thr)
    commands[rr].append(com)

print "Running DeconSeq"
call("ln -s ../db", shell=True)
call("ln -s ../deconseq.pl", shell=True)
call("ln -s ../bwa64", shell=True)
call("ln -s ../DeconSeqConfig.pm", shell=True)
for command in commands:
    processes = [Popen(cmd, shell=True) for cmd in command]
    for p in processes:
        p.wait()

for n in range(1,2):
    concat = ["cat"]
    for fq in splits:
        if fq.startswith("tmp_queries_%s" % (str(n))):
            concat.append("%s.dir/*clean*" % (fq))
    call("%s > %s_clean.fastq" % (" ".join(concat), filename), shell=True)

call("rm db deconseq.pl bwa64 DeconSeqConfig.pm", shell=True)
call("rm tmp_queries*.fastq", shell=True)
call("rm -r tmp_queries*.fastq.dir", shell=True)
call("rm %s" % (file1), shell=True)
os.chdir("../../")

call("mv %s/%s ." % (dsdir,filename), shell=True)

if ext1[-1] == "gz":
    call("rm %s" % (file1), shell=True)

call("rm -r %s" % dsdir, shell=True)
statler:/vol/animalbehaviour/sat_miner_Gsib_test_SE> cat ~/bin/SE_rexp_prepare.py
#!/usr/bin/python

import sys, os
from subprocess import call

print "\nUsage: SE_rexp_prepare.py NumberOfPairedReads File.fastq MinQual MinLen [PREFIX]\n"

##read parameters
#number of reads
try:
    sel_reads = sys.argv[1]
    sel_reads = int(sel_reads)
except:
    sel_reads = raw_input("Number of reads you want select: ")
    sel_reads = int(sel_reads)

#FASTQ files
try:
    r1 = sys.argv[2]
except:
    r1 = raw_input("FASTQ file 1: ")

try:
    mq = sys.argv[3]
    ml = sys.argv[4]
except:
    ml = 101
    mq = 30

#prefix
try:
    prefix = sys.argv[5]
except:
    prefix = ""

#list of files in the current directory
files = [f for f in os.listdir(".") if os.path.isfile(f)]

#files names
rr1 = r1.find(".")
suffix = r1[rr1:]
rr1 = r1[:rr1]
#rrr1 = r1.find("_")
#rrr1 = r1[:rrr1]

print rr1

#with open(r1) as myfile:
#    head = [next(myfile) for x in xrange(2)]
#len_reads = str(len(head[1])-1)

#Trimming with Trimmomatic

#trimmomatic = "trimmomatic SE -phred33 %s %s ILLUMINACLIP:/usr/local/lib/Trimmomatic-0.32/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:%s MINLEN:%s" % (r1, rr1+"_paired.fastq", mq, ml)
trimmomatic = "trimmomatic SE -phred33 %s %s ILLUMINACLIP:/homes/ashah/install_files/Trimmomatic-0.36/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:%s MINLEN:%s" % (r1, rr1+"_single_end.fastq", mq, ml)

print trimmomatic

#random selection of reads

fastq_random_1 = "seqtk sample -s 100 %s %s > %s" % (rr1+"_single_end.fastq",sel_reads,rr1+"_single_end.fastq.subset")

#convert fastq to fasta
fastq_to_fasta =  "seqtk seq -a %s > %s" % (rr1+"_single_end.fastq.subset",rr1+"_all_"+prefix+str(sel_reads)+".fasta")

#Try to run Trimmomatic

if rr1+"_single_end.fastq" not in files:
    try:
        print "Running Trimmomatic\n"
        print trimmomatic
        call(trimmomatic, shell = True)
    except:
        print "Trimmomatic could not run. Try again.\n"
else:
    print "Trimmomatic was already run. Skipping.\n"

#Try to run fastq pe random
try:
    print "Running Fastq-random"
    print fastq_random_1
    call(fastq_random_1, shell = True)
except:
    print "Fastq-random could not run. Try again.\n"

#Try to convert to fasta format
try:
    print "Running Fastq to fasta"
    print fastq_to_fasta
    call(fastq_to_fasta, shell = True)
except:
    print "Fastq to fasta could not run. Try again.\n"

#open output
fatemp = open("%s_all_%s%s_temp.fasta" % (rr1,prefix,str(sel_reads)) ,"w")

#read modified fasta file
print "Editing "+ rr1+"_all_"+prefix+str(sel_reads)+".fastq\n"
fasta = open(rr1+"_all_"+prefix+str(sel_reads)+".fasta").readlines()

#add prefix
for x in range(0,len(fasta)):
    if x%2 == 0:
        line = fasta[x]
        line = line.split(">")
        line = ">%s%s" % (prefix,line[1])
    else:
        line = fasta[x]
    fatemp.write(line)

fatemp.close()

call("mv %s %s" % (rr1+"_all_"+prefix+str(sel_reads)+"_temp.fasta",rr1+"_all_"+prefix+str(sel_reads)+".fasta"), shell=True)

print "\nWe\'re done!\n"
statler:/vol/animalbehaviour/sat_miner_Gsib_test_SE> cat ~/bin/fast
fasta36                      fastq-clipper                fastq-multx                  fastx36
fastacmd                     fastq_edit_ids.py            fastq_paired_combine_id.bak  fastx-graph
fasta-splitter.pl            fastq_edit_ids_sra.py        fastq_paired_combine_id.py   fasty36
fasta_to_fastq.pl            fastq-interleave             fastq-stats
fastf36                      fastq-join                   fasts36
fastm36                      fastq-mcf                    fastuniq
statler:/vol/animalbehaviour/sat_miner_Gsib_test_SE> cat ~/bin/fastq_paired_combine_id.py
#!/usr/bin/python

import sys
from subprocess import call

print "Usage: fastq_paired_combine_id.py file_1.fastq file_2.fastq"

try:
    one = sys.argv[1]
except:
    one = raw_input("Introduce FASTQ file 1: ")

try:
    two = sys.argv[2]
except:
    two = raw_input("Introduce FASTQ file 2: ")

get_reads = """awk 'NR == 1 || NR % 4 == 1' """
trim_reads = """awk '{print substr($0,2, length($0))}' """
#trim_reads = """awk '{print $0}' """

files = sys.argv[1:3]

print "Getting read names"
for file in files:
    call(get_reads + "%s > %s" % (file, file+".r"), shell=True)
    call(trim_reads + "%s > %s" % (file+".r", file+".t"), shell=True)
    call("rm %s" % (file+".r"), shell=True)

one_data = open(files[0]+".t").readlines()
two_data = open(files[1]+".t").readlines()

print "Getting common reads"
commun = set(one_data) & set(two_data)

call("rm %s.t %s.t" % (files[0], files[1]), shell=True)

name = files[0]
name = name.split(".")
name = ".".join(name[:-1])
name = name[:-2]

out = open(name+".list", "w")
for el in commun:
    out.write("%s/1\n%s/2\n" % (el[:-1], el[:-1]))
out.close()

print "Extracting reads from original files"
call("seqtk subseq %s %s.list > %s_paired_1.fastq" % (one,name,name), shell=True)
call("seqtk subseq %s %s.list > %s_paired_2.fastq" % (two,name,name), shell=True)

call("rm %s.list" % (name), shell=True)

print "We're done!"
