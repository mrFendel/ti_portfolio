import creds
from utils import download_all_shares_info


variants = [False, True]

for short in variants:
    for ru in variants:
        for api in variants:
            download_all_shares_info(acc_token=creds.token_ro_all,
                                     short=short,
                                     ru=ru,
                                     api_avalable=api)
