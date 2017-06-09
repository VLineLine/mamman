import process, task, pprint

var = task.read_first() #reading one process
process_id = var.pop('id') #popping ID
var.update({'process_id': process_id }) #adding process ID

pprint.pprint(var)
task.post(var)
