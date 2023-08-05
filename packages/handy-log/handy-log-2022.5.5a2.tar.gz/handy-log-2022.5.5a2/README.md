# Aim
Make the log system easier to use, by simply:
```
import log

log.info("Hello handy-log!")
```

# Features
* While the builtin `logging.info(msg)` uses the `root` logger to record message,
`log.info(msg)` can use `current module`'s logger.  Here, `current module` means 
the module inside which you invoked the `log.info(msg)`. 
You don't have to code like this any more:
    ```
    import logging
    
    logger = logging.getLogger(you_package_name)
    
    logger.info(your_msg)
    ```
* A bunch of predefined formats, handlers, loggers.
* Easy to config, and easy to invoke.

# Mechanism
1. This is a wrapper for python builtin `logging` system.
2. Load yaml to dict, then use the `logging.config.dictConfig(config_dict)` to configure the logging system.
3. When you invoke `log.info(msg)`, `handy-log` will first find `current module`'s logger, 
and then use this `logger` to log the message.

# Configuration/How to use
* Option 1:  
Do nothing, use the default configuration. Just `import log` and use it.
* Option 2:  
  1. Create your own `handy-log.yaml` in your `current work directory`.
  2. Then just `import log` and use it.
* Option 3:
  1. Create your own yaml configuration file.
  2. Invoke `log.init(your_config_file)` to configure the logger.
  
     This will merge `your_config_file`'s content with the builtin `handy-log.yaml` first,
     then apply the merged configuration to the builtin logging system.
     
  3. Then `import log` and use it.
  
# Notes:
* Since the root logger can only be initialized once,
you should invoke `log.init()` before any other logger configuration takes effect.  
* In the configuration file, loggers and handlers have their independent `logging level`,
The message needs to pass through all these `level` to be recorded.
