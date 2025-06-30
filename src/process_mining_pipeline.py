import logging
from tqdm import tqdm
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization

class ProcessMiningPipeline:
    def __init__(self, dataframe):
        self.df = dataframe
        self.event_log = None

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def convert_to_event_log(self):
        logging.info("Converting DataFrame to PM4Py Event Log...")

        # Rename DataFrame columns to PM4Py standards
        self.df.rename(columns={
            'subject_id': 'case:concept:name',
            'event_timestamp': 'time:timestamp',
            'label': 'concept:name'
        }, inplace=True)

        # Drop events without activity labels (just in case)
        self.df = self.df.dropna(subset=['concept:name'])
        self.df = self.df[self.df['concept:name'].str.strip() != '']

        # Convert to PM4Py Event Log
        self.event_log = log_converter.apply(self.df)

        logging.info("Conversion to Event Log completed.")

    def discover_dfg(self):
        if self.event_log is None:
            raise Exception("Event Log not initialized. Run convert_to_event_log() first.")

        logging.info("Discovering Directly-Follows Graph (DFG)...")
        dfg = dfg_discovery.apply(self.event_log)

        logging.info("Processing DFG edges...")
        for edge in tqdm(dfg, desc="Processing DFG Edges"):
            pass  # Just for progress bar display

        logging.info("Preparing DFG visualization...")
        gviz = dfg_visualization.apply(dfg, log=self.event_log, variant=dfg_visualization.Variants.FREQUENCY)

        logging.info("Saving DFG visualization to file...")
        dfg_visualization.save(gviz, "dfg_visualization.svg")

        logging.info("DFG visualization saved as 'dfg_visualization.svg'.")