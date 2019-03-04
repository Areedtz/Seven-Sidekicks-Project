CREATE TABLE template (
    song_id INT(11) NOT NULL,
    last_run DATETIME NOT NULL,
    -- Insert your model specific stuff here
    PRIMARY KEY (song_id)
);
CREATE TABLE track_bpm (
    song_id INT(11) NOT NULL,
    last_run DATETIME NOT NULL,
    bpm NUMERIC(5, 2) NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL,
    PRIMARY KEY (song_id)
);
CREATE TABLE track_timbre (
    song_id INT(11) NOT NULL,
    last_run DATETIME NOT NULL,
    tibre TEXT NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL,
    PRIMARY KEY (song_id)
);
CREATE TABLE track_mood_relaxed (
    song_id INT(11) NOT NULL,
    last_run DATETIME NOT NULL,
    relaxed TEXT NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL,
    PRIMARY KEY (song_id)
);
CREATE TABLE track_mood_party (
    song_id INT(11) NOT NULL,
    last_run DATETIME NOT NULL,
    party TEXT NOT NULL,
    confidence NUMERIC(5, 4) NOT NULL,
    PRIMARY KEY (song_id)
);