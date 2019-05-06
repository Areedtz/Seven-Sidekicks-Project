import numpy as np

from similarity.similarity import process_segment, load_songs, process_db_segment, create_feature, dist, create_bucket, find_best_matches, query_similar, find_matches, analyze_songs


def test_process_segment():
    assert True


def test_load_songs():
    assert True


def test_process_db_segment():
    assert True


def test_create_feature():
    assert True


def test_create_bucket():
    assert True


def test_dist():
    start = np.array([0, 0])
    end = np.array([0, 1])
    assert dist(start, end) == 1

    end = np.array([1, 0])
    assert dist(start, end) == 1


def test_find_best_matches():
    assert True


def test_query_similar():
    assert True


def test_find_matches():
    assert True


def test_analyze_songs():
    assert True
