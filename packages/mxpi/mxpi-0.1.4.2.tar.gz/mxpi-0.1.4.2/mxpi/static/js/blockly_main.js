
var auto_update=true
editor = monaco.editor.create(document.getElementById('monaco'), {
  value: "// No code",
  language: "python",
  automaticLayout: true,
  folding: true,
  theme: 'vs',
  tabSize: 4,//缩进
  fontSize:15,
  lineNumbersMinChars: 3,//显示行号的位数
  minimap: { enabled: this.minimap },
  formatOnPaste: true,//复制粘贴的时候格式化
  foldingStrategy: 'indentation', // 代码可分小段折叠
});
Blockly.Themes.Halloween = Blockly.Theme.defineTheme('halloween', {
    'base': Blockly.Themes.Classic,
    'categoryStyles': {
    'list_category': {
       'colour': "#7158e2"
     },
     'print_category': {
       'colour': '#f0932b',
     },
     'sound_category': {
      'colour': '#336666',
    },
     'loop_category': {
       'colour': "#43A047",
     },
     'text_category': {
       'colour': "#10ac84",
     },
     'math_category': {
        'colour': "#22a6b3",
      },
      'logic_category': {
        'colour': "#40739e",
      },
      'tuple_category': {
        'colour': "#D1A36E",
      },
      'dict_category': {
        'colour': "#B1533C",
      },
      'catSet_category': {
        'colour': "#009933",
      },
      'GPIO_category': {
        'colour': "#c19e10",
      },
      'display_category': {
        'colour': "#FF9900",
      },
      'actuator_category':{
        'colour': "#336699",
      },
      'sensor_category': {
        'colour': "#bc954e",
      },
      'OpenCV_category': {
        'colour': "#0099CC",
      },
      'blynk_category': {
        'colour': "#009966",
      },
      'AI_category': {
        'colour': "#009966",
      },
      'GUI_category': {
        'colour': "#00a8a8",
      },
      'BaiduAI_category': {
        'colour': "#0099CC",
      },
      'neizhi_category': {
        'colour': "#CC3333",
      },
      'vari_category': {
        'colour': "#af5180",
      },
      'pro_category': {
        'colour': "#6D318E",
      },
    },
    'blockStyles': {
     'list_blocks': {
       'colourPrimary': "#fff",
       'colourSecondary':"#fff",
       'colourTertiary':"#fff"
     },
     'print_blocks': {
       'colourPrimary': "#f0932b",
       'colourSecondary':"#fff",
       'colourTertiary':"#F9A825"
     }, 
     'logic_blocks': {
      'colourPrimary': "#41759f",
      'colourSecondary':"#fff",
      'colourTertiary':"#7aa6c7"
    }, 
     'loop_blocks': {
       'colourPrimary': "#85E21F",
       'colourSecondary':"#fff",
       'colourTertiary':"#C5EAFF"
     }, 
     'OpenCV_blocks': {
      'colourPrimary': "#0099CC",
      'colourSecondary':"#fff",
      'colourTertiary':"#0099CC"
    }, 
    'blynk_blocks': {
      'colourPrimary': "#009966",
      'colourSecondary':"#fff",
      'colourTertiary':"#009966"
    }, 
    'AI_blocks': {
      'colourPrimary': "#009966",
      'colourSecondary':"#fff",
      'colourTertiary':"#009966"
    }, 
    'sensor_blocks': {
      'colourPrimary': "#bc954e",
      'colourSecondary':"#fff",
      'colourTertiary':"#bc954e"
    }, 
    'sound_blocks': {
      'colourPrimary': "#336666",
      'colourSecondary':"#fff",
      'colourTertiary':"#336666"
    }, 
    'actuator_blocks': {
      'colourPrimary': "#336699",
      'colourSecondary':"#fff",
      'colourTertiary':"#336699"
    }, 
     'GPIO_blocks': {
      'colourPrimary': "#c19e10",
      'colourSecondary':"#fff",
      'colourTertiary':"#c19e10"
    }, 
    'display_blocks': {
      'colourPrimary': "#d9bf54",
      'colourSecondary':"#fff",
      'colourTertiary':"#d9bf54"
    }, 
    'neizhi_blocks': {
      'colourPrimary': "#CC3333",
      'colourSecondary':"#fff",
      'colourTertiary':"#CC3333"
    }, 
    'BaiduAI_blocks': {
      'colourPrimary': "#0099CC",
      'colourSecondary':"#fff",
      'colourTertiary':"#0099CC"
    }, 
    'GUI_blocks': {
      'colourPrimary': "#00a8a8",
      'colourSecondary':"#fff",
      'colourTertiary':"#00a8a8"
    }, 
     'text_blocks': {
       'colourPrimary': "#f0932b",
       'colourSecondary':"#66BB6A",
       'colourTertiary':"#C5EAFF"
     } 
    },
    'componentStyles': {
      'workspaceBackgroundColour': '#fff',
      'toolboxBackgroundColour': '#EEEEEE',
      'toolboxForegroundColour': '#fff',
      'flyoutBackgroundColour': '#E0E0E0',
      'flyoutForegroundColour': '#252526',
      'flyoutOpacity': 0.5,
      'scrollbarColour': '#757575',
      'insertionMarkerColour': '#fff',
      'insertionMarkerOpacity': 0.3,
      'scrollbarOpacity': 0.4,
      'cursorColour': '#d0d0d0',
      'blackBackground': '#333'
    }
  });

