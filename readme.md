# BattleShip
This repo contains an engine for simulating battleship games and testing AI agents. For a quick demo, make sure to have python 3 installed then run `python main.py` from the project root. The amount of ships deployed and the number of shots fired for a given simulation can be configured in the `main.py` directly. In the future, this could be abstracted into some basic command line arguments.

## Layout
### AI
The AI package contains Agent types for ship placement and targeting tasks

### src
The src package contains the Board Type on which simulations are run, as well as the validation module that enforces constraints on the simulation.

### test
The test package contains unit tests that to ensure that the applied validation logic is working as intended. Unit tests can be run with `python -m unittest discover` from the project root

## Future work:
- Add arg_parse to support configuring and running simulations from the command line + suppressing logs below / above a certain threshold
- Reconfigure Board to keep track of placed boat dimensions so we can know if a HIT causes the target to sink
- Tests for targeting + firing bombs so we can more easily swap out / test different Targeting Agents
- Better Agents for ship placement + targeting
- Better docstrings for integration with tools like Sphinx


