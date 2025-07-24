#!/usr/bin/env python3

from g2bp import utils

"""
Function Library for G2BP.

Functions:
    txt:   Convert a genome GFF3 file -> a gene BED file using a text  file containing Protein IDs.
    fasta: Convert a genome GFF3 file -> a gene BED file using a FASTA file containing Protein IDs.
    fasta4mcscanx: Convert a genome GFF3 file -> a gene BED file for MCScanX.

"""

def txt(gff_file: str, bed_file: str, protein_file: str) -> None:
    """
    Convert a genome GFF3 file -> a gene BED file using a text file containing Protein IDs.

    Args:
        gff_file: Path to the input genome GFF file.
        bed_file: Path to the output gene BED file.
        protein_file: Path to the input text file containing Protein IDs.
    """

    protein_list = utils.parse_text_file(text_file=protein_file)
    gene_dict = utils.load_gene_coordinates(gff_file=gff_file)
    bed_list = utils.load_cds_attributes(gff_file=gff_file, protein_list=protein_list, gene_dict=gene_dict)
    utils.write_bed_file(bed_file=bed_file, bed_list=bed_list)

def fasta(gff_file: str, bed_file: str, protein_file: str) -> None:
    """
    Convert a genome GFF3 file -> a gene BED file using a FASTA file containing Protein IDs.

    Args:
        gff_file: Path to the input genome GFF file.
        bed_file: Path to the output gene BED file.
        protein_file: Path to the input FASTA file containing Protein IDs.
    """

    protein_list = utils.parse_fasta_file(fasta_file=protein_file)
    gene_dict = utils.load_gene_coordinates(gff_file=gff_file)
    bed_list = utils.load_cds_attributes(gff_file=gff_file, protein_list=protein_list, gene_dict=gene_dict)
    utils.write_bed_file(bed_file=bed_file, bed_list=bed_list)

def fasta4mcscanx(gff_file: str, bed_file: str, protein_file: str) -> None:
    """
    Convert a genome GFF3 file -> a gene BED file for MCScanX.

    Args:
        gff_file: Path to the input genome GFF file.
        bed_file: Path to the output gene BED file.
        protein_file: Path to the input FASTA file containing Protein IDs.
    """
    protein_list = utils.parse_fasta_file(fasta_file=protein_file)
    gene_dict = utils.load_gene_coordinates(gff_file=gff_file)
    bed_list = utils.load_cds_attributes_test(gff_file=gff_file, protein_list=protein_list, gene_dict=gene_dict)
    utils.write_bed_file_mcscanx(bed_file=bed_file, bed_list=bed_list)

