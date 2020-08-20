import re
from pathlib import Path

in_file = "idr0090_files.txt"
out_dir = Path("../screens")
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

uod_path = "/uod/idr/filesets/idr0090-ashdown-malaria/20200701-gcloud"

class Plate:
    def __init__(self, name):
        self.name = name
        self.wells = {}
    
    def max_row(self):
        max = 0
        for well in self.wells.values():
            if well.row > max:
                max = well.row
        return max

    def max_col(self):
        max = 0
        for well in self.wells.values():
            if well.col > max:
                max = well.col
        return max

    def n_fields(self):
        for well in self.wells.values():
            return len(well.fields)


class Well:
    def __init__(self, pos):
        self.pos = pos
        self.row = abc.index(pos[0])
        self.col = int(pos[1:]) - 1
        self.fields = []

    def get_fields(self):
        return sorted(self.fields, key=lambda f: f.index)


class Field:
    def __init__(self, index):
        self.index = index
        self.path = ""


plates = {}
exp = "(.+)/NDExp_Well(.{3})_Point00(.{2})_.+"
with open(in_file, "r") as tmp:
    line = tmp.readline()
    while line: # 190129_asexual_withGFP/NDExp_WellC04_Point0026_Seq0570.nd2
        file_name = line.split("/")[1].rstrip()
        search = re.search(exp, line, re.IGNORECASE)
        plate_name = search.group(1).replace("_asexual_withGFP", "")
        well_name = search.group(2)
        field_name = search.group(3)
        #print("{} => {} , {} , {}, {}".format(line, file_name, plate_name, well_name, field_name))
        if plate_name not in plates:
            plates[plate_name] = Plate(plate_name)
        if well_name not in plates[plate_name].wells:
            plates[plate_name].wells[well_name] = Well(well_name)
        field = Field(int(field_name))
        field.path = line.rstrip()
        plates[plate_name].wells[well_name].fields.append(field)
        line = tmp.readline()


plates_tsv = open(Path("../screenA") / "idr0090-screenA-plates.tsv", "w")
for plate in plates.values():
    out_file = out_dir / "{}.screen".format(plate.name)
    writer = open(out_file, "w")
    writer.write("[Plate]\n")
    writer.write("Name = {}\n".format(plate.name))
    writer.write("Rows = {}\n".format(plate.max_row() + 1))
    writer.write("Columns = {}\n".format(plate.max_col() + 1))
    writer.write("Fields = {}\n".format(plate.n_fields()))
    for well in plate.wells.values():
        writer.write("\n[Well {}]\n".format(well.pos))
        writer.write("Row = {}\n".format(well.row))
        writer.write("Column = {}\n".format(well.col))
        for i, field in enumerate(well.get_fields()):
            writer.write("Field_{} = {}/{}\n".format(i, uod_path, field.path))
    writer.close()
    plates_tsv.write("/uod/idr/metadata/idr0090-ashdown-malaria/screens/{}.screen\n".format(plate.name))
plates_tsv.close()

