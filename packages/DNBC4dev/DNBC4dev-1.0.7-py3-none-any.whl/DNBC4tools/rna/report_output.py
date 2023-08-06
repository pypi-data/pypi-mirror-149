import os,argparse,shutil,glob

parser = argparse.ArgumentParser()
parser.add_argument('-i','--indir', metavar='FILE',default=os.getcwd())
parser.add_argument('--no_bam', action='store_true', help='Do not generate a bam file')
args = parser.parse_args()
indir = args.indir

output = os.path.join(indir,'output')
os.system('mkdir -p %s/output'%indir)

def summary_file(indir):
    if os.path.exists("%s/02.count/filter_matrix"%indir):
        shutil.copytree("%s/02.count/filter_matrix"%indir,'%s/output/filter_matrix'%indir,dirs_exist_ok=True)
    if os.path.exists("%s/01.data/raw_matrix"%indir):
        shutil.copytree("%s/01.data/raw_matrix"%indir,'%s/output/raw_matrix'%indir,dirs_exist_ok=True)
    # if os.path.exists('%s/02.count/saturation.png'%indir):
    #     os.makedirs('%s/output/analysis/saturation'%indir, exist_ok=True)
    #     shutil.copy("%s/02.count/saturation.png"%indir,'%s/output/analysis/saturation'%indir)
    #     shutil.copy("%s/02.count/saturation.xls"%indir,'%s/output/analysis/saturation'%indir)
    # if os.path.exists('%s/02.count/beads_count_summary.png'%indir):
    #     os.makedirs('%s/output/analysis/beads'%indir, exist_ok=True)
    #     shutil.copy("%s/02.count/beads_count_summary.png"%indir,'%s/output/analysis/beads'%indir)
    #     shutil.copy("%s/02.count/cellNumber_merge.png"%indir,'%s/output/analysis/beads'%indir)
    if os.path.exists('%s/03.analysis/Clustering/clustering_plot.png'%indir):
        os.makedirs('%s/output/analysis/umap'%indir, exist_ok=True)
        shutil.copy("%s/03.analysis/Clustering/clustering_plot.png"%indir,'%s/output/analysis/umap'%indir)
    if os.path.exists('%s/03.analysis/Clustering/cluster.csv'%indir):
        os.makedirs('%s/output/analysis/clustering'%indir, exist_ok=True)
        shutil.copy("%s/03.analysis/Clustering/cluster.csv"%indir,'%s/output/analysis/clustering'%indir)
        shutil.copy("%s/03.analysis/Clustering/cluster_cell.stat"%indir,'%s/output/analysis/clustering'%indir)
    if os.path.exists('%s/03.analysis/Clustering/cluster_annotation.png'%indir):
        os.makedirs('%s/output/analysis/annotation'%indir, exist_ok=True)
        shutil.copy("%s/03.analysis/Clustering/cluster_annotation.png"%indir,'%s/output/analysis/annotation'%indir)
    if os.path.exists('%s/03.analysis/Clustering/marker.csv'%indir):
        os.makedirs('%s/output/analysis/diffexp'%indir, exist_ok=True)
        shutil.copy("%s/03.analysis/Clustering/marker.csv"%indir,'%s/output/analysis/diffexp'%indir)
    if os.path.exists('%s/04.report/metrics_summary.xls'%indir):
        shutil.copy("%s/04.report/metrics_summary.xls"%indir,'%s/output'%indir)

def glob_file(indir):
    html_list = glob.glob('%s/04.report/*.html'%indir)
    if html_list:
        shutil.copy("%s"%html_list[0],'%s/output'%indir)

def main():
    if args.no_bam:
        pass
    else:
        # if os.path.exists('%s/01.data/final.bam'%indir):
        #     if(os.path.exists("%s/output/raw_feature.bam"%indir)):
        #         os.remove("%s/output/raw_feature.bam"%indir)
        #     shutil.move("%s/01.data/final.bam"%indir,'%s/output/raw_feature.bam'%indir)
        if os.path.exists('%s/02.count/anno_decon.bam'%indir):
            if(os.path.exists("%s/output/filter_feature.bam"%indir)):
                os.remove("%s/output/filter_feature.bam"%indir)
            shutil.move("%s/02.count/anno_decon.bam"%indir,'%s/output/filter_feature.bam'%indir)
    summary_file(indir)
    glob_file(indir)

if __name__ == '__main__':
    main()

    
