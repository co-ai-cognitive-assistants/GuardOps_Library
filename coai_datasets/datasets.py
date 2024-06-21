from coai_datasets.standard.mmlu_dataset import MMLUDataset
from coai_datasets.standard.mlsum_dataset import MLSUMDataset
import pandas as pd 
mmlu = MMLUDataset()
mlsum = MLSUMDataset()

DEFAULT_DATASETS = {
    "mmlu": mmlu,
    "mlsum": mlsum
}