var blocklyArea = document.getElementById('blocklyArea');
var blocklyDiv = document.getElementById('blocklyDiv');
var codesapce = document.getElementById('monaco');
var wnum = blocklyArea .offsetWidth
var workspace = Blockly.inject(blocklyDiv,
    {   disable:true,
        toolbox: document.getElementById('toolbox-categories'),
        media:'./static/media/',
        theme: Blockly.Themes.Halloween,
        grid:   {spacing: 20,
                length: 1,
                colour: '#ccc',
                snap: true},
        move:  {
            scrollbars: {
              horizontal: true,
              vertical: true
            },
            drag: true,
            wheel: false},
        zoom:
            {controls: true,
             wheel: true,
             startScale: 1.0,
             maxScale: 3,
             minScale: 0.3,
             scaleSpeed: 1.3,
             pinch: true},
        trashcan: true,
        
});
var onresize = function(e) {
  // Compute the absolute coordinates and dimensions of blocklyArea.
  var element = blocklyArea;
  var x = 0;
  var y = 0;
  do {
    x += element.offsetLeft;
    y += element.offsetTop;
    element = element.offsetParent;
    
  } while (element);
  // Position blocklyDiv over blocklyArea.
  codesapce.style.width = wnum-blocklyDiv.offsetWidth+'px'
  blocklyDiv.style.left = x + 'px';
  blocklyDiv.style.top = y + 'px';
  blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
  blocklyDiv.style.height = blocklyArea.offsetHeight+ 'px';
  //console.log(blocklyDiv.style.width)
  Blockly.svgResize(workspace);
};
window.addEventListener('resize', onresize, false);
onresize();
Blockly.svgResize(workspace);

function myUpdateFunction(event) {
  //var content = document.getElementById('content_python')
  //content.textContent = '';
  var code = Blockly.Python.workspaceToCode(workspace);
  //content.textContent = code;
  console.log(code)
  //content.className = content.className.replace('prettyprinted', '');
}
workspace.addChangeListener(myUpdateFunction);
var sidecodeDisplay=false;
function sidecodeClick(){
  if(sidecodeDisplay){
  document.getElementById('side_code_parent').style.display = 'none';
  document.getElementById('sidebar').className='right-top';
  document.getElementById('mid_td').style.display = 'none';
  sidecodeDisplay=false;
  }else{
  document.getElementById('side_code_parent').style.display = '';
  document.getElementById('sidebar').className='right-top2';
  document.getElementById('mid_td').style.display = '';
  sidecodeDisplay=true;
  }
  Blockly.fireUiEvent(window, 'resize');
}

function changeThemeFile( theme )
    {
      monaco.editor.setTheme(theme)
    }
$("#CheckboxId").click(function() {
  var check = document.getElementById('CheckboxId')
  if (check.checked==true){
    auto_update=true
  }
  else{
    auto_update=false
  }
}); 
$("#Dark").click(function() {
  changeThemeFile('vs-dark')
}); 
$("#Light").click(function() {
  changeThemeFile('vs')
}); 
$("#Purple").click(function() {
  changeThemeFile('hc-black')
}); 
var require = {
  paths: { vs: "static/onaco-editor/min/vs" },
  "vs/nls": { availableLanguages: { "*": "zh-cn" } },
};
workspace.addChangeListener(rightCodeEvent);
function rightCodeEvent(masterEvent) {
  if (masterEvent.type == Blockly.Events.UI) {
  return;  // Don't update UI events.
  }
  //更新
  var code = Blockly.Python.workspaceToCode(Blockly.mainWorkspace) || '';
  console.log(code)
  if (auto_update==true)
    {
      if (code){
      editor.setValue(code);
      }
      else{
      editor.setValue('');
      }
    }
}

function upcode(){
    var code = Blockly.Python.workspaceToCode(workspace);
    return code
}

function savefile(){
  const xml = Blockly.Xml.workspaceToDom(workspace);
  const xmlText = Blockly.Xml.domToText(xml);
  return xmlText
}

