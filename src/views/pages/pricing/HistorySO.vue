<script setup>
import { ref, computed, onMounted } from 'vue';
import { fetchRequestSOs, updateRequestSO, deleteRequestSO } from '@/_mockApis/apps/requestso/indexRequestSo'; // API untuk SO
import dayjs from 'dayjs'; // Import Day.js

const productlist = ref([]); // Data tabel
const search = ref(''); // Kolom pencarian
const dialogDelete = ref(false); // Dialog hapus
const updateDialog = ref(false); // Dialog update

const headers = ref([
    { title: 'No', key: 'no', align: 'left' },
    { title: 'Id SO', key: 'id', align: 'left' },
    { title: 'Purchase Date', key: 'orderDate', align: 'left' },
    { title: 'Customer Name', key: 'customerName', align: 'left' },
    { title: 'Customer NPWP', key: 'customerNPWP', align: 'left', sortable: false },
    { title: 'Customer Address', key: 'customerAddress', align: 'left', sortable: false },
    { title: 'Customer Phone Number', key: 'customerPhone', align: 'left' },
    { title: 'Item Name', key: 'itemName', align: 'left' },
    { title: 'Item Description', key: 'itemDesc', align: 'left' },
    { title: 'Item Price', key: 'itemPrice', align: 'left', sortable: false },
    { title: 'Item Quantity', key: 'itemQty', align: 'left', sortable: false },
    { title: 'Total Price / Item', key: 'totalPriceperItem', align: 'left' },
    { title: 'Additional Price', key: 'additionalprice', align: 'left' },
    { title: 'Total Item Price (Before Tax)', key: 'totalpricebeforeppn', align: 'left' },
    { title: 'PPn (%)', key: 'ppnpercent', align: 'left' },
    { title: 'PPn (Rp)', key: 'ppnprice', align: 'left' },
    { title: 'Total Item Price (After Tax)', key: 'totalpriceafterppn', align: 'left' },
    { title: 'Payment Method', key: 'customerBankAccount', align: 'left' },
    { title: 'Payment Status', key: 'paymentStatus', align: 'left' },
    { title: 'Payment Proof', key: 'paymentProof', align: 'left' },
    { title: 'Submission User', key: 'submissionUser', align: 'left', sortable: false },
    { title: 'Submission Notes', key: 'submissionNotes', align: 'left', sortable: false },
    { title: 'Verification Status', key: 'verificationStatus', align: 'left' },
    { title: 'Verified By', key: 'verificationUser', align: 'left' },
    { title: 'Verified Notes', key: 'verificationNotes', align: 'left' },
    { title: 'Actions', key: 'actions', align: 'left', sortable: false }
]);



const editedSO = ref({
  soid: '',
  paymentProof: null,
  paymentStatus: '',
  verificationStatus: '',
  verificationNotes: '',
});

const validateUpdateFields = computed(() => {
  return (
    !!editedSO.value.paymentProof ||
    !!editedSO.value.paymentStatus ||
    !!editedSO.value.verificationStatus ||
    !!editedSO.value.verificationNotes
  );
});

const loadRequestSOs = async () => {
  try {
    const data = await fetchRequestSOs();
    productlist.value = data;
  } catch (error) {
    console.error('Failed to load request SOs:', error);
  }
};

const handleFileInputChange = (event) => {
  const file = event.target.files[0]; // Ambil file pertama dari input
  if (file) {
    editedSO.value.paymentProof = file.name; // Simpan nama file
  } else {
    editedSO.value.paymentProof = null; // Reset jika tidak ada file
  }
};

const openUpdateDialog = (item) => {
  editedSO.value = {
    soid: item.id,
    paymentProof: null,
    paymentStatus: item.paymentStatus || '',
    verificationStatus: item.verificationStatus || '',
    verificationNotes: item.verificationNotes || '',
  };
  updateDialog.value = true;
};

const updateSO = async () => {
  try {
    await updateRequestSO(editedSO.value.soid, {
      paymentProof: editedSO.value.paymentProof,
      paymentStatus: editedSO.value.paymentStatus,
      verificationStatus: editedSO.value.verificationStatus,
      verificationNotes: editedSO.value.verificationNotes,
    });
    console.log('Request SO updated successfully');
    updateDialog.value = false;
    await loadRequestSOs();
  } catch (error) {
    console.error('Failed to update Request SO:', error);
  }
};

const deleteItem = (item) => {
  editedSO.value.soid = item.id;
  dialogDelete.value = true;
};

