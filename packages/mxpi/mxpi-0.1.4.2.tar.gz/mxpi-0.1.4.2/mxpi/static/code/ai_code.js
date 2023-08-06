Blockly.Python.yolo_fast_init=function(a){
    Blockly.Python.definitions_['yolo_fast_init'] = 'from Mx import yolo_fast';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var label = Blockly.Python.valueToCode(this,'LABEL',Blockly.Python.ORDER_ASSIGNMENT);
    var Anchor = Blockly.Python.valueToCode(this,'ANCHOR',Blockly.Python.ORDER_ASSIGNMENT);
    var obj = Blockly.Python.valueToCode(this,'OBJ',Blockly.Python.ORDER_ASSIGNMENT);
    var conf = Blockly.Python.valueToCode(this,'CONF',Blockly.Python.ORDER_ASSIGNMENT);
    var nms = Blockly.Python.valueToCode(this,'NMS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'yolo_fast.init('+model+','+label+','+Anchor+','+obj+','+conf+','+nms+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.yolo_fast_process=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.process('+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_face_detection=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var value = Blockly.Python.valueToCode(this,'VALUE',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.face_detection('+value+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_run=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_face_mesh=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.face_mesh('+max+','+dete+','+track+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_hands=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var model = this.getFieldValue('MODEL')
    var num = Blockly.Python.valueToCode(this,'NUM',Blockly.Python.ORDER_ASSIGNMENT);
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.hands('+model+','+num+','+dete+','+track+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_pose=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var model = this.getFieldValue('MODEL')
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var seg = Blockly.Python.valueToCode(this,'SEG',Blockly.Python.ORDER_ASSIGNMENT);
    var vis = Blockly.Python.valueToCode(this,'VIS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.pose('+model+','+dete+','+track+','+seg+','+vis+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.audio_classify=function(a){
    Blockly.Python.definitions_['audio_classify'] = 'from Mx import audio_classify';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'audio_classify.init('+model+','+max+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.audio_classify_run=function(a){
    var name = Blockly.Python.valueToCode(this,'VAR',Blockly.Python.ORDER_ASSIGNMENT);
    var wav = Blockly.Python.valueToCode(this,'WAV',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+wav+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.SoundThread=function(a){
    Blockly.Python.definitions_['audio_classify'] = 'from Mx import audio_classify';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var score = Blockly.Python.valueToCode(this,'SCORE',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'audio_classify.init_continue('+model+','+max+','+score+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.SoundThread_get=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.get()';
    return [code,Blockly.Python.ORDER_ATOMIC];
}