function openfile(data){
  workspace.clear();
  const xml = Blockly.Xml.textToDom(data);
  Blockly.Xml.domToWorkspace(xml, workspace);
  return "项目已打开"
}
var list_num=0
var list_nums=0
var list_num_pip=0
var list_nums_pip=0
var UpBtn = document.getElementById("upfile");
var run_run=false
function upfile(){
  if (run_run==false){
    list_num=0
    list_nums=0
	  var code = editor.getValue()
    var fd = new FormData();
    fd.append('code',code)
	  $.ajax({
	    url:"./upfile_Ajax",
	    type:"post",
	    data:fd,
      contentType: false,  
      processData: false, 
	    success:function(data1){
		console.log(data1)
    clears()
    upclock()
		add('上传成功,开始运行...')
		chatSocket.send(JSON.stringify({'msg':'run'}))
		UpBtn.innerHTML='<i class="fa fa-stop" aria-hidden="true"></i>'
    document.getElementById('upfile').className='button button-action4 button-box';
		run_run=true
	    }
	    })
	}
 else{
    console.log('stop')
    chatSocket.send(JSON.stringify({'msg':'stop'}))
  }
}
var slider1,slider2,slider3,slider4,slider5,slider5,slider6
var h_min=0
var s_min=0
var v_min=0
var h_max=0
var s_max=0
var v_max=0
var instance
var chatSocket
var c
var con_btn=document.getElementById('connect_server')
var con_btn_ui=document.querySelector("#connect_server > i")
var editor
window.onload = function () {      /*chushihua*/
  slider1 = new Slider("#ex1",{tooltip:'hide'});
  slider1.on("slide", function(slideEvt1) {
    $("#ex1SliderVal").text(slideEvt1.value);
    h_min=Number(slideEvt1.value)
    cv2_inRange()
  });       
  slider2 = new Slider("#ex2",{tooltip:'hide'});
  slider2.on("slide", function(slideEvt2) {
    $("#ex2SliderVal").text(slideEvt2.value);
    s_min=Number(slideEvt2.value)
    cv2_inRange()
  });   
  slider3 = new Slider("#ex3",{tooltip:'hide'});
  slider3.on("slide", function(slideEvt3) {
    $("#ex3SliderVal").text(slideEvt3.value);
    v_min=Number(slideEvt3.value)
    cv2_inRange()
  });   
  slider4 = new Slider("#ex4",{tooltip:'hide'});
  slider4.on("slide", function(slideEvt4) {
    $("#ex4SliderVal").text(slideEvt4.value);
    h_max=Number(slideEvt4.value)
    cv2_inRange()
  });   
  slider5 = new Slider("#ex5",{tooltip:'hide'});
  slider5.on("slide", function(slideEvt5) {
    $("#ex5SliderVal").text(slideEvt5.value);
    s_max=Number(slideEvt5.value)
    cv2_inRange()
  });   
  slider6 = new Slider("#ex6",{tooltip:'hide'});
  slider6.on("slide", function(slideEvt6) {
    $("#ex6SliderVal").text(slideEvt6.value);
    v_max=Number(slideEvt6.value)
    cv2_inRange()
  }); 
  slider1.disable();     
  slider2.disable();  
  slider3.disable();  
  slider4.disable();  
  slider5.disable();   
  slider6.disable();              
  chatSocket = new WebSocket('ws://' + window.location.host + '/ws/run/');
  chatSocket.onopen = function () {
    console.log(' ' + 'websocket connection success')
    chatSocket.send(JSON.stringify({'msg':'loadclock'}))
    add('已与树莓派端建立连接')
    c=true
    con_btn.style.color='#00aa1c'
    con_btn_ui.className='fa fa-link'
    
  };
  chatSocket.onerror = function () {
    console.error(' ' + 'websocket connection error')
    add('树莓派端连接失败')
  };
  chatSocket.onclose = function (e) {
    console.error(' ' + 'websocket closed unexpectedly 状态码:' + e.code);
    add('与树莓派端已断开连接,请重新连接...'+' ' + 'websocket closed unexpectedly 状态码:' + e.code)
    con_btn.style.color='#F44336'
    con_btn_ui.className='fa fa-chain-broken'
    c=false
    chatSocket.close();
  };
  chatSocket.onmessage = function (e) {
    var data=JSON.parse(e.data)
    
    if(data['msg']=='run_msg'){
    add(data['data'])
    console.log(data)
    }
    else if (data['msg']=='run_err_msg'){
    adderr(data['data'])
    console.log(data)
    }
    else if(data['msg']=="stop"){
      console.log(data)
      add(data['data'])
      UpBtn.innerHTML='<i class="fa fa-play" aria-hidden="true"></i>'
      document.getElementById('upfile').className='button button-action3 button-box';
      run_run=false
    }
    else if(data['msg']=='pip_msg'){
      console.log(data)
      addpip(data['data'])
    }
    else if(data['msg']=='pip_err_msg'){
      console.log(data)
      addpip_err(data['data'])
    }
    else if(data['msg']=='pip_stop'){
      console.log(data)
      addpip(data['data'])
    }
    else if(data['msg']=='run_msg_err'){
      console.log(data)
      adderr(data['data'])
    }
    else if(data['msg']=='load_msg'){
      console.log(data)
      openfile(data['data'])
    }
    else if(data['msg']=='remote_desktop'){
      var path='data:image/png;base64,'+data['data']
      $("#dk").attr('src',path);
    }
  }
 var oBox = document.getElementById("blockly_box"); 
 var oTop = document.getElementById("blocklyDiv"); 
 var oTop1 = document.getElementById("blocklyArea");
 var oBottom = document.getElementById("side_code_parent");
 var oBottom1 = document.getElementById("output_img");
 var oLine = document.getElementById("mid_td");

 oLine.onmousedown = function(e) {
 	var disX = (e || event).clientX;
 	oLine.left = oLine.offsetLeft;

 	document.onmousemove = function(e) {
 		//console.log(oBox.clientWidth + " " + oLine.style.left + " " + disX + " " + (e || event).clientX);	
  		var iT = oLine.left + ((e || event).clientX - disX);
 		var e=e||window.event,tarnameb=e.target||e.srcElement;
  		var maxT = oBox.clientWidth;
		var minT = Blockly.mainWorkspace.toolbox_.width;
  		oLine.style.margin = 0;
  		iT < minT && (iT = minT);
  		iT > maxT && (iT = maxT);
		//console.log(oBox.clientWidth+" "+iT+" "+oTop1.style.width+" "+oTop.style.width);
		var percent=iT*100/oBox.clientWidth;
  		oTop1.style.width = percent + '%';
  		oTop.style.width = percent  + '%';  // no need this line
  		oLine.style.left = percent  + '%';
  		Blockly.fireUiEvent(window, 'resize');
  		oBottom.style.width = ( 100 - percent ) + '%';
        if(oBottom1 !== null) oBottom1.style.width = (oBox.clientWidth - iT) + "px";
  		return false;
 	}; 
 	document.onmouseup = function() {
  		document.onmousemove = null;
  		document.onmouseup = null; 
  		Blockly.fireUiEvent(window, 'resize');
  		oLine.releaseCapture && oLine.releaseCapture();
 	};
 	oLine.setCapture && oLine.setCapture();
 	return false;
 };
 new Tippy('.tippy',{theme:'light'})
 QuickDemo()
 $(".col-3 input").val("");
  $(".input-effect input").focusout(function(){
    if($(this).val() != ""){
      $(this).addClass("has-content");
    }else{
    $(this).removeClass("has-content");
    }
  });
  
  instance=$('.e-scrollbar-box-2,.e-scrollbar-box-1').overlayScrollbars({
    className       : "os-theme-dark",
    resize          : "none",
    sizeAutoCapable : true,
    paddingAbsolute : true,
    scrollbars : {clickScrolling : true,
                  autoHide :'never'
                  },
                  autoUpdateInterval:true
  }).overlayScrollbars();
  window.setInterval(function (){
    var code=savefile()
    chatSocket.send(JSON.stringify({'msg':'upclock','code':code}))
    add('自动缓存程序...')
  },10*60*1000);
} 
                                                         /*chushihua*/
function upclock()
  {
    var code=savefile()
    chatSocket.send(JSON.stringify({'msg':'upclock','code':code}))
    add('缓存程序...')
  }
var oScroll = document.getElementById("scrollOne");
var i=0

function clears() {
  var oP = document.querySelector("#cmd_ > div.os-padding > div > div")
  oP.innerHTML = '';

}

