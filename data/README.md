# Datasets
출처: [AIHub 수식, 도형, 낙서기호 OCR 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=479)

## Data Info
- 총 개수: 169,196
    - train: 150,450
    - test: 18,746
> train
>> annotations : `.json` \
>> images : `.png`

> test
>> annotations : `.json` \
>> images : `.png`

## Download & Unzip Guide
```
$ cd data
$ chmod +x ./download.sh
$ ./download.sh
$ python ./unzip.py
$ cd ..
```

## Synthdog Dataset Download
https://github.com/clovaai/donut
(Firstly, download synthdog folder in above link)
$ pip install synthtiger
$ synthtiger -o {dataset_path} -c 20000 -w 0 -v template.py SynthDoG config_ko.yaml
