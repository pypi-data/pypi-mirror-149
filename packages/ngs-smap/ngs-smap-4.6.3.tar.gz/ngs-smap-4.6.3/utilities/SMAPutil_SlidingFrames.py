#!usr/bin/python3

# ===============================================================================
# SMAP_SlidingFrames.py
# ===============================================================================

# Yves BAWIN June 2021
# Python script to create an input file with sliding frames for
# SMAP haplotype-sites (BED) or SMAP haplotype-windows (GFF) based on a VCF file.

# ===============================================================================
# Import modules
# ===============================================================================

import argparse
from datetime import datetime
from natsort import natsorted

# ===============================================================================
# Parse arguments
# ===============================================================================

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Create a BED input file for SMAP haplotype based \
                                                on a VCF file.')

'''Mandatory arguments.'''
parser.add_argument('--bed',
                    type=str,
                    help='Bed file with coordinates from the reference genome sequence. \
                    Three columns are required: contig name (first column), start position \
                    of contig (second column), and stop position of contig (third column).')
parser.add_argument('--vcf',
                    type=str,
                    help='Name of the VCF file with variant coordinates.')

'''Input data options.'''
parser.add_argument('-i', '--input_directory',
                    type=str,
                    default='.',
                    help='Input directory (default = current directory).')

'''Analysis options.'''
parser.add_argument('--format',
                    type=str,
                    choices=['BED', 'GFF'],
                    default='BED',
                    help='Format of the output file. Two options are available: BED \
                    (for SMAP haplotype-sites) and \
                    GFF (for SMAP haplotype-windows) (default = sites).')
parser.add_argument('--border_size',
                    type=int,
                    default=5,
                    help='Size of the borders specified in the output GFF file \
                    (default = 5 base pairs).')
parser.add_argument('--offset',
                    type=int,
                    default=0,
                    help='Size of the offset regions (default = 0 base pairs).')
parser.add_argument('--frame_length',
                    type=int,
                    default=1,
                    help='Maximum frame length, which is automatically reset to the minimum \
                    accepted value (i.e. twice the value of the --offset option) if smaller \
                    than this minimum (default = 1 base pairs).')
parser.add_argument('--frame_distance',
                    type=int,
                    default=0,
                    help="Minimum distance between the 3'-end of the previous frame and the \
                    5'-end of the next frame (default = 0 base pairs).")
parser.add_argument('--variable_border_sequences',
                    dest='variants_in_borders',
                    action='store_true',
                    help='Retain frames with variants in the borders of SMAP haplotype-windows \
                    (default = frames with variable border sequences are removed).')
parser.add_argument('--min_var',
                    type=int,
                    default=1,
                    help='minimal number of neighboring variants per sliding frame \
                    (default = 1 variant).')

'''Output data options.'''
parser.add_argument('-o', '--output_directory',
                    type=str,
                    default='.',
                    help='Output directory (default = current directory).')
parser.add_argument('-s', '--suffix',
                    type=str,
                    default='set_1',
                    help='Suffix added to output files (default = set_1).')

# Parse arguments to a dictionary
args = vars(parser.parse_args())

# ===============================================================================
# Functions
# ===============================================================================


def print_date():

    print('-------------------\n')
    print('{}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('-------------------\n\n')
    return


'''Conversion functions'''


def bed2dict(b=args['bed'], in_d=args['input_directory']):

    ref_dict = dict()
    for seqID in open('{}/{}'.format(in_d, b)):
        seqID = seqID.rstrip().split('\t')
        assert seqID[0] not in ref_dict, 'Contig ID {} is mentioned multiple times in the BED \
        file with the reference genome coordinates. Please make sure that each contig ID \
        is mentioned only once in the BED file.'.format(seqID[0])
        ref_dict[seqID[0]] = [int(seqID[1]) + 1, int(seqID[2])]
    return ref_dict


def vcf2dict(f=args['vcf'], in_d=args['input_directory']):

    variant_dict = dict()
    for SNP in open('{}/{}'.format(in_d, f)):
        if not SNP.startswith('#'):
            SNP = SNP.split('\t')
            if SNP[0] not in variant_dict:
                variant_dict[SNP[0]] = [int(SNP[1])]
            else:
                variant_dict[SNP[0]].append(int(SNP[1]))
    return variant_dict


'''Output function'''


def dict2out(ref_dict, variant_dict, format=args['format'], frame_length=args['frame_length'],
             frame_distance=args['frame_distance'], offset=args['offset'],
             border=args['border_size'], variable_borders=args['variants_in_borders'],
             out_d=args['output_directory'], s=args['suffix'], min_nr_variants=args['min_var']):

    new = open('{}/{}_{}.{}'.format(out_d,
               'Sites' if format == 'BED' else 'Windows', s, format.lower()), 'w+')
    if frame_length < 2 * offset + 1:
        frame_length = 2 * offset + 1
    for chrom in natsorted(list(variant_dict.keys())):
        variants = sorted(variant_dict[chrom])
        i = 0
        # nr_var = 0
        start = offset
        if format == 'windows':
            start += border
            count = 1
        nr_variants = 0
        while i < len(variants):
            if variants[i] > start:
                start = variants[i] - offset
                stop = variants[i] + offset
                while i < len(variants) and variants[i] + offset < start + frame_length:
                    stop = variants[i] + offset
                    i += 1
                    nr_variants += 1
                # only print sliding frame if it contains at least the minimal number of variants
                if nr_variants >= min_nr_variants:
                    if format == 'BED' and stop <= ref_dict[chrom][1]:
                        print('{}\t{}\t{}\t{}\t.\t+\t{},{}\t.\t{}\tShotgun_{}'
                              .format(chrom, start-1, stop, '{}:{}-{}_+'
                                      .format(chrom, start, stop),
                                      start, stop, nr_variants, s), file=new)
                    elif format == 'GFF' and stop + border <= ref_dict[chrom][1]:
                        if variable_borders or \
                            not (any(start - border <= x < start for x in variants)
                                 or any(stop < x <= stop + border for x in variants)):
                            print('{}\tSMAP\tBorder_upstream\t{}\t{}\t.\t+\t.\tName={}:{}-{}_+'
                                  .format(chrom, start - border - 1, start-1, chrom, start, stop),
                                  file=new)
                            print('{}\tSMAP\tBorder_downstream\t{}\t{}\t.\t+\t.\tName={}:{}-{}_+'
                                  .format(chrom, stop + 1, stop + border + 1, chrom, start, stop),
                                  file=new)
                            count += 1
                start = stop + frame_distance + offset
                nr_variants = 0
            else:
                i += 1
    return


# ===============================================================================
# Script
# ===============================================================================


if __name__ == '__main__':
    print_date()

    # Convert BED and VCF files into dictionary.
    print(' * Reading BED file with reference genome coordinates and VCF file with SNP \
    coordinates ...')
    ref_dict = bed2dict()
    variant_dict = vcf2dict()

    # Iterate over contigs and delineate sliding frames
    print(' * Creating input {} file with sliding frames for SMAP haplotypes{} ...'
          .format(args['format'], '-sites' if args['format'] == 'BED' else '-windows'))
    dict2out(ref_dict, variant_dict)

    print(' * Finished!\n')
    print_date()
