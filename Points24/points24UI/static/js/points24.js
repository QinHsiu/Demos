//全局变量
var ac=0; //记录用户回答正确的数量
var total=0; //记录生成数据总量
var isNext=true; //是否生成下一个数据
var isNext1=true;//用于判断是否生成下一个数据
var dic={'A1':1,'A2':1,'A3':1,'A4':1,'21':2,'22':2,'23':2,'24':2,'31':3,'32':3,'33':3,'34':3,'41':4,'42':4,'43':4,'44':4,'51':5,'52':5,'53':5,'54':5,'61':6,'62':6,'63':6,'64':6,'71':7,'72':7,'73':7,'74':7,'81':8,'82':8,'83':8,'84':8,'91':9,'92':9,'93':9,'94':9,'101':10,'102':10,'103':10,'104':10,'J1':11,'J2':11,'J3':11,'J4':11,'Q1':12,'Q2':12,'Q3':12,'Q4':12,'K1':13,'K2':13,'K3':13,'K4':13}; //初始化字典
var value; //存放自动生成的数据
var isFalse=false; //不可以通过运算获得24点
var result=""; //记录所有可能结果
var nickname; //存放用户昵称
var isShow=false; //用于记录用户是否查看答案
var scoreResult=""; //记录用户得分
var click=0;//设置music按钮的点击次数（%3==0表示第一首，==1表示第二首;==2表示停止播放）
var modetime=0; //用户选择的模式
var Nowtime; //实时获取当前倒计时时间
var nowT;//时间戳
var showT=0;//表示界面动画首次出现
var b_click=0;//记录背景切换按钮的点击次数
var ctime;//监测图片停留时间
var c_time;//表示图片加载后的时间



//函数主体
function getRandomArrayElements(arr,count) {
    var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    var temp=shuffled.slice(min);
    return temp;
} //从arr中生成count个数据



var s_c=0; //记录弹出框次数

//设置倒计时
function getRtime(){
    nowT=new Date();
    nowT=nowT.getTime()-Nowtime;
    //alert(modetime);
    var m=Math.floor(nowT/1000/60%60);
    var s=Math.floor(nowT/1000%60);

    //如果时间超过所选模式，就停止作答
    //alert(m==modetime);
    document.getElementById("t_m").innerHTML=m+"分";
    document.getElementById("t_s").innerHTML=s+"秒";

    if(m==modetime){ //如果到了时间就显示提示信息
        s_c+=1;
        if(s_c==1){
            alert("Your time is out!");
        }
        //alert("Your time is out!");
        //alert(modetime);
        Show();//直接显示答案

    }
}


//旋转函数
function Trans(){
        //设置旋转
        document.getElementById('i1').className="test_f";
        document.getElementById('i2').className="test_f";
        document.getElementById('i3').className="test_f";
        document.getElementById('i4').className="test_f";

        document.getElementById('i5').className="test_t";
        document.getElementById('i6').className="test_t";
        document.getElementById('i7').className="test_t";
        document.getElementById('i8').className="test_t";
}

//原始类
function Origin(){
        var classi1= document.getElementById('i1').getAttribute("class");
        var classi2= document.getElementById('i2').getAttribute("class");
        var classi3= document.getElementById('i3').getAttribute("class");
        var classi4= document.getElementById('i4').getAttribute("class");
        var classi5= document.getElementById('i5').getAttribute("class");
        var classi6= document.getElementById('i6').getAttribute("class");
        var classi7= document.getElementById('i7').getAttribute("class");
        var classi8= document.getElementById('i8').getAttribute("class");

        classi8=classi8.replace("test_t","");
        document.getElementById('i8').setAttribute("class",classi8);
        classi7=classi7.replace("test_t","");
        document.getElementById('i7').setAttribute("class",classi8);
        classi6=classi6.replace("test_t","");
        document.getElementById('i6').setAttribute("class",classi8);
        classi5=classi5.replace("test_t","");
        document.getElementById('i5').setAttribute("class",classi8);
        classi4=classi4.replace("test_f","");
        document.getElementById('i4').setAttribute("class",classi8);
        classi3=classi3.replace("test_f","");
        document.getElementById('i3').setAttribute("class",classi8);
        classi2=classi2.replace("test_f","");
        document.getElementById('i2').setAttribute("class",classi8);
        classi1=classi1.replace("test_f","");
        document.getElementById('i1').setAttribute("class",classi8);
}

