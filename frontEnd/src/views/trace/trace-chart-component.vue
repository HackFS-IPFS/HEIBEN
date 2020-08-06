<template>
  <div class="trace-chart-container">
    <div id="trace-chart" :style="{width: '100%', height: '100%'}" />
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'TraceChartComponent',
  props: {
    data: {
      type: Array,
      required: true
    },
    rootid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      graph: {
        nodes: [],
        links: []
      },

      nameDataMap: {}
    }
  },
  mounted() {
    this.runRender()
    // this.drawLine()
  },
  methods: {
    async runRender() {
      await this.prepareData()
      await this.convertData()
      await this.drawLine()
    },

    drawLine() {
      var myChart = echarts.init(document.getElementById('trace-chart'))

      var option = {
        xAxis: {
          show: false,
          type: 'value'
        },
        yAxis: {
          show: false,
          type: 'value'
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            var str = ''
            str += '<p>名称：' + params.data.productName + '<p>'
            str += '<p>生产公司：' + params.data.companyName + '<p>'
            str += '<p>生产日期：' + params.data.productionDate + '<p>'

            return str
          }
        },
        series: [
          {
            type: 'graph',
            layout: 'none',

            zoom: 0.9,
            focusNodeAdjacency: true,
            roam: true,
            hoverAnimation: true,
            // draggable: true,
            animationDuration: 1500,
            animationEasingUpdate: 'quinticInOut',

            symbolSize: 180,
            // symbol: 'round',
            // symbolSize: [200, 200],
            // symbol: 'roundRect',
            label: {
              show: true,
              position: 'inside',

              formatter: function(params) {
                var str = ''

                str += '{titleName|商品ID}\n'
                str += '{title|' + params.data.name + '}\n'
                str += '{titleName|名称}\n'
                // str += '{title|' + params.data.productName + '}\n'
                // str += '\n{hr|}\n'

                // str += '{content|名称：' + params.data.productName + '}\n'
                // str += '{contentName|名称：'
                let tempstr = params.data.productName
                let cnt = 0
                str += '{title|'
                while (tempstr.length > 10) {
                  str += tempstr.slice(0, 10)
                  str += '\n'
                  cnt++
                  tempstr = tempstr.slice(cnt * 10, tempstr.length)
                }
                str += tempstr
                str += '}\n'
                return str
              },

              // width: 200,
              // backgroundColor: '#202020',
              // // borderColor: '#333',
              // borderColor: 'rgb(199,86,83)',
              // borderWidth: 2,
              // borderRadius: 5,
              // padding: 10,
              rich: {
                titleName: {
                  fontSize: 14,
                  height: 16,
                  color: '#fff',
                  align: 'center'
                },
                title: {
                  height: 25,
                  fontSize: 16,
                  fontStyle: 'bold',
                  color: '#fff',
                  align: 'center'
                },
                contentName: {
                  height: 16,
                  fontSize: 14,
                  color: '#fff',
                  align: 'left',
                  padding: [0, 40, 0, 0]
                },
                content: {
                  height: 16,
                  fontSize: 14,
                  color: '#fff',
                  // padding: [40, 0, 0, 0],
                  align: 'left'
                },
                hr: {
                  borderColor: '#f2f2f2',
                  width: '100%',
                  borderWidth: 0.5,
                  height: 0
                }
              }
            },
            itemStyle: {
              color: '#101010',
              borderColor: '#fff',
              borderWidth: 1,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.3)'
            },
            // itemStyle: {
            //   color: '#101010',
            //   borderColor: '#fff',
            //   borderWidth: 1,
            //   shadowBlur: 10,
            //   shadowColor: 'rgba(0, 0, 0, 0.3)'
            // },
            // itemStyle: {
            //   normal: {
            //     color: '#F2F2F2',
            //     shadowColor: 'rgba(225,225,225,0.4)',
            //     shadowBlur: 10,
            //     shadowOffsetX: 10,
            //     shadowOffsetY: 10
            //   }
            // },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: 30,
            lineStyle: {
              width: 4,
              shadowColor: 'none',
              color: 'source',
              curveness: 0.3
            },
            emphasis: {
              lineStyle: {
                width: 10
              },
              label: {
                show: false
              }
            },
            // force: {
            //   repulsion: 20,
            //   gravity: 0.2,
            //   edgeLength: 1400
            // },

            data: this.graph.nodes,
            links: this.graph.links
          }
        ]
      }
      myChart.setOption(option)
    },

    prepareData() {
      console.log('prepareData() started')
      console.log('prepareData() started')
      console.log('prepareData() -- this.data = ', this.data)

      this.nameDataMap = new Map()
      this.data.forEach(item => {
        console.log('item = ', item)
        if (this.nameDataMap.has(item.productID)) {
          console.log('has item')
          return true
        }
        this.nameDataMap.set(item.productID, item)
      })

      console.log('prepareData() -- this.data = ', this.data)
      console.log('prepareData() -- this.nameDataMap = ', this.nameDataMap)
      console.log('prepareData() finished')
    },

    convertData() {
      console.log('convertData() started')
      console.log('convertData() -- this.data = ', this.data)
      console.log('convertData() -- this.nameDataMap = ', this.nameDataMap)
      // this.graph.nodes = this.data

      // let rootid = 'zcx-test-000'

      // let levelCnt = 0
      const waitingRetrieve = []
      const havingRetrieved = new Set()
      const levelNodeNumMap = new Map()
      const itemCoordinateMap = new Map()

      let firstLoop = true
      waitingRetrieve.push(this.rootid)
      console.log('this.rootid = ', this.rootid)
      console.log('waitingRetrieve = ', waitingRetrieve)
      while (waitingRetrieve.length) {
        console.log('===== entering new level =====')
        // console.log('levelCnt = ', levelCnt)
        // let siblingCnt = Math.ceil(waitingRetrieve.length / 2) - 1
        // console.log('reset siblingCnt to ', levelCnt)

        const itemName = waitingRetrieve[0]
        console.log('-- new item --')
        console.log('itemName = ', itemName)

        if (havingRetrieved.has(itemName)) {
          return true
        }

        const item = this.nameDataMap.get(itemName)
        console.log('item = ', item)

        item.name = item.productID

        if (firstLoop === true) {
          item.x = 0
          item.y = 0
        } else {
          item.x = itemCoordinateMap.get(itemName)[0]
          item.y = itemCoordinateMap.get(itemName)[1]
        }
        // item.x = levelCnt
        // item.y = siblingCnt

        this.graph.nodes.push(item)
        havingRetrieved.add(itemName)
        waitingRetrieve.shift()
        // siblingCnt++

        console.log('- after retrieving -')
        console.log('item = ', item)
        console.log('this.graph.nodes = ', this.graph.nodes)
        console.log('havingRetrieved = ', havingRetrieved)
        console.log('waitingRetrieve = ', waitingRetrieve)
        // console.log('siblingCnt = ', siblingCnt)

        item.materialsID.forEach(itemName2 => {
          waitingRetrieve.push(itemName2)

          const obj = {
            source: itemName,
            target: itemName2
          }
          this.graph.links.push(obj)

          if (itemCoordinateMap.has(itemName2) === false) {
            let siblingCnt = levelNodeNumMap.get(item.x)
            console.log('siblingCnt = ', siblingCnt)
            if (siblingCnt === undefined) {
              siblingCnt = 0
            }
            console.log('siblingCnt = ', siblingCnt)
            itemCoordinateMap.set(itemName2, [item.x - 1, siblingCnt])
            levelNodeNumMap.set(item.x, siblingCnt + 1)
          }
        })
        console.log('- after updating links -')
        console.log('this.graph.links = ', this.graph.links)
        console.log('waitingRetrieve = ', waitingRetrieve)

        // levelCnt--
        firstLoop = false
      }
      console.log('convertData() finished')
    }
  }
}
</script>

<style scoped>
.trace-chart-container {
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>
