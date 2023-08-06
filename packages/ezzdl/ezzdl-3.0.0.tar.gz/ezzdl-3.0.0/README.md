# ezzdl
Multithreaded downloader with textui colored progress bar

```bash
pip install ezzdl
```

# Use
```python
>>> from ezzdl import dl
>>> dl(["https://github.com/Cactus-0/cabanchik/raw/master/dist/cabanchik.zip",
...         "https://github.com/BarsTiger/daun/raw/master/dist/daun.exe",
...         "https://github.com/BarsTiger/localhost-mc-open/raw/master/localhost_3000_Mc_fusion.exe"],
...         "folder")
[16:20:15] Requesting https://github.com/Cactus-0/cabanchik/raw/master/dist/cabanchik.zip
[16:20:15] Requesting https://github.com/BarsTiger/daun/raw/master/dist/daun.exe
[16:20:15] Requesting https://github.com/BarsTiger/localhost-mc-open/raw/master/localhost_3000_Mc_fusion.exe
[16:20:20] Downloaded D:\Path\To\Folder\folder\daun.exe
[16:20:21] Downloaded D:\Path\To\Folder\folder\cabanchik.zip
[16:20:32] Downloaded D:\Path\To\Folder\folder\localhost_3000_Mc_fusion.exe
               cabanchik.zip ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 13.2/13.2 MB • 2.2 MB/s • 0:00:00
                    daun.exe ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 11.4/11.4 MB • 2.2 MB/s • 0:00:00
localhost_3000_Mc_fusion.exe ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 37.7/37.7 MB • 2.3 MB/s • 0:00:00
```

# Features
- Automatically downloads files from a list of urls and generates its names
- Will create a folder with if it doesn't exist
- Colored
