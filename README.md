# Nine Six

Unified tools for Neural Network logging and managing.

## Quick Start

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
Logger [example] Initialized.

2019-05-14 17:29:09 [Config] (example.py: 189 in <module>()):
{'lr': 0.01, 'lr_decay': 0.0001, 'epoch': 300}

2019-05-14 17:29:11 [Log] (example.py: 171 in forward()):
We're going to start training...

2019-05-14 17:29:22 [Log] (example.py: 237 in <module>()):
epoch     : 300 / 300                                       
------------------------------------------------------------------
loss: 0.22311973571777344  f1: 90.58  

2019-05-14 17:29:22 [Log] (example.py: 237 in <module>()):
final_f1: 90.58

2019-05-14 17:29:11 [Log] (example.py: 171 in forward()):
All done, have fun!
```

You can try `example.py` which is a complete example.
