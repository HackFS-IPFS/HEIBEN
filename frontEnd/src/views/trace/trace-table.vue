<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input
        v-model="idToSearch"
        placeholder="Product ID"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="runGetData"
      />

      <el-button
        v-waves
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="runGetData"
      >Search</el-button>

      <el-button
        v-waves
        class="filter-item"
        type="primary"
        icon="el-icon-s-data"
        @click="showTraceChart"
      >trace-chain visualization</el-button>

      <!-- <el-input
        v-model="listQuery.title"
        placeholder="Product ID"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="getData"
      />-->
      <!-- <el-button
        v-waves
        class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
      >Search</el-button>-->
      <!--      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">-->
      <!--        Add-->
      <!--      </el-button>-->
      <!--      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">-->
      <!--        Export-->
      <!--      </el-button>-->
      <!--      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">-->
      <!--        reviewer-->
      <!--      </el-checkbox>-->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :span-method="arraySpanMethod"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column label="Product ID" prop="id" sortable="custom" align="center" width="100">
        <template slot-scope="{row}">
          <span>{{ row.productID }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Production Date" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.productionDate | parseTime }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Product Name" min-width="150px">
        <template slot-scope="{row}">
          <span>{{ row.productName }}</span>
          <!--          <el-tag>{{ row.type | typeFilter }}</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column label="Manufacturer" min-width="150px">
        <template slot-scope="{row}">
          <span>{{ row.companyName }}</span>
          <!--          <el-tag>{{ row.type | typeFilter }}</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column label="Material ID" min-width="150px">
        <template slot-scope="{row}">
          <span>{{ row.materialID }}</span>
          <!--          <el-tag>{{ row.type | typeFilter }}</el-tag>-->
        </template>
      </el-table-column>
    </el-table>

    <!-- <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="runGetData"
    />-->

    <el-dialog :visible.sync="dialogVisible" width="90%">
      <trace-chart-component :data="rawList" :rootid="rootID" />
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { fetchProduct } from '@/api/trace'
import waves from '@/directive/waves' // waves directive
import TraceChartComponent from './trace-chart-component.vue' // waves directive
// import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { TraceChartComponent },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      idToSearch: '',
      tableKey: 0,
      rootID: '',
      dialogVisible: false,
      list: null,
      rawList: null,
      total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [
        { label: 'ID Ascending', key: '+id' },
        { label: 'ID Descending', key: '-id' }
      ],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [
          { required: true, message: 'type is required', trigger: 'change' }
        ],
        timestamp: [
          {
            type: 'date',
            required: true,
            message: 'timestamp is required',
            trigger: 'change'
          }
        ],
        title: [
          { required: true, message: 'title is required', trigger: 'blur' }
        ]
      },
      downloadLoading: false
    }
  },
  mounted() {
    // this.getList()
    // this.idToSearch = 'zcx-test-000'
    // this.getData(this.idToSearch)
    // this.getData('zcx-test-000')
  },
  methods: {
    async runGetData() {
      this.rootID = this.idToSearch
      console.log(this.idToSearch)
      await this.getData(this.rootID)
      // await this.prepareData()
    },
    getData(rootID) {
      // this.list = [
      //   {
      //     productID: 'zcx-test-000',
      //     productName: 'productNameExample1',
      //     companyName: 'companyNameExample1',
      //     productionDate: '2010-01-01',
      //     materialsID: [
      //       'zcx-test-004',
      //       'zcx-test-007',
      //       'zcx-test-002',
      //       'zcx-test-003'
      //     ]
      //   },
      //   {
      //     productID: 'zcx-test-004',
      //     productName: 'productNameExample2',
      //     companyName: 'companyNameExample2',
      //     productionDate: '2010-01-01',
      //     materialsID: []
      //   },
      //   {
      //     productID: 'zcx-test-007',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: ['zcx-test-008', 'zcx-test-006']
      //   },
      //   {
      //     productID: 'zcx-test-002',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: ['zcx-test-005', 'zcx-test-003']
      //   },
      //   {
      //     productID: 'zcx-test-003',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: []
      //   },
      //   {
      //     productID: 'zcx-test-008',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: []
      //   },
      //   {
      //     productID: 'zcx-test-005',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: ['zcx-test-008', 'zcx-test-006']
      //   },
      //   {
      //     productID: 'zcx-test-006',
      //     productName: 'productNameExample3',
      //     companyName: 'companyNameExample3',
      //     productionDate: '2010-01-01',
      //     materialsID: []
      //   }
      // ]

      this.listLoading = true
      fetchProduct(rootID).then(response => {
        this.listLoading = false
        console.log('response =', response)
        this.list = response
        console.log('this.list', this.list)
        this.prepareData()
      })
      // // this.list.total = response.total
    },
    prepareData() {
      // 去重
      console.log('开始去重')
      const hasItem = new Set()
      console.log('this.list = ', this.list)
      this.list.forEach(item => {
        console.log('item = ', item)
        if (hasItem.has(item)) {
          console.log('has item skip')
          return true
        }

        console.log('add item')
        hasItem.add(item)
        console.log('add item completed')
      })

      console.log('partly complete, hasItem = ', hasItem)
      const rawList = Array.from(hasItem)
      this.rawList = rawList
      console.log('去重完成')
      console.log('rawList = ', rawList)

      const newList = []

      // 根据materialsID展开
      let newItem
      rawList.forEach(item => {
        if (item.materialsID.length === 0) {
          console.log('item.materialsID.length === 0, item = ', item)
          newItem = JSON.parse(JSON.stringify(item))
          newItem.materialID = null
          newList.push(newItem)
        } else if (item.materialsID.length >= 1) {
          console.log(
            'item.materialsID.length =',
            item.materialsID.length,
            'item = ',
            item
          )
          item.materialsID.forEach(materialID => {
            newItem = JSON.parse(JSON.stringify(item))
            // console.log('materialID = ', materialID)
            // console.log('newItem.materialID = ', newItem.materialID)
            newItem.materialID = materialID
            // console.log('materialID = ', materialID)
            // console.log('newItem.materialID = ', newItem.materialID)
            newList.push(newItem)
            console.log('materialID = ', materialID)
            console.log('newItem.materialID = ', newItem.materialID)
            console.log(
              'newList[newList.length - 1].materialID = ',
              newList[newList.length - 1].materialID
            )
          })
        }
      })
      console.log('newList = ', newList)
      this.list = newList
    },
    arraySpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex < 4 && row.materialsID.length > 1) {
        // 判断条件可以设置成你想合并的列的起始位置
        // 判断条件可以设置成你想合并的行的起始位置
        if (row.materialsID[0] === row.materialID) {
          console.log('arraySpanMethod, row = ', row)
          console.log('arraySpanMethod, column = ', column)
          console.log('arraySpanMethod, rowIndex = ', rowIndex)
          console.log('arraySpanMethod, columnIndex = ', columnIndex)
          console.log('arraySpanMethod, rowspan = ', row.materialsID.length)
          return [row.materialsID.length, 1]
        } else {
          return [0, 0]
        }
      }
    },
    showTraceChart() {
      this.dialogVisible = true
    }
  }
}
</script>
