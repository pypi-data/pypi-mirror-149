Blockly.Python.python_file_open=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ATOMIC) || null;
    var v = this.getFieldValue('V')
    var code = 'open('+name+',\"'+v+'\")'
    return [code,Blockly.Python.ORDER_ATOMIC];
  }


  Blockly.Python.python_file_open_msg=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ATOMIC) || null;
    var v = this.getFieldValue('V')
    var code = name+'.'+v
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_file_close=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ATOMIC) || null;
    var code = name+'.close()\n'
    return code;
  }

  Blockly.Python.python_file_write=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ATOMIC) || null;
    var body = Blockly.Python.valueToCode(this,'TXT',Blockly.Python.ORDER_ATOMIC) || null;
    var code = name+'.write('+body+')\n'
    return code;
  }

  Blockly.Python.python_file_read=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ATOMIC) || null;
    var body = this.getFieldValue('V');
    var code = name+'.'+body+"()"
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_time=function(a){
    Blockly.Python.definitions_['time'] = 'import time';
    var v = this.getFieldValue('V');
    var code = 'time.localtime(time.time())['+v+']'
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_time_time=function(a){
    Blockly.Python.definitions_['time'] = 'import time';
    var v = this.getFieldValue('V');
    var code = 'time.time()'
    return [code,Blockly.Python.ORDER_ATOMIC];
  }


  Blockly.Python.python_requests_null=function(a){
    Blockly.Python.definitions_['requests'] = 'import requests';
    var v = this.getFieldValue('V');
    var url = Blockly.Python.valueToCode(this,'URL',Blockly.Python.ORDER_ATOMIC);
    var code = 'requests.'+v+'('+url+')'
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_requests_params=function(a){
    Blockly.Python.definitions_['requests'] = 'import requests';
    var v = this.getFieldValue('V');
    var url = Blockly.Python.valueToCode(this,'URL',Blockly.Python.ORDER_ATOMIC);
    var par = Blockly.Python.valueToCode(this,'PAR',Blockly.Python.ORDER_ATOMIC);
    var code = 'requests.'+v+'(url='+url+',params='+par+')'
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_requests_read=function(a){
    Blockly.Python.definitions_['requests'] = 'import requests';
    var v = this.getFieldValue('V');
    var data = Blockly.Python.valueToCode(this,'DATA',Blockly.Python.ORDER_ATOMIC);
    var code = data+'.'+v
    return [code,Blockly.Python.ORDER_ATOMIC];
  }

  Blockly.Python.python_requests_set_encoding=function(a){
    Blockly.Python.definitions_['requests'] = 'import requests';
    var v = Blockly.Python.valueToCode(this,'V',Blockly.Python.ORDER_ATOMIC);
    var data = Blockly.Python.valueToCode(this,'DATA',Blockly.Python.ORDER_ATOMIC);
    var code = data+'.encoding='+v+'\n';
    return code;
  }

  Blockly.Python.mxpi_url=function(a){
    Blockly.Python.definitions_['Mx'] = 'import Mx';
    var code = 'Mx.url()';
    return [code,Blockly.Python.ORDER_ATOMIC];
  }