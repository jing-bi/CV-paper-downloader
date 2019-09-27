# CV-paper-downloader
Multiprocess web crawler for download paper with specified keywords from OpenCVF access

## Dependence

Use multiprocess for more flexible multiprocessing.

```bash
pip install multiprocess tqdm requests beautifulsoup4
```

## Usage

```python
# keywords are NOT caps sensitive
keywords=['egoc','gaze','first']
# file save path
save_folder=Path(__file__).parent
# get a instance of downloader and assign saved format[pdf/markdown]
downloader=CvSpider(save_folder,keywords)
downloader.save('md')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
