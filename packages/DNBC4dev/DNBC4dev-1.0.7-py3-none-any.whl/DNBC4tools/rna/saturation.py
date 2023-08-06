#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse,os,pathlib
parser = argparse.ArgumentParser(description='sequencing saturation')
parser.add_argument('-i','--inbam', metavar='FILE', type=str,help='input anno_decon.bam')
parser.add_argument('-o','--outdir',help='storage outfile')
parser.add_argument('-q','--quality',type=int, default=20, help='Minimal map quality to filter. Default is 20')
parser.add_argument('-@','--threads',type=int, default=10, help='Analysis threads. Default is 10')
args = parser.parse_args()

inbam = args.inbam
outdir = pathlib.Path(args.outdir)
quality = args.quality
threads = args.threads

'''
umi_saturation = 1-(细胞基因UMI对应的reads仅为1条的组合数目/细胞基因UMI的全部组合数目)
sequencing_saturation = 1-(细胞基因UMI的全部组合数目/比对上细胞基因UMI的全部reads数量)
'''

import pysam,time
import pandas as pd
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as ticker
from scipy.interpolate import make_interp_spline
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

def time_print(str):
	print("\033[32m%s\033[0m %s"%(time.strftime('[%H:%M:%S]',time.localtime(time.time())), str))

def count_result(in_bam,out_dir):
    with open(os.path.join(out_dir,"cell_count_detail.xls"), 'w') as result:
        result.write('\t'.join(['Cell', 'GeneID', 'UMI', 'Count']) + '\n')
        with pysam.AlignmentFile(in_bam, 'rb') as bam:
            gene_umi_dict = defaultdict(lambda:defaultdict(lambda: defaultdict(int)))
            for line in bam:
                if int(line.flag) & 2304 != 0:
                    continue
                elif line.mapping_quality < quality or not line.has_tag('GN') :
                    cell = 'None'
                    gene = 'None'
                    umi = 'None'
                else:
                    cell = line.get_tag('DB')
                    gene = line.get_tag('GN')
                    umi = line.get_tag('UB')
                gene_umi_dict[cell][gene][umi] += 1
            for cell in gene_umi_dict:
                for gene in gene_umi_dict[cell]:
                    for umi in gene_umi_dict[cell][gene]:
                        result.write('%s\t%s\t%s\t%s\n'%(cell,gene,umi,gene_umi_dict[cell][gene][umi]))

