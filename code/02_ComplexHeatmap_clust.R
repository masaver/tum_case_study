# set the working directory
wd = '/Users/masaver/Desktop/masaver/job_applications/TUM/bioinf/case_study/code'
setwd( wd )

# Load Libraries
suppressWarnings( library( ComplexHeatmap ) )
suppressPackageStartupMessages(library(ComplexHeatmap))
suppressWarnings( library(circlize) )
suppressPackageStartupMessages(library(circlize))
suppressWarnings( library( tidyverse ) )
suppressWarnings( library( cluster ) )
suppressWarnings( library( factoextra ) )

# Read the data
corr_df = read_csv( 'correlation_matrix.csv' )
row_names = unlist( corr_df[,1] )
corr_df[,1] = NULL
rownames( corr_df ) = row_names

#Reaad the metadata
metadata = read_csv( 'metadata.csv' )
row_names = unlist( metadata[,1] )
metadata[,1] = NULL
rownames( metadata ) = row_names

# Verify the order of rows and columns
all.equal( rownames( metadata ) , rownames( corr_df ) )
all.equal( rownames( metadata ) , colnames( corr_df ) )

# find the optimal number of clusters
png('elbow_method_analysis.png')
fviz_nbclust( corr_df , hcut, method = "wss")
dev.off()

#Heatmap color scales and annotations
col_fun = colorRamp2(c(0, 0.5, 1), c("blue", "white", "red"))
hm_anno = HeatmapAnnotation( df = metadata[,c('tumor_stage_pathological','histologic_type','age_cat')] )

#Create the heatmap
hm.plot = Heatmap(
  corr_df , 
  show_row_names = F ,
  show_column_names = F , 
  col = col_fun ,
  row_split = 3 , 
  column_split = 3 ,
  top_annotation = hm_anno
)

png('3clusters_heatmap.png')
plot( hm.plot )
dev.off()
