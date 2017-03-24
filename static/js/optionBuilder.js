
function getCashFlowOption(raw_datas){
    var timeData = [];
    var data = [];
    var bxs = [];
    var totals = [];
    for (var i = 0; i < raw_datas.length; i++) {
        var _element = raw_datas[i];
        var now = new Date(_element.timestamp * 1000);
        timeData.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
        data.push(_element.total);
    }

    option = {
        tooltip: {
            trigger: 'axis',
            position: function (pt) {
                return [pt[0], '10%'];
            }
        },
        title: {
            left: 'center',
            text: '现金流',
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: timeData
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%']
        },
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 10
        }, {
            start: 0,
            end: 10,
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],
        series: [
            {
                name:'模拟数据',
                type:'line',
                smooth:true,
                symbol: 'none',
                sampling: 'average',
                itemStyle: {
                    normal: {
                        color: 'rgb(255, 70, 131)'
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgb(255, 158, 68)'
                        }, {
                            offset: 1,
                            color: 'rgb(255, 70, 131)'
                        }])
                    }
                },
                data: data
            }
        ]
    };

    return option;
}


function getMonthlyCashFlowOption(raw_datas){
    xData = []
    total_lst = []
    income_lst = []
    expenses_lst = []
    for(var i=0; i<raw_datas.length; i++){
        item = raw_datas[i]
       xData.push(raw_datas[i].date);
       income_lst.push(raw_datas[i].income);
       expenses_lst.push(raw_datas[i].expenses);
       total_lst.push(raw_datas[i].total);
    }

    option = {
        "title": {
            "text": "环比柱形图",
            "subtext": "昨天 vs 前天",
            "x": "center"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            },
        },
        "grid": {
            "borderWidth": 0,
            "y2": 120
        },
        "legend": {
            "x": "right",
            "data": [ ]
        },
        "toolbox": {
            "show": true,
            "feature": {
                "restore": { },
                "saveAsImage": { }
            }
        },
        "calculable": true,
        "xAxis": [
            {
                "type": "category",
                "splitLine": {
                    "show": false
                },
                "axisTick": {
                    "show": false
                },
                "splitArea": {
                    "show": false
                },
                "axisLabel": {
                    "interval": 0,
                    "rotate": 45,
                    "show": true,
                    "splitNumber": 15,
                    "textStyle": {
                        "fontFamily": "微软雅黑",
                        "fontSize": 12
                    }
                },
                "data": xData,
            }
        ],
        "yAxis": [
            {
                "type": "value",
                "splitLine": {
                    "show": false
                },
                "axisLine": {
                    "show": true
                },
                "axisTick": {
                    "show": false
                },
                "splitArea": {
                    "show": false
                }
            }
        ],
        "dataZoom": [
            {
                "show": true,
                "height": 30,
                "xAxisIndex": [
                    0
                ],
                bottom:40,
                "start": 0,
                "end": 5
            },
            {
                "type": "inside",
                "show": true,
                "height": 15,
                "xAxisIndex": [
                    0
                ],
                "start": 1,
                "end": 5
            }
        ],
        "series": [
            {
                "name": "昨日",
                "type": "bar",
                "stack": "总量",
                "barMaxWidth": 50,
                "barGap": "10%",
                "itemStyle": {
                    "normal": {
                        "barBorderRadius": 0,
                        "color": "rgba(60,169,196,0.5)",
                        "label": {
                            "show": true,
                            "textStyle": {
                                "color": "rgba(0,0,0,1)"
                            },
                            "position": "insideTop",
                            formatter : function(p) {
                                                        return p.value > 0 ? (p.value ): '';
                                                    }
                        }
                    }
                },
                "data": total_lst,
            },
            {
                "name": "人流减少",
                "type": "bar",
                "stack": "总量",
                "itemStyle": {
                    "normal": {
                        "color": "rgba(51,204,112,1)",
                        "barBorderRadius": 0,
                        "label": {
                            "show": true,
                            "position": "top",
                            formatter : function(p) {
                                                        return p.value > 0 ? ('▼'
                                                                + p.value + '')
                                                                : '';
                                                    }
                        }
                    }
                },
                "data": expenses_lst
            },
            {
                "name": "人流增长",
                "type": "bar",
                "stack": "总量",
                "itemStyle": {
                    "normal": {
                        "color": "rgba(193,35,43,1)",
                        "barBorderRadius": 0,
                        "label": {
                            "show": true,
                            "position": "top",
                            formatter : function(p) {
                                                        return p.value > 0 ? ('▲'
                                                                + p.value + '')
                                                                : '';
                                                    }
                        }
                    }
                },
                "data": []
            }
        ]
    }
    return option;
}