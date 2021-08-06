#! /usr/bin/env Rscript

###For using as a subprocess in python.
###Should do the same thing as the ace_dollo.R script.

#install.packages("ape")
require(phytools)

arguments <- commandArgs(trailingOnly = TRUE)
data_for_r <- paste0(arguments[1], "_for_r.csv", collapse = NULL)

flush.console()
roottree <- read.tree(file = "/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling/tree.new")
firstdata<-read.csv(data_for_r, stringsAsFactors=FALSE, header=T, row.names=1, sep="\t")
metdata <- as.data.frame(t(firstdata))

rownames(metdata) <- sapply(strsplit(as.character(rownames(metdata)), "_"), `[`, 1)
row.names(metdata) <- roottree$tip.label
roottree$states <- metdata[,1]
names(roottree$states) <- rownames(metdata)

mettree <- root(roottree, node = 68)

foo<-function(x){
  y<-sapply(x$maps,function(x) names(x)[1])
  names(y)<-x$edge[,1]
  y<-y[as.character(length(x$tip)+1:x$Nnode)]
  return(y)
}

custom_model <- matrix(c(0,2,1,0),2)

ace_trees <- ace(mettree$states, mettree, type = "discrete", "ML",
                 CI = TRUE, model = custom_model)

important <- ace_trees$lik.anc
important
out_from_r <- paste0(arguments[1], "_from_r.csv", collapse = NULL)
write.table(important, file = out_from_r, sep = "\t", row.names = T)
