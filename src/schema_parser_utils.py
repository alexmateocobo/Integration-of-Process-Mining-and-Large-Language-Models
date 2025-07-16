import xml.etree.ElementTree as ET
import logging

class SchemaParser:
    def __init__(self, xml_file_path, output_path="schema_abstraction.txt"):
        self.xml_file_path = xml_file_path
        self.output_path = output_path
        self.tables_info = {}
        self.relations = []
        logging.info(f"Initialized SchemaParser with {xml_file_path}")

    def parse_schema(self):
        logging.info("Parsing XML schema...")
        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()

        for table in root.findall(".//table"):
            table_name = table.get("name")
            columns = []

            for column in table.findall("column"):
                col_name = column.get("name")
                col_type = column.get("type")
                col_remark = column.get("remarks", "").strip()
                columns.append(f"- {col_name} ({col_type}): {col_remark}")

                parent = column.find("parent")
                if parent is not None:
                    ref_table = parent.get("table")
                    ref_column = parent.get("column")
                    self.relations.append(f"{table_name}.{col_name} → {ref_table}.{ref_column}")

            self.tables_info[table_name] = columns

            for column in table.findall("column"):
                for child in column.findall("child"):
                    source_col = column.get("name")
                    target_table = child.get("table")
                    target_col = child.get("column")
                    self.relations.append(f"{target_table}.{target_col} → {table_name}.{source_col}")

        logging.info("Schema parsing completed.")

    def write_abstraction_to_file(self):
        logging.info(f"Writing textual abstraction to {self.output_path}...")
        with open(self.output_path, "w", encoding="utf-8") as f:
            for table, columns in self.tables_info.items():
                f.write(f"## Table: {table}\n")
                for col in columns:
                    f.write(col + "\n")
                f.write("\n")

            f.write("## Foreign Key Relations\n")
            for rel in sorted(set(self.relations)):
                f.write(f"- {rel}\n")

        logging.info("Textual abstraction saved successfully.")
