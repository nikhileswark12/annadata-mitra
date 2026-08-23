import json, zipfile
from tensorflow.keras.models import model_from_json

vision_model_path = "f:/Annadata Mitra/annadata-mitra/ai-services/models/vision/improved/vision_model_improved.keras"
with zipfile.ZipFile(vision_model_path, 'r') as z:
    config = json.loads(z.read('config.json').decode('utf-8'))

config['module'] = "keras.src.models.functional"
if 'compile_config' in config:
    del config['compile_config']

layers = config['config']['layers']
layers_to_remove = ['data_augmentation', 'tf.math.truediv', 'tf.math.subtract']
new_layers = [l for l in layers if l['config']['name'] not in layers_to_remove]
for l in new_layers:
    if 'inbound_nodes' in l and l['inbound_nodes']:
        nodes = l['inbound_nodes'][0]
        if nodes and isinstance(nodes[0], str):
            if nodes[0] in layers_to_remove:
                nodes[0] = 'input_1'
                nodes[1] = 0
        else:
            for node in nodes:
                if isinstance(node, list) and len(node) > 0 and node[0] in layers_to_remove:
                    node[0] = 'input_1'
                    node[1] = 0

config['config']['layers'] = new_layers

def fix_keras3_compat(obj):
    if isinstance(obj, dict):
        class_name = obj.get('class_name')
        if class_name == 'BatchNormalization':
            if 'config' in obj and 'axis' in obj['config']:
                if isinstance(obj['config']['axis'], list):
                    obj['config']['axis'] = obj['config']['axis'][0]
        if class_name == 'DepthwiseConv2D':
            if 'config' in obj and 'groups' in obj['config']:
                del obj['config']['groups']
        for v in obj.values():
            fix_keras3_compat(v)
    elif isinstance(obj, list):
        for item in obj:
            fix_keras3_compat(item)
            
config_str = json.dumps(config).replace('keras.src.engine.functional', 'keras.src.models.functional')
config = json.loads(config_str)
fix_keras3_compat(config)

print("Testing model_from_json...")
model = model_from_json(json.dumps(config))
print("SUCCESS!")