//设置图片加载动画
function Cards(value){
        document.getElementById('i5').src="../../static/others/pictures/"+value[0]+".jpg";
        document.getElementById('i6').src="../../static/others/pictures/"+value[1]+".jpg";
        document.getElementById('i7').src="../../static/others/pictures/"+value[2]+".jpg";
        document.getElementById('i8').src="../../static/others/pictures/"+value[3]+".jpg";
        Origin();
        Trans();
}
//还原旋转






function To(){ //将js生成数据传递到页面上
    var arr=['A1','21','31','41','51','61','71','81','91','101','J1','Q1','K1','A2','22','32','42','52','62','72','82','92','102','J2','Q2','K2','A3','23','33','43','53','63','73','83','93','103','J3','Q3','K3','A4','24','34','44','54','64','74','84','94','104','J4','Q4','K4'];
    var count=4
    if(isNext){
        value=getRandomArrayElements(arr,count);
        ctime=new Date();//更新图片到的时间
        ctime=ctime.getTime();
        Cards(value);//将图片加载到html中
        Nowtime=new Date();//当前时间
        Nowtime=Nowtime.getTime();//获取当前时间戳
        s_c=0; //清零限制时间记录
    }
    isNext=false;//调用完需要设置
}

setInterval(getRtime,1000);


function getScore(){
    document.getElementById("sc").innerHTML=ac*10+"分";
    //alert(modetime);
}

setInterval(getScore,1000);




//递归求解全排列
function permutation(a, m) {
    // 保存最终输出结果
    let result = [];

    // 定义 m 值默认等于 n，即全排列
    let n = a.length;
    m = m || n;

    // 定义递归函数保存结果到数组中
    // _a 为输入数组，
    // tmpResult 为保存单个情况结果的数组
    function recur(_a, tmpResult = []) {
        if (tmpResult.length === m) {

        // 结果达到 m 个时保存结果，
        // 停止递归并进入下一次遍历
        result.push(tmpResult);
} else {
    for (let i = 0; i < _a.length; i++) {

        // 复制一份输入数组，防止引用值被改变
        let tmpA = _a.concat();

        // 复制一份保存结果的数组，防止每次遍历相互影响
        let _tmpResult = tmpResult.concat();

        // 保存当前遍历值
        _tmpResult.push(tmpA[i]);

        // 删除当前遍历值，传递参数进入下一层递归
        tmpA.splice(i, 1);
        recur(tmpA, _tmpResult);
    }
    }
}

    // 开始执行递归，然后返回最后结果
    recur(a);
    return result;
}


//去重
function norepeat(contents) {
     var norepeatContents = [], hash = {};
    for (var i = 0; i < contents.length; i++) {
    if(!hash[contents[i]]) {
         norepeatContents.push(contents[i]);
        hash[contents[i]] = true;
    }
    }
    return norepeatContents;
    }




//无顺序
function tdisoper(f0,f1,f2,f3){
    this[0]=f0;
    this[1]=f1;
    this[2]=f2;
    this[3]=f3;
}//用于存储操作符

function oper(f,m,n){
    if(f==3)return(m*n);
    if(f==2)return(m/n);
    if(f==1)return(parseFloat(m)+parseFloat(n));
    if(f==0)return(m-n);
}//运算符计算

function tb(i1,i2,i4,i8){
    this[1]=i1;
    this[2]=i2;
    this[4]=i4;
    this[8]=i8;
}//存储操作数


