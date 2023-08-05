# PyPercepthor

### Local

```
export PYTHONPATH=/path/to/pypercepthor:$PYTHONPATH
```

### Docker

0. Buid local **development** docker image

```
bash development.sh
```

1. Run **development** image with local source

```
sudo docker run \
  -it \
  --name pypercepthor --rm \
  -v /home/ermiry/Documents/Work/pypercepthor:/home/pypercepthor \
  itpercepthor/pypercepthor:development /bin/bash
```

2. Handle **pypercepthor** module

```
export PYTHONPATH=$pwd:$PYTHONPATH
```
