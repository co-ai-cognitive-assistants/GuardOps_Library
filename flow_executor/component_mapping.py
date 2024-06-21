COMPONENT_MAPPING = {
# Config
"config":{
    "priority":0,
    "creation_lines":[
        "Config.set_user_id('{user_id}')",
        "Config.set_project_id('{project_id}')",
        "Config.set_tracing_key('{tracing_key}')"
    ]
},
# Exporting and evaluation creation
"eval_exporter":{
    "priority":3,
    "instance":True,
    "creation_lines":[
        "{id} = EvalExporter(title='{title}')",
    ],
    "execution_lines":[
        "eval_{framework} = {framework}.evaluate(model={model}, dataset={dataset}.data, eval_name={exporter}.title)",
        "{target}.add_eval(eval_{source})",
        "{target}.export()"
    ]
},
# Models
"openai_model":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = OpenAIModel({api_key},{model_name},{base_url})",
        ],
},
# Datasets
"custom_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = COAIDataset()",
        "{id}.load(dataset_id='{dataset_id}')"
        ],
},

"mlsum_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = MLSUMDataset()",
        "{id}.load()"
        ],
},
"mmlu_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = MMLUDataset()",
        "{id}.load()"
        ],
},
"huggingface_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = HuggingfaceDataset({repo},{tag},{split})",
        "{id}.load()"
        ],
},
"tinyai2arc_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyAI2arcDataset()",
        "{id}.load()"
        ],
},
"tinyalpacaeval_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyAlpacaEvalDataset()",
        "{id}.load()"
        ],
},
"tinygsm8k_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyGSM8kDataset()",
        "{id}.load()"
        ],
},
"tinyhellaswag_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyHellaswagDataset()",
        "{id}.load()"
        ],
},
"tinymmlu_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyMMLUDataset()",
        "{id}.load()"
        ],
},
"tinytruthfulqa_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyTruthfulQADataset()",
        "{id}.load()"
        ],
},
"tinywinogrande_dataset":{
    "priority":1,
    "instance":True,
    "creation_lines":[
        "{id} = TinyWinograndeDataset()",
        "{id}.load()"
        ],
},
# Frameworks
"sum_eval_framework":{
    "priority":2,
    "instance":True,
    "creation_lines":[
        "{id} = SUMEvalFramework(device='cuda')",
    ],
    "execution_lines":[
        
       
     ]
}

}