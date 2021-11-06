#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
copy.py
Description of script_name.py.
"""
import time
import shutil
import subprocess
import os
from pathlib import Path
from unittest import TestCase
import logging


def setup_logging(level=logging.DEBUG):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def copy_shutil_copy(source, destination):
    shutil.copy(source, destination)


def copy_shutil_copy2(source, destination):
    shutil.copy2(source, destination)


def copy_shutil_copyfile(source, destination):
    shutil.copyfile(source, destination)


def copy_subprocess_cp(source, destination):
    subprocess.check_output(['cp', source, destination])


def copy_os_system(source, destination):
    os.system(f'cp {source} {destination}')


def copy_pathlib(source, destination):
    destination.write_bytes(source.read_bytes())


def copy_pathlib02(source, destination):
    with source.open('rb') as src, destination.open('wb') as dest:
        dest.write(src.read())


def copy_pathlib03(source, destination):
    with source.open(mode='rb') as src:
        src_data = src.read()

    with destination.open(mode='wb') as dest:
        dest.write(src_data)


def copy_pathlib_chunks(source: Path, destination: Path, chunk_size=524288):
    with source.open('rb') as src, destination.open('wb') as dest:
        for chunk in iter(lambda: src.read(chunk_size), b''):
            dest.write(chunk)


# uses generator to load segments to memory
def copy_custom01(source, destination):
    def _write(filesrc, filedst):
        filegen = iter(lambda: filesrc.read(16384), b'')
        try:
            while True:
                filedst.write(next(filegen))
        except StopIteration:
            pass

    with open(source, 'rb') as fsrc, open(destination, 'wb') as fdst:
        _write(fsrc, fdst)


def copy_custom02(source, destination):
    with open(source, 'rb') as fsrc:
        with open(destination, 'wb') as fdst:
            fdst.write(fsrc.read())


def copy_custom03(source, destination, chunk_size=16384):
    with open(source, 'rb') as fsrc:
        with open(destination, 'wb') as fdst:
            for x in iter(lambda: fsrc.read(16384), b''):
                fdst.write(x)


def test_copy(method, source, destination, iterations):
    start_time = time.time()
    logging.debug(f'Testing {method.__name__}')

    for i in range(iterations):
        logging.debug(f'Running iteration {i + 1}/{iterations}')
        method(source, destination)
    finish_time = time.time() - start_time
    logging.debug(f'Finished {iterations} iterations in {finish_time} seconds')
    return finish_time


def test_copy_chunks(method, file_size, iterations):
    logging.info(f'Testing {method.__name__} chunks with {file_size} MB file')
    iterations = iterations
    file_size = file_size
    chunk_size = 4096
    source, destination = setup(file_size=file_size)
    results = {'file_size': file_size}
    # Run tests
    for i in range(1, 10):
        chunk_size = chunk_size * 2
        start_time = time.time()
        logging.debug(f'Testing {method.__name__}: {chunk_size}')
        for n in range(iterations):
            logging.debug(f'Running iteration {n}/{iterations}')
            method(source, destination, chunk_size=chunk_size)
        finish_time = time.time() - start_time
        logging.debug(f'Finished {iterations} iterations in {finish_time} seconds')
        results[str(chunk_size)] = finish_time

    present_results(results)


def setup(file_size=32):
    test_folder = Path().home() / 'desktop' / 'copy_test'
    source = test_folder / 'source' / 'copy_test_file.txt'
    source.write_bytes(bytes('0' * 1024 ** 2 * file_size, 'utf-8'))
    destination = test_folder / 'destination' / 'copy_test_file.txt'
    source.parent.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return source, destination


def run_test(file_size, iterations):
    iterations = iterations
    file_size = file_size
    source, destination = setup(file_size=file_size)
    results = {'file_size': file_size}
    # Run tests
    results['shutil.copy'] = test_copy(copy_shutil_copy, source, destination, iterations)
    results['shutil.copy2'] = test_copy(copy_shutil_copy2, source, destination, iterations)
    results['shutil.copyfile'] = test_copy(copy_shutil_copyfile, source, destination, iterations)
    results['subprocess_cp'] = test_copy(copy_subprocess_cp, source, destination, iterations)
    results['os_system'] = test_copy(copy_os_system, source, destination, iterations)
    results['pathlib'] = test_copy(copy_pathlib, source, destination, iterations)
    results['pathlib02'] = test_copy(copy_pathlib02, source, destination, iterations)
    results['pathlib03'] = test_copy(copy_pathlib03, source, destination, iterations)
    results['pathlib_chunks'] = test_copy(copy_pathlib_chunks, source, destination, iterations)
    results['custom01'] = test_copy(copy_custom01, source, destination, iterations)
    results['custom02'] = test_copy(copy_custom02, source, destination, iterations)
    results['custom03'] = test_copy(copy_custom03, source, destination, iterations)
    present_results(results)


def run_pathlib_test():
    logging.info(f'Testing pathlib functions')
    file_size = 1
    for i in range(1, 11):
        file_size = file_size * 2
        iterations = 1000
        if i >= 8:
            iterations = 10
        elif i >= 4:
            iterations = 100
        logging.info(f'Testing {iterations} iterations with {file_size} MB file')
        source, destination = setup(file_size=file_size)
        results = {'file_size': file_size}
        # Run tests
        results['pathlib'] = test_copy(copy_pathlib, source, destination, iterations)
        results['pathlib02'] = test_copy(copy_pathlib02, source, destination, iterations)
        results['pathlib03'] = test_copy(copy_pathlib03, source, destination, iterations)
        results['pathlib_chunks'] = test_copy(copy_pathlib_chunks, source, destination, iterations)
        present_results(results)


def run_chunks_test(file_size, iterations):
    iterations = iterations
    file_size = file_size
    source, destination = setup(file_size=file_size)
    # Run tests
    test_copy_chunks(copy_pathlib_chunks, file_size, iterations)
    # test_copy_chunks(copy_custom03, file_size, iterations)


def present_results(results: dict):
    logging.info('')
    logging.info(f'The results are in! [{results["file_size"]} MB]')
    results.pop('file_size')
    for n, i in enumerate(sorted(results, key=results.get)):
        if n == 0:
            winner = results[i]
            logging.info(f'{n + 1:>2}: {i:16} = {results[i]}')
        else:
            logging.info(f'{n + 1:>2}: {i:16} = {results[i]:<22} {round(((results[i] - winner) / winner) * 100, 2)}%')
    logging.info('')


def main():
    """docstring for main"""
    # Setup
    setup_logging(logging.INFO)
    # # Small files (jpg)
    # logging.info(f'Testing 5 MB file')
    # run_test(file_size=5, iterations=1000)
    # # Bigger files (raw)
    # logging.info(f'Testing 50 MB file')
    # run_test(file_size=50, iterations=100)
    # # Biggest files (video)
    # logging.info(f'Testing 1000 MB file')
    # run_test(file_size=1000, iterations=10)
    # Different sizes
    # file_size = 1
    # iterations = 1000
    # for s in range(1, 11):
    #     file_size = file_size * 2
    #     if s >= 8:
    #         iterations = 10
    #     elif s >= 4:
    #         iterations = 100
    #     logging.info(f'Testing {file_size} MB file')
    #     run_test(file_size=file_size, iterations=iterations)
    # Test chunk sizes
    # run_chunks_test(file_size=5, iterations=1000)
    # run_chunks_test(file_size=50, iterations=100)
    # run_chunks_test(file_size=1000, iterations=10)
    # Test pathlib
    run_pathlib_test()


if __name__ == '__main__':
    main()
