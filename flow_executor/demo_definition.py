FLOW_DEFINITION = {
  
  "nodes": [ 
      {
      "id": "config",
      "label": "Config",
      "type": "custom",
      "fields": [
        {
          "name": "user_id",
          "label": "User ID",
          "type": "text",
          "value": "github|149702207"
        },
        {
          "name": "project_id",
          "label": "Project ID",
          "type": "text",
          "value": "5cc73596-ad33-4659-afbd-b1972826e79b"
        },
        {
          "name": "tracing_key",
          "label": "Tracing Key",
          "type": "text",
          "value":"dummy"
        }
  ],
  "category": "config",
      },
    {
      "id": "c6ab1f73-78ed-4d62-a3dc-e1bd5ed61fa0",
      "type": "custom",
      "position": {
        "x": 612,
        "y": 200.4000015258789
      },
      "data": {
        "id": "mlsum_dataset",
        "label": "MLSUM Dataset",
        "type": "output",
        "outputs": [
          {
            "id": "dataset",
            "label": "Dataset"
          }
        ],
        "category": "default_dataset"
      },
      "width": 196,
      "height": 159
    },
    {
      "id": "f2052763-8ea9-4753-b9c6-f17232fc7c9b",
      "type": "custom",
      "position": {
        "x": 589,
        "y": 514.4000015258789
      },
      "data": {
        "id": "custom_dataset",
        "label": "Custom COAI Dataset",
        "type": "output",
        "outputs": [
          {
            "id": "dataset",
            "label": "Dataset"
          }
        ],
        "fields": [
          {
            "name": "dataset_id",
            "label": "Dataset ID",
            "type": "select",
            "options": {
              "source": "/api/get_datasets",
              "params": "user_id",
              "label": "name",
              "id": "dataset_id"
            },
            "value": "331d506e-d7d0-40e9-b2e0-2a67d626af84"
          }
        ],
        "category": "custom_dataset"
      },
      "width": 196,
      "height": 208,
      "selected": False,
      "positionAbsolute": {
        "x": 589,
        "y": 514.4000015258789
      },
      "dragging": False
    },
    {
      "id": "80d67ff6-7c1d-412c-8cd6-b2eefeea3128",
      "type": "custom",
      "position": {
        "x": 956,
        "y": 190.4000015258789
      },
      "data": {
        "id": "sum_eval_framework",
        "label": "Summarization Evaluation Framework",
        "type": "custom",
        "inputs": [
          {
            "id": "model",
            "label": "Model"
          },
          {
            "id": "dataset",
            "label": "Dataset"
          }
        ],
        "outputs": [
          {
            "id": "evaluation",
            "label": "Evaluation"
          }
        ],
        "category": "evaluation_framework"
      },
      "width": 196,
      "height": 218,
      "selected": False,
      "positionAbsolute": {
        "x": 956,
        "y": 190.4000015258789
      },
      "dragging": False
    },
    {
      "id": "17361a93-42b5-4ff1-bfea-2aee53146129",
      "type": "custom",
      "position": {
        "x": 970,
        "y": 497.4000015258789
      },
      "data": {
        "id": "sum_eval_framework",
        "label": "Summarization Evaluation Framework",
        "type": "custom",
        "inputs": [
          {
            "id": "model",
            "label": "Model"
          },
          {
            "id": "dataset",
            "label": "Dataset"
          }
        ],
        "outputs": [
          {
            "id": "evaluation",
            "label": "Evaluation"
          }
        ],
        "category": "evaluation_framework"
      },
      "width": 196,
      "height": 218,
      "selected": False,
      "positionAbsolute": {
        "x": 970,
        "y": 497.4000015258789
      },
      "dragging": False
    },
    {
      "id": "d461d7ae-cd9b-4ed9-a46d-5907dc3caefb",
      "type": "custom",
      "position": {
        "x": 1438,
        "y": 465.4000015258789
      },
      "data": {
        "id": "eval_exporter",
        "label": "Evaluation Exporter",
        "type": "input",
        "inputs": [
          {
            "id": "add",
            "label": "Evaluation"
          }
        ],
        "fields": [
          {
            "name": "title",
            "label": "Evaluation Title",
            "type": "text",
            "value": "exporter_title"
          }
        ],
        "category": "exporting"
      },
      "width": 196,
      "height": 198
    }
  ],
  "edges": [
    {
      "source": "c6ab1f73-78ed-4d62-a3dc-e1bd5ed61fa0",
      "sourceHandle": "output-mlsum_dataset-0",
      "target": "80d67ff6-7c1d-412c-8cd6-b2eefeea3128",
      "targetHandle": "input-sum_eval_framework-1",
      "id": "reactflow__edge-c6ab1f73-78ed-4d62-a3dc-e1bd5ed61fa0output-mlsum_dataset-0-80d67ff6-7c1d-412c-8cd6-b2eefeea3128input-sum_eval_framework-1"
    },
    {
      "source": "f2052763-8ea9-4753-b9c6-f17232fc7c9b",
      "sourceHandle": "output-custom_dataset-0",
      "target": "17361a93-42b5-4ff1-bfea-2aee53146129",
      "targetHandle": "input-sum_eval_framework-1",
      "id": "reactflow__edge-f2052763-8ea9-4753-b9c6-f17232fc7c9boutput-custom_dataset-0-17361a93-42b5-4ff1-bfea-2aee53146129input-sum_eval_framework-1"
    },
    {
      "source": "80d67ff6-7c1d-412c-8cd6-b2eefeea3128",
      "sourceHandle": "output-sum_eval_framework-0",
      "target": "d461d7ae-cd9b-4ed9-a46d-5907dc3caefb",
      "targetHandle": "input-eval_exporter-0",
      "id": "reactflow__edge-80d67ff6-7c1d-412c-8cd6-b2eefeea3128output-sum_eval_framework-0-d461d7ae-cd9b-4ed9-a46d-5907dc3caefbinput-eval_exporter-0"
    },
    {
      "source": "17361a93-42b5-4ff1-bfea-2aee53146129",
      "sourceHandle": "output-sum_eval_framework-0",
      "target": "d461d7ae-cd9b-4ed9-a46d-5907dc3caefb",
      "targetHandle": "input-eval_exporter-0",
      "id": "reactflow__edge-17361a93-42b5-4ff1-bfea-2aee53146129output-sum_eval_framework-0-d461d7ae-cd9b-4ed9-a46d-5907dc3caefbinput-eval_exporter-0"
    }
  ]
}

  
