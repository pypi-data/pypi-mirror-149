# Installation instructions {#installation-md}

## Prerequisites

You'll need a C compiler, CMake, and Make or Ninja. 
To compile the Matlab interface, you need Matlab and MEX as well.

## Download

Download LADEL from <https://github.com/kul-optec/LADEL.git> ([direct link](https://github.com/kul-optec/LADEL/archive/refs/heads/main.zip)):

```sh
git clone https://github.com/kul-optec/LADEL.git --single-branch --depth 1
```
Alternatively, without git
```sh
wget https://github.com/kul-optec/LADEL/archive/refs/heads/main.tar.gz -O- | tar xzf -
```

## Matlab installation

### Build

Open a terminal inside of the LADEL repository, and configure and build the 
project:

```sh
cmake -B build -S LADEL \
    -D CMAKE_BUILD_TYPE=Release \
    -D LADEL_WITH_MEX=On \
    -D CMAKE_POSITION_INDEPENDENT_CODE=On
```
```sh
cmake --build build \
    --config Release -j
```

### Install

On Linux, Matlab automatically adds `~/Documents/MATLAB` to the path, so it's easiest install LADEL there:

```sh
cmake --install build \
    --config Release \
    --component mex_interface \
    --prefix ~/Documents/MATLAB
```

### Uninstall

To uninstall LADEL, simply remove the `@ladel` folder from where you installed it:

```sh
rm -r "~/Documents/MATLAB/@ladel"
```

## C installation

To install the C libraries and headers, simply follow the standard 
CMake configure, build, install instructions:

```sh
cmake -B build -S LADEL \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_POSITION_INDEPENDENT_CODE=On
cmake --build build --config Release -j
cmake --install build --config Release --prefix /usr/local
```

If you just need the shared libraries, you can use:
```sh
cmake -B build -S LADEL \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_POSITION_INDEPENDENT_CODE=On \
    -D BUILD_SHARED_LIBS=On
cmake --build build --config Release -j
cmake --install build --config Release --component shlib --prefix /usr/local
```