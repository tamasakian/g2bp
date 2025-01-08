#!/usr/bin/env python3

from collections import defaultdict

"""
Function Library.

Functions:
    convert: Convert a genome GFF3 file -> a gene BED file.

"""

def convert(gff_file: str, bed_file: str, protein_file: str) -> None:
    """
    Convert a genome GFF3 file to a gene BED file.

    Args:
        gff_file: Path to the input genome GFF file.
        bed_file: Path to the output gene BED file.
        protein_file: Path to the input text file containing Protein IDs.
    """

    def load_protein_ids(protein_file: str) -> list:
        """
        Parse protein_file to generate a list of Protein IDs.

        Returns:
            list: A list of Protein IDs parsed from protein_file.
        """
        protein_set = set()
        with open(protein_file, "r") as protein_handle:
            for line in protein_handle:
                if line.startswith("#"):
                    continue
                protein_id = line.strip()
                if not protein_id:
                    continue
                protein_set.add(protein_id)

        return list(protein_set)

    def load_gene_coordinates(gff_file: str) -> dict:
        """
        Parse gff_file to store gene coordinates in a dictionary.

        Returns:
            dict: A dictionary where the keys are sequence names
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
                    gene_dict[seq_name].append((start, end))

        return gene_dict

    def load_cds_attributes(gff_file: str, protein_list: list, gene_dict: dict) -> list:
        """
        Parse gff_file to generate bed_file.

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
                            if int(gene_start) <= int(start) and int(end) <= int(gene_end):
                                bed_list.append([seq_name, str(gene_start), str(gene_end), protein_id])
                                protein_list.remove(protein_id)
                                break

        return bed_list

    def write_bed_file(bed_file: str, bed_list: list) -> None:
        """
        Write bed_file.

        """
        with open(bed_file, "w") as bed_handle:
            for bed_entry in bed_list:
                bed_handle.write("\t".join(bed_entry) + "\n")

    protein_list = load_protein_ids(protein_file=protein_file)
    gene_dict = load_gene_coordinates(gff_file=gff_file)
    bed_list = load_cds_attributes(
        gff_file=gff_file,
        protein_list=protein_list,
        gene_dict=gene_dict)

    write_bed_file(bed_file=bed_file, bed_list=bed_list)

