window.LOCAL_URL = '/'; // http://localhost:17310/';
window.LOCAL_VERSION = '0.0.3'


window.vm = new Vue({
  el: '#perf',
  data: {
    params:{},
    selected_device:"",//localStorage.selected_device || "",
    platform:'android',
    device_list:[],
    selected_app:"",//localStorage.selected_app || "",
    package_list:[],
    xAxisData:[],
    perf_chart_data:[],
    colWidth: {"width": "100%", "height": "300px"},
    echart_object:{},
    echart_show:true,
    is_capture:false,
    timer:null,
    perfws:null,
    perf_filepath: null
  },
  watch: {
    selected_device: function (newval) {
      if(this.selected_device.indexOf('iPhone')!==-1 || this.selected_device.indexOf('iOS')!==-1){
        this.platform = 'ios'
      }
      else{
        this.platform = 'android'
      }
      localStorage.setItem('selected_device', newval);
      // console.log('selected device is '+newval)
      if(newval){
        this.getPackageList()
      }
      this.initChartData()
    },
    selected_app:function (newval) {
      if(this.selected_app){
        localStorage.setItem('selected_app', newval);
        // console.log('selected app is '+newval)
        this.startAPP()
        this.initChartData()
      }
    }
  },
  created() {
    //this.colWidth['width'] = (window.outerWidth - 200) / 2 + "px"
  },
  mounted: function () {
    //var URL = window.URL || window.webkitURL;
    if(this.selected_device.indexOf('iPhone')!==-1 || this.selected_device.indexOf('iOS')!==-1){
      this.platform = 'ios'
    }
    else{
      this.platform = 'android'
    }
    this.params = GetRequestParam(window.location.search)
    console.log(this.params)
    this.platform = this.params['platform'] || 'android'
    this.echart_show = true;

    this.getDeviceList()
    this.initChartData()
    this.initPerfWebSocket()
  },
  methods: {
    initChartData: function(){
      this.xAxisData = []
      this.perf_chart_data = {
        app_cpu:{title:"App CPU利用率(%)",label:"app_cpu",ydata:[{data: [ ], name: "App CPU利用率(%)", type: 'line'}],show:true},
        total_cpu:{title:"整体CPU利用率(%)",label:"total_cpu",ydata:[{data: [ ], name: "整体CPU利用率(%)", type: 'line'}],show:true},
        memory:{title:"内存使用量(MB)",label:"memory",ydata:[{data: [ ], name: "内存使用量(MB)", type: 'line'}],show:true},
        virtual_mem:{title:"虚拟内存使用量(MB)",label:"virtual_mem",ydata:[{data: [ ], name: "虚拟内存使用量(MB)", type: 'line'}],show:true},
        threads:{title:"线程数",label:"threads",ydata:[{data: [ ], name: "线程数", type: 'line'}],show:true},
        gpu:{title:"GPU利用率(%)",label:"gpu",ydata:[{data: [ ], name: "GPU利用率(%)", type: 'line'}],show:true},
        fps:{title:"帧率(FPS)",label:"fps",ydata:[{data: [ ], name: "帧率(FPS)", type: 'line'}],show:true},
        traffic_down:{title:"下行流量(KB)",label:"traffic_down",ydata:[{data: [ ], name: "下行流量(KB)", type: 'line'}],show:true},
        traffic_up:{title:"上行流量(KB)",label:"traffic_up",ydata:[{data: [ ], name: "上行流量(KB)", type: 'line'}],show:true},
        //mediasvrd_cpu:{title:"media CPU 占用(%)",label:"mediasvrd_cpu",ydata:[{data: [ ], name: "media CPU 占用(%)", type: 'line'}],show:true},
        wakeups:{title:"唤醒次数",label:"wakeups",ydata:[{data: [], name: "唤醒次数", type: 'line'}],show:true},
      }
      if(this.platform==='android'){
        this.perf_chart_data['activity'] = {title:"Activities数量",label:"activity",ydata:[{data:[],name:"Activities数量",type:"line"}],show:true}
        this.perf_chart_data['native_mem'] = {title:"Native使用量(MB)",label:"native_mem",ydata:[{data:[],name:"Native使用量(MB)",type:"line"}],show:true}
        this.perf_chart_data['dalvik_mem'] = {title:"Dalvik使用量(MB)",label:"dalvik_mem",ydata:[{data:[],name:"Dalvik使用量(MB)",type:"line"}],show:true}
        this.perf_chart_data['mediasvrd_cpu'] = {title:"media CPU 占用(%)",label:"mediasvrd_cpu",ydata:[{data: [ ], name: "media CPU 占用(%)", type: 'line'}],show:false}
      }
      else{
        this.perf_chart_data['activity'] = {title:"Activities数量",label:"activity",ydata:[{data:[],name:"Activities数量",type:"line"}],show:false}
        this.perf_chart_data['native_mem'] = {title:"Real Mem使用量(MB)",label:"native_mem",ydata:[{data:[],name:"Real Mem使用量(MB)",type:"line"}],show:true}
        this.perf_chart_data['dalvik_mem'] = {title:"Real Private Mem使用量(MB)",label:"dalvik_mem",ydata:[{data:[],name:"Real Private Mem使用量(MB)",type:"line"}],show:true}
        this.perf_chart_data['mediasvrd_cpu'] = {title:"media CPU 占用(%)",label:"mediasvrd_cpu",ydata:[{data: [ ], name: "media CPU 占用(%)", type: 'line'}],show:true}
      }
    },
    getDeviceList: function(){
      $.ajax({
        url: LOCAL_URL + "api/v1/devices/list",
        type: "GET",
      })
      .done((ret) => {
          this.device_list = ret.data;
          for(let index=0;index<this.device_list.length;index++){
            let device = this.device_list[index]
            if (device.indexOf(this.params['serial']) !== -1) {
              this.selected_device = device
              break
            }
          }
      })
      .fail((ret) => {
        this.showAjaxError(ret);
      })
    },
    getPackageList: function(){
      if(this.selected_device){
        $.ajax({
          url: LOCAL_URL + "api/v1/devices/"+ encodeURIComponent(this.selected_device) + "/packagelist",
          type: "GET",
        })
        .done((ret) => {
            this.package_list = ret.data;
        })
        .fail((ret) => {
          this.showAjaxError(ret);
        })
      }
      else{
        this.package_list = []
      }
    },
    startAPP: function(){
      if(this.selected_device && this.selected_app){
        $.ajax({
          url: LOCAL_URL + "api/v1/devices/app",
          method: 'POST',
          data: {
            deviceinfo: this.selected_device,
            package: this.selected_app,
          },
        })
        .fail((ret) => {
          this.showAjaxError(ret);
        })
      }
    },
    startCapture: function(){
      let data = {
        platform:this.platform,
        device: this.selected_device,
        package: this.selected_app,
        action:'start'
      }
      this.perf_filepath = null
      //点击后设置按钮不可用
      this.echart_show = false
      if(this.is_capture===false){
        this.is_capture = true
        this.initChartData()
        document.getElementById("capture_start").innerHTML = "停止采集数据"
        if(this.selected_device && this.selected_app){
          data['action'] = 'start'
        }
      }
      else{
        this.is_capture = false
        document.getElementById("capture_start").innerHTML = "开始采集数据"
        data['action'] = 'stop'
      }
      if(this.perfws){
        this.perfws.send(JSON.stringify(data))
      }
    },
    getEchartOption: function(title, label, xAxisData, seriesData){
      // title,  图标, 横坐标 , 数值
      let options = {
        title: {
          text: title,
        },
        grid: {
          left: 53,
          right: '5%',
          bottom: '7%',
          containLabel: false
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        //legend: {data: [1]},
        toolbox: {
          feature: {
            dataView: {readOnly: false},
            // magicType: {type: ['line', 'bar']},
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {data: xAxisData},
        yAxis: {
          type: 'value',
          axisTick: {
            inside: true
          },
          scale: true,
        },
        axisLabel: {
          interval: 0,
          rotate: 40
        },
        series: seriesData,
      };
      return options;
    },
    drawEchart: function(){
      Object.keys(this.perf_chart_data).forEach(key => {
        if(this.perf_chart_data[key].show){
          let chart_data = this.perf_chart_data[key]
          let chart_option = this.getEchartOption(chart_data.title,chart_data.label,this.xAxisData,chart_data.ydata) 
          if(!this.echart_object[chart_data.label]){
            this.echart_object[chart_data.label] = echarts.init(document.getElementById(chart_data.label))
          }
          this.echart_object[chart_data.label].setOption(chart_option);
        }
      })
    },

    initPerfWebSocket() {
      // 初始化变量
      const ws = this.perfws = new WebSocket("ws://" + location.host + "/ws/v1/captrue")
      ws.onopen = () => {
        console.log("websocket opened")
      }
      ws.onmessage = (message) => {
        //数据返回，设置按钮可用
        this.echart_show = true
        const data = JSON.parse(message.data)
        if(data.hasOwnProperty('filepath')){
          this.perf_filepath = data['filepath']
        }else {
          for (let index = 0; index < data.length; index++) {
            let perfdata = data[index]
            this.xAxisData.push(perfdata['time'])
            Object.keys(this.perf_chart_data).forEach(key => {
              if (this.perf_chart_data[key].show) {
                this.perf_chart_data[key].ydata[0].data.push(perfdata[key])
              }
            })
          }
        }
        this.drawEchart()
      }
      ws.onclose = () => {
        this.perfws = null
        .log("websocket closed")
      }
    },

    exportData: function (){
      if(this.perf_filepath){
        window.open(LOCAL_URL + "api/v1/export/"+encodeURIComponent(this.perf_filepath))
      }
    },

    clearData: function(){
      this.echart_show = true;
      this.perf_chart_data = {}
      this.xAxisData = []
      this.initChartData()
      this.drawEchart()
    },
    dateFormat: function(fmt, date) {
      let ret;
      const opt = {
          "Y+": date.getFullYear().toString(),        // 年
          "m+": (date.getMonth() + 1).toString(),     // 月
          "d+": date.getDate().toString(),            // 日
          "H+": date.getHours().toString(),           // 时
          "M+": date.getMinutes().toString(),         // 分
          "S+": date.getSeconds().toString()          // 秒
          // 有其他格式化字符需求可以继续添加，必须转化成字符串
      };
      for (let k in opt) {
          ret = new RegExp("(" + k + ")").exec(fmt);
          if (ret) {
              fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
          };
      };
      return fmt;
  }

  }
})