//计算函数 无顺序
function Twentyfour(value){ //传入数据为一个数组
    var i=0;
    var answer=value;

    if(isNext1) { //如果没有点击下一题就执行
        //alert(answer);
        while (i < answer.length) {
            for(let i=0;i<answer.length;i++) {
                if (answer[i] in dic) {
                    answer[i] = parseInt(dic[answer[i]]);
                } else {
                    answer[i] = parseInt(answer[i]);
                }
            }
            i += 1;
        }
        //alert(answer);
    }

    //开始计算
    var b=new tb(answer[0],answer[1],answer[2],answer[3]);
    var disoper=new tdisoper("-","+","/","*");
    var target=false;//表示是否可以通过计算获得24点
    var m;//存放计算的值
    var i1,i2,i3,i4;
    var f1,f2,f3;

    for(i1=1;i1<=8;i1*=2){
        for(i2=1;i2<=8;i2*=2){
            for(i3=1;i3<=8;i3*=2){
                for(i4=1;i4<=8;i4*=2){
                    if((i1|i2|i3|i4)!=0xf)continue;
                    for(f1=0;f1<=3;f1++){
                        for(f2=0;f2<=3;f2++){
                            for(f3=0;f3<=3;f3++){
                                m=oper(f3,oper(f2,oper(f1,b[i1],b[i2]),b[i3]),b[i4]);
                                if(Math.abs(m-24)<1e-10){
                                    result=result+"(("+b[i1]+disoper[f1]+b[i2]+")"+disoper[f2]+b[i3]+")"+disoper[f3]+b[i4]+"\n";
                                    target=true;
                                }//一组运算操作

                                m=oper(f1,b[i1], oper(f3, oper(f2,b[i2],b[i3]) ,b[i4]));
                                if(Math.abs(m-24)<1e-10){
                                    result=result+b[i1]+disoper[f1]+"(("+b[i2]+disoper[f2]+b[i3]+")"+disoper[f3]+b[i4]+")\n";
                                    target=true;

                                }//一组运算操作

                                m=oper(f3,oper(f1,b[i1],oper(f2,b[i2],b[i3])),b[i4]);
                                if(Math.abs(m-24)<1e-10){
                                    result=result+"("+b[i1]+disoper[f1]+"("+b[i2]+disoper[f2]+b[i3]+"))"+disoper[f3]+b[i4]+"\n";
                                    target=true;
                                }//一组运算操作

                                m=oper(f1, b[i1], oper(f2, b[i2], oper(f3, b[i3], b[i4])));
                                if(Math.abs(m-24)<1e-10){
                                    result=result+b[i1]+disoper[f1]+"("+b[i2]+disoper[f2]+"("+b[i3]+disoper[f3]+b[i4]+"))\n";
                                     target=true;

                                }//一组运算操作

                                m=oper(f2,oper(f1,b[i1],b[i2]), oper(f3,b[i3],b[i4]));
                                if(Math.abs(m-24)<1e-10){
                                    result=result+"("+b[i1]+disoper[f1]+b[i2]+")"+disoper[f2]+"("+b[i3]+disoper[f3]+b[i4]+")\n";
                                     target=true;

                                }//一组运算操作

                             }}
                            }
                     }
                     }
                     }
                     }

    if(target){
        isFalse=false;

     }
     else{
      isFalse=true;
    }
}

//播放音乐
function  onMusic(){
    click+=1;
    var myMusic=document.getElementById("music");
    if(click%3==0){
        document.getElementById("music").src="../../static/others/musics/lucky.mp3";
        myMusic.play();
    }
    else if(click%3==1){
        document.getElementById("music").src="../../static/others/musics/comethru.mp3";
        myMusic.play();
    }else{
        //关闭
        myMusic.pause()
        myMusic.load();
    }

}

