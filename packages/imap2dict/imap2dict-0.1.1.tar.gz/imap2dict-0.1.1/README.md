# imap2dict

## Description

`imap2dict` is a Python library for receiving and deleting emails from an IMAP4 server.

## Installaction

```bash
pip install imap2dict
```

## Usage

```python
from imap2dict import MailClient

host_name = 'mail.example.com'
user_id = 'foo'
password = 'password'

cli = MailClient(host_name, user_id, password)

# Receive email (`search_option` and `timezone` are optional.)
messages = cli.fetch_mail(search_option='UNSEEN', timezone='Asia/Tokyo')
for msg in messages:
    print('UID: {}'.format(msg['uid']))
    print('Subject: {}'.format(msg['subject']))
    print('Body: {}'.format(msg['body']))
    print('From: {}'.format(msg['from']))
    print('To: {}'.format(msg['to']))
    print('Cc: {}'.format(msg['cc']))
    print('Date: {}'.format(msg['date']))
    print('Time: {}'.format(msg['time']))
    print('Format: {}'.format(msg['format']))
    print('Message-ID: {}'.format(msg['msg_id']))
    print('Header: {}'.format(msg['header']))
    for att in msg['attachments']:
        print('File Name: {}'.format(att['file_name']))
        print('File Object: {}'.format(att['file_obj']))
```
