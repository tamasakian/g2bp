#!/usr/bin/env python3

from collections import defaultdict

"""
Function Library for functions.py.

Functions:
    parse_text_file:  Parse text_file  to generate a list of Protein IDs.
    parse_fasta_file: Parse fasta_file to generate a list of Protein IDs.
    load_gene_coordinates: Parse gff_file to store gene coordinates in a dictionary.
    load_cds_attributes: Parse gff_file to map Protein IDs to their corresponding gene coordinates.
    write_bed_file: Write the BED file.

"""

def parse_text_file(text_file: str) -> list:
    """
    Parse text_file to generate a list of Protein IDs.

    Args:
        text_file: Path to the input text file.

    Returns:
        list: A list of Protein IDs parsed from text_file.
    """
    protein_set = set()
    with open(text_file, "r") as protein_handle:
        for line in protein_handle:
            if line.startswith("#"):
                continue
            protein_id = line.strip()
            if not protein_id:
                continue
            protein_set.add(protein_id)

    return list(protein_set)

def parse_fasta_file(fasta_file: str) -> list:
    """
    Parse fasta_file to generate a list of Protein IDs.

    Args:
        fasta_file: Path to the input FASTA file.

    Returns:
        list: A list of Protein IDs parsed from fasta_file.
    """
    protein_set = set()
    with open(fasta_file, "r") as fasta_handle:
        for line in fasta_handle:
            if line.startswith(">"):
                header = line.strip().lstrip(">")
                protein_id = header.split()[0]
                protein_set.add(protein_id)

    return list(protein_set)

def load_gene_coordinates(gff_file: str) -> dict:
    """
    Parse gff_file to store gene coordinates in a dictionary.

    Args:
        gff_file: Path to the input genome GFF file.

    Returns:
        dict: A dictionary where the keys are sequence names.
    """
    gene_dict = defaultdict(list)
    with open(gff_file, "r") as gff_handle:
        for line in gff_handle:
            if line.startswith("#"):
                continue
            li = line.strip().split("\t")
            if len(li) != 9:
                continue
            seq_name, source, feature, start, end, score, strand, phase, attributes = li

            if feature == "gene":
                gene_dict[seq_name].append((int(start), int(end)))

    return gene_dict


def load_cds_attributes(gff_file: str, protein_list: list, gene_dict: dict) -> list:
    """
    Parse gff_file to generate a BED file.

    Args:
        gff_file: Path to the input genome GFF file.
        protein_list: A list of protein IDs to match.
        gene_dict: A dictionary with gene coordinates.

    Returns:
        list: A list of genes in BED format.
    """
    bed_list = []
    with open(gff_file, "r") as gff_handle:
        for line in gff_handle:
            if line.startswith("#"):
                continue
            li = line.strip().split("\t")
            if len(li) != 9:
                continue
            seq_name, source, feature, start, end, score, strand, phase, attributes = li

            if feature == "CDS":
                for protein_id in list(protein_list):
                    if f"protein_id={protein_id}" not in attributes:
                        continue
                    if seq_name not in gene_dict:
                        continue
                    for gene_start, gene_end in gene_dict[seq_name]:
                        if gene_start <= int(start) and int(end) <= gene_end:
                            gene_start = int(gene_start) - 1
                            bed_list.append([seq_name, str(gene_start), str(gene_end), protein_id])
                            protein_list.remove(protein_id)
                            break

    return bed_list


def write_bed_file(bed_file: str, bed_list: list) -> None:
    """
    Write the BED file.

    Args:
        bed_file: Path to the output BED file.
        bed_list: A list of BED entries.
    """
    with open(bed_file, "w") as bed_handle:
        for bed_entry in bed_list:
            bed_handle.write("\t".join(bed_entry) + "\n")