def fraction_reads(outdir):
    cellcount_df = pl.read_csv(
        os.path.join(outdir,"cell_count_detail.xls"),
        has_headers=True,
        sep='\t',
        use_pyarrow=False,
        n_threads=threads,
        ).with_columns(
            [
            pl.col("Cell").cast(pl.Categorical),
            pl.col("GeneID"),
            pl.col("UMI").cast(pl.Categorical),
            pl.col("Count").cast(pl.UInt32),
            ]
            )
    sampling_fractions = [0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    sampling_fractions_length = len(sampling_fractions)
    stats_df = pd.DataFrame(
        {
            "Mean Reads per Cell": np.zeros(sampling_fractions_length, np.float64),
            "Median Genes per Cell": np.zeros(sampling_fractions_length, np.uint32),
            "Mean Gene per Cell": np.zeros(sampling_fractions_length, np.float64),
            "Total Gene": np.zeros(sampling_fractions_length, np.uint32),
            "Sequencing Saturation": np.zeros(sampling_fractions_length, np.float64),
            "UMI Saturation": np.zeros(sampling_fractions_length, np.float64),
        },
        index=pd.Index(data=np.array(sampling_fractions), name="sampling_fraction"),
        )
    cellcount_all_df = cellcount_df.with_column(pl.col("Count").repeat_by(pl.col("Count"))).explode("Count")
    stats_df.loc[1.0, "Mean Reads per Cell"] = cellcount_df.sum().select(pl.col("Count"))[0,0]/(pl.n_unique(cellcount_df['Cell'])-1)
    stats_df.loc[1.0, "UMI Saturation"] = (1- (cellcount_df.filter(pl.col("Count") == 1).height)/(cellcount_df.height-1))*100
    stats_df.loc[1.0, "Sequencing Saturation"] = (1- (cellcount_df.height-1)/cellcount_df.filter(pl.col('Cell')!='None').select([pl.col("Count").sum()])[0,0])*100
    cellcount_df = cellcount_df.with_column(pl.col("GeneID").str.split(";")).explode("GeneID")
    stats_df.loc[1.0, "Median Genes per Cell"] = cellcount_df.filter(pl.col('Cell')!='None').groupby("Cell").agg(
            [pl.n_unique(['GeneID']).alias("MedianGene")]).select([pl.col("MedianGene").median()])["MedianGene"][0]
    stats_df.loc[1.0, "Mean Gene per Cell"] = cellcount_df.filter(pl.col('Cell')!='None').groupby("Cell").agg(
            [pl.n_unique(['GeneID']).alias("MeanGene")]).select([pl.col("MeanGene").mean()])["MeanGene"][0]
    stats_df.loc[1.0, "Total Gene"] = pl.n_unique(cellcount_df['GeneID'])-1
    # numberCell = pl.n_unique(cellcount_df['Cell'])-1
    # readsPerCell = round(stats_df.loc[1.0, "Mean Reads per Cell"])
    # meanUMI = round(cellcount_df.filter(pl.col('Cell')!='None').groupby("Cell").agg(
    #         [pl.count(['UMI']).alias("MeanUMI")]).select([pl.col("MeanUMI").mean()])["MeanUMI"][0])
    # medianUMI = round(cellcount_df.filter(pl.col('Cell')!='None').groupby("Cell").agg(
    #         [pl.count(['UMI']).alias("MedianUMI")]).select([pl.col("MedianUMI").median()])["MedianUMI"][0])
    # totalGene = stats_df.loc[1.0, "Total Gene"]
    # meanGene = round(stats_df.loc[1.0, "Mean Gene per Cell"])
    # meadianGene = round(stats_df.loc[1.0, "Median Genes per Cell"])
    # saturation = round(stats_df.loc[1.0, "Sequencing Saturation"],2)
    # count_report = open(os.path.join(outdir,"cellCount_report.csv"),'w')
    # count_report.write('Estimated Number of Cell,%s'%numberCell+'\n')
    # count_report.write('Mean reads per cell,%s'%readsPerCell+'\n') 
    # count_report.write('Mean UMI counts per cell,%s'%meanUMI+'\n')
    # count_report.write('Median UMI Counts per Cell,%s'%medianUMI+'\n')
    # count_report.write('Total Genes Detected,%s'%totalGene+'\n')
    # count_report.write('Mean Genes per Cell,%s'%meanGene+'\n')
    # count_report.write('Median Genes per Cell,%s'%meadianGene+'\n')
    # count_report.write('Sequencing Saturation,%s'%saturation+'\n')
    # count_report.close()
    del cellcount_df

    for sampling_fraction in sampling_fractions:
        if sampling_fraction == 0.0:
            continue
        elif sampling_fraction == 1.0:
            continue
        else:
            cellcount_sampled=cellcount_all_df.sample(frac=sampling_fraction)
            cellcount_sampled=cellcount_sampled.groupby(["Cell", "GeneID","UMI"]).agg([pl.col("UMI").count().alias("Count")])
            stats_df.loc[sampling_fraction, "Mean Reads per Cell"] = cellcount_sampled.sum().select(pl.col("Count"))[0,0]/(pl.n_unique(cellcount_sampled['Cell'])-1)
            stats_df.loc[sampling_fraction, "UMI Saturation"] = (1- (cellcount_sampled.filter(pl.col("Count") == 1).height)/(cellcount_sampled.height-1))*100
            stats_df.loc[sampling_fraction, "Sequencing Saturation"] = (1- (cellcount_sampled.height-1)/cellcount_sampled.filter(pl.col('Cell')!='None').select([pl.col("Count").sum()])[0,0])*100
            cellcount_sampled = cellcount_sampled.with_column(pl.col("GeneID").str.split(";")).explode("GeneID")
            stats_df.loc[sampling_fraction, "Median Genes per Cell"] = cellcount_sampled.filter(pl.col('Cell')!='None').groupby("Cell").agg(
                    [pl.n_unique(['GeneID']).alias("MedianGene")]).select([pl.col("MedianGene").median()])["MedianGene"][0]
            stats_df.loc[sampling_fraction, "Mean Gene per Cell"] = cellcount_sampled.filter(pl.col('Cell')!='None').groupby("Cell").agg(
                    [pl.n_unique(['GeneID']).alias("MeanGene")]).select([pl.col("MeanGene").mean()])["MeanGene"][0]
            stats_df.loc[sampling_fraction, "Total Gene"] = pl.n_unique(cellcount_sampled['GeneID'])-1
            del cellcount_sampled
    del cellcount_all_df
    stats_df.to_csv(os.path.join(outdir,"saturation.xls"),sep='\t')

def main():
    time_print("count reads")
    count_result(inbam,outdir)
    time_print("Analysis saturation")
    fraction_reads(outdir)
    time_print("plot saturation")
    plot_saturation()
    time_print("Analysis complete")

def to_percent(temp,position):
    return '%d'%(temp/1000) + 'k'

def umi_saturation(ax,table):
    xnew = np.linspace(table['Mean Reads per Cell'].min(),table['Mean Reads per Cell'].max(),300)
    smooth = make_interp_spline(table['Mean Reads per Cell'],table['Sequencing Saturation']/100)(xnew)
    ax.set_xlim([0, table['Mean Reads per Cell'].max()])
    ax.set_ylim([0, 0.9999])
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(to_percent))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.spines['right'].set_visible(False) 
    ax.spines['top'].set_visible(False)
    ax.grid(linestyle='--')
    ax.plot(xnew,smooth,linewidth=3.0)
    ax.axhline(y=0.9,ls="--",c="black",linewidth=2.0)
    ax.set(xlabel='Mean Reads per Cell', ylabel='Sequencing Saturation',title='Sequencing Saturation')

def gene_saturation(ax,table):
    xnew = np.linspace(table['Mean Reads per Cell'].min(),table['Mean Reads per Cell'].max(),300)
    smooth = make_interp_spline(table['Mean Reads per Cell'],table['Median Genes per Cell'])(xnew)
    ax.set_xlim([0, table['Mean Reads per Cell'].max()])
    ax.set_ylim([0, table['Median Genes per Cell'].max()])
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(to_percent))
    ax.yaxis.set_major_locator(MaxNLocator(4))
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.spines['right'].set_visible(False) 
    ax.spines['top'].set_visible(False)
    ax.grid(linestyle='--')
    ax.plot(xnew,smooth,linewidth=3.0)
    ax.set(xlabel='Mean Reads per Cell', ylabel='Median Gene per Cell',title='Median Gene per Cell')

def plot_saturation():
    for_plot = pd.read_table(outdir/'saturation.xls',sep='\t')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), tight_layout=True)
    arts = umi_saturation(ax1,for_plot)
    arts = gene_saturation(ax2,for_plot)
    fig.savefig(outdir/'saturation.png',facecolor='white',transparent=False,dpi=400)
    plt.close(fig)

if __name__=='__main__':
    main()
