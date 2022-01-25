import json
from os.path import join
from random import shuffle, sample

import pandas as pd


def to_readable_full_conversation_format(gamefile):
    messages = []
    with open(gamefile) as inh:
        for ln in inh:
            conversation = json.loads(ln)
            for msg, sender_label, receiver_label, score_delta, speaker, receiver, \
                    year, season in zip(
                            conversation['messages'],conversation['sender_labels'], \
                            conversation['receiver_labels'], conversation['game_score_delta'], \
                            conversation['speakers'], conversation['receivers'], \
                            conversation['years'],
                            conversation['seasons']
                        ):
                msg = {
                        'game_id': conversation['game_id'],
                        'year': year,
                        'season': season,
                        'speaker': speaker,
                        'receiver': receiver, 'message': msg, 'receiver_annotation': receiver_label,\
                        'sender_annotation':sender_label, 'score_delta': int(score_delta)
                    }
                messages.append(msg)
    return messages

def write_conversation(messages, outfile):
    df = pd.DataFrame(messages)
    df.to_csv(outfile)

if __name__ == '__main__':
    ROOT = 'data/'
    
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'validation.jsonl')), 
                                                        join(ROOT, 'validation_conv.csv'))
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'train.jsonl')), 
                                                        join(ROOT, 'train_conv.csv'))
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'test.jsonl')), 
                                                        join(ROOT, 'test_conv.csv'))
