# animations

## Quickstart
Prerequisites:
- git client
- pip
- pipenv (Although pipenv is not required to run the project, it is recommended for the quickstart)
- npm/npx (NPM is not required for the project, but is for the simulator. npx is installed by default with npm>5.2)

Checkout
```
git clone -b develop git@github.com:Rayactivation/animations.git
cd animations
```
In one console, launch the simulator:
```
#From animations directory
npx opc-simulator --layout $(pwd)/layout/block_ray_layout_animated.json
```
In another, run the simple-af framework
```
#From Animations Directory
pipenv shell
python -m simple_af
```