//改变背景
function onChange(){
    b_click+=1;
    var background=document.getElementById("body");
    if(b_click%5==0){
        document.getElementById("body").style.backgroundColor="lightblue";
    }else if(b_click%5==1){
        document.getElementById("body").style.backgroundColor="blue";
    } else if(b_click%5==2){
        document.getElementById("body").style.backgroundColor="green";
    }else if(b_click%5==3){
        document.getElementById("body").style.backgroundColor="white";
    }else{
        document.getElementById("body").style.backgroundColor="pink";
    }
}



//检查数据
function Check(){
    var content=document.getElementById('content').value;
    var actarget=false;
    Twentyfour(value);
    if((content=='false')||(content=="False")){
        if(isNext1){
            if(isFalse){
                actarget=true;
            }
        }
    }
    else{
        var i=0;
        var tempV;
        tempV=content;

        tempV=tempV.replace(/A/g,"1");//替换所有值
        tempV=tempV.replace(/J/g,"11");
        tempV=tempV.replace(/Q/g,"12");
        tempV=tempV.replace(/K/g,"13");

        //捕捉异常
        try{
        var temp=eval(tempV);
        }catch{
            msg="please enter the correct equation.";
            alert(msg);
            return;//如果检查到输入错误信息，就显示提示信息，并停止继续执行
        }

        if(temp==undefined){
            alert("please enter the correct equation.");
            return;
        }

        if(Math.abs(temp-24)<1e-5){
            actarget=true;
        }
    }

    if(actarget){
        ac+=1;
        if(isShow){
            ac-=1;
            alert("You have saw the answer! "+nickname);
        }
        else{
            alert("Congratulations! "+nickname);
        }
    }
   else{
        alert("Cheer Up! "+nickname);
   }
   isNext1=false;
}

//清空
function Reset(){
   document.getElementById('content').value="";

}

//下一个
function Next(){
    isShow=false;//设置答案为未查看
    total+=1; //总数加一
    document.getElementById("result").value=""; //清空上一题答案
    document.getElementById("content").value=""; //清空上一题自己的作答结果
    isNext=true;//修改变量值
    isNext1=true;//修改变量值
    To();
}

//展示结果,展示当前结果
function Show(){
    //alert(value);
    isShow=true;
    Twentyfour(value);
    if(isFalse){
       document.getElementById('result').value="Nothing!";
    }
    else{
      result=result+"Find All!\n";
      document.getElementById('result').value=result;
    }
    result="";
    }

//得分
function Score(){
    var scoreResult="";
    scoreResult=scoreResult+"Total: "+total.toString()+" Ac: "+ac.toString()+" Accuracy Rate: "+(ac/total).toString();
    document.getElementById('score').value=scoreResult;
}

//退出
function Quit(){
    if(confirm("Are you sure to quit?")){
        window.opener=null;
        window.open('','_self');
        window.close();
    }
    else{}
}


