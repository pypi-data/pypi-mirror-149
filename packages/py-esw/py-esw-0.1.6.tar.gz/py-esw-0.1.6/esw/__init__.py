import requests
import os
import time


class ESWrapper:
    origin_tx = ['account', 'txlist', 0, 99999999, 'asc']

    def __init__(self, network, eth_api):

        self.url = network
        self.api = eth_api

    def get_origin_txn(self, account):
        call = self._call('account', 'txlist', start=0, end=99999999999,
                          account=account, sort='asc')

        origin_txn = call[0]
        hash = origin_txn['hash']
        block = origin_txn['blockNumber']
        time = origin_txn['timeStamp']
        creator = origin_txn['from']

        return {'hash': hash, 'block': block, 'time': time, 'creator': creator}

    def get_origin_block(self, contract):
        return self.get_origin_txn(contract)['block']

    def get_tx(self, contract, origin=None, function=None):
        start = origin if origin else self.get_origin_block(contract)
        call = self._call('account', 'txlist', start=start, end=99999999999,
                          account=contract, sort='asc', function=function)
        return call

    def get_from(self, contract, origin=None, function=None):
        start = origin if origin else self.get_origin_block(contract)
        call = self._call('account', 'txlist', start=start, end=99999999999,
                          account=contract, sort='asc', function=function)
        call = list(set(call[i]['from'] for i in range(len(call))))
        return call

    def get_current_block(self):
        ts = int(time.time())
        url = f'{self.url}module=block&action=getblocknobytime&timestamp={ts}&closest=before&apikey={self.api}'
        return int(requests.get(url).json()['result'])

    def get_logs(self, contract, topic, origin: int = None, function: str = None):
        start = origin if origin else self.get_origin_block(contract)
        call = self._call(module='logs', action='getLogs', start=start, end=99999999999,
                          account=contract, sort='asc', max_results=1000, function=function, other=f'{topic}')
        return call

    def _call(self, module, action, start, end, sort, account, max_results=10000, function=None, other=None):
        result = []
        while True:
            url = f'{self.url}module={module}&action={action}&address={account}&startblock={start}&endblock={end}&sort={sort}' \
                  f'&apikey={self.api}{other}'

            response = requests.get(url).json()['result']

            for r in response:
                if function:
                    if str(r['input']).startswith(function):
                        result.append(r)
                else:
                    result.append(r)

            if len(response) < max_results:
                break
            else:
                start = result[-1]['blockNumber']
                time.sleep(1)

        return result
