# Scripts for running a Flask application on the localhost that receives post requests and sends the request body to logstash

### Sample Command for running the flask server
```python
python3 flask_server.py -c CONNECTOR_NAME -v VENDOR_NAME -p FLASK_PORT -H LOGSTASH_HOST -P LOGSTASH_PORT -t TENANT_NAME
```

### Sample Command for posting data to the flask server
```python
curl http://127.0.0.1:8080 -XPOST --header "Content-Type: application/json" --data '{"test":"this"}'
curl http://127.0.0.1:8080 -XPOST --header "Content-Type: application/json" --data '{"test":"that"}'
curl http://127.0.0.1:8080 -XPOST --header "Content-Type: application/json" --data '{"more":"body"}'
```
```python
curl http://127.0.0.1:8080 -XPOST --header "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"addEvents","params":{"events":[{"module":"hd","product_installed":"BEST","user":{"name":"Caitlyn.Todd@douglas.local","sid":"S-1-5-21-507437192-3947216968-132457944-34415"},"companyId":"60c2db52a0e78826f72bdbc5","computer_name":"DPNCL156","computer_fqdn":"dpncl156.douglas.local","computer_ip":"192.168.100.102","computer_id":"60e5079d3f2bd640e920fd5f","malware_type":"file","malware_name":"Gen:Illusion.PUP.Nirsoft.D.1010100","hash":"14801ff8d189dcd12374101754d0212be499fcea3cd2b967d1ae21e8bd6201e0","final_status":"still present","file_path":"C:\\Program Files\\QGIS 3.10\\bin\\nircmd.exe","attack_type":"targeted attack","detection_level":"permissive","is_fileless_attack":0,"process_info_path":"C:\\Users\\caitlyn.todd\\AppData\\Local\\Google\\Chrome\\User Data\\SwReporter\\92.267.200\\software_reporter_tool.exe","parent_process_id":10748,"parent_process_path":"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe","hwid":"4c4c4544-0059-4b10-8036-b9c04f364433-64c901f7db51","date":"2021-09-01T06:10:13.000Z"}]},"id":1630476633383}'
```
