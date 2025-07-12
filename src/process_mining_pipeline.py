import logging
import pandas as pd
import pm4py
from pm4py.vis import view_dfg, view_petri_net


class ProcessMiningPipeline:
    def __init__(self, dataframe):
        self.df = dataframe
        self.event_log = None
        self.dfg = None
        self.start_activities = None
        self.end_activities = None
        self.petri_net = None
        self.initial_marking = None
        self.final_marking = None

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def preprocess_dataframe(self):
        logging.info("Preprocessing DataFrame for PM4Py...")

        # Rename columns for PM4Py compatibility
        self.df.rename(columns={
            "icustay_id": "case:concept:name",
            "event_timestamp": "time:timestamp",
            "label": "concept:name"
        }, inplace=True)

        # Drop rows with missing activity labels
        self.df.dropna(subset=["concept:name", "time:timestamp", "case:concept:name"], inplace=True)
        self.df = self.df[self.df["concept:name"].str.strip() != ""]

        # Convert timestamp to datetime
        self.df["time:timestamp"] = pd.to_datetime(self.df["time:timestamp"], errors="coerce")

        # Format the dataframe
        self.df = pm4py.utils.format_dataframe(
            self.df,
            case_id="case:concept:name",
            activity_key="concept:name",
            timestamp_key="time:timestamp"
        )

        # Convert to event log
        self.event_log = pm4py.convert_to_event_log(self.df)

        # Log stats
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

    def view_petri_net(self):
        if self.petri_net is None:
            raise Exception("Petri net not discovered yet.")

        logging.info("Displaying Petri net...")
        view_petri_net(
            self.petri_net,
            self.initial_marking,
            self.final_marking,
            format="png"
        )