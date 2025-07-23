import csv
from datetime import datetime

# === Setup filenames with date ===
today = datetime.today().strftime("%Y%m%d")
input_file = "predicted_topologies.3line"
output_file = f"predicted_topologies_{today}.csv"
tm_output_file = f"predicted_topologies_TM_only_{today}.csv"
distinct_pdb_file = f"distinctPDBTM_{today}.csv"

# === Initialize storage ===
all_rows = []
tm_rows = []
pdb_ids = set()

# === Parse input file ===
with open(input_file, "r") as infile:
    lines = infile.read().splitlines()

    for i in range(0, len(lines), 3):
        if i + 2 >= len(lines):
            break

        header = lines[i].strip()
        sequence = lines[i + 1].strip()
        topology = lines[i + 2].strip()

        if not header.startswith(">"):
            continue

        parts = header[1:].split("|")
        pdb_chain_id = parts[0].strip()        # e.g., 9CDT_1
        protein_type = parts[-1].strip()       # e.g., GLOB, SP+TM, TM

        row = [pdb_chain_id, protein_type, sequence, topology]
        all_rows.append(row)

        if protein_type in ["TM", "SP+TM"]:
            tm_rows.append(row)
            pdb_id = pdb_chain_id.split("_")[0]  # extract just the PDB ID (e.g., 9CDT)
            pdb_ids.add(pdb_id)

# === Write all rows ===
with open(output_file, "w", newline="") as out_csv:
    writer = csv.writer(out_csv)
    writer.writerow(["ID", "Type", "Sequence", "Topology"])
    writer.writerows(all_rows)

# === Write TM/SP+TM rows ===
with open(tm_output_file, "w", newline="") as tm_csv:
    writer = csv.writer(tm_csv)
    writer.writerow(["ID", "Type", "Sequence", "Topology"])
    writer.writerows(tm_rows)

# === Write distinct PDB IDs ===
with open(distinct_pdb_file, "w", newline="") as pdb_csv:
    writer = csv.writer(pdb_csv)
    writer.writerow(["PDB_ID"])
    for pdb in sorted(pdb_ids):
        writer.writerow([pdb])

# === Done ===
print(f"All entries saved to: {output_file}")
print(f"TM and SP+TM entries saved to: {tm_output_file}")
print(f"Distinct PDB IDs saved to: {distinct_pdb_file}")