from coai_datasets.dataset_manager import DatasetManager
from coai_datasets.standard import *
from config.config import Config
from evaluation.metrics import BLEUMetric, Rouge1Metric
from evaluation import *
from exporter.EvalExporter import EvalExporter
from models.openai_model import OpenAIModel
Config.set_user_id('github|149702207')
Config.set_project_id('5cc73596-ad33-4659-afbd-b1972826e79b')
Config.set_tracing_key('dummy')
c6ab1f7378ed4d62a3dce1bd5ed61fa0 = MLSUMDataset()
c6ab1f7378ed4d62a3dce1bd5ed61fa0.load()
f20527638ea94753b9c6f17232fc7c9b = COAIDataset()
f20527638ea94753b9c6f17232fc7c9b.load(dataset_id='331d506e-d7d0-40e9-b2e0-2a67d626af84')
80d67ff67c1d412c8cd6b2eefeea3128 = SUMEvalFramework(device='cuda')
17361a9342b54ff1bfea2aee53146129 = SUMEvalFramework(device='cuda')
d461d7aecd9b4ed9a46d5907dc3caefb = EvalExporter(title='exporter_title')
eval_80d67ff67c1d412c8cd6b2eefeea3128 = 80d67ff67c1d412c8cd6b2eefeea3128.evaluate(model=dummy, dataset=c6ab1f7378ed4d62a3dce1bd5ed61fa0.data, eval_name=d461d7aecd9b4ed9a46d5907dc3caefb.title)
d461d7aecd9b4ed9a46d5907dc3caefb.add_eval(eval_80d67ff67c1d412c8cd6b2eefeea3128)
d461d7aecd9b4ed9a46d5907dc3caefb.export()
eval_17361a9342b54ff1bfea2aee53146129 = 17361a9342b54ff1bfea2aee53146129.evaluate(model=dummy, dataset=f20527638ea94753b9c6f17232fc7c9b.data, eval_name=d461d7aecd9b4ed9a46d5907dc3caefb.title)
d461d7aecd9b4ed9a46d5907dc3caefb.add_eval(eval_17361a9342b54ff1bfea2aee53146129)
d461d7aecd9b4ed9a46d5907dc3caefb.export()