function clearss() {
  var oP = document.querySelector("#pip_cmd > div.os-padding > div > div")
  oP.innerHTML = '';
}

function mySplit(str,leng){
  let arr = [];
  let index = 0;
  while(index<str.length){
  arr.push(str.slice(index,index +=leng));
  }
  return arr;
  }

  function addpip(txt) {
    list_num_pip = list_num_pip+1
    list_nums_pip = list_nums_pip+1
    if(list_num_pip>1000){
    clearss()
    list_num_pip=0
	}	
    var oP = document.querySelector("#pip_cmd > div.os-padding > div > div")
    var oPs =document.createElement("p");
    var num= list_nums_pip
    oPs.innerHTML = "<div class='d1'><div class='d2'><a class='num'>"+num+"</a></div><div class='d3'><a class='d4'>"+txt+"</a></div></div>";
    oP.appendChild(oPs)
    instance[1].scroll({ y : "100%"  });
}

function add(txt) {
    list_num = list_num+1
    list_nums = list_nums+1
    if(list_num>300){
    clears()
    list_num=0
    list_nums=0
	}	
    var oP = document.querySelector("#cmd_ > div.os-padding > div > div")
    var oPs =document.createElement("p");
    var num= list_nums
    oPs.innerHTML = "<div class='d1'><div class='d2'><a class='num'>"+num+"</a></div><div class='d3'><a class='d4'>"+txt+"</a></div></div>";
    oP.appendChild(oPs)
    instance[0].scroll({ y : "100%"  });
}
function adderr(txt) {
  list_num = list_num+1
  list_nums = list_nums+1
  if(list_num>500){
  clears()
  list_num=0
}	
  var oP = document.querySelector("#cmd_ > div.os-padding > div > div")
  var oPs =document.createElement("p");
  var num= list_nums
  oPs.innerHTML = "<div class='d1'><div class='d2-err'><a class='num'>"+num+"</a></div><div class='d3-err'><a class='d4-err'>"+txt+"</a></div></div>";
  oP.appendChild(oPs)
  instance[0].scroll({ y : "100%"  });
}

function addpip_err(txt) {
  list_num = list_num+1
  list_nums = list_nums+1
  if(list_num>2000){
  clearss()
  list_num=0
}	
  var oP = document.querySelector("#pip_cmd > div.os-padding > div > div")
  var oPs =document.createElement("p");
  var num= list_nums
  oPs.innerHTML = "<div class='d1-err'><div class='d2-err'><a class='num'>"+num+"</a></div><div class='d3-err'><a class='d4-err'>"+txt+"</a></div></div>";
  oP.appendChild(oPs)
  instance[1].scroll({ y : "100%"  });
}

function save(){
  var code=savefile()
  myExport('MxPi.mxpi', code );
  
}
function savepy(){
  var code=upcode()
  myExport('MxPi.py', code );
  
}

function fake_click(obj) {
  var ev = document.createEvent("MouseEvents");
  ev.initMouseEvent(
    "click", true, false, window, 0, 0, 0, 0, 0
    , false, false, false, false, 0, null
  );
  obj.dispatchEvent(ev);
}

function myExport(name, data) {
  var urlObject = window.URL || window.webkitURL || window;
  var myFile = new Blob([data]);
  var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a");
  save_link.href = urlObject.createObjectURL(myFile);
  save_link.download = name;
  fake_click(save_link);
}

function open_program(){
  $("#files").click();
}

function fileImport() {
  //获取读取我文件的File对象
  var selectedFile = document.getElementById('files').files[0];
  var name = selectedFile.name; //读取选中文件的文件名
  var size = selectedFile.size; //读取选中文件的大小
  console.log("文件名:" + name + "大小:" + size);
  var reader = new FileReader(); //这是核心,读取操作就是由它完成.
  reader.readAsText(selectedFile); //读取文件的内容,也可以读取文件的URL
  reader.onload = function() {
      //当读取完成后回调这个函数,然后此时文件的内容存储到了result中,直接操作即可
      console.log(this.result);
      openfile(this.result)
  }
}