//动画
var RENDERER = {
	ROW : 4,
	COLUMN : 12,
	MAX_STATUS_COUNT : 50,
	MAX_WAITING_COUNT : 30, //每一步动画等待时间
	MAX_STATUS : 8,

	init : function(){
		this.setParameters();
		this.createCards();
		this.reconstructMethods();
		this.render();

	},
	setParameters : function(){
		this.$container = $('#jsi-cards-container');
		this.width = this.$container.width();
		this.height = this.$container.height();
		this.$canvas = $('<canvas />').attr({width : this.width, height : this.height}).appendTo(this.$container);
		this.context = this.$canvas.get(0).getContext('2d');
		this.cards = [];
		this.status = 0;
		this.statusCount = 0;
		this.waitingCount = 0;
		this.gradient = this.context.createRadialGradient(this.width / 2, this.height / 2, 0, this.width / 2, this.height / 2, Math.sqrt(Math.pow(this.width / 2, 2) + Math.pow(this.height / 2, 2)));
		this.gradient.addColorStop(0, 'hsl(210, 100%, 30%)');
		this.gradient.addColorStop(1, 'hsl(210, 100%, 10%)');
	},
	createCards : function(){
		for(var i = 0; i < this.ROW; i++){
			for(var j = 0; j < this.COLUMN; j++){
				this.cards.push(new CARD(this, i, j));
			}
		}
		this.cards.sort(function(card1, card2){
			return card2.radian[0] - card1.radian[0];
		});
	},
	reconstructMethods : function(){
		this.render = this.render.bind(this);
	},
	controlStatus : function(){
		if(++this.statusCount > this.MAX_STATUS_COUNT){
			if(++this.waitingCount > this.MAX_WAITING_COUNT){
				if(++this.status > this.MAX_STATUS){
					this.status = 1;
				}
				this.statusCount = 0;
				this.waitingCount = 0;
			}
		}
	},
	easeInOutQuad: function(t){
		return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
	},
	render : function(){
		requestAnimationFrame(this.render);
		this.context.fillStyle = this.gradient;
		this.context.fillRect(0, 0, this.width, this.height);
		var rate = this.easeInOutQuad(Math.min(1, this.statusCount / this.MAX_STATUS_COUNT));

		for(var i = 0, length = this.cards.length; i < length; i++){
			this.cards[i].render(this.context, this.status, rate);
		}
		this.controlStatus();

        console.log(showT);
        if(showT>0){//如果界面已经出现就关闭画布

            //cancelAnimationFrame(this.render);
            //this.context.clearRect(0, 0, this.width, this.height);//清除画布

            //删除动画内容
            var animation=document.getElementById("jsi-cards-container");
            animation.parentNode.removeChild(animation);


            //展示答题界面
             document.getElementById('form').style.opacity=1;
             document.getElementById('button').style.opacity=1;
            //document.getElementById("jsi-cards-container").style.opacity=0;

            //删除开始按钮
            //var beginButton=document.getElementById("begin");
            //beginButton.parentNode.removeChild(beginButton);
            document.getElementById('welcome').innerHTML="Welcome! "+nickname+"                        "; //显示用户名
            Next();
        }

	}
};




