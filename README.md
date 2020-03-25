# Spark UI by @techguybiswa

![Github Actions Status](jupyter/workflows/Build/badge.svg)

playing around with jupyter

## IMP NOTE: 

After you start multiple spark clusters on localhost:4040, 4041 and so on , make sure to  install <a href="https://chrome.google.com/webstore/detail/moesif-orign-cors-changer/digfbfaphojjndkpccljibejjbppifbc"> Moesif CORS </a> so as to disable CORS. Or else none of the APIs that connect the extension with the spark UI  will work.

## Requirements

* JupyterLab >= 1.0

## Install

```bash
jupyter labextension install bisso
```

## Contributing

### Install

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Move to bisso directory
# Install dependencies
jlpm
# Build Typescript source
jlpm build
# Link your development version of the extension with JupyterLab
jupyter labextension link .
# Rebuild Typescript source after making changes
jlpm build
# Rebuild JupyterLab after making any changes
jupyter lab build
```

You can watch the source directory and run JupyterLab in watch mode to watch for changes in the extension's source and automatically rebuild the extension and application.

```bash
# Watch the source directory in another terminal tab
jlpm watch
# Run jupyterlab in watch mode in one terminal tab
jupyter lab --watch
```

### Uninstall

```bash
jupyter labextension uninstall bisso
```

