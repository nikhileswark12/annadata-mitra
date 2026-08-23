import json
import zipfile
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(base_dir, "../models/vision/vision_model.keras")
dst = os.path.join(base_dir, "vision_model_patched.keras")

with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(dst, 'w') as zout:
        for item in zin.infolist():
            if item.filename == 'config.json':
                s = zin.read(item.filename).decode('utf-8')
                config = json.loads(s)
                
                # Fix module
                config['module'] = "keras.src.models.functional"
                
                layers = config['config']['layers']
                
                # Remove data_augmentation
                da_idx = -1
                for i, l in enumerate(layers):
                    if l['config']['name'] == 'data_augmentation':
                        da_idx = i
                        break
                
                if da_idx != -1:
                    del layers[da_idx]
                
                # Fix inbound_nodes and axis
                for l in layers:
                    # Point conv2d to input_1 instead of data_augmentation
                    if 'inbound_nodes' in l and l['inbound_nodes']:
                        for node in l['inbound_nodes'][0]:
                            if node[0] == 'data_augmentation':
                                node[0] = 'input_1'
                                node[1] = 0
                    
                    # Fix BatchNormalization axis
                    if l['class_name'] == 'BatchNormalization':
                        if isinstance(l['config'].get('axis'), list):
                            l['config']['axis'] = l['config']['axis'][0]

                # Remove compile_config to prevent optimizer loading errors in Keras 3
                if 'compile_config' in config:
                    del config['compile_config']

                s_out = json.dumps(config)
                zout.writestr(item, s_out)
            else:
                zout.writestr(item, zin.read(item.filename))

print("Patched successfully to", dst)
