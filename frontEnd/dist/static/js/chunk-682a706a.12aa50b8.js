(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-682a706a"],{6724:function(e,t,a){"use strict";a("8d41");var i="@@wavesContext";function l(e,t){function a(a){var i=Object.assign({},t.value),l=Object.assign({ele:e,type:"hit",color:"rgba(0, 0, 0, 0.15)"},i),o=l.ele;if(o){o.style.position="relative",o.style.overflow="hidden";var n=o.getBoundingClientRect(),s=o.querySelector(".waves-ripple");switch(s?s.className="waves-ripple":(s=document.createElement("span"),s.className="waves-ripple",s.style.height=s.style.width=Math.max(n.width,n.height)+"px",o.appendChild(s)),l.type){case"center":s.style.top=n.height/2-s.offsetHeight/2+"px",s.style.left=n.width/2-s.offsetWidth/2+"px";break;default:s.style.top=(a.pageY-n.top-s.offsetHeight/2-document.documentElement.scrollTop||document.body.scrollTop)+"px",s.style.left=(a.pageX-n.left-s.offsetWidth/2-document.documentElement.scrollLeft||document.body.scrollLeft)+"px"}return s.style.backgroundColor=l.color,s.className="waves-ripple z-active",!1}}return e[i]?e[i].removeHandle=a:e[i]={removeHandle:a},a}var o={bind:function(e,t){e.addEventListener("click",l(e,t),!1)},update:function(e,t){e.removeEventListener("click",e[i].removeHandle,!1),e.addEventListener("click",l(e,t),!1)},unbind:function(e){e.removeEventListener("click",e[i].removeHandle,!1),e[i]=null,delete e[i]}},n=function(e){e.directive("waves",o)};window.Vue&&(window.waves=o,Vue.use(n)),o.install=n;t["a"]=o},"89ff":function(e,t,a){"use strict";a.d(t,"b",(function(){return l})),a.d(t,"a",(function(){return o}));var i=a("b775");function l(e){return Object(i["a"])({url:"/api/trace/",method:"GET",params:{productID:e}})}function o(e){return Object(i["a"])({url:"/api/add/",method:"POST",data:e})}},"8d41":function(e,t,a){},"8fc0":function(e,t,a){"use strict";a.r(t);var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container"},[a("el-form",{ref:"dataForm",staticStyle:{width:"400px","margin-left":"50px"},attrs:{rules:e.rules,model:e.temp,"v-loading":e.loading,"label-position":"left","label-width":"100px"}},[a("el-form-item",{attrs:{label:"产品ID",prop:"productID"}},[a("el-input",{model:{value:e.temp.productID,callback:function(t){e.$set(e.temp,"productID",t)},expression:"temp.productID"}})],1),a("el-form-item",{attrs:{label:"产品名称",prop:"productName"}},[a("el-input",{model:{value:e.temp.productName,callback:function(t){e.$set(e.temp,"productName",t)},expression:"temp.productName"}})],1),a("el-form-item",{attrs:{label:"生产日期",prop:"productionDate"}},[a("el-date-picker",{attrs:{type:"date",placeholder:"Please pick a date"},model:{value:e.temp.productionDate,callback:function(t){e.$set(e.temp,"productionDate",t)},expression:"temp.productionDate"}})],1),a("el-form-item",{attrs:{label:"加工厂商",prop:"companyName"}},[a("el-input",{model:{value:e.temp.companyName,callback:function(t){e.$set(e.temp,"companyName",t)},expression:"temp.companyName"}})],1),e._l(e.temp.materialsID,(function(t,i){return a("span",{key:i},[a("el-form-item",[a("span",{attrs:{slot:"label"},slot:"label"},[e._v("原材料"+e._s(i+1)+" ID")]),a("el-input",{attrs:{placeholder:"原材料编号"},model:{value:e.temp.materialsID[i],callback:function(t){e.$set(e.temp.materialsID,i,t)},expression:"temp.materialsID[index]"}}),a("el-button",{staticClass:"button",attrs:{size:"mini",plain:"",icon:"el-icon-delete"},on:{click:e.deleteListObjItem}},[e._v("删除此原材料")])],1)],1)})),a("el-form-item",[a("el-button",{staticClass:"button",attrs:{size:"mini",plain:"",icon:"el-icon-plus"},on:{click:e.addListObjItem}},[e._v("添加原材料")])],1)],2),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogFormVisible=!1}}},[e._v("取消")]),a("el-button",{attrs:{type:"primary"},on:{click:function(t){return e.createData()}}},[e._v("添加")])],1),a("el-dialog",{attrs:{visible:e.dialogPvVisible,title:"Reading statistics"},on:{"update:visible":function(t){e.dialogPvVisible=t}}},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.pvData,border:"",fit:"","highlight-current-row":""}},[a("el-table-column",{attrs:{prop:"key",label:"Channel"}}),a("el-table-column",{attrs:{prop:"pv",label:"Pv"}})],1),a("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{type:"primary"},on:{click:function(t){e.dialogPvVisible=!1}}},[e._v("Confirm")])],1)],1)],1)},l=[],o=a("89ff"),n=a("6724"),s={name:"ComplexTable",directives:{waves:n["a"]},filters:{statusFilter:function(e){var t={published:"success",draft:"info",deleted:"danger"};return t[e]}},data:function(){return{formerItems:["2"],formerItemsObj:[{value:"1"}],tableKey:0,list:null,total:0,loading:!1,listLoading:!0,listQuery:{page:1,limit:20,importance:void 0,title:void 0,type:void 0,sort:"+id"},importanceOptions:[1,2,3],sortOptions:[{label:"ID Ascending",key:"+id"},{label:"ID Descending",key:"-id"}],statusOptions:["published","draft","deleted"],showReviewer:!1,temp:{productID:"",productName:"",companyName:"",productionDate:"2010-01-01",materialsID:[]},dialogFormVisible:!0,dialogStatus:"",textMap:{update:"Edit",create:"Create"},dialogPvVisible:!1,pvData:[],rules:{productID:[{required:!0,message:"请输入产品ID",trigger:"change"}],productName:[{required:!0,message:"请输入产品名称",trigger:"change"}],productionDate:[{required:!0,message:"请选择生产日期",trigger:"change"}],companyName:[{required:!0,message:"请输入生产厂家",trigger:"change"}]},downloadLoading:!1}},methods:{addListObjItem:function(){this.temp.materialsID.push("")},deleteListObjItem:function(){this.temp.materialsID.pop()},resetTemp:function(){this.temp={id:void 0,importance:1,remark:"",timestamp:new Date,title:"",status:"published",type:""}},handleCreate:function(){var e=this;this.resetTemp(),this.dialogStatus="create",this.dialogFormVisible=!0,this.$nextTick((function(){e.$refs["dataForm"].clearValidate()}))},createData:function(){var e=this;console.log(this.temp);var t=this.$loading({lock:!0});Object(o["a"])(this.temp).then((function(){t.close(),e.$notify({title:"Success",message:"Created Successfully",type:"success",duration:2e3})}))}}},r=s,c=a("2877"),p=Object(c["a"])(r,i,l,!1,null,null,null);t["default"]=p.exports}}]);