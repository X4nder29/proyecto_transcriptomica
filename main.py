from Bio import SeqIO
import os
import subprocess
import multiprocessing

def validate_fasta(fasta_file):
    try:
        with open(fasta_file, "r") as file:
            records = list(SeqIO.parse(file, "fasta"))
            return len(records) > 0
    except Exception as e:
        print(f"Error al validar {fasta_file}: {e}")
        return False

def validate_fastq(fastq_file):
    try:
        with open(fastq_file, "r") as file:
            records = list(SeqIO.parse(file, "fastq"))
            return len(records) > 0
    except Exception as e:
        print(f"Error al validar {fastq_file}: {e}")
        return False

def convert_fasta_to_fastq(fasta_file, fastq_file):
    with open(fastq_file, "w") as fq:
        for record in SeqIO.parse(fasta_file, "fasta"):
            sequence = str(record.seq)
            quality = "I" * len(sequence)
            fq.write(f"@{record.id}\n{sequence}\n+\n{quality}\n")

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {command}: {e}")

def run_fastqc(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    run_command(["fastqc", input_file, "-o", output_dir])
    print(f"Reporte FastQC generado en: {output_dir}")

def run_trimmomatic(input_fastq, output_fastq, trimmomatic_jar, adapters_file):
    output_dir = "trimmed_sequences"
    os.makedirs(output_dir, exist_ok=True)
    output_fastq_path = os.path.join(output_dir, output_fastq)
    trimmomatic_command = [
        "java", "-jar", trimmomatic_jar, "SE", "-phred33",
        input_fastq, output_fastq_path,
        f"ILLUMINACLIP:{adapters_file}:2:30:10",
        "LEADING:3", "TRAILING:3", "SLIDINGWINDOW:4:15", "MINLEN:36"
    ]
    run_command(trimmomatic_command)
    return output_fastq_path

def run_kraken2(input_fastq, output_file, db_path):
    run_command(["kraken2-2.14/kraken2", "--db", db_path, "--output", output_file, "--report", f"{output_file}.report", input_fastq])
    print(f"Kraken 2 completado, resultados en {output_file}")

def run_blast(input_fasta, db_path, output_file):
    run_command(["blastn", "-query", input_fasta, "-db", db_path, "-out", output_file, "-outfmt", "6"])
    print(f"BLAST completado, resultados en {output_file}")

def add_column_headers(report_file):
    headers = """\
Porcentaje de lecturas asignadas (%)\tNúmero de lecturas en este taxón (incluyendo descendientes)\tNúmero de lecturas directamente asignadas a este taxón\tNivel taxonómico\tTaxon ID\tNombre del taxón
"""
    if os.path.exists(report_file):
        with open(report_file, "r") as file:
            lines = file.readlines()

        with open(report_file, "w") as file:
            file.write(headers)
            file.writelines(lines)


def main():
    fasta_path = "MP (2).fas"
    fastq_path = "MP_2.fastq"
    fastqc_initial_output = "fastqc_initial"
    fastqc_final_output = "fastqc_final"
    trimmomatic_jar = "Trimmomatic-0.39/trimmomatic-0.39.jar"
    adapters_file = "Trimmomatic-0.39/adapters/TruSeq3-SE.fa"
    kraken_db = "/home/niespihu/python_bioinformatica/kraken2-2.14/kraken2_db/"
    blast_db = "/path/to/blast_db"
    kraken_output = "kraken2_results.txt"
    blast_output = "blast_results.txt"

    if not os.path.exists(fasta_path) or not validate_fasta(fasta_path):
        raise FileNotFoundError(f"El archivo {fasta_path} no es válido o no existe.")

    convert_fasta_to_fastq(fasta_path, fastq_path)
    
    with multiprocessing.Pool(processes=2) as pool:
        pool.starmap(run_fastqc, [(fastq_path, fastqc_initial_output)])
    
    trimmed_fastq = run_trimmomatic(fastq_path, "MP_2_trimmed.fastq", trimmomatic_jar, adapters_file)
    
    if validate_fastq(trimmed_fastq):
         with multiprocessing.Pool(processes=2) as pool:
            pool.starmap(run_fastqc, [(trimmed_fastq, fastqc_final_output)])
            pool.starmap(run_kraken2, [(trimmed_fastq, kraken_output, kraken_db)])

    # Agregar encabezados al archivo de Kraken2
    add_column_headers(kraken_output + ".report")

    with multiprocessing.Pool(processes=2) as pool:
        pool.starmap(run_blast, [(fasta_path, blast_db, blast_output)])
    
    print("Proceso de control de calidad completado.")

if __name__ == "__main__":
    main()
