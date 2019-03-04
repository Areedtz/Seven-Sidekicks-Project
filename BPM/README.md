# BPM module
Takes a folder containing Diskoteket *.wav* files and prints a table with the ID of the Song, the BPM and the confidence in the BPM prediction

Can be run with the following command
```
python BPM FOLDERPATH
```

If trying to retrieve the BPM and confidence for a single *.wav* file, use ``BPM_extractor.get_song_BPM(FILENAME)``