import hashlib as hasher
import datetime as date
import csv
import pickle


class Block:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') + str(self.prev_hash).encode('utf-8'))
        return sha.hexdigest()


def create_genesis_block():
    return Block(0, date.datetime.now(), "Genesis Block", 0)


def next_block(last_block_index, last_block_hash):
    cur_index = last_block_index + 1
    cur_timestamp = date.datetime.now()
    cur_data = "New Block. Index is " + str(cur_index)
    cur_prev_hash = last_block_hash
    return Block(cur_index, cur_timestamp, cur_data, cur_prev_hash)


def read_dig_profile(file_name):
    with (open(file_name, "rb")) as digital_profile:
        while True:
            try:
                print(pickle.load(digital_profile))
            except EOFError:
                break
    digital_profile.close()


def write_dig_profile(file_name, data):
    digital_profile = open(file_name, "ab")
    pickle.dump(data, digital_profile)
    digital_profile.close()


def append_blockchain():
    chain_file = open("blockchain.csv", "r+", encoding='utf-8')
    chain_reader = csv.reader(chain_file, delimiter=";")
    chain_writer = csv.writer(chain_file, delimiter=";", lineterminator="\n")
    chain_block_row = []
    count = 0

    for row in chain_reader:
        chain_block_row = row
        count += 1

    if count == 0:
        first_block = create_genesis_block()
        chain_writer.writerow([first_block.hash, first_block.index, first_block.timestamp,
                               first_block.data, first_block.prev_hash])
        chain_block_row = [first_block.hash, first_block.index]

    block_to_add = next_block(int(chain_block_row[1]), chain_block_row[0])
    chain_writer.writerow([block_to_add.hash, block_to_add.index, block_to_add.timestamp,
                           block_to_add.data, block_to_add.prev_hash])
