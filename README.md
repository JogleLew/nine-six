# Nine Six

Unified tools for Neural Network logging and managing.

## Quick Start

### Pretty Logging 

```python
from ninesix import Logger # import logger
logger = Logger("example_nn") # Initialize logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser() # Define your argument parser
    ... 
    args = parser.args()
    args = logger.config(args, "argparse") # Wrap the argparse object to log config
    
    logger.msg("We're going to start training...") # Log text message
    ... # Prepare your model
    for epoch in range(args.epoch):
        logger.progress("epoch", epoch + 1, total=args.epoch) # Record epoch as a progress variable
        ... # Train your model
        logger.value({"loss": loss, "f1": f1}) # Log value(s) associated with progress variable(s)
        ...
    logger.unwatch("epoch") # Unregister progress variable
    ...
    logger.value("final_f1": final_f1}) # Log value(s)
    logger.msg("All done, have fun!") # Log text message
```
The output you will get at stdout:
```
2019-05-14 17:29:09 [Log] (log.py: 44 in __init__()):
Logger [example_nn] Initialized.

2019-05-14 17:29:09 [Config] (example.py: 189 in <module>()):
{
    "epoch": 300,
    "lr": 0.01,
    "lr_decay": 0.0001
}

2019-05-14 17:29:11 [Log] (example.py: 171 in <module>()):
We're going to start training...

2019-05-14 17:29:22 [Log] (example.py: 237 in <module>()):
epoch     : 300 / 300                                       
------------------------------------------------------------------
loss: 0.22311973571777344  f1: 90.58  

2019-05-14 17:29:22 [Log] (example.py: 247 in <module>()):
final_f1: 90.58

2019-05-14 17:29:11 [Log] (example.py: 371 in <module>()):
All done, have fun!
```

At the same time, you'll get a JSON log file `~/96log/example_nn/2019-05-14/172909.json`:

```json
[{"type": "msg", "tag": "Log", "time": "2019-05-14 17:29:09", "content": "JSON Writer Initialized."},
{"type": "config", "tag": "Log", "time": "2019-05-14 17:29:09", "content": {"lr": 0.01, "lr_decay": 0.0001, "epoch": 300}},
{"type": "msg", "tag": "Log", "time": "2019-05-14 17:29:11", "content": "We're going to start training..."},
{"type": "value", "tag": "Log", "time": "2019-05-14 17:29:12", "content": {"progress": {"epoch": {"current": 50, "max": 300}}, "value": {"-L": 5.2108306884765625, "f1": 73.26}}},
{"type": "value", "tag": "Log", "time": "2019-05-14 17:29:13", "content": {"progress": {"epoch": {"current": 100, "max": 300}}, "value": {"-L": 1.3068847656252345, "f1": 85.81}}},
...
{"type": "value", "tag": "Log", "time": "2019-05-14 17:29:22", "content": {"progress": {"epoch": {"current": 300, "max": 300}}, "value": {"-L": 0.22311973571777344, "f1": 90.58}}},
{"type": "value", "tag": "Log", "time": "2019-05-14 17:29:22", "content": {"progress": {}, "value": {"final_f1": 90.58}}},
{"type": "msg", "tag": "Log", "time": "2019-05-14 17:29:11", "content": "All done, have fun!"}]
```

You can try `example.py` which is a complete example.

### Grid Search

Command Line: 
```
python3 ninesix/tool/grid.py -p lr 0.1 0.01 0.001 -p epoch 100 to 201 jump 50 -g 1 2 3 -c "python example.py"
```

You can use `python3 ninesix/tool/grid.py -h` for more help.

Python code:

```python
from ninesix import GridSearch

gs = GridSearch()
# set environment settings
gs.cmd_env = ""
# set default command
gs.cmd_template = "python3 example.py" 
# set available GPUs
gs.gpus = [0]
# set parameter options
gs.param_grid = {
    "lr": [0.1, 0.01, 0.001],
    "epoch": [100, 150, 200]
}
# generate scripts
gs.generate_grid_search()
# execute scripts
gs.execute_script()
```