const deleteItemConfirm = async () => {
  try {
    await deleteRequestSO(editedSO.value.soid);
    productlist.value = productlist.value.filter((item) => item.id !== editedSO.value.soid);
    dialogDelete.value = false;
  } catch (error) {
    console.error('Failed to delete item:', error);
  }
};

const closeDelete = () => {
  dialogDelete.value = false;
};

onMounted(() => {
  loadRequestSOs();
});
</script>
<template>
    <v-row>
      <v-col cols="12">
        <UiParentCard title="History Request SO">
          <v-data-table
            :headers="headers"
            :items="productlist"
            v-model:search="search"
            items-per-page="5"
            color="primary"
          >
            <template v-slot:item.no="{ index }">
              <span>{{ index + 1 }}</span>
            </template>
  
            <template v-slot:item.id="{ item }">
              <span>{{ item.id }}</span>
            </template>
  
            <template v-slot:item.orderDate="{ item }">
              <span>{{ item.orderDate ? dayjs(item.orderDate).format('YYYY-MM-DD HH:mm:ss') : '-' }}</span>
            </template>
  
            <template v-slot:item.customerName="{ item }">
              <span>{{ item.customerName }}</span>
            </template>
  
            <template v-slot:item.customerAddress="{ item }">
              <span>{{ item.customerAddress }}</span>
            </template>
        
            <!-- Kolom Item Name -->
            <template v-slot:item.itemName="{ item }">
                <ul>
                    <li v-for="name in item.itemName.split('|')" :key="name">{{ name }}</li>
                </ul>
            </template>

            <!-- Kolom Item Description -->
            <template v-slot:item.itemDesc="{ item }">
                <ul>
                    <li v-for="desc in item.itemDesc.split('|')" :key="desc">{{ desc }}</li>
                </ul>
            </template>

            <!-- Kolom Item Price -->
            <template v-slot:item.itemPrice="{ item }">
                <ul>
                    <li v-for="price in item.itemPrice.split('|')" :key="price">{{ price }}</li>
                </ul>
            </template>

            <!-- Kolom Item Quantity -->
            <template v-slot:item.itemQty="{ item }">
                <ul>
                    <li v-for="qty in item.itemQty.split('|')" :key="qty">{{ qty }}</li>
                </ul>
            </template>

            <!-- Kolom Total Price per Item -->
            <template v-slot:item.totalPriceperItem="{ item }">
                <ul>
                    <li v-for="tppi in item.totalPriceperItem.split('|')" :key="tppi">{{ tppi }}</li>
                </ul>
            </template>
  
            <template v-slot:item.paymentStatus="{ item }">
              <span>{{ item.paymentStatus }}</span>
            </template>
  
            <template v-slot:item.verificationStatus="{ item }">
              <span>{{ item.verificationStatus }}</span>
            </template>
  
            <template v-slot:item.actions="{ item }">
              <EditIcon
                height="20"
                width="20"
                class="cursor-pointer text-primary"
                @click="openUpdateDialog(item)"
              />
              <TrashIcon
                height="20"
                width="20"
                class="cursor-pointer text-error"
                @click="deleteItem(item)"
              />
            </template>
          </v-data-table>
  
          <!-- Dialog Update -->
          <v-dialog v-model="updateDialog" max-width="500">
            <v-card>
              <v-card-title>Update Request SO</v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-select
                        v-model="editedSO.paymentStatus"
                        :items="['PAID', 'UNPAID']"
                        label="Select Payment Status"
                      />
                    </v-col>
                    <v-col cols="12">
                      <v-select
                        v-model="editedSO.verificationStatus"
                        :items="['ACCEPT', 'PENDING', 'REJECT']"
                        label="Select Verification Status"
                      />
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="editedSO.verificationNotes"
                        label="Enter Verification Notes"
                      />
                    </v-col>
                    <v-col cols="12">
                      <v-file-input
                        label="Upload Payment Proof"
                        accept="image/*"
                        @change="handleFileInputChange"
                      />
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-btn text @click="updateDialog = false">Cancel</v-btn>
                <v-btn color="primary" @click="updateSO" :disabled="!validateUpdateFields">Update</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
  
          <!-- Dialog Delete -->
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title>Are you sure you want to delete this SO?</v-card-title>
              <v-card-actions>
                <v-btn text @click="closeDelete">Cancel</v-btn>
                <v-btn color="error" @click="deleteItemConfirm">Delete</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </UiParentCard>
      </v-col>
    </v-row>
  </template>