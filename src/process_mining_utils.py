import logging
import os
import pandas as pd
import pm4py
from pm4py.vis import view_dfg, view_petri_net, save_vis_dfg, save_vis_petri_net


class ProcessMiningUtils:
    def __init__(self, dataframe, output_dir):
        self.df = dataframe
        self.output_dir = output_dir
        self.event_log = None
        self.dfg = None
        self.start_activities = None
        self.end_activities = None
        self.petri_net = None
        self.initial_marking = None
        self.final_marking = None

        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess_dataframe(self):
        logging.info("Preprocessing DataFrame for PM4Py...")

        self.df.rename(columns={
            "icustay_id": "case:concept:name",
            "event_timestamp": "time:timestamp",
            "label": "concept:name"
        }, inplace=True)

        self.df.dropna(subset=["concept:name", "time:timestamp", "case:concept:name"], inplace=True)
        self.df = self.df[self.df["concept:name"].str.strip() != ""]
        self.df["time:timestamp"] = pd.to_datetime(self.df["time:timestamp"], errors="coerce")

        self.df = pm4py.utils.format_dataframe(
            self.df,
            case_id="case:concept:name",
            activity_key="concept:name",
            timestamp_key="time:timestamp"
        )

        self.event_log = pm4py.convert_to_event_log(self.df)

        logging.info(f"Total cases: {self.df['case:concept:name'].nunique()}")
        logging.info(f"Total activities: {self.df['concept:name'].nunique()}")
        logging.info(f"Total events: {len(self.df)}")

    def discover_dfg(self):
        logging.info("Discovering DFG...")

        self.dfg, self.start_activities, self.end_activities = pm4py.discovery.discover_dfg(
            self.event_log,
            activity_key="concept:name",
            case_id_key="case:concept:name",
            timestamp_key="time:timestamp"
        )

        logging.info("DFG discovery completed.")

        # Save the visualization immediately
        output_path = os.path.join(self.output_dir, "dfg.png")
        logging.info(f"Exporting DFG to {output_path}...")

        save_vis_dfg(
            self.dfg,
            self.start_activities,
            self.end_activities,
            file_path=output_path,
            bgcolor='white',
            rankdir='LR'
        )

        logging.info("DFG export completed.")

    def view_dfg(self):
        if self.dfg is None:
            raise Exception("DFG not discovered yet.")

        logging.info("Displaying DFG...")
        view_dfg(
            self.dfg,
            self.start_activities,
            self.end_activities,
            format='png',
            bgcolor='white',
            rankdir='LR'
        )

    def abstract_dfg_to_text(self):
        if self.dfg is None:
            raise Exception("DFG not discovered yet.")

        logging.info("Generating textual summary from DFG...")

        summary = ["The process starts with:"]
        for act, freq in self.start_activities.items():
            summary.append(f"  - {act} ({freq} times)")

        summary.append("\nThe main activity transitions are:")
        for (src, tgt), freq in sorted(self.dfg.items(), key=lambda x: -x[1]):
            summary.append(f"  - '{src}' → '{tgt}' occurred {freq} times")

        summary.append("\nThe process ends with:")
        for act, freq in self.end_activities.items():
            summary.append(f"  - {act} ({freq} times)")

        text = "\n".join(summary)

        # Save to file
        output_path = os.path.join(self.output_dir, "dfg_summary.txt")
        with open(output_path, "w") as f:
            f.write(text)

        logging.info(f"DFG textual summary saved to {output_path}")
        return text

    def discover_petri_net(self):
        logging.info("Discovering Petri net using inductive miner...")

        self.petri_net, self.initial_marking, self.final_marking = pm4py.discovery.discover_petri_net_inductive(
            self.event_log,
            activity_key='concept:name',
            case_id_key='case:concept:name',
            timestamp_key='time:timestamp',
            multi_processing=True
        )

        logging.info("Petri net discovery completed.")

        # Save the visualization immediately
        output_path = os.path.join(self.output_dir, "petri_net.png")
        logging.info(f"Exporting Petri net to {output_path}...")

        save_vis_petri_net(
            self.petri_net,
            self.initial_marking,
            self.final_marking,
            file_path=output_path,
            bgcolor='white',
            rankdir='LR',
            debug=True
        )

        logging.info("Petri net export completed.")
    
    def abstract_petri_net_to_text(self):
        if self.petri_net is None:
            raise Exception("Petri net not discovered yet.")

        logging.info("Generating textual summary from Petri net...")

        transitions = [t.label for t in self.petri_net.transitions if t.label]
        places = list(self.petri_net.places)
        arcs = [(a.source.name, a.target.name) for a in self.petri_net.arcs]

        summary = [
            f"The Petri net contains {len(transitions)} transitions, {len(places)} places, and {len(arcs)} arcs.",
            "Transitions (activities) include:"
        ]
        for label in transitions:
            summary.append(f"  - {label}")

        summary.append("\nInitial marking places:")
        for place, tokens in self.initial_marking.items():
            summary.append(f"  - {place.name}: {tokens} token(s)")

        summary.append("\nFinal marking places:")
        for place, tokens in self.final_marking.items():
            summary.append(f"  - {place.name}: {tokens} token(s)")

        text = "\n".join(summary)

        # Save to file
        output_path = os.path.join(self.output_dir, "petri_net_summary.txt")
        with open(output_path, "w") as f:
            f.write(text)

        logging.info(f"Petri net textual summary saved to {output_path}")
        return text