function QuickDemo(){
  $("#authors").PopupWindow({
    height      : 410,
    width       : 600,
    title       : "关于",
    autoOpen    : false,
    buttons         : {
      close           : true,          // Boolean
      maximize        : false,          // Boolean
      collapse        : false,          // Boolean
      minimize        : false,          // Boolean
  },
  buttonsTexts        : {
    close               : "退出",
    maximize            : "最大化",
    minimize            : "最小化",
    collapse            : "搜索",
  }, 
  draggable           : true,
  nativeDrag          : true,
  dragOpacity         : 1,
  resizable:false,
  resizeOpacity: 1,
  });

  $("#pip_content").PopupWindow({
      height      : 620,
      width       : 880,
      title       : "库管理",
      autoOpen    : false,
      buttons         : {
        close           : true,          // Boolean
        maximize        : false,          // Boolean
        collapse        : false,          // Boolean
        minimize        : false,          // Boolean
    },
    buttonsTexts        : {
      close               : "退出",
      maximize            : "最大化",
      minimize            : "最小化",
      collapse            : "搜索",
    }, 
    draggable           : true,
    nativeDrag          : true,
    dragOpacity         : 1,
    resizable:false,
    resizeOpacity: 1,
  });
  $("#file_content").PopupWindow({
    height      : 620,
    width       : 1000,
    title       : "文件管理",
    autoOpen    : false,
    buttons         : {
      close           : true,          // Boolean
      maximize        : false,          // Boolean
      collapse        : false,          // Boolean
      minimize        : false,          // Boolean
  },
  buttonsTexts        : {
    close               : "退出",
    maximize            : "最大化",
    minimize            : "最小化",
    collapse            : "搜索",
  }, 
  draggable           : true,
  nativeDrag          : true,
  dragOpacity         : 1,
  resizable:false,
  resizeOpacity: 1,
});
$("#HSV_content").PopupWindow({
  height      : 650,
  width       : 1000,
  title       : "阈值编辑器",
  autoOpen    : false,
  buttons         : {
    close           : true,          // Boolean
    maximize        : false,          // Boolean
    collapse        : false,          // Boolean
    minimize        : false,          // Boolean
},
buttonsTexts        : {
  close               : "退出",
  maximize            : "最大化",
  minimize            : "最小化",
  collapse            : "搜索",
}, 
draggable           : true,
nativeDrag          : true,
dragOpacity         : 1,
resizable:false,
resizeOpacity: 1,
});
$("#DK_content").PopupWindow({
  height      : 700,
  width       : 1200,
  title       : "桌面图像",
  autoOpen    : false,
  buttons         : {
    close           : true,          // Boolean
    maximize        : false,          // Boolean
    collapse        : false,          // Boolean
    minimize        : false,          // Boolean
},
buttonsTexts        : {
  close               : "退出",
  maximize            : "最大化",
  minimize            : "最小化",
  collapse            : "搜索",
}, 
draggable           : true,
nativeDrag          : true,
dragOpacity         : 1,
resizable:false,
resizeOpacity: 1,
});
$("#hear_content").PopupWindow({
  height      : 260,
  width       : 600,
  title       : "音频播放",
  autoOpen    : false,
  buttons         : {
    close           : true,          // Boolean
    maximize        : false,          // Boolean
    collapse        : false,          // Boolean
    minimize        : false,          // Boolean
},
buttonsTexts        : {
  close               : "退出",
  maximize            : "最大化",
  minimize            : "最小化",
  collapse            : "搜索",
}, 
draggable           : true,
nativeDrag          : true,
dragOpacity         : 1,
resizable:false,
resizeOpacity: 1,
});

  $("#filemodel").on("click", function(event){
      $("#file_content").PopupWindow("open");
      file_list()
  });
  $("#pipmodel").on("click", function(event){
    $("#pip_content").PopupWindow("open");
    pip_list()
  });
  $("#authormodel").on("click", function(event){
    $("#authors").PopupWindow("open");
  });
  $("#HSVmodel").on("click", function(event){
    $("#HSV_content").PopupWindow("open");
  });
  $("#DKmodel").on("click", function(event){
    var dk=chatSocket.send(JSON.stringify({'msg':'remote_desktop'}))
    $("#DK_content").PopupWindow("open");
  });
}

$("#pip_content").on("minimize.popupwindow", function(event){
  var models=document.getElementsByClassName('popupwindow_overlay')
  models[0].style.width='0px'
})

$("#pip_content").on("collapse.popupwindow", function(event){
  var models=document.getElementsByClassName('popupwindow_overlay')
  models[0].style.width='0px'
})

$("#pip_content").on("unminimize.popupwindow", function(event){
  var models=document.getElementsByClassName('popupwindow_overlay')
  models[0].style.width='100%'
})

$("#pip_content").on("uncollapse.popupwindow", function(event){
  var models=document.getElementsByClassName('popupwindow_overlay')
  models[0].style.width='100%'
})
var wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: 'violet',
  progressColor: 'purple'
});
function hear_wav(url){
wavesurfer.load(url);
}
function pipinstall(){
  clearss()
  list_num_pip=0
  list_nums_pip=0
  var pip_install_name=document.getElementById('pip_install_name').value;
  chatSocket.send(JSON.stringify({'msg':'pip_install','name':pip_install_name,'url':'https://pypi.doubanio.com/simple'}))
}