var CARD = function(renderer, row, column){
	 this.renderer = renderer;
	 this.row = row;
	 this.column = column;
	 this.init();
};
CARD.prototype = {
	WIDTH_RATIO : 1 / 12,
	HEIGHT_RATIO : 1 / 8,
	SCALE_RATIO : 4 / 5,

	init : function(){
		var index = this.column * this.renderer.ROW + this.row;
		this.width = Math.min(this.renderer.width, this.renderer.height) * this.WIDTH_RATIO;
		this.height = Math.min(this.renderer.width, this.renderer.height) * this.HEIGHT_RATIO;
		this.axis = [
			{x : this.renderer.width / 2, y : this.renderer.height / 2},
			{x : this.renderer.width / 4 + this.renderer.width / 2 * (this.row % 2), y : this.renderer.height / 4 + this.renderer.height / 2 * Math.floor(this.row / 2)},
			{x : this.width * 2, y : this.renderer.height / 8 + this.height / 2 + this.renderer.height / 4 * this.row},
			{x : this.width / 2 + (this.renderer.width - this.width * 3 / 2) * this.column / this.renderer.COLUMN, y : this.renderer.height / 8 + this.height / 2 + this.renderer.height / 4 * this.row},
			{x : this.width / 2 + (this.renderer.width - this.width * 2) * index / this.renderer.ROW / this.renderer.COLUMN, y : this.renderer.height / 2 + this.height / 2},
			{x : this.width / 2 + (this.renderer.width - this.width * 2) * index / this.renderer.ROW / this.renderer.COLUMN, y : this.height * 3 / 2 + (this.renderer.height - this.height * 2) * (1 - Math.abs(1 - index / this.renderer.ROW / this.renderer.COLUMN * 2))},
			{x : this.renderer.width / 6 + this.renderer.width / 3 * (this.column % 3), y : this.renderer.height / 10 + this.height / 2 + this.renderer.height / 4 * Math.floor(this.column / 3)},
			{x : this.renderer.width / 2, y : this.renderer.height / 2}
		];
		this.radian = [index / this.renderer.ROW / this.renderer.COLUMN, this.column / this.renderer.COLUMN, this.row / (this.renderer.ROW - 1)];
		this.scale = this.SCALE_RATIO * this.row / (this.renderer.ROW - 1);
		this.hue = this.radian[0] * 360 | 0;
	},
	controlStatus : function(context, status, rate){
		if(status == 0){
			this.x = this.axis[status].x;
	 		this.y = this.axis[status].y;
		}else{
			var next = (status == this.renderer.MAX_STATUS) ? 0 : status;
			this.x = this.axis[status - 1].x + (this.axis[next].x - this.axis[status - 1].x) * rate;
	 		this.y = this.axis[status - 1].y + (this.axis[next].y - this.axis[status - 1].y) * rate;
		}
		switch(status){
		case 0:
			context.rotate(this.radian[0] * Math.PI * 2 * rate);
			context.translate(0, -this.height);
			break;
		case 1:
			context.rotate(this.translateAngle(this.radian[0] * Math.PI * 2, this.radian[1] * Math.PI * 2, rate));
	 		context.translate(0, -this.height * (1 - rate));
	 		break;
	 	case 2:
             context.rotate(this.translateAngle(this.radian[1] * Math.PI * 2, Math.PI * 2, rate));
             break;
	 	case 6:
	 		context.rotate((this.radian[2] * Math.PI / 2 - Math.PI / 4) * rate);
	 		context.translate(-this.width / 2 * rate, 0);
             showT+=1;
	 		break;
	 	case 7:
	 		context.rotate(this.translateAngle(this.radian[2] * Math.PI / 2 - Math.PI / 4, this.radian[1] * Math.PI * 2, rate));
	 		context.scale(1 - this.scale * rate, 1 - this.scale * rate);
	 		context.translate(-this.width / 2, -this.height * 3 * rate);
	 		break;
	 	case 8:
	 		context.rotate(this.translateAngle(this.radian[1] * Math.PI * 2, this.radian[0] * Math.PI * 2, rate));
	 		context.scale(1 - this.scale * (1 - rate), 1 - this.scale * (1 - rate));
	 		context.translate(-this.width / 2 * (1 - rate), this.height * (2 * rate - 3));
	 	}
	},
	translateAngle : function(source, destination, rate){
		return source + (destination - source) * rate;
	},
	render : function(context, status, rate){
		context.save();
		context.translate(this.x, this.y);
		this.controlStatus(context, status, rate);
		context.lineWidth = this.width / 20;
		context.strokeStyle = 'hsl(' + this.hue + ', 60%, 90%)';
		context.fillStyle = 'hsl(' + this.hue + ', 60%, 60%)';
		context.fillRect(0, -this.height, this.width, this.height);
		context.strokeRect(0, -this.height, this.width, this.height);
		context.restore();
	}
};

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});//显示提示信息



function Begin(){
     nickname=document.getElementById("nickname").value;
     //alert(nickname);
     if(nickname==""){
        alert("please input your nickname.")
     }
     else{


        var mode=document.getElementById("mode").value;//获取答题模式

         if(mode=="Hard"){
             modetime=1;
         }else if(mode=="Mid"){
             modetime=2;
         }else{
             modetime=3;
         }

         //显示模式信息
        if (modetime==3) {
                document.getElementById("m_d").innerHTML = "Easy";//显示模式信息
        } else if (modetime==2) {
            document.getElementById("m_d").innerHTML = "Mid";//显示模式信息
        } else {
            document.getElementById("m_d").innerHTML = "Hard";//显示模式信息
        }


         //删除开始界面的内容
        var beginPage=document.getElementById("begin-page");
        beginPage.parentNode.removeChild(beginPage);

        //播放动画
         RENDERER.init();

     }
}

