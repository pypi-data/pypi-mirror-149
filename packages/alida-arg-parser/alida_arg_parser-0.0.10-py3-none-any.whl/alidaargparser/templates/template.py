{
    "name": "{{ name }}",
    "description": "{{ description }}",
    "mode": "{{mode.upper()}}",
    "area": "{{area.upper()}}",
    "url":  {{json.dumps(docker_image)}},
    "version": "1.0.0",
    "framework": {
        "id": 6,
        "name": "Python",
        "version": "3",
        "imageUrl": "https://cdn.alidalab.it/static/images/frameworks/python_logo.png"
    },
    "properties": [
        {% for property in properties %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "description": {{json.dumps(property.description)}},
                "mandatory": {{json.dumps(property.required)}},
                "defaultValue": {{json.dumps(property.default)}},
                "value": null,
                "key": {{json.dumps(property.name)}},
                "type": {{json.dumps(translation['type'][property.type])}},
                "inputData": null,
                "outputData": null
            }
        },
        {% endfor %}
        {% for input_dataset in input_datasets %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "defaultValue": null,
                "description": {{json.dumps(input_dataset.description)}},
                "key": "input-dataset",
                "mandatory": true,
                "type": "STRING",
                "value": null,
                "inputData": true,
                "outputData": null
            }
        },
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "defaultValue": {{json.dumps(translation['column_types'][input_dataset.columns_type])}},
                "description": "Selected columns from table",
                "key": "input-columns",
                "mandatory": true,
                "type": "STRING",
                "value": null,
                "inputData": null,
                "outputData": null
            }
        },
        {% endfor %}
        {% for output_dataset in output_datasets %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "defaultValue": null,
                "description": {{json.dumps(output_dataset.description)}},
                "key": "output-dataset",
                "mandatory": true,
                "type": "STRING",
                "value": null,
                "inputData": null,
                "outputData": true
            }
        },
        {% endfor %}

        {% if input_models|length + output_models|length != 0  %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.StaticProperty": {
                "description": "The URL for Web HDFS service",
                "mandatory": true,
                "defaultValue": null,
                "value": null,
                "key": "webHdfsUrl",
                "type": "STRING"
            }
        },
        {% endif %}

        {% for input_model in input_models %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.StaticProperty": {
                "description": "The storage type where the input model is stored.",
                "mandatory": true,
                "defaultValue": null,
                "value": "hdfs",
                "key": "dataStorageType-input-model",
                "type": "STRING"
            }
        },
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "description": "HDFS path where to read the model",
                "mandatory": true,
                "defaultValue": null,
                "value": null,
                "key": "input-model",
                "type": "STRING",
                "inputData": true,
                "outputData": false
            }
        },
        {% endfor %}

        {% for output_model in output_models %}
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.StaticProperty": {
                "description": "The storage type where the input model is stored.",
                "mandatory": true,
                "defaultValue": null,
                "value": "hdfs",
                "key": "dataStorageType-output-model",
                "type": "STRING"
            }
        },
        {
            "it.eng.alidalab.applicationcatalogue.domain.service.ApplicationProperty": {
                "description": "HDFS path where to read the model",
                "mandatory": true,
                "defaultValue": null,
                "value": null,
                "key": "output-model",
                "type": "STRING",
                "inputData": true,
                "outputData": false
            }
        },
        {% endfor %}

    ],
    "metrics": []
}

