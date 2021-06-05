# Full-Data-For-CNN-DM

The CNN DM(CNN DailyMail) dataset is the most widely used summarization dataset. 
Although widely used, it is difficult to find preprocessed file or dataset that collects meta information(e.g. `title`, `url`, `date` -- 
actually available for tasks) and summary(both of abstractive and extractive summarization).

So, This code produces meta information of CNN DM dataset and collect golden summary for Abstractive and Extractive summarization.

### Installation & Requirements

* `pip install tqdm`
* `pip install beautifulsoup4`

### Usage

**First,** Download CNN DM Dataset supported by HarvardNLP. You can download at [here](https://s3.amazonaws.com/opennmt-models/Summary/cnndm.tar.gz). After downloading, unzip `cnndm.tar.gz` and store all files in `harvardnlp_data` directory.

**Second,** Download List of urls for CNN Daily Mail Dataset. You can download at [here](https://github.com/abisee/cnn-dailymail/tree/master/url_lists). You don't have to download all the files(e.g. `cnn_wayback_test_urls.txt`). However, `all_train.txt`, `all_val.txt` `all_test.txt` must be downloaded. After downloading, store all files in `url_list` directory.

**Last,** Run following code. After running, you can see `full_cnn_dm` directory which files are stored at.

```bash

$ python collect_full_data.py

```

### TODO
- [x] Code for collecting meta informations
- [x] Code for Abstractive Summary
- [ ] Code for Extractive Summary
- [ ] Code for Fast Request -- url get

### Refrences