function connect_server(){
  if(c==false){
    add('开始连接树莓派端')
    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/run/');
    chatSocket.onopen = function () {
      console.log(' ' + 'websocket connection success')
      add('已与树莓派端建立连接')
      con_btn.style.color='#00aa1c'
      con_btn_ui.className='fa fa-link'
      con_btn.disable=false
      
    };
    chatSocket.onerror = function () {
      console.error(' ' + 'websocket connection error')
      add('树莓派端连接失败')
    };
    chatSocket.onclose = function (e) {
      console.error(' ' + 'websocket closed unexpectedly 状态码:' + e.code);
      add('与树莓派端已断开连接,请重新连接...'+' ' + 'websocket closed unexpectedly 状态码:' + e.code)
      con_btn.style.color='#F44336'
      con_btn_ui.className='fa fa-chain-broken'
      document.querySelector("body > div:nth-child(16) > div > div.tippy-tooltip-content").innerHTML='重新连接'
      con_btn.disable=true
      chatSocket.close();
    };
    chatSocket.onmessage = function (e) {
      var data=JSON.parse(e.data)
      console.log(data)
      if(data['msg']=='run_msg'){
      add(data['data'])
      }
      else if (data['msg']=='run_err_msg'){
      adderr(data['data'])
      }
      else if(data['msg']=="stop"){
        add(data['data'])
        UpBtn.innerHTML='<i class="fa fa-play" aria-hidden="true"></i>'
        document.getElementById('upfile').className='button button-action3 button-box';
        run_run=false
      }
      else if(data['msg']=='pip_msg'){
        addpip(data['data'])
      }
      else if(data['msg']=='pip_err_msg'){
        addpip_err(data['data'])
      }
      else if(data['msg']=='pip_stop'){
        addpip(data['data'])
      }
      else if(data['msg']=='remote_desktop'){
        var path='data:image/png;base64,'+data['data']
        $("#dk").attr('src',path);
      }
    }
  }
}
function dateFormat(fmt, date) {
  let ret;
  const opt = {
      "Y+": date.getFullYear().toString(),        // 年
      "m+": (date.getMonth() + 1).toString(),     // 月
      "d+": date.getDate().toString(),            // 日
      "H+": date.getHours().toString(),           // 时
      "M+": date.getMinutes().toString(),         // 分
      "S+": date.getSeconds().toString()          // 秒
  };
  for (let k in opt) {
      ret = new RegExp("(" + k + ")").exec(fmt);
      if (ret) {
          fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
      };
  };
  return fmt;
}
function file_list(){
  var printIcon = function(value, data, cell, row, options){ //plain text value
    var file_type=data.url.substring(data.url.lastIndexOf('.') + 1);
    var jpg_=['png', 'jpg','JPG', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff']
    var wav_=['wav']
    let result =jpg_.indexOf(file_type)
    let result_wav =wav_.indexOf(file_type)
    if(result>-1){
      return "<div style='display:flex;justify-content: flex-start;'><div onclick='copy(\""+data.url+"\")'><i class='fa fa-clipboard' style='color: #00bd15;margin-right: 30px;margin-left: 30px;'></i></div><i id='eye' class='fa fa-eye' style='color:#0099CC;margin-right: 30px;' onclick='see_img(\""+data.url+"\")'></i><i class='fa fa-close' style='color: red;' onclick='del(\""+data.url+"\")'></i></div>"
    }
    else{
      if (result_wav>-1)
      {return "<div style='display:flex;justify-content: flex-start;'><div onclick='copy(\""+data.url+"\")'><i class='fa fa-clipboard' style='color: #00bd15;margin-right: 30px;margin-left: 30px;'></i></div><i class='hears fa  fa-play-circle' style='color:#0099CC;margin-right: 30px;'onclick='hear_wav(\""+data.url_g+"\")'></i><i class='fa fa-close' style='color: red;' onclick='del(\""+data.url+"\")'></i></div>"}
      else{return "<div style='display:flex;justify-content: flex-start;'><i class='fa fa-clipboard' style='color: #00bd15;margin-right: 75px;margin-left: 30px;' onclick='copy(\""+data.url+"\")'></i><i class='fa fa-close' style='color: red;' onclick='del(\""+data.url+"\")'></i></div>"}
    }
  };
  $("#file_list").tabulator({
    columns:[
      {title:"名称", field:"name", sortable:true, sorter:"string", width:'30%', align:'center' ,editable:false},
      {title:"大小", field:"size", sortable:true, sorter:"number", width:'30%',align:'center' ,editable:false},
      {title:"修改时间", field:"last", sortable:true, sorter:"string", width:'20%',align:'center' ,editable:false},
      {title:"操作", field:"operate", sortable:false, sorter:"string",width:'20%', align:'left',formatter:printIcon},
  ],
  height:'450px',
  });

  $.ajax({
    url:"./file_list",
    type:"GET",
    data:{},
    success:function(data1){
        var data=JSON.parse(data1)
        for(da of data['data']){
          da['last']=dateFormat("YYYY/mm/dd HH:MM:SS", new Date(da['last']))
        }
          $("#file_list").tabulator("setData",data['data'])
        for (da of data['data']){
          $(".hears").on("click", function(event){
            $("#hear_content").PopupWindow("open");
          });
        }
      }
    })
}

function copy(data) {
  let transfer = document.createElement('input');
  document.body.appendChild(transfer);
  transfer.value = data;  // 这里表示想要复制的内容
  transfer.focus();
  transfer.select();
  if (document.execCommand('copy')) {
      document.execCommand('copy');
  }
  transfer.blur();
  document.body.removeChild(transfer);
  spop({
    template: '复制成功',
    position  : 'top-right',
    autoclose: 1500,
    style: 'success'
  });
}

function del(data){
  console.log(data)
  $.ajax({
    url:"./file_remove",
    type:"GET",
    data:{'data':data},
    success:function(data1){
      console.log(data1)
      spop({
        template: '删除成功',
        position  : 'top-right',
        autoclose: 1500,
        style: 'success'
      });
      file_list()
      }
    })
}

$(".upfile").on("change","input[type='file']",function(){
  document.querySelector("#load-ico").style.visibility="visible";
  var fd = new FormData();
  fd.append("avatar",$("#i1")[0].files[0]);
 $.ajax({
     url: '/files',
     type: 'post',
     data: fd,
     contentType: false,  
     processData: false,
     xhr: function() { //用以显示上传进度  
      var xhr = $.ajaxSettings.xhr();
      if (xhr.upload) {
            xhr.upload.addEventListener('progress', function(event) {
                var percent = Math.floor(event.loaded / event.total * 100); //进度值（百分比制）
                console.log(percent)
                document.getElementById('fileupp').innerHTML=percent+'%'
            }, false);
          }
          return xhr
      },
     success:function (res) {
       if(res=='ok'){
         file_list()
         document.querySelector("#load-ico").style.visibility="hidden";
         spop({
          template: '上传成功',
          position  : 'top-right',
          autoclose: 1500,
          style: 'success'
        });
       }
       else{
        document.querySelector("#load-ico").style.visibility="hidden";
        spop({
          template: '上传错误',
          position  : 'top-right',
          autoclose: 1500,
          style: 'error'
        });
       }
     }
 })
});

function downloadFile(content, fileName) { //下载base64图片
  var base64ToBlob = function(code) {
      let parts = code.split(';base64,');
      let contentType = parts[0].split(':')[1];
      let raw = window.atob(parts[1]);
      let rawLength = raw.length;
      let uInt8Array = new Uint8Array(rawLength);
      for(let i = 0; i < rawLength; ++i) {
          uInt8Array[i] = raw.charCodeAt(i);
      }
      return new Blob([uInt8Array], {
          type: contentType
      });
  };
  let aLink = document.createElement('a');
  let blob = base64ToBlob(content); //new Blob([content]);
  let evt = document.createEvent("HTMLEvents");
  evt.initEvent("click", true, true); //initEvent 不加后两个参数在FF下会报错  事件类型，是否冒泡，是否阻止浏览器的默认行为
  aLink.download = fileName;
  aLink.href = URL.createObjectURL(blob);
  aLink.click();
};

function saveimg(){
  workspace.cleanUp()
  saveSvgAsPng(workspace.svgBlockCanvas_,'program.png', {scale:2})
}

function see_img(url){
  var pos = url.lastIndexOf('/');
  var file_type = url.substring(url.lastIndexOf('.') + 1);
  var name = url.substr(pos+1)//截取文件名称字符串
  BigPicture({
    el:  document.getElementById('eye'),
    imgSrc: 'static/file/'+name
  }); 
}

function setClickHandler(id, fn) {
  document.getElementById(id).onclick = fn;
}

var images = '';
function show(file){
  var reader = new FileReader();    // 实例化一个FileReader对象，用于读取文件
  var img = document.getElementById('imageHSV');     // 获取要显示图片的标签

  //读取File对象的数据
  reader.onload = function(evt){
      img.width  =  "80";
      img.height =  "80";
      img.src = evt.target.result;
  }
  reader.readAsDataURL(file.files[0]);
}

function main(){
  const canvas = document.getElementById("canvasInput");
  const ctx = canvas.getContext("2d");
  console.log(document.getElementById("filess").files)
  const inputFile = document.querySelector("input[type=file]");
  const files=document.getElementById("filess").files
  if (files.length > 0) {
    const file = files[0]; // First file
    console.log(file);
    const image = new Image();
    image.src = URL.createObjectURL(file);
    image.onload = function(event) {
        // console.log(event, this);
        URL.revokeObjectURL(this.src);
        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0);
        let src = cv.imread('canvasInput');
        //cv.cvtColor(src, src, cv.COLOR_BGR2HSV , 0);
        let dst = new cv.Mat();
        let low = new cv.Mat(src.rows, src.cols, src.type(), [0, 0, 0, 0]);
        let high = new cv.Mat(src.rows, src.cols, src.type(), [150, 150, 150, 255]);
        // You can try more different parameters
        cv.inRange(src, low, high, dst);
        cv.imshow('canvasOutput', dst);
        src.delete(); dst.delete(); low.delete(); high.delete();
        slider1.enable();slider2.enable();slider3.enable();slider4.enable();slider5.enable();slider6.enable();
    }
  }
}

