<template>
  <div class="app-container">
    <el-form
      ref="dataForm"
      :rules="rules"
      :model="temp"
      label-position="left"
      label-width="150px"
      style="width: 400px; margin-left:50px;"
    >
      <el-form-item label="Product ID" prop="productID">
        <el-input v-model="temp.productID" />
      </el-form-item>
      <el-form-item label="Product Name" prop="productName">
        <el-input v-model="temp.productName" />
      </el-form-item>
      <el-form-item label="Production Date" prop="productionDate">
        <el-date-picker v-model="temp.productionDate" type="date" placeholder="Please pick a date" />
      </el-form-item>
      <el-form-item label="Manufacturer" prop="companyName">
        <el-input v-model="temp.companyName" />
      </el-form-item>
      <!--      <el-input v-for="(item, index) in formerItemsObj" :key="index" v-model="formerItemsObj[index].value" />-->
      <span v-for="(item, index) in temp.materialsID" :key="index">
        <el-form-item>
          <span slot="label">Material{{ index+1 }} ID</span>
          <el-input v-model="temp.materialsID[index]" placeholder="原材料编号" />
          <el-button
            size="mini"
            class="button"
            plain
            icon="el-icon-delete"
            @click="deleteListObjItem"
          >Delete Material</el-button>
        </el-form-item>
        <!-- <el-form-item>
          <span slot="label">原材料名称</span>
          <el-input placeholder="原材料名称" :disabled="true" />
        </el-form-item>
        <el-form-item>
          <span slot="label">加工厂商</span>
          <el-input placeholder="原材料编号" :disabled="true" />
        </el-form-item>-->
      </span>
      <el-form-item>
        <el-button
          size="mini"
          class="button"
          plain
          icon="el-icon-plus"
          @click="addListObjItem"
        >Add Material</el-button>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogFormVisible = false">CANCEL</el-button>
      <el-button type="primary" @click="createData()">ADD</el-button>
    </div>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { createProduct } from '@/api/trace'
import waves from '@/directive/waves' // waves directive
// import { parseTime } from '@/utils'
// import axios from 'axios'
// arr to obj, such as { CN : "China", US : "USA" }

export default {
  name: 'ComplexTable',
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      formerItems: ['2'],
      formerItemsObj: [{ value: '1' }],
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      sortOptions: [
        { label: 'ID Ascending', key: '+id' },
        { label: 'ID Descending', key: '-id' }
      ],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        productID: '',
        productName: '',
        companyName: '',
        productionDate: '2010-01-01',
        materialsID: []
      },
      dialogFormVisible: true,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        productID: [
          { required: true, message: '请输入产品ID', trigger: 'change' }
        ],
        productName: [
          { required: true, message: '请输入产品名称', trigger: 'change' }
        ],
        productionDate: [
          { required: true, message: '请选择生产日期', trigger: 'change' }
        ],
        companyName: [
          { required: true, message: '请输入生产厂家', trigger: 'change' }
        ]
      },
      downloadLoading: false
    }
  },
  methods: {
    addListObjItem() {
      this.temp.materialsID.push('')
    },
    deleteListObjItem() {
      this.temp.materialsID.pop()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      console.log(this.temp)

      // axios.post('http://127.0.0.1:5000/api/add/', this.temp).then(res => {
      //   console.log(res)
      // })

      createProduct(this.temp).then(() => {
        // this.list.unshift(this.temp)
        this.$notify({
          title: 'Success',
          message: 'Created Successfully',
          type: 'success',
          duration: 2000
        })
      })

      // this.$refs['dataForm'].validate(valid => {
      //   if (valid) {
      //     // {
      //     // productID: 'zcx-test-003',
      //     // productName: 'productNameExample3',
      //     // companyName: 'companyNameExample3',
      //     // productionDate: '2010-01-01',
      //     // materialsID: []
      //     // }
      //     this.temp.productID = this.temp.author = 'vue-element-admin'
      //     createProduct(this.temp).then(() => {
      //       // this.list.unshift(this.temp)
      //       this.dialogFormVisible = false
      //       this.$notify({
      //         title: 'Success',
      //         message: 'Created Successfully',
      //         type: 'success',
      //         duration: 2000
      //       })
      //     })
      //   }
      // })
    }
  }
}
</script>
