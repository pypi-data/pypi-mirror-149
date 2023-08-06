Please run optilog-scenario ./relative/path/to/this/scenario/ in order to perform your desired actions.

Examples:

# Launch all instances
> optilog-scenario ./example_glucose launch

# Launch all instances (overwrite previous logs)
> optilog-scenario ./example_glucose launch --overwrite

# Delete execution logs
> optilog-scenario ./example_glucose clean

# List all tasks. This will print the task's id and instance path.
> optilog-scenario ./example_glucose list

# Launch a specific task, overwrite the logs and use a different seed
> optilog-scenario ./example_glucose launch --overwrite --task 3 --seed 64

# Launch a specific task, overwrite the logs and use multiple seeds
> optilog-scenario ./example_glucose launch --overwrite --task 3 --seed 64,82

# Launch multiple tasks, overwrite the logs and use multiple seeds
> optilog-scenario ./example_glucose launch --overwrite --task 3,8,9 --seed 64,82