function cv2_inRange(){
  let src = cv.imread('canvasInput');
  let dst = new cv.Mat();
  //cv.cvtColor(src, src, cv.COLOR_BGR2HSV, 0);
  //var lows=hsv2rgb_low(h_min, s_min, v_min)
  //var hight=hsv2rgb_h(h_max, s_max, v_max)

  var lows=[v_min, s_min, h_min,0]
  var hight=[v_max, s_max, h_max,255]
  console.log(lows,hight)
  let low = new cv.Mat(src.rows, src.cols, src.type(), lows);
  let high = new cv.Mat(src.rows, src.cols, src.type(), hight);
  // You can try more different parameters
  cv.inRange(src, low, high, dst);
  //console.log(rgbToHsv([h_max, s_max, v_max]))
  cv.imshow('canvasOutput', dst);
  document.getElementById('inrange').value=h_min+','+s_min+','+v_min+','+h_max+','+s_max+','+v_max
  //document.getElementById('inrange').value=rgbToHsv([h_min, s_min, v_min])+','+rgbToHsv([h_max, s_max, v_max]);
  src.delete(); dst.delete(); low.delete(); high.delete();
}

function rgbToHsv(arr){
    var r=arr[0];
    var g=arr[1];
    var b=arr[2]
    hsv_red = Number(r) / 255; hsv_green = Number(g) / 255; hsv_blue = Number(b) / 255;
      var hsv_max = Math.max(hsv_red, hsv_green, hsv_blue), hsv_min = Math.min(hsv_red, hsv_green, hsv_blue);
      var hsv_h, hsv_s, hsv_v = hsv_max;
  
      var hsv_d = hsv_max - hsv_min;
      hsv_s = hsv_max == 0 ? 0 : hsv_d / hsv_max;
  
      if(hsv_max == hsv_min)
          hsv_h = 0; 
      else
      {
          switch(hsv_max)
          {
              case hsv_red: hsv_h = (hsv_green - hsv_blue) / hsv_d + (hsv_green < hsv_blue ? 6 : 0); break;
              case hsv_green: hsv_h = (hsv_blue - hsv_red) / hsv_d + 2; break;
              case hsv_blue: hsv_h = (hsv_red - hsv_green) / hsv_d + 4; break;
          }
          hsv_h /= 6;
      }
      
      return [parseInt(hsv_h.toFixed(4)*180),parseInt(hsv_s.toFixed(4)*255),parseInt(hsv_v.toFixed(4)*255)];
   
  }

  function hsv2rgb_low(h,s,v)
{
    hsv_h = Number(h)/180; hsv_s = Number(s)/255; hsv_v = Number(v)/255;

    var i = Math.floor(hsv_h * 6);
    var f = hsv_h * 6 - i;
    var p = hsv_v * (1 - hsv_s);
    var q = hsv_v * (1 - f * hsv_s);
    var t = hsv_v * (1 - (1 - f) * hsv_s);

    var rgb_r = 0,rgb_g = 0,rgb_b = 0;
    switch(i % 6){
        case 0: rgb_r = hsv_v; rgb_g = t; rgb_b = p; break;
        case 1: rgb_r = q; rgb_g = hsv_v; rgb_b = p; break;
        case 2: rgb_r = p; rgb_g = hsv_v; rgb_b = t; break;
        case 3: rgb_r = p; rgb_g = q; rgb_b = hsv_v; break;
        case 4: rgb_r = t; rgb_g = p; rgb_b = hsv_v; break;
        case 5: rgb_r = hsv_v, rgb_g = p, rgb_b = q; break;
    }

  return [parseInt(Math.floor(rgb_b*255)),parseInt(Math.floor(rgb_g*255)),parseInt(Math.floor(rgb_r*255)),0];
}

