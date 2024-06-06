This library supplies a mechanism to download water meter usage data for homes
serviced by a water company that uses `<town_name>.watersmart.com` URLs 
for such data.

It supplies a simple `watersmart-cli` CLI that prints all hourly logs, but
is generally expected to be used from another tool, like Home Assistant.

## Developing

```shell
python -m venv .venv
. .venv/bin/activate
pip install -e .[test]
python -m pytest .
```