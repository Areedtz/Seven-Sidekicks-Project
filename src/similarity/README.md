# Overview

This document serves to give a high level overview of the similarity module, specifically how to use it and how it functions.

## How it works

Every song is divided into 5 second segments, which are used as a basis for the similarity lookup.

For every segment, three features are computed (MFCC, Chroma and tempogram) and combined to create a single feature vector, which is what is used for comparison.

For every segment, a bucket (described later) is searched for n similar segments, the results of all these searches are then aggregated and the n best matches from all bucket searches are stored.

### Features

For feature extraction we use a library called librosa, which allows us to compute various features from a piece of audio.

The features we have chosen are the following:

- MFCC
- Chroma
- Tempogram

### LSH and buckets

We use a library called falconn to efficiently (O(1)) compute similar values. This is achieved by using LSH(Locality sensitive hashing), which is a way to ensure that similar feature vectors hash to similar values, which allows querying for similar values in constant time.

However due to the large collection of songs in the library, segments are sorted into buckets. Buckets are collections of segments, which are inserted into the same LSH table, which a new segment is then queried against. By scaling the size of the buckets we can ensure that our tables stay inside the RAM limitaions of a given system. while still allowing us to search all segments.

## Usage

### Config options

#### Matches

Matches simply determines the amount of similar segments that should be found when searching for a segment.

A search may still return fewer matches if the database is not very large and it then finds many segments from the song it originates from, which are considered invalid matches.

#### Buckets

Buckets determines the amount of segments there should be in each bucket. Scaling this up allows for faster similarity finding, however it also increases the amount of ram necessary on the machine.

### REST API

The REST API is automatically documented using swagger, which is found at the root url.