function hsv2rgb_h(h,s,v)
{
  hsv_h = Number(h)/180; hsv_s = Number(s)/255; hsv_v = Number(v)/255;

    var i = Math.floor(hsv_h * 6);
    var f = hsv_h * 6 - i;
    var p = hsv_v * (1 - hsv_s);
    var q = hsv_v * (1 - f * hsv_s);
    var t = hsv_v * (1 - (1 - f) * hsv_s);

    var rgb_r = 0,rgb_g = 0,rgb_b = 0;
    switch(i % 6){
        case 0: rgb_r = hsv_v; rgb_g = t; rgb_b = p; break;
        case 1: rgb_r = q; rgb_g = hsv_v; rgb_b = p; break;
        case 2: rgb_r = p; rgb_g = hsv_v; rgb_b = t; break;
        case 3: rgb_r = p; rgb_g = q; rgb_b = hsv_v; break;
        case 4: rgb_r = t; rgb_g = p; rgb_b = hsv_v; break;
        case 5: rgb_r = hsv_v, rgb_g = p, rgb_b = q; break;
    }

  return [parseInt(Math.floor(rgb_b*255)),parseInt(Math.floor(rgb_g*255)),parseInt(Math.floor(rgb_r*255)),255];
}

function pip_list(){
  $("#pip-table").tabulator({columns:[
    {title:"名称", field:"name", sortable:true,align:'center',sorter:"string", width:'20%'},
    {title:"简介", field:"col", sorter:"string", sortable:false, width:'50%'},
    {title:"系统", field:"arr", sorter:"string",align:'center',sortable:false, width:'20%'},
    {title:"操作", field:"cheese", sortable:true,align:'center',width:'10%'},
    ],
    height:'270px',
    }
    )
  $("#pip-table").tabulator("setData",[
    {id:1, name:"opencv", col:"opencv库", arr:'arrch64/windows',cheese:re('opencv-python')},
    {id:2, name:"pyqt5",  col:"Pyqt5", arr:'arrch64/windows',cheese:re('pyqt5')},
    {id:3, name:"Tensorflow 2.8.0",  col:"Tensorflow", arr:'arrch64/windows',cheese:re('tensorflow')},
    {id:4, name:"Mediapipe",  col:"Mediapipe", arr:'arrch64/windwos',cheese:re('mediapipe')},
    {id:5, name:"sounddevice",  col:"录音与播放音乐", arr:'arrch64/windows',cheese:re('sounddevice')},
    {id:6, name:"SoundFile",  col:"音频文件操作", arr:'arrch64/windows',cheese:re('SoundFile')},
    {id:7, name:"librosa",  col:"用于音乐和音频分析的python包", arr:'arrch64/windows',cheese:re('librosa')},
    {id:8, name:"hcsr04sensor",  col:"超声波传感器的依赖库", arr:'arrch64',cheese:re('hcsr04sensor')},
  ]);
}
function re(name){
  return "<div style='display:flex;justify-content: space-around;'><div onclick='install_ku(\""+name+"\")'><i class='fa fa-arrow-circle-down' style='color: #00bd15;margin-right: 30px;margin-left: 30px;'></i></div></div>"
}
function install_ku(name){
  console.log(name)
  addpip('开始安装 '+name+' ,请保持网络畅通。')
  chatSocket.send(JSON.stringify({'msg':'install_ku','name':name}))
}

var rec=false
var recorder
$("#Recording").on("click", function(event){
  if (rec==false){
    recorder = new Recorder({
      sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
      sampleRate: 16000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
      numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
      // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
    });
    recorder.start().then(() => {
      add('开始录音')
      rec=true
    }, (error) => {
      // 出错了
      rec=false
      if (error.message=='浏览器不支持 getUserMedia !'){
      prompt(`${error.name} : ${error.message}\n`+
      '\n'+
      '原因：浏览器不支持http：IP开头的路径，认为这个路径不安全\n'+
      '解决方法示例：\n'+
      '例如chrome浏览器\n'+
      '1.地址栏输入：chrome://flags/#unsafely-treat-insecure-origin-as-secure\n'+
      '2.在Insecure origins treated as secure中添加MxPi的IP地址\n'+
      '3.点击“Relaunch”按钮重启浏览器\n'
      ,'chrome://flags/#unsafely-treat-insecure-origin-as-secure'
      )
      console.log(`${error.name} : ${error.message}`);
      recorder.destroy().then(function() {
        recorder = null;
    });
  }
  else{
    prompt(`${error.name} : ${error.message}\n`,`${error.name} : ${error.message}\n`)
      recorder.destroy().then(function() {
        recorder = null;
    });
    }
  });
  }
  else{
    recorder.stop();
    rec=false;
    add('录音结束')
    var data=recorder.getWAVBlob();
    console.log(data)
    var fd = new FormData();
    fd.append('avatar',data);
    $.ajax({
        url: '/files',
        type: 'post',
        data: fd,
        contentType: false,  
        processData: false,  
        success:function (res) {
          if(res=='ok'){
            file_list()
            document.querySelector("#load-ico").style.visibility="hidden";
            spop({
              template: '上传成功',
              position  : 'top-right',
              autoclose: 1500,
              style: 'success'
            });
          }
          else{
            document.querySelector("#load-ico").style.visibility="hidden";
            spop({
              template: '上传错误',
              position  : 'top-right',
              autoclose: 1500,
              style: 'error'
            });
          }
        }
    })
  }
});

function play_wav(){
  wavesurfer.playPause();
}
function pause_wav(){
  wavesurfer.playPause();
}
wavesurfer.on('interaction', function () {
  t1=wavesurfer.getDuration().toFixed(3)
  t2=wavesurfer.getCurrentTime().toFixed(3)
  document.getElementById('wav_time1').innerHTML=t2
  document.getElementById('wav_time3').innerHTML=t1
  wavesurfer.pause();
});

wavesurfer.on('ready', function () {
  t1=wavesurfer.getDuration().toFixed(3)
  t2=wavesurfer.getCurrentTime().toFixed(3)
  document.getElementById('wav_time1').innerHTML=t2
  document.getElementById('wav_time3').innerHTML=t1
});

wavesurfer.on('audioprocess', function () {
  t1=wavesurfer.getDuration().toFixed(3)
  t2=wavesurfer.getCurrentTime().toFixed(3)
  document.getElementById('wav_time1').innerHTML=t2
});

