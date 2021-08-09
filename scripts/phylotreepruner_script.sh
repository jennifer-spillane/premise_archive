#! /bin/bash

#We want to run PhyloTree Pruner but have too many orthogroups, so we filter them down based on how many missing taxa they have.
#use get_og_list_min_taxa.py to filter down the orthogroup list, and then pull_alignments.py to get the alignments in their own di$

/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/get_og_list_min_taxa.py \
-c /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthogroups.GeneCount.csv \
-o /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/passing_og_names.txt \
-m 1

/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/pull_alignments.py \
-l /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/passing_og_names.txt \
-a /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/Alignments/ \
-n /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_alignments/


#now I have to pull out the trees that correspond to the alignments

mkdir /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_trees

for file in /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_alignments/*.fa
do
    fanamepath=${file%.fa}
    faname=${fanamepath##*/}
    #echo $faname
        if [ -s /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/Gene_Trees/${faname}_tree.txt ]
        treefile=/mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/Gene_Trees/${faname}_tree.txt
        then cp $treefile /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_trees
        fi
done

#and run PhyloTree Pruner on the desired OGs

parallel -j14 --xapply 'PhyloTreePruner {1} 10 {2} 0.5 u' :::  \
/mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_trees/*_tree.txt :::  \
/mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_alignments/*.fa

mkdir /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned; \
mv /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/top_alignments/*pruned* \
/mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned

#align pruned OGs

parallel -j14 'mafft --auto {} > {.}_aln'  ::: /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned/*.fa

#trim alignments

parallel -j14 '/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/gblocks_wrapper.pl {}' ::: \
/mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned/*_aln

rm *.htm

#re-align trimmed alignments

parallel -j14 'mafft --auto {} > {.}_gb.aln' ::: /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned/*gb

rm *htm

#cut off OG idenfier, leaving only species label so that seqCat can concatenate

parallel -j14 'cut -f1 -d"|" {} > {.}_rename' ::: /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned/*_gb.aln

#concatenate all OGs into single nexus

ls /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/pruned/*_rename > /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/parts_list

/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/seq_cat.pl -d /mnt/lustre/macmaneslab/jlh1023/phylo_qual/small_test/bad/bad_prots/Results_Apr18/Orthologues_Apr18/parts_list
