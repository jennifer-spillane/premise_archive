#! /usr/bin/env Rscript

###For using as a subprocess in python.
###Should do the same thing as the dollo_compare_metdata.R script.

#install.packages("phytools")
require(phytools)
packageVersion("phytools")

arguments <- commandArgs(trailingOnly = TRUE)
data_for_r <- paste0(arguments[1], "_for_r.csv", collapse = NULL)

#reading in the necessary data
flush.console()
tr <- read.tree("/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling/tree.new")
firstdata<-read.csv(data_for_r, stringsAsFactors=FALSE, header=T, row.names=1, sep="\t")
metdata <- as.data.frame(t(firstdata))

#rooting the tree correctly
mettree <- ladderize(reroot(tr,node=4,position=0.1))

rownames(metdata) <- sapply(strsplit(as.character(rownames(metdata)), "_"), `[`, 1)
row.names(metdata) <- mettree$tip.label
mettree$states <- metdata[,1]
names(mettree$states) <- rownames(metdata)

foo<-function(x){
  y<-sapply(x$maps,function(x) names(x)[1])
  names(y)<-x$edge[,1]
  y<-y[as.character(length(x$tip)+1:x$Nnode)]
  return(y)
}

cust_model <- matrix(c(0,2,1,0),2,2)
mtrees2 <- make.simmap(mettree, mettree$states, model = cust_model, nsim=100, pi=c(0.99,0.01))
AA <- sapply(mtrees2, foo)
important <- t(apply(AA, 1, function(x, levels, Nsim) summary(factor(x, levels))/Nsim, levels = levels(factor(mettree$states)), Nsim=100))

out_from_r <- paste0(arguments[1], "_from_r.csv", collapse = NULL)
write.table(important, file = out_from_r, sep = "\t", row.names = T)
