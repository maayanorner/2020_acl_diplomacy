import json
from os.path import join
from random import shuffle, sample
from itertools import zip_longest
import textwrap

import pandas as pd

def zip_equal(*iterables):
    sentinel = object()
    for combo in zip_longest(*iterables, fillvalue=sentinel):
        if sentinel in combo:
            raise ValueError('Iterables have different lengths')
        yield combo


def to_readable_full_conversation_format(gamefile):
    messages = []
    with open(gamefile) as inh:
        for ln in inh:
            conversation = json.loads(ln)
            for msg, sender_label, receiver_label, score_delta, speaker, receiver, \
                    year, season in zip_equal(
                            conversation['messages'],conversation['sender_labels'], \
                            conversation['receiver_labels'], conversation['game_score_delta'], \
                            conversation['speakers'], conversation['receivers'], \
                            conversation['years'],
                            conversation['seasons'],
                            
                        ):
                msg = {
                        'game_id': conversation['game_id'],
                        'year': year,
                        'season': season,
                        'speaker': speaker,
                        'receiver': receiver, 'message': msg, 'receiver_annotation': receiver_label,\
                        'sender_annotation':sender_label, 'score_delta': int(score_delta),
                        'players': conversation['players']
                    }
                messages.append(msg)
    return messages

def write_conversation(messages, outfile):
    df = pd.DataFrame(messages)
    df.to_csv(outfile)

def write_texts(messages, outfile):
    current_game_id = None
    #current_timestep = None
    #current_players = None

    with open(outfile, 'w') as f:
        for message in messages:
            if message['game_id'] != current_game_id:
                current_timestep = None
                current_players = None
                f.write(f'Game number {message["game_id"]:}\n')
                f.write('-'*10 + '\n')
                current_game_id = message['game_id']

            timestep = f'{message["year"]}, {message["season"]}'
            players =  ', '.join(message['players'])
            
            if current_players != players:
                current_players = players
                f.write('\n')
                f.write(f'Between {current_players}:\n')

            if timestep != current_timestep:
                current_timestep = timestep
                f.write(f'\n{current_timestep}:\n')
                f.write('-'*4 + '\n')
            no_long_messages = textwrap.wrap(f'{message["speaker"]}: {message["message"]}\n', width=130)
            pretty_text = '\n'.join(no_long_messages)
            f.write(f'{pretty_text}\n\n')
        
        
if __name__ == '__main__':
    ROOT = 'data/'
    
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'validation.jsonl')), 
                                                        join(ROOT, 'validation_conv.csv'))
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'train.jsonl')), 
                                                        join(ROOT, 'train_conv.csv'))
    write_conversation(to_readable_full_conversation_format(join(ROOT, 'test.jsonl')), 
                                                        join(ROOT, 'test_conv.csv'))


    write_texts(to_readable_full_conversation_format(join(ROOT, 'validation.jsonl')), 
                                                        join(ROOT, 'validation_conv.text'))
    write_texts(to_readable_full_conversation_format(join(ROOT, 'train.jsonl')), 
                                                        join(ROOT, 'train_conv.text'))
    write_texts(to_readable_full_conversation_format(join(ROOT, 'test.jsonl')), 
                                                        join(ROOT, 'test_conv.text'))
