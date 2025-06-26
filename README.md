# g2bp

**G2BP**: A GFF to gene BED Converter driven by Protein ID.

## Version
Current version: `v1.3.0`

## Install

```
pip3 install git+https://github.com/tamasakian/g2bp.git
```

If you want to install in editable mode,

```
pip3 install -e git+https://github.com/tamasakian/g2bp.git#egg=g2bp
```

## Usage

Create a gene BED file using Protein IDs.  
Protein IDs are loaded from text or FASTA files.

For text files (one per line):

```
python3 -m g2bp txt [GFF filename] [BED filename] [Protein ID filename]
```

For FASTA files (sequence name in header):

```
python3 -m g2bp fasta [GFF filename] [BED filename] [Protein ID filename]
```

If you want to use MCScanX, you can change the output format to MCScanX compatible BED format.

```
python3 -m g2bp fasta4mcscanx [GFF filename] [BED filename] [Protein ID filename]
```
