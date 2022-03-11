Updatetracker allows to post updates from multiple places and to query what updates happened when.

This is a useful component in monitoring liveliness of distributed IT systems.

## Usage

curl -X POST http://updatetracker.example.com/clear
curl -X POST http://updatetracker.example.com/update/foo
curl http://updatetracker.example.com/list

## Setup

in apache config add
<VirtualHost *>
  ServerName updatetracker.example.com
  ScriptAlias / /path/to/updatetracker.cgi/
</VirtualHost>

It needs 1 writable directory to store its updates in.
